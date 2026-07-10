import re
from urllib.parse import unquote


def extract_place_name(url: str):
    """
    Extract the place name from a Google Maps URL.
    """

    match = re.search(r"/place/([^/@]+)", url)

    if not match:
        return None

    name = match.group(1)
    name = unquote(name)
    name = name.replace("+", " ")

    return name


def scrape_google_maps(url):
    """
    Placeholder for future Google Maps support.
    """
    return {
        "url": url
    }