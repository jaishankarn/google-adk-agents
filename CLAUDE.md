# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Google ADK (Agent Development Kit) agent project that uses Google's Gemini models to create an AI agent with tool-calling capabilities.

## Architecture

**Core Components:**
- `agent.py`: Contains the root agent definition using Google ADK's `Agent` class
  - Configured to use `gemini-2.5-flash` model
  - Implements a simple time-telling agent with tool support
  - Tools are defined as Python functions decorated for the agent

**Agent Pattern:**
- Agents are created using `google.adk.agents.llm_agent.Agent`
- Each agent requires: `model`, `name`, `description`, `instruction`, and `tools` parameters
- Tools are regular Python functions that the agent can call
- Tool functions should have clear docstrings as the agent uses them to understand tool capabilities

## Environment Configuration

The project uses a `.env` file with the following variables:
- `GOOGLE_GENAI_USE_VERTEXAI`: Set to 0 to use Google AI Studio (set to 1 for Vertex AI)
- `GOOGLE_API_KEY`: API key for Google AI Studio

**Important:** The `.env` file is tracked in this repository but should contain placeholder values only.

## Running the Agent

To run the agent:
```bash
python agent.py
```

or import and use programmatically:
```python
from agent import root_agent
# Use root_agent for interactions
```

## Development Notes

**Adding New Tools:**
1. Define a Python function with type hints and a clear docstring
2. Add the function to the `tools` list in the Agent constructor
3. The agent will automatically understand how to use the tool based on its signature and docstring

**Modifying Agent Behavior:**
- Update the `instruction` parameter to change the agent's base behavior
- Update the `description` parameter to change how the agent describes itself
- Switch models by changing the `model` parameter (e.g., `gemini-2.5-flash`, `gemini-2.0-pro`)
