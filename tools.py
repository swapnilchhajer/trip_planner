import random

def get_places_to_visit(destination: str) -> dict:
    """Returns a list of top places to visit in a specified destination (city, country, or region).

    Args:
        destination: The name of the destination, city, or country to visit.

    Returns:
        A dictionary containing the destination and a list of places to visit, each with details.
    """
    # Normalize destination for key matching
    dest_lower = destination.lower().strip()
    
    # Predefined mock database for highly professional answers
    database = {
        "paris": [
            {"name": "Eiffel Tower", "description": "Iconic iron lattice tower on the Champ de Mars, offering panoramic city views.", "category": "Landmark", "recommended_duration": "2-3 hours"},
            {"name": "Louvre Museum", "description": "The world's largest art museum, home to the Mona Lisa and Venus de Milo.", "category": "Museum / Culture", "recommended_duration": "3-4 hours"},
            {"name": "Notre-Dame Cathedral", "description": "A masterpiece of French Gothic architecture, located on the Île de la Cité.", "category": "Historical / Religious", "recommended_duration": "1-2 hours"},
            {"name": "Champs-Élysées & Arc de Triomphe", "description": "Famous avenue lined with shops and cafes, culminating at the monumental triumphal arch.", "category": "Sightseeing", "recommended_duration": "1-2 hours"},
            {"name": "Seine River Cruise", "description": "A scenic boat tour along the river Seine, passing under historic bridges.", "category": "Activity", "recommended_duration": "1 hour"}
        ],
        "tokyo": [
            {"name": "Senso-ji Temple", "description": "Tokyo's oldest and most significant Buddhist temple, located in Asakusa.", "category": "Historical / Religious", "recommended_duration": "1-2 hours"},
            {"name": "Shibuya Crossing", "description": "The world's busiest pedestrian intersection, a vibrant symbol of modern Tokyo.", "category": "Landmark / Sightseeing", "recommended_duration": "1 hour"},
            {"name": "Meiji Jingu Shrine", "description": "A serene Shinto shrine dedicated to Emperor Meiji, nestled in a dense forest.", "category": "Historical / Nature", "recommended_duration": "1-2 hours"},
            {"name": "Tokyo Skytree", "description": "The tallest structure in Japan, offering breathtaking 360-degree views of the city.", "category": "Landmark", "recommended_duration": "1-2 hours"},
            {"name": "Akihabara", "description": "The ultimate district for electronics, gaming, anime, and manga culture.", "category": "Shopping / Culture", "recommended_duration": "3-4 hours"}
        ],
        "london": [
            {"name": "British Museum", "description": "World-famous museum dedicated to human history, art, and culture.", "category": "Museum / Culture", "recommended_duration": "3-4 hours"},
            {"name": "Tower of London & Tower Bridge", "description": "Historic castle on the north bank of the River Thames, alongside the iconic bridge.", "category": "Historical", "recommended_duration": "2-3 hours"},
            {"name": "London Eye", "description": "Giant Ferris wheel on the South Bank, offering modern views of the London skyline.", "category": "Landmark", "recommended_duration": "1 hour"},
            {"name": "Westminster Abbey & Big Ben", "description": "The Gothic abbey church and the clock tower, landmarks of British political history.", "category": "Historical / Landmark", "recommended_duration": "2 hours"},
            {"name": "Hyde Park", "description": "One of the largest royal parks in London, perfect for a relaxing walk or boating.", "category": "Nature / Park", "recommended_duration": "1-2 hours"}
        ],
        "japan": [
            {"name": "Fushimi Inari-taisha Shrine (Kyoto)", "description": "Famous shrine known for its path of thousands of vibrant orange torii gates.", "category": "Historical / Religious", "recommended_duration": "2-3 hours"},
            {"name": "Mount Fuji", "description": "Japan's iconic snow-capped volcanic peak, a sacred and scenic masterpiece.", "category": "Nature", "recommended_duration": "1 day"},
            {"name": "Todai-ji Temple (Nara)", "description": "Massive temple housing one of Japan's largest bronze Buddha statues, surrounded by free-roaming deer.", "category": "Historical", "recommended_duration": "2 hours"},
            {"name": "Shibuya Crossing (Tokyo)", "description": "The iconic multi-way crosswalk representing modern Japanese urban energy.", "category": "Landmark", "recommended_duration": "1 hour"},
            {"name": "Hiroshima Peace Memorial Park", "description": "A deeply moving memorial park dedicated to legacy of the atomic bomb and world peace.", "category": "Historical", "recommended_duration": "2 hours"}
        ],
        "france": [
            {"name": "Eiffel Tower (Paris)", "description": "Iconic iron tower representing French culture and offering unmatched views.", "category": "Landmark", "recommended_duration": "2 hours"},
            {"name": "Palace of Versailles", "description": "The opulent royal residence of King Louis XIV, featuring the Hall of Mirrors.", "category": "Historical / Palace", "recommended_duration": "3-4 hours"},
            {"name": "French Riviera (Côte d'Azur)", "description": "The glamorous Mediterranean coastline known for beaches, yachts, and cities like Nice and Cannes.", "category": "Nature / Resort", "recommended_duration": "2-3 days"},
            {"name": "Mont Saint-Michel", "description": "A stunning medieval abbey built on a rocky tidal island in Normandy.", "category": "Historical / Landmark", "recommended_duration": "4-5 hours"},
            {"name": "Chamonix-Mont-Blanc", "description": "A world-renowned alpine resort area at the foot of Mont Blanc, ideal for skiing and hiking.", "category": "Nature / Adventure", "recommended_duration": "1-2 days"}
        ]
    }
    
    # Match database or generate fallback places to visit dynamically
    for key in database:
        if key in dest_lower:
            return {
                "status": "success",
                "destination": destination,
                "places": database[key]
            }
            
    # Dynamic fallback generator for any other destination
    fallback_places = [
        {
            "name": f"Historic Old Town of {destination}",
            "description": f"The charming, historic heart of {destination}, filled with classic architecture, local shops, and cafes.",
            "category": "Historical / Cultural",
            "recommended_duration": "2-3 hours"
        },
        {
            "name": f"{destination} City Park",
            "description": f"A beautiful green sanctuary offering walking paths, scenic views, and a peaceful escape from the urban rush.",
            "category": "Nature / Relaxation",
            "recommended_duration": "1-2 hours"
        },
        {
            "name": f"Grand Museum of {destination}",
            "description": f"The premier cultural institution in {destination}, showcasing regional history, artifacts, and art collections.",
            "category": "Museum / Culture",
            "recommended_duration": "2-3 hours"
        },
        {
            "name": f"Main Observation Deck",
            "description": f"The best vantage point in {destination} to capture breathtaking panoramic views of the entire region.",
            "category": "Sightseeing / Landmark",
            "recommended_duration": "1 hour"
        },
        {
            "name": f"Local Market Square",
            "description": f"A bustling market where visitors can sample authentic street food, buy local crafts, and experience daily life.",
            "category": "Food / Shopping",
            "recommended_duration": "1-2 hours"
        }
    ]
    
    return {
        "status": "success",
        "destination": destination,
        "places": fallback_places
    }


