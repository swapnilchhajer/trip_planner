import os
import re
import logging
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TripPlannerAgent")

from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool, ToolContext, BaseTool
from google.adk.models import Gemini
from google.adk.apps import App
from google.adk.apps.app import EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types as genai_types

from tools import get_places_to_visit, get_transportation_options, get_overall_pricing_estimate

# ---------------------------------------------------------------------------
# 1. Human-in-the-Loop Conditional stops for Sensitive / High-Cost tools
# ---------------------------------------------------------------------------

def needs_approval(destination: str, days: int, travel_style: str) -> bool:
    """Evaluates if the requested trip budget calculation is a high-impact operation requiring approval.
    
    Triggers explicit human-in-the-loop stop if duration is long (> 14 days) or travel style is Luxury.
    """
    return days > 14 or travel_style.lower() == "luxury"

pricing_tool = FunctionTool(
    get_overall_pricing_estimate,
    require_confirmation=needs_approval
)

# Standard mock tool
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}


# ---------------------------------------------------------------------------
# 2. SQLite Persistent Long-Term Memory Service
# ---------------------------------------------------------------------------

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.db")

def init_sqlite_memory_db():
    """Initializes sqlite database for persistent user preference and profile memory."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_memories (
                user_id TEXT PRIMARY KEY,
                preferences TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        logger.info("SQLite Persistent Memory database successfully initialized.")
    except Exception as e:
        logger.error(f"Error initializing SQLite database: {e}")

# Initialize database
init_sqlite_memory_db()

def load_user_preferences(user_id: str) -> str:
    """Retrieves user preferences persistently from the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT preferences FROM user_memories WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
    except Exception as e:
        logger.error(f"Error loading user preferences from SQLite: {e}")
    return "No prior preferences stored."

def save_user_preferences(user_id: str, preferences: str):
    """Saves user preferences persistently into the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_memories (user_id, preferences)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET preferences = excluded.preferences
        """, (user_id, preferences))
        conn.commit()
        conn.close()
        logger.info(f"Successfully saved persistent SQLite memory for user: {user_id}")
    except Exception as e:
        logger.error(f"Error saving user preferences to SQLite: {e}")


# ---------------------------------------------------------------------------
# 3. Security, Privacy (PII Redaction) & Guardrails
# ---------------------------------------------------------------------------

PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "PHONE": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b"
}

def active_redact_pii(text: str) -> str:
    """Actively redacts high-risk Personal Identifiable Information (PII) before model processing."""
    redacted = text
    for pii_type, pattern in PII_PATTERNS.items():
        redacted = re.sub(pattern, f"[{pii_type}_REDACTED]", redacted)
    return redacted

# Safety policy check list
PROHIBITED_KEYWORDS = ["weapons", "hacking", "explosives", "contraband", "darkweb"]


# ---------------------------------------------------------------------------
# 4. Agent Callbacks (PII, Safety, Intent/Outcome Logging, Memory Sync)
# ---------------------------------------------------------------------------

async def before_agent_callback(callback_context: CallbackContext) -> None:
    """Loads long-term user memories from SQLite and pre-loads them into the state."""
    user_id = callback_context.state.get("user_id", "default_user")
    memories = load_user_preferences(user_id)
    callback_context.state["sqlite_user_memory"] = memories
    logger.info(f"Loaded persistent memories for {user_id}: {memories}")

async def after_agent_callback(callback_context: CallbackContext) -> genai_types.Content | None:
    """Analyzes the agent session to extract and persist new user preferences to SQLite."""
    user_id = callback_context.state.get("user_id", "default_user")
    
    # Simple extraction of key facts (e.g. user likes luxury, specific food, etc.)
    # In a full app, a sub-model can summarize, we will scan the history for travel style preferences
    pref_acc = []
    
    # Access and search events
    events = callback_context.session.events
    for event in events:
        if event.author == "user" and event.content:
            text = str(event.content).lower()
            if "luxury" in text:
                pref_acc.append("Prefers luxury travel.")
            elif "budget" in text:
                pref_acc.append("Prefers budget travel.")
            elif "vegetarian" in text:
                pref_acc.append("Prefers vegetarian dining.")
            elif "history" in text:
                pref_acc.append("Interested in historical landmarks.")

    if pref_acc:
        existing = load_user_preferences(user_id)
        combined = set(existing.split("; ") + pref_acc)
        save_user_preferences(user_id, "; ".join(combined))
    
    return None

