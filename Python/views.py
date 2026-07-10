import discord
from urllib.parse import quote
from urllib.parse import quote
from datetime import datetime

class PlaceView(discord.ui.View):

    def __init__(self, data):
        super().__init__(timeout=None)

        # -------------------------
        # Google Maps
        # -------------------------

        location = (
            data.get("address")
            or data.get("location")
            or ""
        )

        if location:

            maps_url = (
                "https://www.google.com/maps/search/?api=1&query="
                + quote(location)
            )

            self.add_item(
                discord.ui.Button(
                    label="Open Maps",
                    emoji="📍",
                    url=maps_url
                )
            )

        # -------------------------
        # Website
        # -------------------------

        website = data.get("website")

        if website:

            website = website.strip()

            if not website.startswith(("http://", "https://")):
                website = "https://" + website

            self.add_item(
                discord.ui.Button(
                    label="Website",
                    emoji="🌐",
                    url=website
                )
            )

# -------------------------
# Google Calendar
# -------------------------

        if data.get("category") == "event":

            title = quote(data.get("title", ""))

            location = quote(
                data.get("address")
                or data.get("location")
                or ""
            )

            details = quote(data.get("summary", ""))

            date = data.get("event_date", "")

            if date:

                try:

                    start = datetime.strptime(date, "%Y-%m-%d")

                    # Default duration: 2 hours
                    end = start.replace(hour=18)

                    dates = (
                        start.strftime("%Y%m%d")
                        + "/"
                        + end.strftime("%Y%m%d")
                    )

                    calendar_url = (
                        "https://calendar.google.com/calendar/render"
                        "?action=TEMPLATE"
                        f"&text={title}"
                        f"&dates={dates}"
                        f"&location={location}"
                        f"&details={details}"
                    )

                    self.add_item(
                        discord.ui.Button(
                            label="Add to Calendar",
                            emoji="📅",
                            url=calendar_url
                        )
                    )

                except Exception:
                    pass