def get_transportation_options(origin: str, destination: str) -> dict:
    """Returns a list of possible transportation options between the origin and destination.

    Args:
        origin: The starting location of the trip.
        destination: The destination city, country, or place.

    Returns:
        A dictionary with status, origin, destination, and details of possible transportation options.
    """
    options = []
    
    # Flight option (generally applicable for far distances)
    options.append({
        "mode": "Flight",
        "description": f"Direct or connecting commercial flights from {origin} to nearest airport to {destination}.",
        "estimated_duration": "2-12 hours depending on stops and route",
        "price_range_usd": "150 - 800 (economy round-trip)",
        "frequency": "Multiple daily options"
    })
    
    # Train option (applicable for typical mid-range distances or specific routes)
    options.append({
        "mode": "Train",
        "description": "High-speed or regional train networks connecting the areas.",
        "estimated_duration": "3-8 hours depending on directness",
        "price_range_usd": "50 - 150",
        "frequency": "Several departures per day"
    })
    
    # Bus/Coach option
    options.append({
        "mode": "Express Bus / Coach",
        "description": "Intercity budget bus service with comfortable amenities.",
        "estimated_duration": "5-12 hours depending on traffic",
        "price_range_usd": "25 - 60",
        "frequency": "Daily departures"
    })
    
    # Car Rental / Road Trip option
    options.append({
        "mode": "Car Rental",
        "description": "Drive yourself via scenic highways.",
        "estimated_duration": "Varies (highly flexible)",
        "price_range_usd": "40 - 100 per day + fuel and toll costs",
        "frequency": "On-demand (unlimited flexibility)"
    })
    
    return {
        "status": "success",
        "origin": origin,
        "destination": destination,
        "transportation_options": options
    }


def get_overall_pricing_estimate(destination: str, days: int, travel_style: str) -> dict:
    """Estimates overall pricing and budget breakdown for a trip of a given number of days to a destination.

    Args:
        destination: The destination city, country, or place.
        days: The duration of the trip in days.
        travel_style: The style of travel. Choose from 'budget', 'mid-range', or 'luxury'.

    Returns:
        A dictionary containing the pricing breakdown, daily average cost, and total estimated budget.
    """
    style = travel_style.lower().strip()
    if style not in ["budget", "mid-range", "luxury"]:
        style = "mid-range"  # Safe default if input is unexpected
        
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
        }
    }
    
    selected_rates = rates[style]
    
    # Calculate costs
    nights = max(1, days - 1) if days > 0 else 1
    accommodation_total = selected_rates["accommodation_per_night"] * nights
    meals_total = selected_rates["meals_per_day"] * days
    activities_total = selected_rates["activities_per_day"] * days
    local_transport_total = selected_rates["local_transport_per_day"] * days
    
    subtotal = accommodation_total + meals_total + activities_total + local_transport_total
    contingency = round(subtotal * 0.10, 2)
    grand_total = round(subtotal + contingency, 2)
    
    breakdown = {
        "accommodation": {
            "rate_per_night_usd": selected_rates["accommodation_per_night"],
            "nights": nights,
            "total_usd": round(accommodation_total, 2)
        },
        "meals_and_food": {
            "rate_per_day_usd": selected_rates["meals_per_day"],
            "days": days,
            "total_usd": round(meals_total, 2)
        },
        "activities_and_sightseeing": {
            "rate_per_day_usd": selected_rates["activities_per_day"],
            "days": days,
            "total_usd": round(activities_total, 2)
        },
        "local_transportation": {
            "rate_per_day_usd": selected_rates["local_transport_per_day"],
            "days": days,
            "total_usd": round(local_transport_total, 2)
        },
        "miscellaneous_contingency": {
            "percentage": "10%",
            "total_usd": contingency
        }
    }
    
    return {
        "status": "success",
        "destination": destination,
        "duration_days": days,
        "travel_style": style,
        "average_cost_per_day_usd": round(grand_total / days, 2) if days > 0 else grand_total,
        "estimated_grand_total_usd": grand_total,
        "breakdown": breakdown
    }
