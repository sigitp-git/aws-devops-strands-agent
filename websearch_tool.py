#!/usr/bin/env python3
"""
Web search tool using DuckDuckGo with timeout protection.
"""

import signal
from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException
from strands.tools import tool
from config import SEARCH_TIMEOUT_SECONDS, DEFAULT_MAX_SEARCH_RESULTS, MAX_SEARCH_RESULTS_LIMIT


@tool
def websearch(
    keywords: str, region: str = "us-en", max_results: int | None = DEFAULT_MAX_SEARCH_RESULTS
) -> str:
    """Search the web to get updated information quickly.
    Args:
        keywords (str): The search query keywords.
        region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
        max_results (int | None): The maximum number of results to return (default: 3 for speed).
    Returns:
        List of dictionaries with search results.
    """
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Search timeout after {SEARCH_TIMEOUT_SECONDS} seconds")
    
    try:
        # Set timeout for search operation
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(SEARCH_TIMEOUT_SECONDS)
        
        # Limit results for faster responses
        if max_results is None or max_results > MAX_SEARCH_RESULTS_LIMIT:
            max_results = DEFAULT_MAX_SEARCH_RESULTS
            
        print(f"🔍 Searching for: {keywords}")
        results = DDGS().text(keywords, region=region, max_results=max_results)
        
        # Cancel timeout
        signal.alarm(0)
        
        if results:
            print(f"✅ Found {len(results)} results")
            return results
        else:
            return "No results found."
            
    except TimeoutError:
        signal.alarm(0)
        return "Search timeout - please try a more specific query."
    except RatelimitException:
        return "Rate limit reached - please try again in a moment."
    except DDGSException as d:
        return f"Search service error: {d}"
    except Exception as e:
        return f"Search failed: {e}"
    finally:
        signal.alarm(0)  # Ensure timeout is always cancelled