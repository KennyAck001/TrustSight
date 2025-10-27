import os
import base64
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from cachetools import TTLCache

from search import async_search
from fetcher import async_fetch_and_clean
from claims import extract_claims
from trust_scoring import update_trust_score, approve_source, mark_source_unreliable
from cve import cross_validate_claims
from summarizer import summarize_results
from graph_generator import generate_graph

app = FastAPI(title="AI Research Agent Backend")

response_cache = TTLCache(maxsize=100, ttl=300)  # Cache up to 100 queries for 5 minutes

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchQuery(BaseModel):
    query: str

class SourceURL(BaseModel):
    source: str

@app.post("/research")
async def research_endpoint(request: ResearchQuery):
    start_time = time.time()
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Check cache first
    cache_key = query.lower()
    if cache_key in response_cache:
        print(f"DEBUG: Cache hit for query '{query}'")
        return response_cache[cache_key]

    # Step 0: Classify intent
    intent_start = time.time()
    from response_generator import classify_intent
    intent = await classify_intent(query)
    intent_time = time.time() - intent_start
    print(f"DEBUG: Classified intent for query '{query}': {intent} (took {intent_time:.2f}s)")

    if intent == "conversation":
        # Generate conversational response
        conv_start = time.time()
        from response_generator import generate_conversation
        response = await generate_conversation(query)
        conv_time = time.time() - conv_start
        print(f"DEBUG: Conversation response generated (took {conv_time:.2f}s)")
        return response

    # Research path
    # Detect query types (points, table, graph) - can detect multiple
    # For simplicity, use keyword heuristics here; can be replaced with LLM classification
    query_lower = query.lower()
    query_types = []
    if any(k in query_lower for k in ["table", "compare", "list", "dataframe"]):
        query_types.append("table")
    if any(k in query_lower for k in ["graph", "plot", "chart", "visualize"]):
        query_types.append("graph")
    if not query_types:
        query_types = ["points"]

    # Step 1: Search web asynchronously
    search_start = time.time()
    search_results = await async_search(query)
    search_time = time.time() - search_start
    print(f"DEBUG: Search completed (took {search_time:.2f}s)")

    # Step 2: Fetch and clean content asynchronously
    fetch_start = time.time()
    contents = await async_fetch_and_clean(search_results)
    fetch_time = time.time() - fetch_start
    print(f"DEBUG: Fetch completed (took {fetch_time:.2f}s), contents length: {len(contents)}, first content preview: {contents[0][:200] if contents else 'No contents'}")

    if not contents:
        raise HTTPException(status_code=503, detail="Failed to fetch data from web sources. Please try again later.")

    # Step 3: Generate response directly using LLM based on query and content
    generate_start = time.time()
    from response_generator import generate_response
    response = await generate_response(query, contents, query_types)
    generate_time = time.time() - generate_start
    print(f"DEBUG: Response generation completed (took {generate_time:.2f}s)")

    total_time = time.time() - start_time
    print(f"DEBUG: Total request time: {total_time:.2f}s")

    # Cache the response
    response_cache[cache_key] = response

    return response

@app.post("/approve_source")
async def approve_source_endpoint(request: SourceURL):
    source_url = request.source.strip()
    if not source_url:
        raise HTTPException(status_code=400, detail="Source URL cannot be empty")
    approve_source(source_url)
    return {"message": f"Source {source_url} approved and trust score updated."}

@app.post("/flag_source")
async def flag_source_endpoint(request: SourceURL):
    source_url = request.source.strip()
    if not source_url:
        raise HTTPException(status_code=400, detail="Source URL cannot be empty")
    mark_source_unreliable(source_url)
    return {"message": f"Source {source_url} flagged as unreliable and trust score updated."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
