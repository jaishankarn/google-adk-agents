# Support Ticket Insights Agent

An AI-powered support analytics agent built with Google ADK that analyzes support ticket data and provides actionable insights.

## Folder Structure

```
agents/
└── support_agent/
    ├── agent.py              # Main agent with root_agent
    ├── Support_Metrics.csv   # Support ticket data
    └── tools/
        ├── __init__.py
        └── db_tools.py       # Data fetching and analysis tools
```

## Running the Agent

### From the project root directory:

```bash
cd /Users/jaishankar/Documents/stuffs/my_agent
adk web
```

This will:
1. Scan the `agents/` directory
2. Find the `support_agent` folder
3. Load `agent.py` with `root_agent`
4. Start the web interface in your browser

### Access the agent:
- The web interface will open at `http://localhost:8000` (or similar)
- Select "support_agent" from the available agents
- Start asking questions about your support tickets!

## Example Queries

Try asking the agent:

### Category Analysis
- "Which category has the most tickets?"
- "Show me the top 5 categories by ticket volume"
- "What's the ticket distribution by category?"

### SLA Performance
- "Show categories with the most SLA breaches"
- "What's the overall SLA compliance rate?"
- "Which categories have the worst SLA performance?"

### Time Analysis
- "What's the average resolution time by category?"
- "Which categories take the longest to resolve?"
- "Show resolution time statistics"

### Agent Performance
- "Which support agent resolved the most tickets?"
- "Show me agent performance metrics"
- "Compare agents by SLA compliance"
- "Who is the top performing agent?"

### Issue Analysis
- "What are the common issues in Bug category?"
- "Summarize recurring problems"
- "What issues appear most frequently?"

## Agent Capabilities

The agent has access to 3 tools:

1. **fetch_tickets(days, category, sla_status)**
   - Retrieves ticket data with flexible filtering
   - Filter by time period (default: last 90 days)
   - Filter by category or SLA status

2. **get_category_summary(top_n)**
   - Aggregates tickets by Main category
   - Shows ticket counts, SLA breaches, avg resolution time
   - Returns top N categories sorted by volume

3. **get_agent_performance()**
   - Analyzes individual support agent metrics
   - Calculates tickets resolved, avg time, SLA compliance
   - Excludes Ghost/UnAssigned entries

## Data Overview

The `Support_Metrics.csv` contains:
- **7,089 tickets** (last 90 days)
- **26 columns** of data
- Key categories: Bug, Offline, Config, Service Failure, etc.
- SLA tracking: "within sla" vs "outside sla"
- Resolution times in minutes and days
- Agent assignments and performance data

### Key Statistics:
- Top category: **Bug** (18,949 total tickets)
- SLA breach rate: **~48%** for Bug category
- Highest breach rate: **Config** (92.4%)
- Multiple support agents tracked

## Dependencies

Required packages (install from project root):
```bash
pip install pandas python-dotenv google-generativeai google-adk
```

## Environment Setup

Ensure you have a `.env` file in the project root with:
```
GOOGLE_API_KEY=your_api_key_here
```

## Troubleshooting

### Agent not appearing in ADK web interface?
- Verify the folder structure matches: `agents/support_agent/agent.py`
- Ensure `agent.py` contains `root_agent` variable
- Check that all imports work: `python3 agent.py`

### CSV file not found?
- Ensure `Support_Metrics.csv` is in the same directory as `agent.py`
- The tools look for the CSV relative to their location

### Tool errors?
- Test tools independently: `python3 -c "from tools.db_tools import fetch_tickets; print(fetch_tickets())"`
- Ensure pandas is installed
- Check CSV file permissions

## Notes

- The agent uses Google's Gemini 2.5 Flash model
- All data analysis happens locally from the CSV file
- No external database connection required
- Tools are optimized for fast response times
