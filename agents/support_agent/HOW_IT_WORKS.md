# How the Support Agent Works - Technical Deep Dive

## The Magic: Tool-Calling (Function Calling)

Your support agent uses **Google ADK's tool-calling capabilities**, which is fundamentally different from just chatting with an LLM.

## Step-by-Step: What Happens When You Ask a Question

### Example Query: "What are the top support categories?"

#### Step 1: User Input → Agent
```
You: "What are the top support categories?"
```

#### Step 2: Agent Reasoning (LLM thinks)
```
Agent (Gemini 2.5 Flash model):
"The user wants category information. Let me check my available tools:
- fetch_tickets ❌ (too granular, returns all rows)
- get_category_summary ✅ (perfect! returns aggregated category stats)
- get_agent_performance ❌ (not relevant)

I should call get_category_summary()"
```

#### Step 3: Tool Execution (Python code runs)
```python
# Google ADK calls your function:
result = get_category_summary(top_n=20)

# Your Python code executes:
1. Opens Support_Metrics.csv
2. Reads 23,000+ rows with pandas
3. Groups by 'Main category'
4. Calculates:
   - Total tickets per category
   - SLA breaches per category
   - Average resolution time
5. Sorts by ticket count
6. Returns top 20 categories

# Returns structured data:
{
  "status": "success",
  "summary": [
    {"Category": "Bug", "Total Tickets": 18949, "SLA Breaches": 9090, ...},
    {"Category": "Duplicate", "Total Tickets": 1210, "SLA Breaches": 82, ...},
    ...
  ]
}
```

#### Step 4: Agent Receives Tool Result
```
Agent receives: Dictionary with 20 categories and their stats
```

#### Step 5: Agent Formats Response (LLM presents)
```
Agent (Gemini):
"Now I have the data. Let me present it clearly to the user:
- Show top categories
- Highlight important insights (high SLA breaches)
- Calculate percentages
- Make it actionable"
```

#### Step 6: User Sees Final Answer
```
Agent responds:

"Based on analysis of 23,000+ support tickets, here are the top categories:

📊 Top Support Categories:

1. **Bug** - 18,949 tickets
   - SLA Breaches: 9,090 (48.0%)
   - Avg Resolution: 774.1 minutes (~13 hours)

2. **Duplicate** - 1,210 tickets
   - SLA Breaches: 82 (6.8%)
   - Avg Resolution: 5,549 minutes (~92 hours)

3. **New Use Case** - 896 tickets
   - SLA Breaches: 550 (61.4%)
   - Avg Resolution: 1,225 minutes (~20 hours)

⚠️ Areas of Concern:
- Config category has 92.4% SLA breach rate
- Proofing category has 94.2% SLA breach rate

Would you like me to analyze why certain categories have high breach rates?"
```

---

## The Key Difference: Tool-Calling vs Regular Chat

### Regular ChatGPT Conversation
```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ "What are top categories?"
       ▼
┌─────────────┐
│   ChatGPT   │ ❌ "I don't have access to your data"
└─────────────┘
```

### Your Tool-Calling Agent
```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ "What are top categories?"
       ▼
┌─────────────────────────────────────┐
│         Gemini Agent (LLM)          │
│  "I need to call a tool for this"   │
└──────┬──────────────────────────────┘
       │ Decides to call get_category_summary()
       ▼
┌─────────────────────────────────────┐
│      Google ADK Framework           │
│   Executes: get_category_summary()  │
└──────┬──────────────────────────────┘
       │ Function call
       ▼
┌─────────────────────────────────────┐
│    Your Python Code (db_tools.py)   │
│  1. Read CSV file                   │
│  2. Process with pandas             │
│  3. Calculate statistics            │
│  4. Return structured data          │
└──────┬──────────────────────────────┘
       │ Returns: {"summary": [...]}
       ▼
┌─────────────────────────────────────┐
│         Gemini Agent (LLM)          │
│  Receives data, formats response    │
└──────┬──────────────────────────────┘
       │ Natural language summary
       ▼
┌─────────────┐
│    User     │ Sees: "Based on 23,000 tickets..."
└─────────────┘
```

---

## Why This is Powerful

### 1. **Real Data Access**
- ✅ Your agent can read files, query databases, call APIs
- ✅ Works with datasets too large for chat context (23,000+ rows)
- ✅ Always uses latest data (no manual copy-paste)

### 2. **Accurate Calculations**
- ✅ Python does the math (not LLM estimation)
- ✅ Pandas aggregations are precise
- ✅ No hallucination of numbers

### 3. **Autonomous Decision Making**
The agent **decides on its own**:
- Which tool to call
- What parameters to pass
- When to call multiple tools
- How to combine results

Example:
```
User: "Compare Bug vs Offline performance"

Agent thinks:
1. I need data for both categories
2. I'll call get_category_summary() to get all categories
3. Filter for Bug and Offline from the results
4. Compare their metrics
5. Present insights
```

### 4. **Dynamic & Interactive**
```
User: "Show top categories"
Agent: [calls get_category_summary()] "Here are top 10..."

User: "Show me top 5 instead"
Agent: [calls get_category_summary(top_n=5)] "Here are top 5..."

User: "What about just Bug tickets from last 30 days?"
Agent: [calls fetch_tickets(days=30, category="Bug")] "Found 1,240 tickets..."
```

---

## How the Agent "Knows" What to Do

