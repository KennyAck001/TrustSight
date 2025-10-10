from typing import List, Dict
import datetime
from urllib.parse import urlparse
import re

# Global trust scores for sources
source_trust_scores = {}

def calculate_domain_authority(url: str) -> float:
    """
    Calculate domain authority based on known high-authority domains and TLD.
    """
    domain = urlparse(url).netloc.lower()
    high_authority = ['wikipedia.org', 'bbc.com', 'nytimes.com', 'reuters.com', 'apnews.com', 'theguardian.com', 'cnn.com', 'foxnews.com', 'wsj.com', 'forbes.com', 'bloomberg.com', 'economist.com']
    if any(d in domain for d in high_authority):
        return 0.9
    gov_edu = ['.gov', '.edu', '.ac.uk', '.edu.au']
    if any(d in domain for d in gov_edu):
        return 0.8
    org = ['.org']
    if any(d in domain for d in org):
        return 0.7
    else:
        return 0.5

def calculate_recency(url: str, content: str) -> float:
    """
    Calculate recency score by attempting to find dates in content.
    """
    date_patterns = [r'\b\d{4}-\d{2}-\d{2}\b', r'\b\d{2}/\d{2}/\d{4}\b', r'\b\d{2}-\d{2}-\d{4}\b', r'\b\d{4}/\d{2}/\d{2}\b']
    for pattern in date_patterns:
        if re.search(pattern, content):
            return 0.8  # Recent if date found
    return 0.6  # Default

def calculate_author_credibility(content: str) -> float:
    """
    Calculate author credibility based on presence of author information.
    """
    if 'author' in content.lower() or 'by ' in content.lower() or 'written by' in content.lower():
        return 0.7
    return 0.5

def calculate_structural_completeness(content: str) -> float:
    """
    Calculate structural completeness based on length, links, sentences, and structure.
    """
    length = len(content)
    score = 0.0
    if length > 2000:
        score += 0.4
    elif length > 1000:
        score += 0.3
    elif length > 500:
        score += 0.2
    if 'http' in content or 'www.' in content:
        score += 0.2
    sentences = len(content.split('.'))
    if sentences > 10:
        score += 0.2
    if 'table' in content.lower() or 'list' in content.lower() or 'figure' in content.lower():
        score += 0.2
    return min(score, 1.0)

def calculate_cross_reference(url: str, claims: List[Dict]) -> float:
    """
    Calculate cross-reference validation based on number of sources.
    """
    num_sources = len(set(c.get("source") for c in claims))
    if num_sources > 1:
        return 0.7
    return 0.5

def update_trust_score(claims: List[Dict]) -> List[Dict]:
    """
    Update trust scores for claims based on multilayer scoring.
    """
    for claim in claims:
        url = claim.get("url", "")
        content = claim.get("content", "")
        score = 0.0
        if url and content:
            score += calculate_domain_authority(url) * 0.3
            score += calculate_recency(url, content) * 0.2
            score += calculate_author_credibility(content) * 0.2
            score += calculate_structural_completeness(content) * 0.2
            score += calculate_cross_reference(url, claims) * 0.1
            # Check if source is approved
            if source_trust_scores.get(url, 0) > 0:
                score += 0.2
        claim["trust_score"] = min(score, 1.0)
    return claims

def approve_source(url: str):
    """
    Approve a source and boost its trust score.
    """
    source_trust_scores[url] = 1.0

def mark_source_unreliable(url: str):
    """
    Mark a source as unreliable and update trust scores.
    """
    source_trust_scores[url] = 0.1
