# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Pydantic Schemas for Explicit JSON Input/Output Verification
# ---------------------------------------------------------------------------


class Place(BaseModel):
    name: str = Field(description="Name of the attraction or sight.")
    description: str = Field(description="Descriptive overview of the attraction.")
    category: str = Field(
        description="Category of the sight (e.g., Landmark, Museum, Nature)."
    )
    recommended_duration: str = Field(description="Recommended duration for visiting.")


class PlacesToVisitResponse(BaseModel):
    status: str = Field(description="Execution status, always 'success'.")
    destination: str = Field(description="The destination planned.")
    places: list[Place] = Field(description="List of top places to visit.")


class TransitOption(BaseModel):
    mode: str = Field(
        description="Mode of transportation (e.g., Flight, High-Speed Train, Express Bus, Car Rental)."
    )
    duration: str = Field(description="Estimated duration of the transit.")
    price_range_usd: str = Field(description="Estimated price range in USD.")
    frequency: str = Field(description="How often this transit option is available.")
    details: str = Field(description="Additional details about the route.")


class TransportationOptionsResponse(BaseModel):
    status: str = Field(description="Execution status, always 'success'.")
    origin: str = Field(description="The starting location.")
    destination: str = Field(description="The final destination.")
    transportation_options: list[TransitOption] = Field(
        description="List of transit options between origin and destination."
    )


class CostItem(BaseModel):
    rate_per_day_usd: float = Field(description="Daily rate in USD.")
    days: int = Field(description="Number of days.")
    total_usd: float = Field(description="Total cost in USD.")


class AccommodationItem(BaseModel):
    rate_per_night_usd: float = Field(description="Nightly rate in USD.")
    nights: int = Field(description="Number of nights.")
    total_usd: float = Field(description="Total cost in USD.")


class ContingencyItem(BaseModel):
    percentage: str = Field(description="Contingency percentage of the subtotal.")
    total_usd: float = Field(description="Contingency buffer in USD.")


class PricingBreakdown(BaseModel):
    accommodation: AccommodationItem = Field(
        description="Accommodation budget details."
    )
    meals_and_food: CostItem = Field(description="Food and meals budget details.")
    activities_and_sightseeing: CostItem = Field(
        description="Sightseeing and activities budget details."
    )
    local_transportation: CostItem = Field(description="Local transit budget details.")
    miscellaneous_contingency: ContingencyItem = Field(
        description="Safety margin and contingency details."
    )


class PricingEstimateResponse(BaseModel):
    status: str = Field(description="Execution status, always 'success'.")
    destination: str = Field(description="Destination being planned.")
    duration_days: int = Field(description="Trip duration in days.")
    travel_style: str = Field(description="Travel style (budget, mid-range, luxury).")
    average_cost_per_day_usd: float = Field(description="Average cost per day in USD.")
    estimated_grand_total_usd: float = Field(description="Total estimated cost in USD.")
    breakdown: PricingBreakdown = Field(description="Itemized budget breakdown.")


class ErrorResponse(BaseModel):
    status: str = Field(description="Execution status, always 'error' on failures.")
    error_code: str = Field(
        description="Machine-readable error identifier for programmatic parsing."
    )
    message: str = Field(description="Human-readable explanation of what went wrong.")
    recovery_instructions: str = Field(
        description="Guided instructions instructing the LLM how to recover and what clarification to ask the user."
    )


# ---------------------------------------------------------------------------
# Guided Error Recovery Tools with Explicit JSON Output Schemas
# ---------------------------------------------------------------------------