async def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> LlmResponse | None:
    """Enforces active PII redaction and security guardrails."""
    # Redact PII in user inputs
    for content in llm_request.contents:
        if content.parts:
            for part in content.parts:
                if part.text:
                    # Security Guardrail: Check for prohibited content
                    for kw in PROHIBITED_KEYWORDS:
                        if kw in part.text.lower():
                            logger.warning(f"Guardrail triggered! Prohibited keyword detected: {kw}")
                            # Bypass model call, return standard policy violation response
                            return LlmResponse(
                                text="I'm sorry, but I cannot assist with inquiries regarding illegal, dangerous, or restricted topics."
                            )
                    # Active Privacy PII Redaction
                    part.text = active_redact_pii(part.text)
    return None

async def before_tool_callback(tool: BaseTool, args: dict, tool_context: ToolContext) -> dict | None:
    """Logs the intent of the agent before invoking external tools."""
    logger.info(f"--- [INTENT LOG] Calling tool '{tool.name}' with arguments: {args}")
    return None

async def after_tool_callback(tool: BaseTool, args: dict, tool_context: ToolContext, tool_response: dict) -> dict | None:
    """Logs the outcomes and results of the executed tools."""
    logger.info(f"--- [OUTCOME LOG] Tool '{tool.name}' returned status: {tool_response.get('status', 'unknown')}")
    return None


# ---------------------------------------------------------------------------
# 5. Multi-Agent Orchestration & Strategic Model Routing
# ---------------------------------------------------------------------------

destination_agent = Agent(
    model='gemini-3-flash-preview',
    name='destination_agent',
    description="A specialist agent that focuses strictly on identifying and planning top places to visit and sights.",
    instruction="""You are the destination specialist. Your unique role is to find the best attractions, sightseeing locations, and landmarks for a destination.
    You must use the 'get_places_to_visit' tool to get high-quality sightseeing results, then present them in an elegant, structured format.
    Always refer back to the coordinator or other agents once your task is complete.""",
    tools=[get_places_to_visit],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)

transport_agent = Agent(
    model='gemini-3-flash-preview',
    name='transport_agent',
    description="A specialist agent that focuses strictly on transportation routes, flight details, and inter-city transit.",
    instruction="""You are the transit and transportation specialist. Your unique role is to discover the best routes, flights, high-speed rail, or express bus options.
    Use the 'get_transportation_options' tool to fetch accurate, fast, and eco-friendly options, and summarize them beautifully.
    Always refer back to the coordinator or other agents once your task is complete.""",
    tools=[get_transportation_options],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)

budget_agent = Agent(
    model='gemini-3-flash-preview',
    name='budget_agent',
    description="A specialist agent that focuses strictly on trip pricing, budget breakdowns, and accommodation costs.",
    instruction="""You are the financial and budget specialist. Your unique role is to plan overall pricing, daily averages, and contingencies based on the selected travel style.
    Use the 'get_overall_pricing_estimate' tool to fetch accurate budget details, and present an itemized breakdown.
    Always refer back to the coordinator once your task is complete.""",
    tools=[pricing_tool],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)

root_agent = Agent(
    model='gemini-3-flash-preview',
    name='root_agent',
    description="The main coordinator that orchestrates the overall trip planning process and delegates to specialized sub-agents.",
    instruction="""You are the lead coordinator for the elite Trip Planner service. Your job is to orchestrate and delegate to your specialized sub-agents:
    1. For top sights and places to visit, delegate to 'destination_agent'.
    2. For flight, train, or road route options, delegate to 'transport_agent'.
    3. For budgeting, rates, and costs, delegate to 'budget_agent'.
    
    Inject the persistent user memories: {sqlite_user_memory} to tailor recommendations.
    
    Synthesize all their specialist findings into a cohesive, breathtaking master travel itinerary.
    If the user's query is simple or lacks details (such as origin or travel style), politely ask for clarification or use sensible defaults/guesses while letting them know.
    You can also use 'get_current_time' directly to answer any time-related questions.""",
    sub_agents=[destination_agent, transport_agent, budget_agent],
    tools=[get_current_time],
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
    before_model_callback=before_model_callback,
)


# ---------------------------------------------------------------------------
# 6. Advanced Context Optimization & Events Compaction App Configuration
# ---------------------------------------------------------------------------

from google.genai import types as genai_types

app = App(
    root_agent=root_agent,
    name="trip_planner",
    # Prevents context overflow on long sessions by automatically summarizing older events in a sliding window
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=15,  # Summarize every 15 events
        overlap_size=3,          # Keep last 3 events for seamless continuity
        summarizer=LlmEventSummarizer(llm=Gemini(model="gemini-3-flash-preview")),
    )
)
