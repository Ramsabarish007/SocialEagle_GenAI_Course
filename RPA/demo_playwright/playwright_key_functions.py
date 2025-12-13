from playwright.async_api import async_playwright
import asyncio

async def playwright_function():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # Navigation
        await page.goto("https://google.com")
        await page.wait_for_timeout(1000)
        print(await page.title())
        await browser.close()
        
        # CSS,XPATH Selectors

if __name__ == "__main__":
    asyncio.run(playwright_function())