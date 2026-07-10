from playwright.async_api import async_playwright
import asyncio

URL = "https://www.instagram.com/reel/DYm6WTAAnFO/"

async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)

        page = await browser.new_page()

        await page.goto(URL)

        await page.wait_for_timeout(5000)

        print(await page.locator("article").count())
        print(await page.locator("main").count())
        print(await page.locator("section").count())

        input()

        await browser.close()

asyncio.run(main())