def get_places_to_visit(destination: str) -> PlacesToVisitResponse | ErrorResponse:
    """Returns a list of top places to visit in a specified destination (city, country, or region).

    Args:
        destination: The name of the destination, city, or country to visit.

    Returns:
        Structured PlacesToVisitResponse on success or ErrorResponse on failure.
    """
    # GUIDED ERROR HANDLING: Verify input destination
    if not destination or not destination.strip():
        return ErrorResponse(
            status="error",
            error_code="INVALID_DESTINATION",
            message="Destination is missing or empty.",
            recovery_instructions="Please politely ask the user to specify a destination city, country, or place they would like to visit.",
        )

    # Normalize destination for key matching
    dest_lower = destination.lower().strip()

    # Predefined mock database for highly professional answers
    database = {
        "paris": [
            {
                "name": "Eiffel Tower",
                "description": "Iconic iron lattice tower on the Champ de Mars, offering panoramic city views.",
                "category": "Landmark",
                "recommended_duration": "2-3 hours",
            },
            {
                "name": "Louvre Museum",
                "description": "The world's largest art museum, home to the Mona Lisa and Venus de Milo.",
                "category": "Museum / Culture",
                "recommended_duration": "3-4 hours",
            },
            {
                "name": "Notre-Dame Cathedral",
                "description": "A masterpiece of French Gothic architecture, located on the Île de la Cité.",
                "category": "Historical / Religious",
                "recommended_duration": "1-2 hours",
            },
            {
                "name": "Champs-Élysées & Arc de Triomphe",
                "description": "Famous avenue lined with shops and cafes, culminating at the monumental triumphal arch.",
                "category": "Sightseeing",
                "recommended_duration": "1-2 hours",
            },
            {
                "name": "Seine River Cruise",
                "description": "A scenic boat tour along the river Seine, passing under historic bridges.",
                "category": "Activity",
                "recommended_duration": "1 hour",
            },
        ],
        "tokyo": [
            {
                "name": "Senso-ji Temple",
                "description": "Tokyo's oldest and most significant Buddhist temple, located in Asakusa.",
                "category": "Historical / Religious",
                "recommended_duration": "1-2 hours",
            },
            {
                "name": "Shibuya Crossing",
                "description": "The world's busiest pedestrian intersection, a vibrant symbol of modern Tokyo.",
                "category": "Landmark / Sightseeing",
                "recommended_duration": "1 hour",
            },
            {
                "name": "Meiji Jingu Shrine",
                "description": "A serene Shinto shrine dedicated to Emperor Meiji, nestled in a dense forest.",
                "category": "Historical / Nature",
                "recommended_duration": "1-2 hours",
            },
            {
                "name": "Tokyo Skytree",
                "description": "The tallest structure in Japan, offering breathtaking 360-degree views of the city.",
                "category": "Landmark",
                "recommended_duration": "1-2 hours",
            },
            {
                "name": "Akihabara",
                "description": "The ultimate district for electronics, gaming, anime, and manga culture.",
                "category": "Shopping / Culture",
                "recommended_duration": "3-4 hours",
            },
        ],
        "london": [
            {
                "name": "British Museum",
                "description": "World-famous museum dedicated to human history, art, and culture.",
                "category": "Museum / Culture",
                "recommended_duration": "3-4 hours",
            },
            {
                "name": "Tower of London & Tower Bridge",
                "description": "Historic castle on the north bank of the River Thames, alongside the iconic bridge.",
                "category": "Historical",
                "recommended_duration": "2-3 hours",
            },
            {
                "name": "London Eye",
                "description": "Giant Ferris wheel on the South Bank, offering modern views of the London skyline.",
                "category": "Landmark",
                "recommended_duration": "1 hour",
            },
            {
                "name": "Westminster Abbey & Big Ben",
                "description": "The Gothic abbey church and the clock tower, landmarks of British political history.",
                "category": "Historical / Landmark",
                "recommended_duration": "2 hours",
            },
            {
                "name": "Hyde Park",
                "description": "One of the largest royal parks in London, perfect for a relaxing walk or boating.",
                "category": "Nature / Park",
                "recommended_duration": "1-2 hours",
            },
        ],
        "japan": [
            {
                "name": "Fushimi Inari-taisha Shrine (Kyoto)",
                "description": "Famous shrine known for its path of thousands of vibrant orange torii gates.",
                "category": "Historical / Religious",
                "recommended_duration": "2-3 hours",
            },
            {
                "name": "Mount Fuji",
                "description": "Japan's iconic snow-capped volcanic peak, a sacred and scenic masterpiece.",
                "category": "Nature",
                "recommended_duration": "1 day",
            },
            {
                "name": "Todai-ji Temple (Nara)",
                "description": "Massive temple housing one of Japan's largest bronze Buddha statues, surrounded by free-roaming deer.",
                "category": "Historical",
                "recommended_duration": "2 hours",
            },
            {
                "name": "Shibuya Crossing (Tokyo)",
                "description": "The iconic multi-way crosswalk representing modern Japanese urban energy.",
                "category": "Landmark",
                "recommended_duration": "1 hour",
            },
            {
                "name": "Hiroshima Peace Memorial Park",
                "description": "A deeply moving memorial park dedicated to legacy of the atomic bomb and world peace.",
                "category": "Historical",
                "recommended_duration": "2 hours",
            },
        ],
        "france": [
            {
                "name": "Eiffel Tower (Paris)",
                "description": "Iconic iron tower representing French culture and offering unmatched views.",
                "category": "Landmark",
                "recommended_duration": "2 hours",
            },
            {
                "name": "Palace of Versailles",
                "description": "The opulent royal residence of King Louis XIV, featuring the Hall of Mirrors.",
                "category": "Historical / Palace",
                "recommended_duration": "3-4 hours",
            },
            {
                "name": "French Riviera (Côte d'Azur)",
                "description": "The glamorous Mediterranean coastline known for beaches, yachts, and cities like Nice and Cannes.",
                "category": "Nature / Resort",
                "recommended_duration": "2-3 days",
            },
            {
                "name": "Mont Saint-Michel",
                "description": "A stunning medieval abbey built on a rocky tidal island in Normandy.",
                "category": "Historical / Landmark",
                "recommended_duration": "4-5 hours",
            },
            {
                "name": "Chamonix-Mont-Blanc",
                "description": "A world-renowned alpine resort area at the foot of Mount Fuji / Mont Blanc, ideal for skiing and hiking.",
                "category": "Nature / Adventure",
                "recommended_duration": "1-2 days",
            },
        ],
    }

    # Match database or generate fallback places to visit dynamically
    for key in database:
        if key in dest_lower:
            places_list = [Place(**p) for p in database[key]]
            return PlacesToVisitResponse(
                status="success", destination=destination, places=places_list
            )

    # Dynamic fallback generator for any other destination
    fallback_places = [
        Place(
            name=f"Historic Old Town of {destination}",
            description=f"The charming, historic heart of {destination}, filled with classic architecture, local shops, and cafes.",
            category="Historical / Cultural",
            recommended_duration="2-3 hours",
        ),
        Place(
            name=f"{destination} City Park",
            description="A beautiful green sanctuary offering walking paths, scenic views, and a peaceful escape from the urban rush.",
            category="Nature / Relaxation",
            recommended_duration="1-2 hours",
        ),
        Place(
            name=f"Grand Museum of {destination}",
            description=f"The premier cultural institution in {destination}, showcasing regional history, artifacts, and art collections.",
            category="Museum / Culture",
            recommended_duration="2-3 hours",
        ),
        Place(
            name="Main Observation Deck",
            description=f"The best vantage point in {destination} to capture breathtaking panoramic views of the entire region.",
            category="Sightseeing / Landmark",
            recommended_duration="1 hour",
        ),
        Place(
            name="Local Market Square",
            description="A bustling market where visitors can sample authentic street food, buy local crafts, and experience daily life.",
            category="Food / Shopping",
            recommended_duration="1-2 hours",
        ),
    ]

    return PlacesToVisitResponse(
        status="success", destination=destination, places=fallback_places
    )


