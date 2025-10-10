import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict

async def fetch_content(url: str) -> str:
    """
    Fetch content from a URL asynchronously.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    return html
                else:
                    return ""
    except Exception as e:
        return ""

def clean_html(html: str) -> str:
    """
    Clean HTML content to extract plain text.
    """
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    # Get text
    text = soup.get_text()
    # Break into lines and remove leading/trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

async def async_fetch_and_clean(search_results: List[Dict]) -> List[str]:
    """
    Fetch and clean content from search results asynchronously.
    """
    contents = []
    for result in search_results:
        url = result.get("link")
        if url:
            html = await fetch_content(url)
            clean_text = clean_html(html)
            contents.append(clean_text)
    return contents
