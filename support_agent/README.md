# Support Ticket Insights Agent

An AI-powered support analytics agent built with Google ADK that analyzes support ticket data and provides actionable insights.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file in the parent directory with:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Running the Agent

### Using Google ADK Web Interface

Navigate to the support_agent directory and run:
```bash
adk web
```

This will start the ADK web interface in your browser where you can interact with the agent.

### Using the Agent Programmatically

```python
from agents.ticket_insights_agent import ticket_insights_agent

# The agent is ready to use
# Integrate with your application or use with ADK Runner
```

## Example Queries

Try asking the agent:

1. **Category Analysis:**
   - "Which category has the most tickets?"
   - "Show me the top 5 categories by ticket volume"
   - "What's the ticket distribution by category?"

2. **SLA Performance:**
   - "Show categories with the most SLA breaches"
   - "What's the overall SLA compliance rate?"
   - "Which categories consistently breach SLA?"

3. **Time Analysis:**
   - "What's the average resolution time by category?"
   - "Which categories take the longest to resolve?"

4. **Agent Performance:**
   - "Which agent resolved the most tickets?"
   - "Show me agent performance metrics"
   - "Compare agents by SLA compliance"

5. **Issue Analysis:**
   - "What are the common issues in Bug category?"
   - "Summarize recurring problems"

## Agent Capabilities

- Analyzes 7,000+ support tickets
- Tracks SLA compliance across categories
- Monitors agent performance
- Identifies recurring issues
- Provides data-driven recommendations

## Data Source

The agent reads from `Support_Metrics.csv` containing:
- Ticket IDs and metadata
- Categories and subcategories
- Issue descriptions
- Resolution times
- SLA status
- Agent assignments

## Tools Available

1. **fetch_tickets** - Retrieve raw ticket data with filtering
2. **get_category_summary** - Get aggregated category statistics
3. **get_agent_performance** - Analyze agent performance metrics
