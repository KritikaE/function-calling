from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import re, json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

@app.get("/execute")
def execute(q: Optional[str] = None):
    if not q:
        return {"error": "No query provided. Use ?q=your question"}

    # Ticket status
    m = re.search(r"ticket\s+(\d+)", q, re.IGNORECASE)
    if m:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": int(m.group(1))})
        }

    # Schedule meeting — capture date, time, and room name (strip trailing punctuation)
    m = re.search(r"(\d{4}-\d{2}-\d{2}).*?(\d{2}:\d{2}).*?(Room\s+[\w\s]+?)[\.\,]?\s*$", q, re.IGNORECASE)
    if m:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": m.group(1),
                "time": m.group(2),
                "meeting_room": m.group(3).strip()
            })
        }

    # Expense balance
    m = re.search(r"expense balance.*?employee\s+(\d+)", q, re.IGNORECASE)
    if m:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": int(m.group(1))})
        }

    # Performance bonus
    m = re.search(r"bonus.*?employee\s+(\d+).*?(\d{4})", q, re.IGNORECASE)
    if m:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(m.group(1)),
                "current_year": int(m.group(2))
            })
        }

    # Office issue
    m = re.search(r"issue\s+(\d+).*?(?:the\s+)?(\w+)\s+department", q, re.IGNORECASE)
    if m:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(m.group(1)),
                "department": m.group(2)
            })
        }

    return {"error": "No matching function found"}
