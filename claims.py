import os
import google.generativeai as genai
from typing import List, Dict

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCOlB0QQX-FiF9HCTxTeIH2pn0MY3pzy7M")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

async def extract_claims(contents: List[str], search_results: List[Dict], query: str) -> List[Dict]:
    """
    Extract claims/facts from cleaned content using Google Gemini.
    Returns a list of dicts with 'claim', 'source' (index), 'url', 'content'.
    """
    claims = []
    for i, content in enumerate(contents):
        if not content.strip():
            continue
        url = search_results[i].get("link", "")
        prompt = f"Extract only the key claims, facts, and detailed information that directly answer the query '{query}' from the following text. Do not include any information that is not directly related to the query. Ensure each bullet point is directly relevant and provides information specifically requested by the query. If no relevant information is found, return an empty list. List them as comprehensive bullet points:\n\n{content}"
        try:
            response = model.generate_content(prompt)
            extracted_text = response.text.strip()
            # Parse bullet points
            bullet_points = [line.strip('- ').strip() for line in extracted_text.split('\n') if line.strip()]
            # Limit to top 5 claims per source to focus on most relevant
            for claim in bullet_points[:5]:
                if claim:
                    claims.append({"claim": claim, "source": i, "url": url, "content": content})
        except Exception as e:
            print(f"Error extracting claims from content {i}: {e}")
            # Fallback: Extract basic claims from content using simple text processing
            if content.strip():
                # Simple fallback: split content into sentences and take first few as claims
                sentences = [s.strip() for s in content.split('.') if s.strip()]
                fallback_claims = sentences[:5]  # Take up to 5 sentences as claims
                for claim in fallback_claims:
                    if claim:  # Include all non-empty claims
                        claims.append({"claim": claim, "source": i, "url": url, "content": content})
    return claims
