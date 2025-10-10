from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def cluster_claims(claims: List[Dict]) -> List[List[Dict]]:
    """
    Cluster similar claims using TF-IDF and K-Means.
    """
    if not claims:
        return []
    texts = [claim["claim"] for claim in claims]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)
    num_clusters = min(len(claims), 5)  # Adjust as needed
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    clustered_claims = [[] for _ in range(num_clusters)]
    for i, claim in enumerate(claims):
        clustered_claims[clusters[i]].append(claim)
    return clustered_claims

def detect_contradictions(cluster: List[Dict]) -> List[Dict]:
    """
    Detect contradictions within a cluster (placeholder logic).
    """
    # Placeholder: assume no contradictions for simplicity
    for claim in cluster:
        claim["contradiction"] = False
    return cluster

def assign_confidence_scores(clustered_claims: List[List[Dict]]) -> List[Dict]:
    """
    Assign confidence scores based on cluster agreement.
    """
    all_claims = []
    for cluster in clustered_claims:
        cluster_size = len(cluster)
        avg_trust = np.mean([c.get("trust_score", 0.5) for c in cluster])
        for claim in cluster:
            claim["confidence"] = avg_trust * (cluster_size / len(clustered_claims)) if clustered_claims else 0.5
            all_claims.append(claim)
    return all_claims

def cross_validate_claims(claims: List[Dict]) -> List[Dict]:
    """
    Run cross-validation engine: cluster, detect contradictions, assign confidence.
    """
    clustered = cluster_claims(claims)
    for cluster in clustered:
        detect_contradictions(cluster)
    validated = assign_confidence_scores(clustered)
    return validated
