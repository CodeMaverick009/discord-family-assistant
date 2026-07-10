import requests
from bs4 import BeautifulSoup


def scrape_page(url):

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15,
            allow_redirects=True,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # -----------------------------
        # Title
        # -----------------------------

        title = ""

        if soup.title:
            title = soup.title.get_text(strip=True)

        # -----------------------------
        # Meta Description
        # -----------------------------

        description = ""

        meta = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta:
            description = meta.get("content", "")

        # -----------------------------
        # Open Graph Title
        # -----------------------------

        og_title = ""

        og = soup.find(
            "meta",
            property="og:title"
        )

        if og:
            og_title = og.get("content", "")

        # -----------------------------
        # Open Graph Description
        # -----------------------------

        og_description = ""

        og = soup.find(
            "meta",
            property="og:description"
        )

        if og:
            og_description = og.get("content", "")

        # -----------------------------
        # Open Graph Image
        # -----------------------------

        og_image = ""

        og = soup.find(
            "meta",
            property="og:image"
        )

        if og:
            og_image = og.get("content", "")

        # -----------------------------
        # Visible Page Text
        # -----------------------------

        text = soup.get_text(" ", strip=True)

        # Prevent huge prompts
        text = text[:6000]

        # -----------------------------
        # Return
        # -----------------------------

        return {

            "title": title,

            "description": description,

            "og_title": og_title,

            "og_description": og_description,

            "og_image": og_image,

            "text": text,

            "url": response.url

        }

    except Exception as e:

        return {
            "error": str(e)
        }