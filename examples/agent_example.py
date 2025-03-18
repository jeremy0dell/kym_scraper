#!/usr/bin/env python3
"""
Example implementation showing how to use the Know Your Meme scraper in an AI agent.
This is a simplified example that demonstrates the integration pattern.
"""

import sys
import json
from typing import Dict, Any, List
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kym_scraper.ai_integration import KYMAgentTool

class SimpleAgent:
    """
    A simple AI agent that can use the KYM tool.
    This is a minimal implementation for demonstration purposes.
    """
    
    def __init__(self):
        # Initialize tools
        self.kym_tool = KYMAgentTool()
        
        # Register available tools
        self.tools = {
            "get_newest_memes": self.kym_tool.get_newest_memes,
            "get_meme_details": self.kym_tool.get_meme_details
        }
        
        # Get tool schemas for function calling
        self.tool_schemas = self.kym_tool.get_tool_functions()
    
    def process_request(self, request: str) -> Dict[str, Any]:
        """
        Process a natural language request and determine what tool to use.
        
        In a real implementation, this would use an LLM to:
        1. Parse the request
        2. Determine the appropriate tool
        3. Extract parameters
        4. Execute the tool
        5. Format the response
        
        Args:
            request: Natural language request from the user
            
        Returns:
            Response dictionary with tool results
        """
        # This is where an LLM would determine what tool to use
        # For this example, we'll use simple keyword matching
        
        if "newest" in request.lower() or "latest" in request.lower():
            # Extract limit parameter (in a real agent, an LLM would do this)
            limit = 5  # Default
            if "limit" in request.lower():
                # Simple extraction - a real agent would use NLP
                try:
                    limit = int(request.split("limit")[1].split()[0])
                except (IndexError, ValueError):
                    pass
            
            # Call the tool
            memes = self.tools["get_newest_memes"](limit=limit)
            
            # Format the response
            return {
                "tool_used": "get_newest_memes",
                "parameters": {"limit": limit},
                "result": memes,
                "response": f"Here are the {limit} newest memes from Know Your Meme:"
            }
            
        elif "details" in request.lower() and "url" in request.lower():
            # Extract URL parameter (in a real agent, an LLM would do this)
            url = None
            if "http" in request:
                # Simple extraction - a real agent would use NLP
                try:
                    url = request.split("http")[1].strip()
                    url = "http" + url.split()[0]
                except (IndexError, ValueError):
                    url = None
            
            if not url:
                return {
                    "error": "Could not extract URL from request",
                    "response": "Please provide a valid URL to get meme details."
                }
            
            # Call the tool
            details = self.tools["get_meme_details"](url=url)
            
            # Format the response
            return {
                "tool_used": "get_meme_details",
                "parameters": {"url": url},
                "result": details,
                "response": f"Here are the details for the meme at {url}:"
            }
        
        else:
            # Unknown request
            return {
                "error": "Unknown request",
                "response": "I can help you get the newest memes or details about a specific meme. Please specify what you need."
            }

# Example usage
if __name__ == "__main__":
    agent = SimpleAgent()
    
    # Example requests
    requests = [
        "Show me the 3 newest memes",
        "Get details for the meme at https://knowyourmeme.com/memes/example",
        "What can you do?"
    ]
    
    print("Simple AI Agent with KYM Tool Demo\n")
    
    for req in requests:
        print(f"User request: {req}")
        response = agent.process_request(req)
        
        print(f"Agent response: {response['response']}")
        
        if "result" in response:
            if response["tool_used"] == "get_newest_memes":
                memes = response["result"]
                for i, meme in enumerate(memes, 1):
                    print(f"  {i}. {meme['title']} - {meme['url']}")
            elif response["tool_used"] == "get_meme_details":
                details = response["result"]
                print(f"  Status: {details.get('status_code')}")
                print(f"  URL: {details.get('url')}")
                if "error" in details:
                    print(f"  Error: {details['error']}")
        
        print() 