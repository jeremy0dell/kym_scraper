#!/usr/bin/env python3
"""
Integration module for using the Know Your Meme scraper with AI frameworks.
This provides examples for integrating with different AI agent frameworks.
"""

import json
from typing import Dict, Any, List, Optional, Callable
from .agent import agent_main

class KYMAgentTool:
    """
    Tool class for integrating KYM scraper with AI agent frameworks.
    This follows a common pattern used in frameworks like LangChain and similar.
    """
    
    def __init__(self):
        self.name = "know_your_meme_tool"
        self.description = "Tool for retrieving information about internet memes from KnowYourMeme.com"
        
    def get_newest_memes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the newest memes from Know Your Meme."""
        result = agent_main("get_newest_memes", {"limit": limit})
        return result["data"]
    
    def get_meme_details(self, url: str) -> Dict[str, Any]:
        """Get details for a specific meme."""
        result = agent_main("get_meme_details", {"url": url})
        return result["data"]

    def get_tool_functions(self) -> List[Dict[str, Any]]:
        """
        Return tool definitions in OpenAI function calling format.
        This format works with many AI frameworks.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_newest_memes",
                    "description": "Get the newest memes from Know Your Meme",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of memes to return"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_meme_details",
                    "description": "Get details for a specific meme",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL of the meme to fetch details for"
                            }
                        },
                        "required": ["url"]
                    }
                }
            }
        ]

# Example: Implementation for LangChain-style framework
def create_langchain_tool():
    """
    Create a tool compatible with LangChain-style frameworks.
    
    Returns:
        Dict containing tool configuration
    """
    kym_tool = KYMAgentTool()
    
    # This is a template - actual implementation would depend on the framework
    return {
        "name": "know_your_meme",
        "description": "Tool for retrieving information about internet memes.",
        "func": lambda params: agent_main(params["action"], params["params"]),
        "schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_newest_memes", "get_meme_details"],
                    "description": "The action to perform"
                },
                "params": {
                    "type": "object",
                    "description": "Parameters for the action"
                }
            },
            "required": ["action"]
        }
    }

# Example: Implementation for direct function calling
def register_agent_callbacks(callback_registry: Dict[str, Callable]):
    """
    Register callback functions to be used by an AI agent.
    
    Args:
        callback_registry: Dictionary to register callbacks to
    """
    kym_tool = KYMAgentTool()
    
    callback_registry["get_newest_memes"] = kym_tool.get_newest_memes
    callback_registry["get_meme_details"] = kym_tool.get_meme_details
    
    return callback_registry

# Example usage when run directly
if __name__ == "__main__":
    print("KYM Agent Tool Configuration:")
    kym_tool = KYMAgentTool()
    print(json.dumps(kym_tool.get_tool_functions(), indent=2))
    
    print("\nExample usage:")
    newest_memes = kym_tool.get_newest_memes(limit=2)
    print(f"Found {len(newest_memes)} newest memes")
    
    if newest_memes:
        first_meme = newest_memes[0]
        print(f"First meme: {first_meme['title']} - {first_meme['url']}") 