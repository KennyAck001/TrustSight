from typing import List, Dict, Union
import pandas as pd

def summarize_points(claims: List[Dict]) -> Dict[int, Dict]:
    """
    Summarize claims as a dictionary of point objects with scores.
    """
    points = {}
    for i, c in enumerate(claims):
        points[i] = {
            "text": c['claim'],
            "trust_score": c.get('trust_score', 0),
            "confidence": c.get('confidence', 0)
        }
    return points

def summarize_table(claims: List[Dict]) -> pd.DataFrame:
    """
    Summarize claims as a pandas DataFrame.
    """
    data = []
    for c in claims:
        data.append({
            "Claim": c["claim"],
            "Source": c.get("source", ""),
            "Trust Score": c.get("trust_score", 0),
            "Confidence": c.get("confidence", 0)
        })
    df = pd.DataFrame(data)
    return df

def summarize_graph(claims: List[Dict]) -> str:
    """
    Summarize claims for graph generation (textual explanation).
    """
    avg_trust = sum(c.get('trust_score', 0) for c in claims) / len(claims) if claims else 0
    avg_conf = sum(c.get('confidence', 0) for c in claims) / len(claims) if claims else 0
    return f"Graph summary: Claims clustered by confidence scores. Average Trust Score: {avg_trust:.2f}, Average Confidence: {avg_conf:.2f}."

def summarize_results(claims: List[Dict], query_type: str) -> Union[str, pd.DataFrame, Dict[int, Dict]]:
    """
    Summarize verified information according to query type.
    """
    if query_type == "points":
        return summarize_points(claims)
    elif query_type == "table":
        return summarize_table(claims)
    elif query_type == "graph":
        return summarize_graph(claims)
    else:
        return summarize_points(claims)
