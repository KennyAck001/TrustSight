import os
import aiohttp
from typing import List, Dict

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "d9f7e092b0a3239c686d07270524424638f1d209")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCOlB0QQX-FiF9HCTxTeIH2pn0MY3pzy7M")

async def serper_search(query: str) -> List[Dict]:
    """
    Perform a web search using Serper API.
    Returns a list of search result dicts with 'title' and 'link'.
    """
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query, "num": 10}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                results = []
                for item in data.get("organic", []):
                    results.append({
                        "title": item.get("title"),
                        "link": item.get("link")
                    })
                return results
            else:
                return []

async def google_gemini_search(query: str) -> List[Dict]:
    """
    Perform a web search using Google Gemini API.
    Returns a list of search result dicts with 'title' and 'link'.
    """
    # Placeholder for Google Gemini API call
    # This requires Google API client setup and credentials
    # For now, return empty list
    return []

async def async_search(query: str) -> List[Dict]:
    """
    Perform web search using Serper API first, fallback to Google Gemini API.
    """
    results = await serper_search(query)
    if not results:
        results = await google_gemini_search(query)
    return results
