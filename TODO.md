# TODO: Optimize Response Speed

- [x] Add in-memory caching for query responses to avoid redundant processing
- [x] Implement timing logs in main.py to measure duration of each step (search, fetch, generate)
- [x] Summarize fetched content before passing to LLM prompts in response_generator.py
- [x] Reduce unnecessary LLM calls by making graph and table generation conditional or optional
- [x] Test the optimizations and measure performance improvements
