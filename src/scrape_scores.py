from playwright.sync_api import sync_playwright
import csv
import re
import random

def main():
    url = "https://www.kaggle.com/competitions/santa-2025/code?sortBy=scoreAscending"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        for _ in range(50):
            page.keyboard.press('End')
            page.wait_for_timeout(random.randint(300, 800))

        html = page.content()
        browser.close()

    with open('debug.html', 'w') as f:
        f.write(html)

    scores = {}

    pattern = r'href="/code/([^"]+)"[^>]*>.*?Score:\s*(\d+\.\d+)'
    for match in re.finditer(pattern, html, re.DOTALL):
        ref = match.group(1)
        score = match.group(2)
        if ref not in scores and not ref.endswith('/comments'):
            scores[ref] = score

    pattern2 = r'aria-label="([^"]+) List Item".*?href="/([a-zA-Z0-9_-]+)"[^>]*target="_blank".*?Score:\s*(\d+\.\d+)'
    for match in re.finditer(pattern2, html, re.DOTALL):
        title = match.group(1)
        author = match.group(2)
        score = match.group(3)
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        ref = f"{author}/{slug}"
        if ref not in scores:
            scores[ref] = score

    print(f"Found {len(scores)} scores")

    with open('notebook_scores.csv', 'w') as f:
        f.write("ref,top_score\n")
        for ref, score in scores.items():
            f.write(f"{ref},{score}\n")

    print("Saved to notebook_scores.csv")

main()
