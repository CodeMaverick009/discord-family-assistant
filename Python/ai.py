import os
from dotenv import load_dotenv
from google import genai

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"

# ==========================================
# Normal AI Chat
# ==========================================

def ask_ai(prompt: str):

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


# ==========================================
# Analyze Shared Websites
# ==========================================

def analyze_page(page):

    prompt = f"""
You are Family Assistant.

You help families organize places, restaurants, trips, events and shopping ideas.

Your job is to analyze the webpage below and return structured information.

==========================
RULES
==========================

1. Use the webpage as your primary source.
2. If important information is missing (for example location or famous attractions),
   use well-known public knowledge.
3. Never invent facts.
4. If you are unsure, leave the field empty.
5. Return ONLY valid JSON.
6. Do NOT wrap the JSON inside ```json ```.

If the webpage contains an official public rating (such as a Google Maps rating),
store it in "google_rating".

Store the number of reviews in "google_reviews".

Then estimate a separate "family_score" from 1-10 based on how suitable
the place is for families.

Never use the Google rating as the family score.

If the content describes an event:

- Extract the exact event date if mentioned.
- Extract the exact start time if mentioned.
- Extract the end time if mentioned.
- Extract the full address if available.
- If there is no full address, extract the most precise location possible.
- Never invent an address.
- Include the official website if available.

If the event takes place over multiple days, include both the start and end dates.

If the location is only a city, return the city.

If the location is a venue, include:
Venue Name
Street
City
Country

==========================
JSON SCHEMA
==========================

{{
    "category": "",
    "subcategory": "",
    "title": "",
    "date":"",
    "summary": "",
    "description": "",
    "location": "",
    "address": "",
    "city": "",
    "country": "",
    "website": "",
    "estimated_visit_time": "",
    "best_for": "",
    "price_range": "",
    "opening_hours": "",
    "google_rating": 0,
    "google_reviews": 0,
    "family_score": 0,
    "confidence": 0.0,
    "highlights": [],
    "tips": []
}}

==========================
ALLOWED CATEGORIES
==========================

place
restaurant
event
shopping
trip
unknown

==========================
EXAMPLE SUBCATEGORIES
==========================

theme_park
museum
zoo
water_park
beach
nature
hotel
camping
italian
indian
japanese
concert
festival
football
shopping_center

==========================
WEBPAGE INFORMATION
==========================

Title:
{page.get("title", "")}

Meta Description:
{page.get("description", "")}

Date:
{page.get("date", "")}

Open Graph Title:
{page.get("og_title", "")}

Open Graph Description:
{page.get("og_description", "")}

Visible Website Content:
{page.get("text", "")[:5000]}

Website URL:
{page.get("url", "")}

==========================
IMPORTANT
==========================

If this is a well-known place, include:

- Correct location
- Country
- Good summary
- Useful highlights
- Family tips
- Visit duration

Return ONLY JSON.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()