def get_transportation_options(
    origin: str, destination: str
) -> TransportationOptionsResponse | ErrorResponse:
    """Provides a list of possible transportation options from an origin to a destination with details.

    Args:
        origin: The starting city or country.
        destination: The destination city or country.

    Returns:
        Structured TransportationOptionsResponse on success or ErrorResponse on failure.
    """
    # GUIDED ERROR HANDLING: Verify inputs
    if not origin or not origin.strip():
        return ErrorResponse(
            status="error",
            error_code="INVALID_ORIGIN",
            message="Origin starting location is missing or empty.",
            recovery_instructions="Please politely ask the user what starting city or country they are traveling from so I can compute accurate travel options.",
        )

    if not destination or not destination.strip():
        return ErrorResponse(
            status="error",
            error_code="INVALID_DESTINATION",
            message="Destination location is missing or empty.",
            recovery_instructions="Please politely ask the user where they are planning to travel.",
        )

    orig_lower = origin.lower().strip()
    dest_lower = destination.lower().strip()

    options = []

    # London to Paris Specifics
    if "london" in orig_lower and "paris" in dest_lower:
        options = [
            TransitOption(
                mode="High-Speed Train (Eurostar)",
                duration="2 hours 16 mins",
                price_range_usd="70 - 180",
                frequency="Up to 15 departures per day",
                details="Departs from St Pancras International, arrives at Paris Gare du Nord. Fast, sustainable, and directly city-center to city-center.",
            ),
            TransitOption(
                mode="Flight",
                duration="1 hour 15 mins (flight time)",
                price_range_usd="50 - 150",
                frequency="Frequent daily flights",
                details="Flights from Heathrow, Gatwick, or Luton to Paris CDG or Orly. Requires airport transfer and security queues, adding 3-4 hours total travel time.",
            ),
            TransitOption(
                mode="Express Bus (FlixBus / BlaBlaCar)",
                duration="8 - 9 hours",
                price_range_usd="30 - 60",
                frequency="3-5 times per day",
                details="Budget-friendly option utilizing the Eurotunnel or ferry crossing. Includes scenic views and stops.",
            ),
        ]
    # US to Tokyo/Japan Specifics
    elif (
        "new york" in orig_lower
        or "san francisco" in orig_lower
        or "los angeles" in orig_lower
    ) and ("tokyo" in dest_lower or "japan" in dest_lower):
        options = [
            TransitOption(
                mode="Direct Flight (Premium / Luxury First & Business)",
                duration="14 hours (from NYC) / 11 hours (from West Coast)",
                price_range_usd="1,200 - 8,000 (Round-trip)",
                frequency="Daily departures",
                details="Available via ANA, Japan Airlines, United, or Delta. Business and First class feature full flatbed suites, five-star dining, and luxury airport lounges.",
            ),
            TransitOption(
                mode="Direct Flight (Economy)",
                duration="14 hours (from NYC) / 11 hours (from West Coast)",
                price_range_usd="600 - 1,400 (Round-trip)",
                frequency="Multiple flights daily",
                details="Great budget or standard travel option directly into Tokyo Haneda (HND) or Narita (NRT) airports.",
            ),
        ]
    else:
        # Realistic fallback generator
        options = [
            TransitOption(
                mode="International Flight",
                duration="Depends on routing (approx 8-12 hours)",
                price_range_usd="400 - 1,200",
                frequency="Daily departures",
                details=f"Connecting or direct air travel from {origin} to closest international airport in {destination}.",
            ),
            TransitOption(
                mode="Self-Drive / Car Rental",
                duration="Flexible",
                price_range_usd="50 - 120 per day",
                frequency="Available 24/7",
                details="Excellent option for exploring regional countryside and stopping in scenic villages at your own pace.",
            ),
        ]

    return TransportationOptionsResponse(
        status="success",
        origin=origin,
        destination=destination,
        transportation_options=options,
    )


