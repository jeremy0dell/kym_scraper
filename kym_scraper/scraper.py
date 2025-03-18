import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any

def scrape_newest_memes(limit: int = 20, return_html_on_failure: bool = False) -> List[Dict[str, Any]]:
    """
    Scrapes the newest memes from Know Your Meme website.
    
    Args:
        limit: Maximum number of memes to return
        return_html_on_failure: If True and no memes are found, returns the raw HTML
        
    Returns:
        List of dictionaries containing meme information including title and URL
    """
    url = "https://knowyourmeme.com/memes?kind=submissions&sort=newest"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return [{"error": f"Failed to fetch data: Status code {response.status_code}"}]
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Based on our debug results, we know these selectors work
    results = []
    
    # Look for meme links - this works according to our debugging
    meme_links = soup.select("a[href*='/memes/']")
    
    for link in meme_links:
        href = link.get("href", "")
        
        # Exclude links that are not actual meme pages:
        # - Not pagination links (containing 'page/' or '?page=')
        # - Not category or submission links
        # - Only actual meme pages
        if (href.startswith("/memes/") and 
            not href.startswith("/memes/new") and
            not href.startswith("/memes/trending") and
            not href.startswith("/memes/confirmed") and
            not re.search(r'/page/\d+', href) and
            not re.search(r'\?page=\d+', href) and
            "/categories/" not in href):
            
            # Try to get title from different attributes
            title = (
                link.get("alt") or 
                link.get("title") or 
                link.get("data-author") or
                link.text.strip() or
                href.split("/")[-1].replace("-", " ").title() or
                "Unknown Meme"
            )
            
            # We found links with class "item" that seem to be meme entries
            if link.get("class") and "item" in link.get("class"):
                title = link.get("alt") or title
            
            full_url = f"https://knowyourmeme.com{href}" if href.startswith("/") else href
            
            # Only add if this URL isn't already in results
            # And make sure it's not just a number (pagination)
            if (not any(r["url"] == full_url for r in results) and 
                not title.isdigit()):
                results.append({
                    "title": title,
                    "url": full_url
                })
    
    # Limit the results
    results = results[:limit]
    
    # If no results were found and return_html_on_failure is True
    if len(results) == 0 and return_html_on_failure:
        return [{"error": "No memes found", "html": response.text}]
    
    return results


def get_meme_html(url: str) -> Dict[str, Any]:
    """
    Fetches the HTML content of a specific meme URL.
    
    Args:
        url: The URL of the meme page to scrape
        
    Returns:
        Dict with HTML content if successful, or error information
        {
            "html": str,           # The full HTML content of the page
            "status_code": int,    # HTTP status code
            "url": str,            # The URL that was fetched (in case of redirects)
            "error": str           # Error message (only present if there was an error)
        }
    """
    # Make sure the URL is valid and points to Know Your Meme
    if not url.startswith("http"):
        url = f"https://knowyourmeme.com{url}" if url.startswith("/") else f"https://knowyourmeme.com/{url}"
    
    # Use the same headers as the main scraper function
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        result = {
            "html": response.text,
            "status_code": response.status_code,
            "url": response.url
        }
        
        if response.status_code != 200:
            result["error"] = f"Failed to fetch URL: HTTP {response.status_code}"
        
        return result
        
    except requests.RequestException as e:
        return {
            "html": "",
            "status_code": 0,
            "url": url,
            "error": f"Request error: {str(e)}"
        } 