from datetime import datetime

def create_ics(data):

    title = data.get("title", "")

    description = data.get("summary", "")

    location = (
        data.get("address")
        or data.get("location")
        or ""
    )

    start_date = data.get("start_date")
    end_date = data.get("end_date")

    start_time = data.get("start_time") or "09:00"
    end_time = data.get("end_time") or "17:00"

    start = datetime.strptime(
        f"{start_date} {start_time}",
        "%Y-%m-%d %H:%M"
    )

    end = datetime.strptime(
        f"{end_date} {end_time}",
        "%Y-%m-%d %H:%M"
    )

    return f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{title}
DTSTART:{start.strftime("%Y%m%dT%H%M%S")}
DTEND:{end.strftime("%Y%m%dT%H%M%S")}
LOCATION:{location}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR
"""