#!/usr/bin/env python3
"""
AI Agent interface for the Know Your Meme scraper.
This module provides functions that can be easily called from AI agents.
"""
from typing import List, Dict, Any, Optional
from .scraper import scrape_newest_memes, get_meme_html

def get_newest_memes(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get the newest memes from Know Your Meme.
    
    Args:
        limit: Maximum number of memes to return (default: 5)
        
    Returns:
        List of dictionaries containing meme information
    """
    return scrape_newest_memes(limit=limit)

def get_meme_details(url: str) -> Dict[str, Any]:
    """
    Get the HTML content of a specific meme page and extract key details.
    
    Args:
        url: URL of the meme to fetch details for
        
    Returns:
        Dictionary with meme details and full HTML
    """
    result = get_meme_html(url)
    return result

def agent_main(action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Main entry point for AI agent to call scraper functions.
    
    Args:
        action: The action to perform ("get_newest_memes" or "get_meme_details")
        params: Dictionary of parameters for the action
        
    Returns:
        Result of the requested action
    """
    if params is None:
        params = {}
    
    if action == "get_newest_memes":
        limit = params.get("limit", 5)
        memes = get_newest_memes(limit=limit)
        return {"status": "success", "data": memes}
    
    elif action == "get_meme_details":
        url = params.get("url")
        if not url:
            return {"status": "error", "message": "URL is required for get_meme_details action"}
        
        details = get_meme_details(url)
        return {"status": "success", "data": details}
    
    else:
        return {
            "status": "error", 
            "message": f"Unknown action: {action}. Available actions: get_newest_memes, get_meme_details"
        }

# Example usage when run directly (not as an imported module)
if __name__ == "__main__":
    import sys
    import json
    
    # Simple CLI interface for testing
    if len(sys.argv) < 2:
        print("Usage: python agent.py <action> [params_json]")
        print("Example: python agent.py get_newest_memes '{\"limit\": 3}'")
        sys.exit(1)
    
    action = sys.argv[1]
    params = {}
    
    if len(sys.argv) > 2:
        try:
            params = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            print("Error: params must be a valid JSON string")
            sys.exit(1)
    
    result = agent_main(action, params)
    print(json.dumps(result, indent=2)) 