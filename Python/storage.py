import json
import os
from pathlib import Path
from datetime import datetime

# ==========================================
# Data Folder
# ==========================================

DATA_FOLDER = Path("data")

DATA_FOLDER.mkdir(exist_ok=True)

FILES = {
    "place": "places.json",
    "restaurant": "restaurants.json",
    "event": "events.json",
    "shopping": "shopping.json",
    "trip": "trips.json",
    "unknown": "unknown.json"
}


# ==========================================
# Create file if it doesn't exist
# ==========================================

def ensure_file(category):

    filename = FILES.get(category, "unknown.json")

    path = DATA_FOLDER / filename

    if not path.exists():
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    return path


# ==========================================
# Save item
# ==========================================

def save_item(data):

    category = data.get("category", "unknown").lower()

    path = ensure_file(category)

    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)

    data["date_added"] = datetime.now().isoformat()

    items.append(data)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            items,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# Check duplicate
# ==========================================

def already_exists(data):
    """
    Returns the existing item if found, otherwise None.
    """

    website = data.get("website", "").strip().lower()
    title = data.get("title", "").strip().lower()

    for file in DATA_FOLDER.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:
            items = json.load(f)

        for item in items:

            saved_website = item.get("website", "").strip().lower()
            saved_title = item.get("title", "").strip().lower()

            if website and website == saved_website:
                return item

            if title and title == saved_title:
                return item

    return None