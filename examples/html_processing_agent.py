#!/usr/bin/env python3
"""
Example script that demonstrates:
1. Fetching the latest memes
2. Retrieving their HTML content
3. Passing the HTML to an agent for processing

The agent only takes over after the HTML data is collected.
"""

import sys
import os
import json
from typing import Dict, Any, List

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kym_scraper import get_newest_memes, get_meme_details

class HTMLProcessingAgent:
    """
    Agent that processes HTML content of memes.
    
    This demonstrates how an AI agent would take HTML content
    and extract useful information from it.
    """
    
    def __init__(self):
        self.processed_memes = []
    
    def process_html(self, meme_data: Dict[str, Any], html_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the HTML content of a meme and extract key information.
        
        Args:
            meme_data: Basic meme info (title, URL)
            html_data: HTML content and metadata for the meme
            
        Returns:
            Dictionary with extracted information
        """
        # In a real AI agent, this would use NLP or other techniques to extract
        # information from the HTML. For this example, we'll do some basic extraction.
        
        result = {
            "title": meme_data["title"],
            "url": meme_data["url"],
            "http_status": html_data["status_code"],
            "content_length": len(html_data["html"]),
            "analysis": self._analyze_meme_content(html_data["html"], meme_data["title"])
        }
        
        self.processed_memes.append(result)
        return result
    
    def _analyze_meme_content(self, html: str, title: str) -> Dict[str, Any]:
        """
        Analyze the meme content and extract useful information.
        
        This simulates what an AI agent would do with the HTML.
        In a real application, this would use language models or other
        techniques to extract meaningful data.
        
        Args:
            html: The HTML content
            title: The meme title
            
        Returns:
            Dictionary with analysis results
        """
        # For demonstration purposes, we'll do some basic analysis
        paragraph_count = html.count("<p>")
        image_count = html.count("<img")
        
        # Check for social media meta tags
        twitter_card = "twitter:card" in html
        og_image = "og:image" in html
        
        # Look for meme content indicators
        has_origin_section = "Origin</h2>" in html or "origin" in html.lower()
        has_spread_section = "Spread</h2>" in html or "spread" in html.lower()
        has_examples_section = "Examples</h2>" in html or "examples" in html.lower()
        
        # This is where an AI agent would perform more sophisticated analysis
        # For example, summarizing the meme, extracting key dates, identifying related memes, etc.
        
        return {
            "paragraph_count": paragraph_count,
            "image_count": image_count,
            "has_twitter_card": twitter_card,
            "has_og_image": og_image,
            "has_origin_section": has_origin_section,
            "has_spread_section": has_spread_section,
            "has_examples_section": has_examples_section,
            "estimated_content_quality": "high" if paragraph_count > 10 else "medium" if paragraph_count > 5 else "low"
        }
    
    def summarize_findings(self) -> Dict[str, Any]:
        """
        Summarize the analysis of all processed memes.
        
        Returns:
            Summary statistics and insights
        """
        if not self.processed_memes:
            return {"error": "No memes have been processed"}
        
        # Calculate some basic statistics
        total_memes = len(self.processed_memes)
        avg_content_length = sum(meme["content_length"] for meme in self.processed_memes) / total_memes
        
        quality_counts = {
            "high": sum(1 for meme in self.processed_memes if meme["analysis"]["estimated_content_quality"] == "high"),
            "medium": sum(1 for meme in self.processed_memes if meme["analysis"]["estimated_content_quality"] == "medium"),
            "low": sum(1 for meme in self.processed_memes if meme["analysis"]["estimated_content_quality"] == "low")
        }
        
        # This is where an AI agent would generate insights based on the collected data
        
        return {
            "total_memes_processed": total_memes,
            "average_content_length": avg_content_length,
            "content_quality_distribution": quality_counts,
            "memes_with_origin_section": sum(1 for meme in self.processed_memes if meme["analysis"]["has_origin_section"]),
            "memes_with_spread_section": sum(1 for meme in self.processed_memes if meme["analysis"]["has_spread_section"]),
            "memes_with_examples_section": sum(1 for meme in self.processed_memes if meme["analysis"]["has_examples_section"])
        }


def main():
    print("Know Your Meme HTML Processing Agent Demo\n")
    print("Step 1: Fetching the latest memes...")
    
    # Get the 3 latest memes
    limit = 3
    memes = get_newest_memes(limit=limit)
    
    print(f"Found {len(memes)} memes\n")
    for i, meme in enumerate(memes, 1):
        print(f"{i}. {meme['title']} - {meme['url']}")
    
    print("\nStep 2: Retrieving HTML content for each meme...")
    
    # Get HTML content for each meme
    memes_with_html = []
    for meme in memes:
        print(f"Fetching HTML for: {meme['title']}")
        html_data = get_meme_details(meme['url'])
        
        if "error" in html_data:
            print(f"  Error: {html_data['error']}")
        else:
            print(f"  Success: {len(html_data['html'])} bytes, Status: {html_data['status_code']}")
            memes_with_html.append({
                "meme": meme,
                "html": html_data
            })
    
    print(f"\nSuccessfully retrieved HTML for {len(memes_with_html)} memes")
    
    print("\nStep 3: Handing off to the agent for processing...")
    
    # Initialize the agent
    agent = HTMLProcessingAgent()
    
    # Process each meme
    for item in memes_with_html:
        print(f"Agent processing: {item['meme']['title']}")
        result = agent.process_html(item['meme'], item['html'])
        
        # Print some analysis results
        print(f"  Content quality: {result['analysis']['estimated_content_quality']}")
        print(f"  Paragraph count: {result['analysis']['paragraph_count']}")
        print(f"  Image count: {result['analysis']['image_count']}")
        
        if result['analysis']['has_origin_section']:
            print("  Has origin section: Yes")
        if result['analysis']['has_spread_section']:
            print("  Has spread section: Yes")
        if result['analysis']['has_examples_section']:
            print("  Has examples section: Yes")
        
        print()
    
    # Get the summary
    print("Agent summary of all processed memes:")
    summary = agent.summarize_findings()
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main() 