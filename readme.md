# Research Paper Analysis Agent

## Overview

This project implements a Research Paper Analysis Agent that automates the process of searching for academic papers, analyzing their content, and exporting structured insights to Excel. The agent is built using LangGraph, allowing for a directed workflow that breaks down the research process into manageable steps.

## Architecture

The agent follows a directed graph architecture with the following components:

```
[Search Papers] → [Analyze Content] → [Extract Insights] → [Export Results]
```

### Key Components

1. **Scholar Service**: Connects to Google Scholar API to retrieve relevant papers based on search queries.
2. **Analysis Engine**: Uses LLMs to extract key information from papers, including:
   - Key findings
   - Research limitations
   - Methodology
   - Future research directions

3. **Export Service**: Formats the analyzed data and exports it to Excel with proper formatting.

4. **Models**: Pydantic models for structured data handling throughout the pipeline.

## Data Flow

1. User submits a research topic query
2. Agent searches for relevant papers via Google Scholar
3. For each paper:
   - Metadata is extracted (title, authors, year, URL)
   - Content is analyzed using GPT-4
   - Key insights are structured
4. Results are exported to Excel with formatting

## Setup and Usage

### Prerequisites

- Python 3.9+
- Required libraries:
  - langchain
  - langgraph
  - scholarly
  - pydantic
  - pandas
  - openai
  - python-dotenv

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
```

### Running the Agent

```python
from main import main

main()
```

## Code Structure

- `main.py`: Entry point for the application
- `models.py`: Pydantic data models
- `scholar_service.py`: Paper search functionality
- `export_service.py`: Excel export functionality

## Example Output

The agent generates an Excel file with the following information for each paper:
- Title
- Authors
- Year
- URL
- Key Points
- Limitations
- Methodology
- Future Directions

## Extending the Agent

### Adding New Search Sources

To add additional academic sources beyond Google Scholar:

1. Create a new service file (e.g., `arxiv_service.py`)
2. Implement the search interface
3. Update the main workflow to incorporate the new source

### Enhancing Analysis Capabilities

To improve the depth of paper analysis:

1. Modify the prompts in `scholar_service.py`
2. Add new fields to the `ResearchPaper` model
3. Update the export service to include the new fields

## LangGraph Implementation

The agent uses LangGraph to create a directed workflow:

```python
from langgraph.graph import StateGraph

# Define the agent states
states = ["search", "analyze", "export"]

# Create the graph
graph = StateGraph()

# Add nodes
graph.add_node("search", search_papers)
graph.add_node("analyze", analyze_papers) 
graph.add_node("export", export_results)

# Define edges
graph.add_edge("search", "analyze")
graph.add_edge("analyze", "export")

# Compile the graph
workflow = graph.compile()
```

## Advanced Usage

### Custom Analysis Workflows

You can customize the analysis workflow by:

1. Creating specialized analyzers for different research domains
2. Implementing conditional paths in the graph based on paper type
3. Adding human-in-the-loop verification steps

### Batch Processing

For analyzing large collections of papers:

```python
topics = ["AI ethics", "mental health therapy", "machine learning in healthcare"]
for topic in topics:
    papers = search_papers(topic, num_results=10)
    export_to_excel(papers, f"{topic.replace(' ', '_')}_results.xlsx")
```