def get_overall_pricing_estimate(
    destination: str, days: int, travel_style: str
) -> PricingEstimateResponse | ErrorResponse:
    """Estimates overall pricing and budget breakdown for a trip of a given number of days to a destination.

    Args:
        destination: The destination city, country, or place.
        days: The duration of the trip in days.
        travel_style: The style of travel. Choose from 'budget', 'mid-range', or 'luxury'.

    Returns:
        Structured PricingEstimateResponse on success or ErrorResponse on failure.
    """
    # GUIDED ERROR HANDLING: Verify inputs
    if not destination or not destination.strip():
        return ErrorResponse(
            status="error",
            error_code="INVALID_DESTINATION",
            message="Destination location is missing or empty.",
            recovery_instructions="Please politely ask the user where they are planning to travel.",
        )

    if days <= 0:
        return ErrorResponse(
            status="error",
            error_code="INVALID_DURATION",
            message=f"Trip duration '{days}' is invalid. It must be at least 1 day.",
            recovery_instructions="The user provided an invalid duration. Please politely ask the user to clarify how many days they would like to travel for (minimum 1 day).",
        )

    style = travel_style.lower().strip()
    if style not in ["budget", "mid-range", "luxury"]:
        style = "mid-range"  # Safe default if input is unexpected

    # Determine if destination is premium (e.g., Tokyo, Paris, London, Japan, France)
    dest_lower = destination.lower()
    premium_destinations = ["tokyo", "paris", "london", "japan", "france"]
    is_premium = any(p in dest_lower for p in premium_destinations)

    if is_premium:
        # Premium/high-cost destination rates
        rates = {
            "budget": {
                "accommodation_per_night": 60.0,
                "meals_per_day": 25.0,
                "activities_per_day": 15.0,
                "local_transport_per_day": 12.0,
            },
            "mid-range": {
                "accommodation_per_night": 180.0,
                "meals_per_day": 65.0,
                "activities_per_day": 45.0,
                "local_transport_per_day": 22.0,
            },
            "luxury": {
                "accommodation_per_night": 850.0,
                "meals_per_day": 220.0,
                "activities_per_day": 150.0,
                "local_transport_per_day": 80.0,
            },
        }
    else:
        # Standard rates based on style
        rates = {
            "budget": {
                "accommodation_per_night": 30.0,
                "meals_per_day": 15.0,
                "activities_per_day": 10.0,
                "local_transport_per_day": 8.0,
            },
            "mid-range": {
                "accommodation_per_night": 90.0,
                "meals_per_day": 40.0,
                "activities_per_day": 25.0,
                "local_transport_per_day": 15.0,
            },
            "luxury": {
                "accommodation_per_night": 280.0,
                "meals_per_day": 120.0,
                "activities_per_day": 80.0,
                "local_transport_per_day": 45.0,
            },
        }

    selected_rates = rates[style]

    # Calculate costs
    nights = max(1, days - 1)
    accommodation_total = selected_rates["accommodation_per_night"] * nights
    meals_total = selected_rates["meals_per_day"] * days
    activities_total = selected_rates["activities_per_day"] * days
    local_transport_total = selected_rates["local_transport_per_day"] * days

    subtotal = (
        accommodation_total + meals_total + activities_total + local_transport_total
    )
    contingency = round(subtotal * 0.10, 2)
    grand_total = round(subtotal + contingency, 2)

    breakdown = PricingBreakdown(
        accommodation=AccommodationItem(
            rate_per_night_usd=selected_rates["accommodation_per_night"],
            nights=nights,
            total_usd=round(accommodation_total, 2),
        ),
        meals_and_food=CostItem(
            rate_per_day_usd=selected_rates["meals_per_day"],
            days=days,
            total_usd=round(meals_total, 2),
        ),
        activities_and_sightseeing=CostItem(
            rate_per_day_usd=selected_rates["activities_per_day"],
            days=days,
            total_usd=round(activities_total, 2),
        ),
        local_transportation=CostItem(
            rate_per_day_usd=selected_rates["local_transport_per_day"],
            days=days,
            total_usd=round(local_transport_total, 2),
        ),
        miscellaneous_contingency=ContingencyItem(
            percentage="10%", total_usd=contingency
        ),
    )

    return PricingEstimateResponse(
        status="success",
        destination=destination,
        duration_days=days,
        travel_style=style,
        average_cost_per_day_usd=round(grand_total / days, 2)
        if days > 0
        else grand_total,
        estimated_grand_total_usd=grand_total,
        breakdown=breakdown,
    )
