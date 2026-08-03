import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_openrouter(prompt: str, model: str = "meta-llama/llama-3-8b-instruct:free"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "Company Research Assistant"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert corporate research assistant. You must output valid JSON only, with no markdown formatting or extra text."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        
        # Clean markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:].strip()
            content = content.split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        return {
            "company_name": "Error Parsing Data",
            "website": "",
            "phone": "N/A",
            "address": "N/A",
            "summary": f"Could not parse AI response: {str(e)}",
            "products_services": ["N/A"],
            "pain_points": ["N/A"],
            "competitors": []
        }

def analyze_company_data(company_query: str, scraped_text: str, search_results: dict, model: str):
    prompt = f"""
    Analyze the company or website '{company_query}' based on the provided website crawl content and search results.
    Return ONLY a valid JSON object with the following exact keys:
    - "company_name": string (official company name)
    - "website": string
    - "phone": string (or "N/A")
    - "address": string (or "N/A")
    - "summary": string (short professional summary)
    - "products_services": list of strings
    - "pain_points": list of strings
    - "competitors": list of objects, each with keys "name" and "website"

    Search Results:
    {json.dumps(search_results)}

    Crawled Website Content:
    {scraped_text[:8000]}
    """
    return call_openrouter(prompt, model)