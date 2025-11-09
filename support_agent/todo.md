# Support Ticket Insights Agent - Implementation Plan

## Phase 1: Setup Directory Structure ✓

Create the necessary folders and files:
```
support_agent/
├── agents/
│   └── ticket_insights_agent.py    # Main agent definition
├── tools/
│   └── db_tools.py                 # CSV data fetching tool
├── Support_Metrics.csv              # ✓ Already exists
├── prd.md                          # ✓ Already exists
└── todo.md                         # ✓ This file
```

**Status:** Partially complete (need to create `agents/` and `tools/` folders)

---

## Phase 2: Build the Data Tool

### Task 2.1: Create `tools/` directory
```bash
mkdir -p support_agent/tools
```

### Task 2.2: Create `tools/db_tools.py`

Implement `fetch_tickets()` function that:
- Reads from `Support_Metrics.csv`
- Parses CSV data into structured format
- Returns columns and rows (similar to database query result)
- Supports optional filtering:
  - By date range (last 90 days, last 30 days, etc.)
  - By category
  - By SLA status

**Key Implementation Details:**
```python
import pandas as pd
from datetime import datetime, timedelta

def fetch_tickets(days=90, category=None, sla_status=None):
    """
    Fetch support tickets from CSV file.

    Args:
        days: Number of days to look back (default: 90)
        category: Filter by Main category (optional)
        sla_status: Filter by Completed Type (optional)

    Returns:
        Dictionary with 'columns' and 'rows' keys
    """
    # Implementation here
```

**CSV Columns to Focus On:**
- `Req ID` - Unique identifier
- `Request Category` - Issue category
- `Main category`, `Sub category`, `SubSub category` - Classification
- `Issue Reported` - Problem description
- `Completed Type` - SLA status (within sla / outside sla)
- `Time Taken in Minutes` - Resolution time
- `Time Taken in Days` - Resolution time in days
- `Agent name` - Who resolved the ticket
- `Request Date` - When ticket was created
- `Resolution Date` - When ticket was resolved
- `Stage Name` - Current stage
- `Level` - Support level (level-2, level-3)

---

## Phase 3: Create the Agent

### Task 3.1: Create `agents/` directory
```bash
mkdir -p support_agent/agents
```

### Task 3.2: Create `agents/ticket_insights_agent.py`

Implement the agent with:

```python
from google.adk.agents.llm_agent import Agent
from google.adk.tools import Tool
import sys
sys.path.append('..')
from tools.db_tools import fetch_tickets

# Create tool wrapper
fetch_tool = Tool(
    function=fetch_tickets,
    name="fetch_tickets",
    description="Fetch support tickets from CSV including category, SLA status, resolution time, and agent performance data."
)

# Create agent
ticket_insights_agent = Agent(
    model="gemini-2.5-flash",
    name="ticket_insights_agent",
    description="Analyzes support tickets and provides insights on issues, categories, SLAs, and agent performance.",
    instruction=(
        "You are a support analytics expert. Use the fetch_tickets tool to retrieve support ticket data. "
        "Analyze trends by category, SLA performance, resolution times, and agent performance. "
        "Detect recurring issues by examining the 'Issue Reported' field. "
        "Provide actionable insights with specific numbers and percentages. "
        "Summarize findings clearly and highlight problem areas that need attention."
    ),
    tools=[fetch_tool]
)
```

---

## Phase 4: Key Capabilities to Implement

The agent should be able to answer:

### Category Analysis
- "Which category has the most tickets?"
- "What's the distribution of tickets by Main category?"
- "Show ticket volume by Sub category"

### SLA Performance
- "Show categories with most SLA breaches"
- "What percentage of tickets meet SLA?"
- "Which categories consistently breach SLA?"

### Time Analysis
- "What's the average resolution time by category?"
- "Which tickets take the longest to resolve?"
- "Show resolution time trends"

### Common Issues Detection
- "What are recurring problems in the Bug category?"
- "Summarize common issues from 'Issue Reported' field"
- "What are users complaining about most?"

### Agent Performance
- "Which agent resolved the most tickets?"
- "Show average resolution time by agent"
- "Compare agent performance"

### Comparative Analysis
- "Compare Bug vs Config tickets"
- "Trend analysis for last 30 days vs last 90 days"

---

## Phase 5: Dependencies & Setup

### Task 5.1: Create `requirements.txt`
```txt
google-generativeai
google-adk
pandas
python-dotenv
```

### Task 5.2: Install dependencies
```bash
pip install -r support_agent/requirements.txt
```

### Task 5.3: Update `.env` file
Ensure Google API key is configured (already done)

---

## Phase 6: Testing & Validation

### Task 6.1: Test basic queries
Run the agent and test with:
- "Summarize tickets by Main category"
- "Which category has the most SLA breaches?"
- "Show average resolution time by agent"

### Task 6.2: Test advanced queries
- "What are the top 3 common problems users are reporting?"
- "Compare Bug vs Offline processing performance"
- "Which agents have the best SLA compliance?"

### Task 6.3: Validate insights accuracy
- Cross-check agent responses with manual CSV analysis
- Ensure percentages and counts are correct
- Verify date filtering works properly

---

## Phase 7: Optional Enhancements

### Task 7.1: Add report export functionality
Create `tools/report_tools.py` with:
- `export_to_csv(data, filename)` - Export analysis to CSV
- `generate_summary_report()` - Create formatted markdown report

### Task 7.2: Add visualization capabilities
- Create simple charts using matplotlib/plotly
- Generate category distribution charts
- Create SLA compliance visualizations

### Task 7.3: Add scheduled reporting
- Create script to run daily/weekly analysis
- Email reports to stakeholders
- Track trends over time

---

## Success Criteria

- [ ] Agent successfully reads CSV data
- [ ] Agent can answer category-based questions
- [ ] Agent can calculate SLA performance metrics
- [ ] Agent can identify recurring issues
- [ ] Agent provides accurate statistics (counts, percentages, averages)
- [ ] Response time < 5 seconds for typical queries
- [ ] Insights are actionable and clearly presented

---

## Notes

### CSV Data Insights
Based on the Support_Metrics.csv file:
- **Total columns:** 26
- **Key categories:** Bug, Offline, Config, Service Failure, Duplicate, New Use Case
- **SLA statuses:** "within sla", "outside sla"
- **Support levels:** level-2, level-3
- **Date format:** YYYY-MM-DD HH:MM:SS

### Common Issue Patterns Observed
- PDF generation failures
- DTD/XML validation errors
- Float placement issues
- Base alignment problems
- Template updates needed

### Agent Performance Data Available
- Agent names in `Agent name` column
- Resolution times in `Time Taken in Minutes` and `Time Taken in Days`
- Assignment tracking in `Assigned To` column

---

## Getting Started

1. Create directory structure (Phase 1)
2. Implement `tools/db_tools.py` (Phase 2)
3. Implement `agents/ticket_insights_agent.py` (Phase 3)
4. Install dependencies (Phase 5)
5. Test with sample queries (Phase 6)
6. Iterate and improve based on results

---

## Questions to Resolve

- [ ] Should we filter out "Duplicate" entries from analysis?
- [ ] How to handle entries with 0 resolution time?
- [ ] Should we analyze both "Time Taken in Minutes" and "Time Taken in Minutes (Business)"?
- [ ] How to parse and summarize the "Issue Reported" field for common themes?
