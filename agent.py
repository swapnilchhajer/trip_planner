from dotenv import load_dotenv
load_dotenv()

from google.adk.agents.llm_agent import Agent
from tools import get_places_to_visit, get_transportation_options, get_overall_pricing_estimate

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-3-flash-preview',
    name='root_agent',
    description="A helpful assistant that plans trips with itineraries, transportation options, and budget/pricing estimates.",
    instruction="""You are an expert trip planner. Your job is to help users plan amazing trips to their desired destinations.
When a user provides a destination, origin, number of days, and/or travel preferences:
1. Suggest top places to visit using the 'get_places_to_visit' tool.
2. Provide possible transportation options from their origin or general travel options using the 'get_transportation_options' tool.
3. Offer an overall pricing estimate for their trip based on the destination, duration, and travel style (budget, mid-range, or luxury) using the 'get_overall_pricing_estimate' tool.

Synthesize all this information into a beautifully structured, engaging, and professional travel itinerary and guide.
If the user's query is simple or lacks details (like origin or travel style), politely ask for clarification or use sensible defaults/guesses while letting them know.
You can also use 'get_current_time' if the user asks about the time in a city.""",
    tools=[get_current_time, get_places_to_visit, get_transportation_options, get_overall_pricing_estimate],
)

from google.adk.apps import App

app = App(root_agent=root_agent, name="trip_planner")
