import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime


class AsyncBingSearchExtractor:
    def __init__(self, headless: bool = False):
        self.headless = headless

    async def run_search_and_extract(self, search_text: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # 1. Open Bing
                await page.goto("https://www.bing.com", wait_until="domcontentloaded")

                # 2. Search
                search_box = page.locator('xpath=//*[@id="sb_form_q"]')
                await search_box.wait_for()
                await search_box.fill(search_text)
                await search_box.press("Enter")

                # 3. Wait for navigation + network idle
                await page.wait_for_load_state("networkidle")

                # 4. Wait directly for first result (more reliable)
                first_result = page.locator("li.b_algo h2 a").first
                await first_result.wait_for(timeout=20000)

                # 5. Click first result
                await first_result.click()

                # 6. Wait for target page load
                await page.wait_for_load_state("networkidle")

                # 7. Extract data
                page_title = await page.title()
                meta_description = await page.locator(
                    "meta[name='description']"
                ).get_attribute("content")

                body_text = await page.evaluate(
                    "() => document.body.innerText"
                )

                # 8. Save to TXT
                filename = f"extracted_{datetime.now():%Y%m%d_%H%M%S}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"SEARCH QUERY:\n{search_text}\n\n")
                    f.write(f"PAGE TITLE:\n{page_title}\n\n")
                    f.write(f"META DESCRIPTION:\n{meta_description}\n\n")
                    f.write("PAGE CONTENT:\n")
                    f.write(body_text)

                print(f"Extraction completed: {filename}")

            except PlaywrightTimeoutError as e:
                print("Timeout occurred. Capturing screenshot...")
                await page.screenshot(path="timeout_error.png")
                raise e

            finally:
                await context.close()
                await browser.close()


async def main():
    extractor = AsyncBingSearchExtractor(headless=False)
    await extractor.run_search_and_extract(
        "football match today top rated player"
    )


if __name__ == "__main__":
    asyncio.run(main())
