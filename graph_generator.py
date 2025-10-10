import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict, Tuple

def generate_graph(claims: List[Dict]) -> Tuple[str, str]:
    """
    Generate a real graph using matplotlib, save as base64 image, and provide textual explanation.
    """
    # Example: Bar chart of confidence scores
    claims_text = [c["claim"] for c in claims]  # Full claims for labels
    confidences = [c.get("confidence", 0) for c in claims]

    plt.figure(figsize=(10, 6))
    plt.barh(claims_text, confidences, color='skyblue')
    plt.xlabel('Confidence Score')
    plt.title('Claim Confidence Scores')
    plt.tight_layout()

    # Save to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    # Textual explanation
    explanation = "This bar chart shows the confidence scores of extracted claims. Higher bars indicate more reliable claims based on trust scoring and cross-validation."

    return img_base64, explanation
