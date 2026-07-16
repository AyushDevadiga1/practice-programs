import requests
import time

# TO THIS EXACT SYSTEM API MACHINE PATHWAY:
URL = "https://en.wikipedia.org/w/api.php"

# 2. Use a direct, identifiable string to satisfy security protocols
headers = {
    "User-Agent": "HistoryResearchBot/2.5 (yourname@gmail.com; data_extract_project)"
}

# 3. Define configuration parameters - "titles" tells the API what to find
PARAMS = {
    "action": "query",
    "prop": "extracts",
    "explaintext": True,   # Automatically cleans out raw HTML markup junk
    "titles": "History of bitcoin",
    "format": "json"
}

print(f"Connecting to database endpoint: {URL}")

# Multi-attempt safety framework to prevent network rate blocks
for attempt in range(3):
    response = requests.get(url=URL, params=PARAMS, headers=headers)
    
    if response.status_code == 429:
        wait_seconds = int(response.headers.get("Retry-After", 5))
        print(f"Rate limit triggered. Pausing for {wait_seconds} seconds...")
        time.sleep(wait_seconds)
        continue
        
    elif response.status_code == 200:
        try:
            data = response.json()
            pages = data["query"]["pages"]

            with open("wiki_api_output.txt", "w", encoding="utf-8") as file:
                for page_id, page_info in pages.items():
                    if "missing" in page_info:
                        print(f"Error: The page '{PARAMS['titles']}' does not exist.")
                    else:
                        file.write(f"Title: {page_info['title']}\n")
                        file.write("="*20 + "\n")
                        file.write(page_info["extract"])
                        print("Success! Full article content saved to wiki_api_output.txt")
            break
            
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON. Verify your URL layout string matches.")
            break
    else:
        print(f"Server connections dropped. Status: {response.status_code}")
        break
