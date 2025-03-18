# Know Your Meme Scraper for AI Agents

This package provides tools for scraping and retrieving information about internet memes from [Know Your Meme](https://knowyourmeme.com/) website. It is specifically designed to be integrated into AI agents.

## High Level Overview

The KYM Scraper allows AI agents to:
1. Retrieve the latest memes from Know Your Meme
2. Fetch detailed HTML content for specific memes
3. Process and analyze meme information

This enables AI agents to stay up-to-date with internet culture trends and integrate meme-related information into their services.

## Features

- Retrieve the newest memes from Know Your Meme
- Get detailed information about specific memes
- Easy integration with AI agent frameworks
- Clean API for agent function calling
- Multiple integration patterns for different AI frameworks

## Getting Started

### Installation

#### Option 1: Install from the repository

1. Clone this repository
```bash
git clone https://github.com/yourusername/kym_scraper.git
cd kym_scraper
```

2. Install the package in development mode:
```bash
pip install -e .
```

#### Option 2: Install dependencies only

```bash
pip install -r requirements.txt
```

### Quick Start

1. Get the latest memes:
```python
from kym_scraper import get_newest_memes

# Get the 5 newest memes
memes = get_newest_memes(limit=5)

# Display results
for meme in memes:
    print(f"{meme['title']} - {meme['url']}")
```

2. Get details for a specific meme:
```python
from kym_scraper import get_meme_details

# Get details for a specific meme
details = get_meme_details(url="https://knowyourmeme.com/memes/brazen-bull")

# Print stats
print(f"Status: {details['status_code']}")
print(f"Content length: {len(details['html'])} bytes")
```

## Usage

### Command Line Interface

You can use the scraper directly from the command line:

```bash
# Get the 5 newest memes
python -m kym_scraper.agent get_newest_memes '{"limit": 5}'

# Get details for a specific meme
python -m kym_scraper.agent get_meme_details '{"url": "https://knowyourmeme.com/memes/brazen-bull"}'
```

### Integration with AI Agents

This package provides multiple ways to integrate with AI agents:

#### 1. Direct Function Calling

Import the `agent_main` function from the package:

```python
from kym_scraper import agent_main

# Get newest memes
result = agent_main("get_newest_memes", {"limit": 3})
memes = result["data"]

# Get details for a specific meme
result = agent_main("get_meme_details", {"url": "https://knowyourmeme.com/memes/brazen-bull"})
details = result["data"]
```

#### 2. Using the KYMAgentTool Class

For more advanced integration, use the `KYMAgentTool` class:

```python
from kym_scraper.ai_integration import KYMAgentTool

# Create a tool instance
kym_tool = KYMAgentTool()

# Get tool definitions in OpenAI function calling format
tool_definitions = kym_tool.get_tool_functions()

# Use the tool methods directly
newest_memes = kym_tool.get_newest_memes(limit=5)
meme_details = kym_tool.get_meme_details(url="https://knowyourmeme.com/memes/brazen-bull")
```

#### 3. Framework-Specific Integration

For integration with LangChain or similar frameworks:

```python
from kym_scraper.ai_integration import create_langchain_tool

# Get a LangChain compatible tool definition
langchain_tool = create_langchain_tool()

# Use in your LangChain agent
# agent = Agent(tools=[langchain_tool])
```

## Example Agents

The package includes example agent implementations that demonstrate different usage patterns:

### 1. Simple Agent with Natural Language Processing

This example shows a simple agent that can understand basic natural language requests:

```bash
python examples/agent_example.py
```

### 2. HTML Processing Agent

This example demonstrates how to:
1. Fetch the latest memes
2. Retrieve their HTML content
3. Hand off the HTML data to an agent for processing

```bash
python examples/html_processing_agent.py
```

The HTML processing agent analyzes the meme content to extract useful information such as:
- Content quality assessment
- Paragraph and image counts
- Detection of key sections (origin, spread, examples)
- Summary statistics across multiple memes

## Package Structure

- `kym_scraper/`: Main package
  - `scraper.py`: Core scraping functionality
  - `agent.py`: Agent-friendly wrapper for scraper functions
  - `ai_integration.py`: Integration examples for AI frameworks
- `examples/`: Example implementations
  - `agent_example.py`: Simple agent using the KYM tools
  - `html_processing_agent.py`: Agent that processes HTML content
- `requirements.txt`: Package dependencies
- `setup.py`: Package installation configuration

## Integration Patterns

### Pattern 1: Direct API Usage
Use the package functions directly in your code.

### Pattern 2: Agent-driven Queries
Let your agent determine what information to fetch based on user queries.

### Pattern 3: Data Collection + Agent Processing
First collect the data, then hand it off to an agent for processing (as shown in the HTML processing example).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 