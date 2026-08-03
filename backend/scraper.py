import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def crawl_website(base_url: str, max_pages: int = 5):
    visited = set()
    to_visit = [base_url]
    scraped_content = []
    
    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc

    ignored_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.css', '.js', '.zip']
    ignored_keywords = ['login', 'signin', 'signup', 'cart', 'checkout', 'account', 'register']

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        
        visited.add(url)
        
        try:
            response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
                
            text = soup.get_text(separator=' ', strip=True)
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            scraped_content.append(f"Source URL: {url}\nContent: {text[:3000]}")
            
            # Find links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                parsed_link = urlparse(full_url)
                
                # Check domain
                if parsed_link.netloc != base_domain:
                    continue
                
                # Check ignored extensions/keywords
                if any(full_url.lower().endswith(ext) for ext in ignored_extensions):
                    continue
                if any(kw in full_url.lower() for kw in ignored_keywords):
                    continue
                
                if full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)
                    
        except Exception:
            continue
            
    return "\n\n".join(scraped_content)