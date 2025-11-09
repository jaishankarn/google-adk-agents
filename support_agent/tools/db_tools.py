import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Optional

def fetch_tickets(days: int = 90, category: Optional[str] = None, sla_status: Optional[str] = None) -> dict:
    """
    Fetch support tickets from CSV file with optional filtering.

    Args:
        days: Number of days to look back from today (default: 90)
        category: Filter by Main category (optional, e.g., "Bug", "Offline", "Config")
        sla_status: Filter by Completed Type (optional, e.g., "within sla", "outside sla")

    Returns:
        A dictionary containing:
        - 'columns': List of column names
        - 'rows': List of rows (each row is a list of values)
        - 'count': Total number of tickets returned
        - 'summary': Brief summary of the data
    """
    try:
        # Get the CSV file path (relative to this file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, '..', 'Support_Metrics.csv')

        # Read CSV file
        df = pd.read_csv(csv_path)

        # Convert date columns to datetime
        df['Request Date'] = pd.to_datetime(df['Request Date'], errors='coerce')
        df['Resolution Date'] = pd.to_datetime(df['Resolution Date'], errors='coerce')

        # Filter by date range (last N days)
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            df = df[df['Request Date'] >= cutoff_date]

        # Filter by category if provided
        if category:
            df = df[df['Main category'].str.lower() == category.lower()]

        # Filter by SLA status if provided
        if sla_status:
            df = df[df['Completed Type'].str.lower() == sla_status.lower()]

        # Get columns and rows
        columns = df.columns.tolist()
        rows = df.values.tolist()

        # Create summary
        summary = f"Retrieved {len(rows)} tickets"
        if days:
            summary += f" from the last {days} days"
        if category:
            summary += f" in category '{category}'"
        if sla_status:
            summary += f" with SLA status '{sla_status}'"

        return {
            "status": "success",
            "columns": columns,
            "rows": rows,
            "count": len(rows),
            "summary": summary
        }

    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"CSV file not found at {csv_path}",
            "columns": [],
            "rows": [],
            "count": 0
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reading CSV: {str(e)}",
            "columns": [],
            "rows": [],
            "count": 0
        }


def get_category_summary(top_n: int = 20) -> dict:
    """
    Get a summary of tickets grouped by Main category.

    Args:
        top_n: Number of top categories to return (default: 20)

    Returns:
        Dictionary with category breakdown including count and SLA performance
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, '..', 'Support_Metrics.csv')

        df = pd.read_csv(csv_path)

        # Group by Main category
        category_summary = df.groupby('Main category').agg({
            'Req ID': 'count',
            'Completed Type': lambda x: (x == 'outside sla').sum(),
            'Time Taken in Minutes': 'mean'
        }).reset_index()

        category_summary.columns = ['Category', 'Total Tickets', 'SLA Breaches', 'Avg Resolution Time (min)']

        # Sort by ticket count and get top N
        category_summary = category_summary.sort_values('Total Tickets', ascending=False).head(top_n)

        return {
            "status": "success",
            "summary": category_summary.to_dict('records'),
            "total_categories": len(df['Main category'].unique())
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating summary: {str(e)}"
        }


def get_agent_performance() -> dict:
    """
    Get performance metrics for each support agent.

    Returns:
        Dictionary with agent performance data including tickets resolved and avg time
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, '..', 'Support_Metrics.csv')

        df = pd.read_csv(csv_path)

        # Filter out system/ghost entries
        df = df[~df['Agent name'].isin(['Ghost', 'UnAssigned', ''])]

        # Group by Agent name
        agent_summary = df.groupby('Agent name').agg({
            'Req ID': 'count',
            'Time Taken in Minutes': 'mean',
            'Completed Type': lambda x: (x == 'within sla').sum() / len(x) * 100
        }).reset_index()

        agent_summary.columns = ['Agent', 'Tickets Resolved', 'Avg Resolution Time (min)', 'SLA Compliance (%)']
        agent_summary = agent_summary.sort_values('Tickets Resolved', ascending=False)

        return {
            "status": "success",
            "summary": agent_summary.to_dict('records')
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating agent performance: {str(e)}"
        }
