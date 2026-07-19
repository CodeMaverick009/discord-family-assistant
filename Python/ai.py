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

MODEL = "gemini-3.1-flash-lite"

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

Your job is to analyze webpages, Instagram posts, YouTube videos, Google Maps pages, and other shared links.

Extract as much structured information as possible.

==========================
RULES
==========================

1. Use the webpage as the primary source.
2. If some information is missing but is publicly well known, you may use it.
3. Never invent facts.
4. If a value is unknown, leave it empty.
5. Return ONLY valid JSON.
6. Do NOT wrap the JSON inside ```json.

If a Google rating exists:
- store it in "google_rating"
- store the number of reviews in "google_reviews"

Never use the Google rating as the family score.

The family_score is YOUR own rating from 1-10 based on:

- family friendliness
- value
- accessibility
- entertainment
- overall experience

==========================
EVENTS
==========================

If the content describes an event, extract:

"display_date": "Friday 11–Sunday 13 September 2026",

Example:
Friday 11–Sunday 13 September 2026

"start_date": "YYYY-MM-DD",

Example:
2026-09-11

"end_date": "YYYY-MM-DD",
"start_time": "HH:MM",
"end_time": "HH:MM",

Example:
2026-09-13

Example:
10:00

Example:
18:00

Extract the most precise location possible.

If available include:

Venue
Street
City
Country

Never invent addresses or dates.

If only one date is mentioned, use the same value for both
start_date and end_date.

==========================
RECIPES
==========================

If the content is a recipe, also extract:

prep_time

cook_time

servings

difficulty

ingredients

steps

shopping_list

==========================
JSON SCHEMA
==========================

{{
    "category": "",
    "subcategory": "",

    "title": "",

    "summary": "",
    "description": "",

    "display_date": "",

    "start_date": "",
    "end_date": "",

    "start_time": "",
    "end_time": "",

    "location": "",
    "address": "",
    "city": "",
    "country": "",

    "website": "",
    "video_url": "",

    "estimated_visit_time": "",

    "best_for": "",

    "price_range": "",

    "opening_hours": "",

    "prep_time": "",
    "cook_time": "",
    "servings": "",
    "difficulty": "",

    "ingredients": [],

    "steps": [],

    "shopping_list": [],

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

recipe

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
mexican
chinese

concert
festival
football
car_show

breakfast
lunch
dinner
dessert
drink
snack

shopping_center

==========================
WEBPAGE INFORMATION
==========================

Title:
{page.get("title","")}

Meta Description:
{page.get("description","")}

Date:
{page.get("date","")}

Open Graph Title:
{page.get("og_title","")}

Open Graph Description:
{page.get("og_description","")}

Visible Website Content:
{page.get("text","")[:7000]}

Website URL:
{page.get("url","")}

==========================
IMPORTANT
==========================

If this is a famous place, restaurant, event or attraction, include:

- correct location
- city
- country
- useful summary
- highlights
- tips
- estimated visit time

IMPORTANT

The JSON MUST exactly match the schema above.

Do NOT create extra fields.

Do NOT return a field named "date".

For events, ALWAYS return:

"display_date"
"start_date"
"end_date"
"start_time"
"end_time"

If a value is unknown, return an empty string "".

Always include every field from the schema, even if it is empty.

Return ONLY valid JSON.
"""

    response = client.models.generate_content(
    model=MODEL,
    contents=prompt
    )

    return response.text.strip()