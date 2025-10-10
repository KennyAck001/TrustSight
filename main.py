import os
import base64
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from search import async_search
from fetcher import async_fetch_and_clean
from claims import extract_claims
from trust_scoring import update_trust_score, approve_source, mark_source_unreliable
from cve import cross_validate_claims
from summarizer import summarize_results
from graph_generator import generate_graph

app = FastAPI(title="AI Research Agent Backend")

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
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

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
    search_results = await async_search(query)

    # Step 2: Fetch and clean content asynchronously
    contents = await async_fetch_and_clean(search_results)
    print(f"DEBUG: Fetched contents length: {len(contents)}, first content preview: {contents[0][:200] if contents else 'No contents'}")

    if not contents:
        raise HTTPException(status_code=503, detail="Failed to fetch data from web sources. Please try again later.")

    # Step 3: Generate response directly using LLM based on query and content
    from response_generator import generate_response
    response = await generate_response(query, contents, query_types)

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
