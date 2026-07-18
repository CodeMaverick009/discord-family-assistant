import os
import re
import json
from pathlib import Path
from views import PlaceView
import discord
from discord.ext import commands
from dotenv import load_dotenv

from recipe_embed import create_recipe_embed
from maps import extract_place_name
from maps import scrape_google_maps
from storage import save_item, already_exists
from ai import ask_ai, analyze_page
from scraper import scrape_page
from instagram import scrape_instagram
from config import (
    IDEAS_CHANNEL,
    SAVED_PLACES_CHANNEL,
    FAVORITES_CHANNEL,
    MAPS_CHANNEL,
    RESTAURANTS_CHANNEL,
    CALENDAR_CHANNEL,
    SHOPPING_CHANNEL,
    TRIPS_CHANNEL,

    BREAKFAST_CHANNEL,
    LUNCH_CHANNEL,
    DINNER_CHANNEL,
    DESSERT_CHANNEL,
    DRINKS_CHANNEL,
    SNACKS_CHANNEL,
)
# ==========================================
# Icons & Colors
# ==========================================

CATEGORY_ICONS = {
    "place": "🎢",
    "restaurant": "🍽️",
    "event": "🎉",
    "shopping": "🛍️",
    "trip": "✈️",
    "unknown": "📌"
}

SUBCATEGORY_ICONS = {
    "theme_park": "🎢",
    "museum": "🏛️",
    "zoo": "🦁",
    "water_park": "🌊",
    "beach": "🏖️",
    "nature": "🌳",
    "hotel": "🏨",
    "camping": "🏕️",
    "shopping_center": "🛍️",
    "italian": "🍝",
    "indian": "🍛",
    "japanese": "🍣",
    "concert": "🎵",
    "festival": "🎪",
    "football": "⚽"
}

CATEGORY_COLORS = {
    "place": discord.Color.green(),
    "restaurant": discord.Color.orange(),
    "event": discord.Color.red(),
    "shopping": discord.Color.gold(),
    "trip": discord.Color.blue(),
    "unknown": discord.Color.light_grey()
}

# ==========================================
# Load Environment Variables
# ==========================================

dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found!")

# ==========================================
# Discord Setup
# ==========================================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ==========================================
# Category Routing
# ==========================================

CATEGORY_TO_CHANNEL = {
    "place": SAVED_PLACES_CHANNEL,
    "restaurant": RESTAURANTS_CHANNEL,
    "event": CALENDAR_CHANNEL,
    "shopping": SHOPPING_CHANNEL,
    "trip": TRIPS_CHANNEL,
    "breakfast": BREAKFAST_CHANNEL,
    "lunch": LUNCH_CHANNEL,
    "dinner": DINNER_CHANNEL,
    "dessert": DESSERT_CHANNEL,
    "drink": DRINKS_CHANNEL,
    "snack": SNACKS_CHANNEL,
}

