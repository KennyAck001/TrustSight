import os
import json
import asyncio
from typing import List, Dict, Union
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

async def summarize_content(contents: List[str]) -> str:
    if len(contents) == 0:
        return ""
    # Summarize if total content is too long (e.g., > 10000 chars)
    total_length = sum(len(c) for c in contents)
    if total_length > 10000:
        combined = "\n\n".join(contents)
        prompt = f"Summarize the following web content into a concise version (max 5000 characters) while preserving key facts, data, and insights relevant for research queries. Keep it informative.\n\nContent:\n{combined[:15000]}"  # Limit input to avoid token limits
        try:
            response = model.generate_content(prompt)
            return response.text.strip()[:5000]  # Cap summary length
        except Exception as e:
            print(f"Error summarizing content: {e}")
            return combined[:5000]  # Fallback to truncated original
    else:
        return "\n\n".join(contents)

async def generate_points(query: str, contents: List[str]) -> Dict[int, Dict]:
    content_text = await summarize_content(contents)
    prompt = f"Based on the following summarized web content, generate 10-15 detailed bullet points that directly answer the query '{query}', including related insights, additional context, supporting details, and any relevant related fields or points for comprehensive business analyst research. Ensure the information is in-depth and useful. Format as bullet points, each starting with '-'.\n\nContent:\n{content_text}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        lines = [line.lstrip('- ').strip() for line in text.split('\n') if line.strip() and len(line) > 5 and not line.lower().startswith(('here', 'the', 'based', 'content', 'points', 'bullet'))]
        points = {}
        if lines:
            for i, line in enumerate(lines[:15]):  # Limit to 15
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
    content_text = await summarize_content(contents)
    prompt = f"Based on the following summarized web content, generate a JSON array of objects representing a table that answers the query '{query}'. Each object should have keys like 'Item', 'Description', 'Details'. Include up to 10 rows. Output only valid JSON.\n\nContent:\n{content_text}"
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

async def classify_intent(query: str) -> str:
    prompt = f"Classify the following user query as either 'research' or 'conversation'. 'Research' means the query requires searching the web, analyzing data, or providing in-depth information on a topic. 'Conversation' means casual chat, greetings, small talk, or simple questions that don't require external research. Respond with only one word: 'research' or 'conversation'.\n\nQuery: {query}"
    try:
        response = model.generate_content(prompt)
        intent = response.text.strip().lower()
        if intent in ['research', 'conversation']:
            return intent
        else:
            return 'research'  # Default to research if unclear
    except Exception as e:
        print(f"Error classifying intent: {e}")
        return 'research'  # Default to research on error

async def generate_conversation(query: str) -> Dict:
    prompt = f"Respond to the following user query in a friendly, conversational manner. Keep the response engaging, helpful, and casual. Do not provide research or in-depth analysis. If it's a greeting, respond warmly. If it's a question, answer briefly and naturally.\n\nQuery: {query}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        return {
            "type": "conversation",
            "response": text
        }
    except Exception as e:
        print(f"Error generating conversation: {e}")
        return {
            "type": "conversation",
            "response": "I'm sorry, I couldn't process that right now. Let's try again!"
        }

async def generate_response(query: str, contents: List[str], query_types: List[str]) -> Dict:
    tasks = []
    task_keys = []
    if "points" in query_types or not query_types:
        tasks.append(generate_points(query, contents))
        task_keys.append("points")
    if "table" in query_types:
        tasks.append(generate_table(query, contents))
        task_keys.append("table")
    if "graph" in query_types:
        tasks.append(generate_graph_data(query, contents))
        task_keys.append("graph_data")
    # Always include insights and suggestions, but limit to essentials
    tasks.append(generate_related_insights(query, contents))
    task_keys.append("related_insights")
    tasks.append(generate_follow_up_suggestions(query, contents))
    task_keys.append("follow_up_suggestions")

    if not tasks:
        return {}

    gathered = await asyncio.gather(*tasks, return_exceptions=True)
    results = {}
    for key, result in zip(task_keys, gathered):
        if isinstance(result, Exception):
            print(f"Error in {key}: {result}")
            results[key] = {} if key in ["points", "related_insights"] else [] if key in ["table", "follow_up_suggestions"] else {}
        else:
            results[key] = result

    response = {}
    if "points" in task_keys:
        response["points"] = results["points"]
    if "table" in task_keys:
        response["table"] = results["table"]
    if "graph_data" in task_keys:
        graph_data = results["graph_data"]
        from graph_generator import generate_graph
        claims = []
        if "labels" in graph_data and "values" in graph_data:
            for label, value in zip(graph_data["labels"], graph_data["values"]):
                claims.append({"claim": label, "confidence": value})
        graph_img_b64, graph_text = generate_graph(claims)
        response["graph"] = {
            "image_base64": graph_img_b64,
            "explanation": graph_text
        }
    response["related_insights"] = results["related_insights"]
    response["follow_up_suggestions"] = results["follow_up_suggestions"]
    return response
