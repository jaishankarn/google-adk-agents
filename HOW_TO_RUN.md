# How to Run the Support Ticket Insights Agent

## ✅ Correct Setup

Your agent is properly configured at:
```
my_agent/
└── agents/
    └── support_agent/
        ├── agent.py (contains root_agent) ✅
        ├── tools/
        │   └── db_tools.py
        └── Support_Metrics.csv
```

## 🚀 Running the Agent

### Step 1: Navigate to PROJECT ROOT
```bash
cd /Users/jaishankar/Documents/stuffs/my_agent
```

**IMPORTANT:** You must run `adk web` from the `my_agent` directory (the project root), NOT from inside `support_agent`!

### Step 2: Start ADK Web Interface
```bash
adk web
```

### Step 3: Access the Agent
- Your browser will open automatically (usually `http://localhost:8000`)
- You should see "support_agent" in the list of available agents
- Click on it to start chatting!

## ❌ Common Mistakes

### Wrong: Running from inside support_agent folder
```bash
cd /Users/jaishankar/Documents/stuffs/my_agent/support_agent  # ❌ WRONG
adk web  # Won't find the agent correctly
```

### Right: Running from project root
```bash
cd /Users/jaishankar/Documents/stuffs/my_agent  # ✅ CORRECT
adk web
```

## 🧪 Testing the Agent Manually

To verify the agent works before running adk web:
```bash
cd /Users/jaishankar/Documents/stuffs/my_agent/agents/support_agent
python3 agent.py
```

You should see:
```
Support Ticket Insights Agent initialized successfully!
Agent name: ticket_insights_agent
Number of tools: 3

Available tools:
  - fetch_tickets
  - get_category_summary
  - get_agent_performance
```

## 🔍 Troubleshooting

### Error: "No module named 'tools'"
**Solution:** Make sure you're running `adk web` from `/Users/jaishankar/Documents/stuffs/my_agent`, not from a subfolder.

### Error: "Default value None of parameter... is not compatible"
**Solution:** This was fixed by using `Optional[str]` type hints instead of `str = None`. The fix is already applied.

### Agent doesn't appear in the list
**Solution:**
1. Verify folder structure: `agents/support_agent/agent.py` exists
2. Verify `agent.py` contains `root_agent` variable
3. Check there are no syntax errors: `python3 agents/support_agent/agent.py`

### CSV file not found
**Solution:** Ensure `Support_Metrics.csv` is in the same directory as `agent.py`:
```bash
ls agents/support_agent/Support_Metrics.csv
```

## 📝 Example Queries

Once the agent is running, try:
- "Which category has the most tickets?"
- "Show me SLA performance by category"
- "What are the top 5 performing agents?"
- "What's the average resolution time for Bug tickets?"

## 🗂️ Note About Duplicate Folders

You currently have TWO support_agent folders:
1. `my_agent/agents/support_agent/` ✅ (Used by ADK)
2. `my_agent/support_agent/` ⚠️ (Old location, can be deleted)

The ADK only uses the one in `agents/` directory. You can safely delete the old one if you want.
