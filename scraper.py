import requests
import json
import time
import random
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_problems():
    print("Fetching problem list...")
    try:
        r = requests.get("https://codeforces.com/api/problemset.problems", headers=HEADERS)
        all_problems = [p for p in r.json()['result']['problems'] if 'rating' in p and 1500 <= p['rating'] <= 1900]
        subset = random.sample(all_problems, 50) # Grab 50 random ones for the day
        final_db = []
        
        session = requests.Session()
        for p in subset:
            url = f"https://codeforces.com/problemset/problem/{p['contestId']}/{p['index']}"
            try:
                time.sleep(2)
                resp = session.get(url, headers=HEADERS)
                soup = BeautifulSoup(resp.text, 'html.parser')
                statement = soup.find('div', class_='problem-statement')
                desc = str(statement.find('div', class_='header').find_next_sibling('div')).replace('$$$', '$')
                input_spec = statement.find('div', class_='input-specification')
                final_db.append({
                    "title": p['name'], "desc": desc, "tags": p['tags'], "difficulty": str(p['rating']),
                    "constraints": str(input_spec).replace('$$$', '$') if input_spec else "Standard Constraints"
                })
                print(f"Success: {p['name']}")
            except: print(f"Failed: {p['name']}")

        with open('problems_db.json', 'w', encoding='utf-8') as f:
            json.dump(final_db, f, indent=4, ensure_ascii=False)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    get_problems()