import asyncio
import csv
import os
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError

# ---------------- CONFIG ---------------- #

TARGET_URLS = [
    {
        "country": "European Union",
        "url": "https://digital-strategy.ec.europa.eu/en/policies/artificial-intelligence"
    },
    {
        "country": "United States",
        "url": "https://www.whitehouse.gov/ostp/ai/"
    }
]

OUTPUT_FILE = "output/ai_policies.csv"

# ---------------- UTILS ---------------- #

async def safe_wait(page, selector, timeout=10000):
    try:
        await page.wait_for_selector(selector, timeout=timeout)
        return True
    except TimeoutError:
        print(f"[WARN] Timeout waiting for selector: {selector}")
        return False


def classify_policy(text):
    text = text.lower()

    if "safety" in text or "risk" in text:
        return "AI Safety & Risk"
    if "regulation" in text or "law" in text or "act" in text:
        return "AI Regulation"
    if "governance" in text or "oversight" in text:
        return "AI Governance"
    if "innovation" in text or "research" in text:
        return "AI Innovation"
    if "ethics" in text or "bias" in text:
        return "AI Ethics"

    return "General AI Policy"


def export_to_csv(filename, rows):
    headers = [
        "country",
        "policy_title",
        "category",
        "publication_date",
        "summary",
        "source_url"
    ]

    # ✅ FIX: Ensure output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if not rows:
        print("[WARN] No data collected. CSV not created.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[INFO] CSV exported successfully → {filename}")

# ---------------- SCRAPING ---------------- #

async def extract_policies(page, country, source_url):
    policies = []

    articles = await page.query_selector_all(
        "article, .policy, .content-item, .views-row"
    )

    for article in articles:
        try:
            title_el = await article.query_selector("h1, h2, h3")
            summary_el = await article.query_selector("p")
            date_el = await article.query_selector("time")

            title = await title_el.inner_text() if title_el else "Untitled Policy"
            summary = await summary_el.inner_text() if summary_el else ""

            date = (
                await date_el.get_attribute("datetime")
                if date_el else datetime.utcnow().date().isoformat()
            )

            policies.append({
                "country": country,
                "policy_title": title.strip(),
                "category": classify_policy(title + " " + summary),
                "publication_date": date,
                "summary": summary[:300].strip(),
                "source_url": source_url
            })

        except Exception as e:
            print(f"[WARN] Failed to parse article: {e}")

    return policies

# ---------------- MAIN ---------------- #

async def main():
    all_policies = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            )
        )

        page = await context.new_page()

        for target in TARGET_URLS:
            print(f"[INFO] Scraping {target['country']} policies...")

            try:
                await page.goto(target["url"], timeout=30000)
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(2000)

                policies = await extract_policies(
                    page,
                    target["country"],
                    target["url"]
                )

                print(f"[INFO] Collected {len(policies)} policies")
                all_policies.extend(policies)

            except TimeoutError:
                print(f"[ERROR] Timeout loading {target['url']}")

        await browser.close()

    export_to_csv(OUTPUT_FILE, all_policies)

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    asyncio.run(main())
