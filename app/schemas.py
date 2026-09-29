from typing import Optional
from pydantic import BaseModel, Field, field_validator


class PlannerRequest(BaseModel):
    planner: str
    budget: float = Field(gt=0)
    details: dict = {}

    @field_validator("planner")
    @classmethod
    def valid_planner(cls, value):
        allowed = {"home", "party", "jewelry"}
        if value not in allowed:
            raise ValueError("planner must be home, party, or jewelry")
        return value


class RecommendationItem(BaseModel):
    category: str
    suggestion: str
    estimated_price: str
    platform: str
    reason: str


class PlannerResponse(BaseModel):
    planner: str
    budget: float
    allocation: dict
    recommendations: list[RecommendationItem]
    tips: list[str]
    mode: str
