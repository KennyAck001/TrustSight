# AI Research Agent Backend

## Overview

This is a Python FastAPI backend for an AI Research Agent that accepts research queries and returns real data outputs such as bullet points, tables, or graphs based on the query type.

## Features

- POST `/research`: Accepts a research query and returns:
  - Bullet points text for "points" queries
  - Pandas DataFrame (as JSON) for "table" queries
  - Graph image (base64) + textual explanation for "graph" queries
- POST `/approve_source`: Approves a source URL and updates trust scores
- POST `/flag_source`: Flags a source URL as unreliable

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download the project files.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SERPER_API_KEY`: Your Serper API key
   - `GEMINI_API_KEY`: Your Google Gemini API key (optional fallback)

## Running Locally

Run the FastAPI server:
```
python main.py
```
Or with uvicorn:
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### POST `/research`

**Input:**
```json
{
  "query": "string"
}
```

**Output:**
- For points queries (default):
  ```json
  {
    "points": "- Claim 1\n- Claim 2\n..."
  }
  ```
- For table queries (if query contains "table", "compare", etc.):
  ```json
  {
    "table": [
      {"Claim": "Claim 1", "Source": 0, "Trust Score": 0.8, "Confidence": 0.7},
      ...
    ]
  }
  ```
- For graph queries (if query contains "graph", "plot", etc.):
  ```json
  {
    "graph_image_base64": "base64_encoded_image",
    "explanation": "Textual explanation of the graph"
  }
  ```

### POST `/approve_source`

**Input:**
```json
{
  "source": "https://example.com"
}
```

**Output:**
```json
{
  "message": "Source https://example.com approved and trust score updated."
}
```

### POST `/flag_source`

**Input:**
```json
{
  "source": "https://example.com"
}
```

**Output:**
```json
{
  "message": "Source https://example.com flagged as unreliable and trust score updated."
}
```

## Sample Queries

- Points: "What are the benefits of renewable energy?"
- Table: "Compare different programming languages in a table"
- Graph: "Show a graph of global temperature changes"

## Modules

- `search.py`: Web search using Serper API
- `fetcher.py`: Async content fetching and cleaning
- `claims.py`: LLM-based claim extraction
- `trust_scoring.py`: Multilayer trust scoring
- `cve.py`: Cross-validation engine
- `summarizer.py`: Query-type based summarization
- `graph_generator.py`: Real graph generation with matplotlib

## Notes

- Query type is detected using keyword heuristics; can be enhanced with LLM classification.
- Graphs are generated as PNG images encoded in base64.
- Trust scoring includes domain authority, recency, author credibility, structural completeness, and cross-reference validation.
- Cross-validation clusters similar claims and assigns confidence scores.
