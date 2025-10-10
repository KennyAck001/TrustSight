import os
import json
from typing import List, Dict, Union
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCOlB0QQX-FiF9HCTxTeIH2pn0MY3pzy7M")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

async def generate_points(query: str, contents: List[str]) -> Dict[int, Dict]:
    content_text = "\n\n".join(contents)
    prompt = f"Based on the following web content, generate 15-20 detailed bullet points that directly answer the query '{query}', including related insights, additional context, supporting details, and any relevant related fields or points for comprehensive business analyst research. Ensure the information is in-depth and useful. Format as bullet points, each starting with '-'.\n\nContent:\n{content_text}"
    try:
        response = model.generate_content(prompt)
        print(f"DEBUG: Full LLM response object for points:\n{response}\n")  # Full response debug
        text = response.text.strip()
        print(f"DEBUG: Raw LLM output for points:\n{text}\n")  # Debug log
        lines = [line.lstrip('- ').strip() for line in text.split('\n') if line.strip() and len(line) > 5 and not line.lower().startswith(('here', 'the', 'based', 'content', 'points', 'bullet'))]
        print(f"DEBUG: Extracted lines for points:\n{lines}\n")  # Lines debug
        points = {}
        if lines:
            for i, line in enumerate(lines[:20]):  # Limit to 20
                points[i] = {
                    "text": line,
                    "trust_score": 1.0,  # Default high score
                    "confidence": 1.0
                }
        else:
            # Fallback if no relevant lines
            points[0] = {
                "text": "No relevant information found in the fetched content for the query.",
                "trust_score": 0.0,
                "confidence": 0.0
            }
        return points
    except Exception as e:
        print(f"Error generating points: {e}")
        return {}

async def generate_table(query: str, contents: List[str]) -> List[Dict]:
    content_text = "\n\n".join(contents)
    prompt = f"Based on the following web content, generate a comprehensive JSON array of objects representing a detailed table that answers the query '{query}'. Each object should have multiple keys for columns such as 'Item', 'Description', 'Category', 'Details', 'Impact', 'Source', and any other relevant fields to provide in-depth information for business analyst research. Include as many rows as possible with relevant data. Output only valid JSON.\n\nContent:\n{content_text}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Extract JSON
        start = text.find('[')
        end = text.rfind(']') + 1
        json_str = text[start:end]
        table = json.loads(json_str)
        return table if isinstance(table, list) else []
    except Exception as e:
        print(f"Error generating table: {e}")
        return []

async def generate_graph_data(query: str, contents: List[str]) -> Dict:
    content_text = "\n\n".join(contents)
    prompt = f"Based on the following web content, generate comprehensive JSON data for a detailed chart that visualizes the answer to the query '{query}'. Include 'type' (bar, line, pie), 'labels' (a list of at least 10 strings for detailed categories), 'values' (a corresponding list of numbers), 'title', and optionally 'additional_data' for more insights. Ensure the data is rich and suitable for business analyst research. Output only valid JSON. If you cannot generate valid JSON, output an empty JSON object {{}}.\n\nContent:\n{content_text}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Extract JSON
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        data = json.loads(json_str)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"Error generating graph data: {e}")
        return {}

async def generate_related_insights(query: str, contents: List[str]) -> Dict[int, Dict]:
    content_text = "\n\n".join(contents)
    prompt = f"Based on the following web content, generate 10-15 bullet points on related insights, additional context, related topics, or interesting fields that complement the query '{query}' for deeper business analyst research. Include broader implications, trends, or connected areas. Format as bullet points, each starting with '-'.\n\nContent:\n{content_text}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        lines = [line.lstrip('- ').strip() for line in text.split('\n') if line.strip() and len(line) > 5 and not line.lower().startswith(('here', 'the', 'based', 'content', 'points', 'bullet'))]
        insights = {}
        if lines:
            for i, line in enumerate(lines[:15]):  # Limit to 15
                insights[i] = {
                    "text": line,
                    "trust_score": 1.0,
                    "confidence": 1.0
                }
        else:
            insights[0] = {
                "text": "No related insights found.",
                "trust_score": 0.0,
                "confidence": 0.0
            }
        return insights
    except Exception as e:
        print(f"Error generating related insights: {e}")
        return {}

async def generate_follow_up_suggestions(query: str, contents: List[str]) -> List[str]:
    content_text = "\n\n".join(contents)
    prompt = f"Based on the query '{query}' and the following content, generate 2-3 follow-up questions or suggestions that a business analyst might find useful for deeper research. These should be related topics, additional details, or expansions on the original query. Format as a JSON array of strings.\n\nContent:\n{content_text}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Extract JSON
        start = text.find('[')
        end = text.rfind(']') + 1
        json_str = text[start:end]
        suggestions = json.loads(json_str)
        return suggestions if isinstance(suggestions, list) else []
    except Exception as e:
        print(f"Error generating follow-up suggestions: {e}")
        return []

async def generate_response(query: str, contents: List[str], query_types: List[str]) -> Dict:
    response = {}
    if "points" in query_types or not query_types:
        response["points"] = await generate_points(query, contents)
    if "table" in query_types:
        response["table"] = await generate_table(query, contents)
    if "graph" in query_types:
        graph_data = await generate_graph_data(query, contents)
        # Then generate graph image
        from graph_generator import generate_graph
        # Use existing generate_graph function with claims-like data
        # Here we simulate claims from graph_data for visualization
        claims = []
        if "labels" in graph_data and "values" in graph_data:
            for label, value in zip(graph_data["labels"], graph_data["values"]):
                claims.append({"claim": label, "confidence": value})
        graph_img_b64, graph_text = generate_graph(claims)
        response["graph"] = {
            "image_base64": graph_img_b64,
            "explanation": graph_text
        }
    # Always include related insights for more detailed research
    response["related_insights"] = await generate_related_insights(query, contents)
    # Generate follow-up suggestions for better interaction
    response["follow_up_suggestions"] = await generate_follow_up_suggestions(query, contents)
    return response
