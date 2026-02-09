from playwright.sync_api import sync_playwright
import re
import random
import csv

def main():
    teams = []
    with open('/Users/v0/santa2025_research/leaderboard.csv') as f:
        next(f)
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                teams.append((parts[0], parts[1]))

    print(f'Scraping top 300 teams...')
    mapping = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            for i, (rank, team) in enumerate(teams[:300]):
                url = f'https://www.kaggle.com/competitions/santa-2025/leaderboard?search={team.replace(" ", "+").replace("&", "%26")}'
                page.goto(url)
                page.wait_for_timeout(random.randint(4000, 6000))
                html = page.content()

                usernames = re.findall(r'href="/([a-z][a-z0-9_-]{2,30})"', html)
                skip = {'competitions','code','datasets','models','learn','discussions','benchmarks','cookies','game-arena','about','terms','privacy','support','blog','host'}
                usernames = [u for u in usernames if u not in skip and not u.startswith('static')]
                usernames = list(set(usernames))

                if usernames:
                    mapping[team] = (rank, usernames)

                print(f'{i+1}/300: {team} -> {len(usernames)} users')
        finally:
            browser.close()
            save(mapping)

def save(mapping):
    with open('/Users/v0/santa2025_research/team_usernames.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['rank', 'team', 'usernames'])
        for team, (rank, users) in mapping.items():
            writer.writerow([rank, team, ';'.join(users)])
    print(f'Saved {len(mapping)} teams to team_usernames.csv')

main()