### Your Instruction Template (in agent.py)
```python
instruction=(
    "You are a support analytics expert with access to tools..."
    "Available Tools:"
    "1. fetch_tickets - Retrieve raw ticket data"
    "2. get_category_summary - Get aggregated statistics"
    "3. get_agent_performance - Analyze agent metrics"

    "Guidelines:"
    "- Always use the appropriate tool to fetch data before analyzing"
    "- Provide specific numbers, percentages"
    "- Highlight problem areas"
    ...
)
```

This instruction gives the LLM:
- **Context**: What its role is
- **Capabilities**: What tools it has
- **Guidelines**: How to use them
- **Examples**: What good responses look like

### Tool Descriptions
```python
def get_category_summary(top_n: int = 20) -> dict:
    """
    Get a summary of tickets grouped by Main category.

    Args:
        top_n: Number of top categories to return (default: 20)

    Returns:
        Dictionary with category breakdown including ticket counts,
        SLA breaches, and average resolution times.
    """
```

The LLM reads:
- Function name: `get_category_summary`
- Parameters: `top_n` (optional, default 20)
- Docstring: What it does and returns
- Return type: `dict`

Then decides: "This function gives me category stats. Perfect for the user's question!"

---

## Real-World Example Flow

### Complex Query: "Which agents are struggling with SLA compliance?"

**Step 1:** Agent analyzes the question
```
Keywords detected: "agents", "struggling", "SLA compliance"
→ This needs agent performance data with SLA metrics
→ Tool: get_agent_performance()
```

**Step 2:** Calls Python function
```python
result = get_agent_performance()
# Returns agent stats with SLA compliance %
```

**Step 3:** Agent processes results
```
Agent sees:
- Sreeman: 32.2% SLA compliance (struggling!)
- Alexraj: 39.9% SLA compliance (below average)
- Sathish: 49.4% SLA compliance (borderline)
```

**Step 4:** Agent responds with insights
```
"Based on performance data:

🔴 Agents Struggling with SLA:

1. Sreeman - 32.2% compliance
   - Resolved 2,256 tickets
   - Avg time: 1,177 minutes (slowest)
   - Recommendation: Review workload and ticket complexity

2. Alexraj - 39.9% compliance
   - Resolved 3,123 tickets (highest volume!)
   - Avg time: 895 minutes
   - Recommendation: May be overloaded, consider redistribution

💡 Insight: These agents handle high volumes but need support
to improve resolution times."
```

---

## What Makes This "Agentic"

### Traditional Approach (Manual)
```
1. You: Open Excel
2. You: Filter data
3. You: Create pivot table
4. You: Calculate percentages
5. You: Make charts
6. You: Write summary
⏱️ Time: 30+ minutes
```

### Your Agent (Autonomous)
```
1. You: Ask question
2. Agent: Decides what to do
3. Agent: Executes tools
4. Agent: Analyzes results
5. Agent: Presents insights
⏱️ Time: 5 seconds
```

The agent is **autonomous** because:
- ✅ Makes its own decisions
- ✅ Chooses appropriate tools
- ✅ Handles errors gracefully
- ✅ Combines multiple data sources
- ✅ Adapts to different questions

---

## Under the Hood: Google ADK Framework

```python
# When you run: adk web

1. ADK loads your agent.py
2. Finds root_agent = Agent(...)
3. Wraps your tools in FunctionTool objects
4. Sends tool schemas to Gemini API
5. Starts web server
6. Waits for user input

# When user asks a question:

1. User message → ADK → Gemini API
2. Gemini decides: "I need to call get_category_summary"
3. Gemini returns: function_call request
4. ADK intercepts and executes your Python function
5. Python returns data
6. ADK sends data back to Gemini
7. Gemini formats natural language response
8. ADK shows response in web UI
```

---

## The Power of This Pattern

### You Can Add More Tools!

Want weather data in reports?
```python
def get_weather_impact(date_range: str) -> dict:
    """Check if weather affected support volume"""
    # Call weather API
    # Correlate with ticket dates
    return weather_correlation

root_agent = Agent(
    tools=[fetch_tickets, get_category_summary,
           get_agent_performance, get_weather_impact]  # ← New tool!
)
```

Want to create tickets?
```python
def create_ticket(title: str, category: str, priority: str) -> dict:
    """Create a new support ticket"""
    # Call your ticketing API
    return {"ticket_id": "12345", "status": "created"}
```

Want email alerts?
```python
def send_sla_alert(category: str, breach_rate: float) -> dict:
    """Send alert if SLA breaches exceed threshold"""
    if breach_rate > 0.5:
        # Send email to ops team
        return {"alert_sent": True}
```

The agent automatically learns to use new tools based on their docstrings!

---

## Summary: ChatGPT vs Your Agent

| Feature | ChatGPT | Your Support Agent |
|---------|---------|-------------------|
| Data Access | ❌ None | ✅ Full CSV access |
| Real Calculations | ❌ Estimates | ✅ Accurate (Python/pandas) |
| Large Datasets | ❌ Limited by context | ✅ Handles 23,000+ rows |
| Tool Usage | ❌ No tools | ✅ 3 custom tools |
| Autonomy | ❌ Passive | ✅ Active decision making |
| Custom Logic | ❌ Generic | ✅ Your business logic |
| Real-time Data | ❌ Static | ✅ Always current |
| Extensibility | ❌ Fixed | ✅ Add unlimited tools |

---

## Key Takeaway

**Your agent didn't just "respond to a prompt"** - it:

1. **Understood** your intent
2. **Decided** which tool to use
3. **Executed** Python code to analyze 23,000+ tickets
4. **Processed** real data with pandas
5. **Calculated** precise statistics
6. **Synthesized** insights
7. **Presented** results in natural language

This is **agentic AI** - the model acts as an autonomous agent that can use tools to accomplish tasks, not just generate text!
