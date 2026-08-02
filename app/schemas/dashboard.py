from pydantic import BaseModel

class StatusBreakdown(BaseModel):
    status: str
    count: int

class PriorityBreakdown(BaseModel):
    priority: str
    count: int

class DashboardSummary(BaseModel):
    total_tickets: int
    status_breakdown: list[StatusBreakdown]
    priority_breakdown: list[PriorityBreakdown]