# ==========================================
# Events
# ==========================================

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("🤖 Family Assistant is online!")
    print("-" * 50)


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    # Keep commands working
    await bot.process_commands(message)

    print("\n==============================")
    print("Message:", message.content)
    print("Channel ID:", message.channel.id)

    # Only monitor the Ideas channel
    if message.channel.id != IDEAS_CHANNEL:
        print("❌ Wrong channel")
        return

    # Find URLs
    url_pattern = r"https?://[^\s]+"
    urls = re.findall(url_pattern, message.content)

    if not urls:
        print("❌ No URL detected")
        return

    url = urls[0]

    # Google Maps detection
    is_google_maps = (
        "google.com/maps" in url
        or "maps.app.goo.gl" in url
    )

    is_instagram = (
        "instagram.com" in url
        or "instagr.am" in url
        )

    if is_google_maps:
        print("🗺️ Google Maps link detected")

    print("✅ URL:", url)

    status = await message.channel.send("🔍 Analyzing webpage...")

    try:

        # Google Maps (temporary)


        
        if is_google_maps:
            place = extract_place_name(url)
            page = scrape_page(url)  
            print(place)

        elif is_instagram:
            page = await scrape_instagram(url)

        else:
            page = scrape_page(url)

        if "error" in page:
            await status.edit(
                content=f"❌ {page['error']}"
            )
            return

        # Analyze with Gemini
        response = analyze_page(page)

        response = response.strip()

        if response.startswith("```json"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        # Convert JSON string to Python dictionary
        data = json.loads(response)

        existing = already_exists(data)

        if existing:

            embed = discord.Embed(
                title="⚠️ Already Saved",
                description=(
                    f"**{existing['title']}** is already in your database."
                ),
                color=discord.Color.orange()
            )

            embed.add_field(
                name="📅 Added",
                value=existing.get("date_added", "Unknown"),
                inline=False
            )

            embed.add_field(
                name="🌐 Website",
                value=existing.get("website", "Unknown"),
                inline=False
            )

            await status.delete()

            await message.channel.send(embed=embed)

            return

        save_item(data)

        subcategory = data.get("subcategory", "").lower()
        category = data.get("category", "").lower()

        icon = SUBCATEGORY_ICONS.get(
            subcategory,
            CATEGORY_ICONS.get(category, "📌")
        )

        color = CATEGORY_COLORS.get(
            category,
            discord.Color.blurple()
        )

        # ==========================================
        # Beautiful Embed
        # ==========================================

        description = (
            f"📍 **{data.get('location', 'Unknown')} • {data.get('country', '')}**\n\n"
        )

        # Show Google rating if available
        if data.get("google_rating", 0):
            description += f"⭐ **Google Rating:** {data.get('google_rating')}/5"

            if data.get("google_reviews", 0):
                description += f" ({data.get('google_reviews')} reviews)"

            description += "\n"

        # Always show Family Score
        description += (
            f"❤️ **Family Score:** {data.get('family_score', 0)}/10\n\n"
        )

        description += data.get("summary", "")
        recipe_categories = [
            "breakfast",
            "lunch",
            "dinner",
            "dessert",
            "drink",
            "snack",
        ]

        if category in recipe_categories:

            embed = create_recipe_embed(data)

        else:
            embed = discord.Embed(
                title=f"{icon} {data.get('title', 'Unknown')}",
                description=description,
                color=color
            )
        # Must See
        if data.get("highlights"):

            highlights = []

            for item in data["highlights"][:5]:

                emoji = "✨"

                if "symbolica" in item.lower():
                    emoji = "🎠"

                elif "baron" in item.lower():
                    emoji = "🎢"

                elif "forest" in item.lower():
                    emoji = "🌳"

                elif "python" in item.lower():
                    emoji = "🐉"

                highlights.append(f"{emoji} {item}")

            embed.add_field(
                name="━━━━━━━━━━━━━━━━━━━━━━\n✨ Must See",
                value="\n".join(highlights),
                inline=False
            )

        # Best For
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━\n👨‍👩‍👧 Perfect For",
            value=data.get("best_for", "Unknown"),
            inline=False
        )

        # Tips
        if data.get("tips"):

            embed.add_field(
                name="━━━━━━━━━━━━━━━━━━━━━━\n💡 Insider Tips",
                value="\n".join(
                    f"• {tip}" for tip in data["tips"][:3]
                ),
                inline=False
            )

        # Website
        website = data.get("website", "Unknown")

        if len(website) > 100:
            website = website[:100] + "..."

        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━\n🌐 Website",
            value=website,
            inline=False
        )

        embed.set_footer(
            text=f"Confidence: {round(data.get('confidence', 0) * 100)}%"
        )
        # Determine destination channel
        category = data.get("category", "unknown").lower()

        print("Full JSON:")
        print(data)
        
        destination_id = CATEGORY_TO_CHANNEL.get(
            category,
            IDEAS_CHANNEL
        )

        print("Reached routing")
        print("Destination ID:", destination_id)
        destination_channel = bot.get_channel(destination_id)
        print("Destination Channel:", destination_channel)

        if destination_channel is None:

            await status.edit(
                content="❌ Destination channel not found."
            )
            return

        print("About to send embed...")

        await destination_channel.send(
        embed=embed,
        view=PlaceView(data)
        )

        print("Embed sent!")

        # Save confirmation
        await status.edit(
            content=f"✅ Saved **{data.get('title', 'Item')}** to {destination_channel.mention}"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        await status.edit(
            content=f"❌ Error\n```{e}```"
        )
# ==========================================
# Commands
# ==========================================

@bot.hybrid_command(name="ping")
async def ping(ctx):
    await ctx.send("🏓 Pong!")


@bot.hybrid_command(name="ask")
async def ask(ctx, *, question):

    await ctx.defer()

    try:

        response = ask_ai(question)

        if len(response) > 1900:
            response = response[:1900] + "..."

        await ctx.send(response)

    except Exception as e:

        await ctx.send(f"❌ {e}")

# ==========================================
# Run Bot
# ==========================================

bot.run(TOKEN)