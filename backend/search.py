import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_web(query: str, num_results: int = 5):
    url = "https://google.serper.dev/search"
    payload = {"q": query, "num": num_results}
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def find_official_website(company_name: str) -> str:
    results = search_web(f"{company_name} official website")
    if "organic" in results and len(results["organic"]) > 0:
        return results["organic"][0].get("link", "")
    return ""