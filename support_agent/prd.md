# 🧠 Support Ticket Insights Agent — PRD

## 📘 Overview

The **Support Ticket Insights Agent** is an AI-powered reporting and analytics agent built using **Google Agent Development Kit (ADK)**.
It connects to the company’s **support ticket database**, analyzes ticket patterns, identifies recurring issues, SLA breaches, and category trends, and generates **human-readable insights and reports** on demand.

This agent is designed to assist **Support Operations**, **Engineering**, and **Customer Success** teams in understanding problem areas, improving response efficiency, and making data-driven decisions.

---

## 🌟 Objectives

| Goal                             | Description                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------- |
| **Data-driven insights**         | Identify categories with the most tickets, SLAs breached, and recurring issues. |
| **Common issue detection**       | Summarize user complaints and detect common patterns in support text.           |
| **Performance monitoring**       | Highlight which areas have the highest SLA violations or resolution delays.     |
| **Automated reporting**          | Generate summaries, tables, or charts on demand or via scheduled triggers.      |
| **Natural language interaction** | Allow non-technical users to query insights in plain English (via ADK UI).      |

---

## 🧩 Use Cases

| # | Use Case                              | Example Query                                                                 |
| - | ------------------------------------- | ----------------------------------------------------------------------------- |
| 1 | **Category trend analysis**           | “Which category has the most tickets this month?”                             |
| 2 | **SLA compliance check**              | “Show categories with the most SLA breaches.”                                 |
| 3 | **User sentiment / recurring issues** | “What are users complaining about in Login issues?”                           |
| 4 | **Monthly summary report**            | “Generate a summary report of ticket volume by category and SLA performance.” |
| 5 | **Comparative analysis**              | “Compare billing vs authentication issue trends for the last 90 days.”        |

---

## 🧱 System Architecture

```
User Query
    ↓
Google ADK (Ticket Insights Agent)
    ↓
Database Tool (fetch_tickets)
    ↓
Support Ticket Database (Postgres / MySQL / BigQuery)
    ↓
Data Returned (rows)
    ↓
LLM Processing + Analysis (via Gemini model)
    ↓
Aggregated Insights + Summaries
    ↓
Response / Report / Visualization
```

---

## 🛠️ Components

### 1. **Agent**

**File:** `agents/ticket_insights_agent.py`

Responsible for:

* Reasoning about data
* Determining what tools to call
* Summarizing results in human-readable format

```python
from google.adk.agents.llm_agent import Agent
from google.adk.tools import Tool
from tools.db_tools import fetch_tickets

fetch_tool = Tool(
    function=fetch_tickets,
    name="fetch_tickets",
    description="Fetch support tickets including category, message, and SLA status."
)

ticket_insights_agent = Agent(
    model="gemini-2.5-flash",
    name="ticket_insights_agent",
    description="Analyzes support tickets and provides insights on issues, categories, and SLAs.",
    instruction=(
        "Fetch ticket data using available tools, analyze trends by category and SLA, "
        "detect recurring issues, and summarize findings clearly. "
        "Provide actionable insights rather than raw data."
    ),
    tools=[fetch_tool]
)
```

---

### 2. **Tool**

**File:** `tools/db_tools.py`

Fetches data from the support database.

```python
import psycopg2
import yaml
import os

def load_database_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'database.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def fetch_tickets():
    """
    Fetch support tickets from the database.
    Connects to the configured database service and retrieves ticket data.
    """
    config = load_database_config()
    conn = psycopg2.connect(**config['database'])

    cur = conn.cursor()
    cur.execute("""
        SELECT id, category, message, sla_status, created_at, resolved_at
        FROM support_tickets
        WHERE created_at >= NOW() - INTERVAL '90 days';
    """)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return {"columns": columns, "rows": rows}
```

---

### 3. **Database**

* Source of truth for all support ticket data.
* Should include columns:

  * `id`
  * `category`
  * `message`
  * `sla_status`
  * `created_at`
  * `resolved_at`

---

### 4. **Optional Reporting Tools**

**File:** `tools/report_tools.py`

* For chart or CSV export.
* Functions:

  * `generate_category_chart(data)`
  * `generate_sla_summary(data)`
  * `export_csv(report_data)`

---

## ⚙️ Features & Functionality

| Feature                   | Description                       | Status       |
| ------------------------- | --------------------------------- | ------------ |
| Fetch all support tickets | Pulls latest ticket data          | ✅            |
| Category-wise analysis    | Groups and summarizes by category | ✅            |
| SLA performance report    | Tracks SLA compliance             | ✅            |
| Common issue detection    | Identifies repeated themes        | ✅            |
| Export / visualization    | Create CSV or charts              | ⏳ (optional) |
| Scheduled reports         | Generate periodic insights        | ⏳ (optional) |

---

## 💬 Example Prompts

| Prompt                                                           | Example Response                                                                      |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| “Show me which category has the most tickets in the last month.” | *Login Issues (42%) had the highest volume with common complaint “OTP not received”.* |
| “What are the top 3 common problems users are reporting?”        | *OTP failures, password reset delays, payment verification errors.*                   |
| “Summarize SLA performance for each category.”                   | *Billing – 28% breaches, Login – 12%, General – 5%.*                                  |
| “Generate a report comparing Billing vs Technical Support.”      | *Billing tickets doubled last month, while Technical remained stable.*                |

---

## 🔐 Security & Governance

| Area                | Consideration                                                    |
| ------------------- | ---------------------------------------------------------------- |
| **Database Access** | Use read-only credentials for analytics.                         |
| **PII Handling**    | Mask sensitive fields (e.g., names, emails).                     |
| **Model Safety**    | Restrict tool access; prevent unsafe SQL generation.             |
| **Data Volume**     | Limit to recent data or batch summaries to control context size. |

---

## 🚀 Future Enhancements

| Feature                     | Description                                       |
| --------------------------- | ------------------------------------------------- |
| **Sentiment Analysis**      | Add NLP model to analyze tone of ticket messages. |
| **Multi-agent workflow**    | Split into “Fetcher Agent” + “Analyzer Agent”.    |
| **Scheduled Reporting**     | Auto-generate daily or weekly email reports.      |
| **Visualization Dashboard** | Integrate with Streamlit or Google Looker Studio. |
| **RAG Integration**         | Use previous resolutions for better insights.     |

---

## 🦯 Success Metrics

| Metric                            | Target                                 |
| --------------------------------- | -------------------------------------- |
| Report generation time            | < 5 seconds                            |
| Accuracy of insights              | > 90% correct summaries                |
| User adoption                     | Used weekly by support/ops             |
| Reduction in manual analysis time | 60%+ faster than spreadsheet workflows |

---

## 🧱 Folder Structure

```
support-insights-agent/
│
├── agents/
│   └── ticket_insights_agent.py
│
├── tools/
│   ├── db_tools.py
│   └── report_tools.py
│
├── config/
│   └── database.yaml
│
├── requirements.txt
└── PRD.md
```

---

## ⚡ Setup & Run

```bash
# 1. Install dependencies
pip install google-adk psycopg2 pandas

# 2. Configure database connection
# Update config/database.yaml with your database credentials

# 3. Run locally
adk web

# 4. Interact in browser
> "Summarize tickets by category and SLA performance"
```

---

## 🧠 Summary

**Purpose:**
Provide automated, AI-driven insights on support ticket trends and SLA performance using Google ADK.

**Outcome:**
A natural-language reporting assistant for your support data — helping reduce analysis effort, surface recurring problems, and generate actionable insights instantly.
