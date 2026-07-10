from playwright.async_api import async_playwright


async def scrape_instagram(url):

    try:

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            page = await browser.new_page()

            await page.goto(url)

            await page.wait_for_timeout(5000)

            text = await page.locator("body").inner_text()

            await browser.close()

            return {

                "title": "Instagram Reel",

                "description": "",

                "text": text[:6000],

                "url": url

            }

    except Exception as e:

        return {

            "error": str(e)

        }