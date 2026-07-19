import discord
from urllib.parse import quote
from urllib.parse import quote
from datetime import datetime
from apple_calendar import create_ics

class PlaceView(discord.ui.View):

    def __init__(self, data):
        super().__init__(timeout=None)

        self.data = data

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

            details = ""

            start_date = data.get("start_date", "")
            end_date = data.get("end_date", "")
            start_time = data.get("start_time", "")
            end_time = data.get("end_time", "")

            if start_date:

                try:

                    if start_time:
                        start = datetime.strptime(
                            f"{start_date} {start_time}",
                            "%Y-%m-%d %H:%M"
                        )
                    else:
                        start = datetime.strptime(
                            start_date,
                            "%Y-%m-%d"
                        )

                    if end_time:
                        end = datetime.strptime(
                            f"{end_date} {end_time}",
                            "%Y-%m-%d %H:%M"
                        )
                    else:
                        end = start

                    # Create dates HERE
                    dates = (
                        start.strftime("%Y%m%dT%H%M%S")
                        + "/"
                        + end.strftime("%Y%m%dT%H%M%S")
                    )

                    calendar_url = (
                        "https://calendar.google.com/calendar/render"
                        "?action=TEMPLATE"
                        f"&text={title}"
                        f"&dates={dates}"
                        f"&location={location}"
                    )

                    self.add_item(
                        discord.ui.Button(
                            label="Add to Calendar",
                            emoji="📅",
                            url=calendar_url
                        )
                    )

                except Exception as e:
                    print("Calendar Error:", e)