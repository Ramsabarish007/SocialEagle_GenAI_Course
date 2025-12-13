import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


class AsyncBingSearchAutomation:
    def __init__(self, headless: bool = False):
        self.headless = headless

    async def run_search(self, search_text: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # Step 1: Open Bing
                await page.goto("https://www.bing.com", timeout=60000)

                # Step 2: Locate search input (CSS selector)
                search_box = page.locator('xpath=//*[@id="sb_form_q"]')
                await search_box.wait_for(timeout=10000)

                # Step 3: Type query dynamically
                await search_box.fill(search_text)
                await search_box.press("Enter")

                # Step 4: Wait for search results container
                await page.wait_for_selector("#b_content", timeout=10000)

                # Step 5: Locate first organic search result
                first_result = page.locator(
                    "li.b_algo h2 a"
                ).first

                # Step 6: Click the first result
                await first_result.click()

                # Step 7: Wait for page load completion
                await page.wait_for_load_state("networkidle")

                print("Bing search completed and first link opened successfully.")

            except PlaywrightTimeoutError as e:
                print("Timeout error during Bing automation:", e)

            finally:
                await context.close()
                await browser.close()


async def main():
    automation = AsyncBingSearchAutomation(headless=False)

    await automation.run_search(
        search_text="football match today top rated player"
    )


if __name__ == "__main__":
    asyncio.run(main())
