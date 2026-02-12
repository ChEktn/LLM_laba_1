from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LiteratureRequest(BaseModel):
    topic: str = Field(..., description="Research topic")
    year_from: Optional[int] = Field(None, description="Start year filter")
    year_to: Optional[int] = Field(None, description="End year filter")


class PlannerOutput(BaseModel):
    topic: str
    year_from: Optional[int]
    year_to: Optional[int]
    need_trend_analysis: bool
    need_author_analysis: bool


class Paper(BaseModel):
    title: str
    abstract: str
    authors: List[str]
    year: int


class TrendSummary(BaseModel):
    trend: str
    explanation: str


class AuthorStats(BaseModel):
    author: str
    paper_count: int


class LiteratureReview(BaseModel):
    key_papers: List[str]
    main_trends: List[str]
    top_authors: List[str]
    open_questions: List[str]


class ReviewFeedback(BaseModel):
    improved_review: LiteratureReview
    comments: List[str]


class GraphState(BaseModel):
    user_request: LiteratureRequest
    plan: Optional[PlannerOutput] = None
    papers: Optional[List[Paper]] = None
    trends: Optional[List[TrendSummary]] = None
    authors: Optional[List[AuthorStats]] = None
    final_answer: Optional[LiteratureReview] = None
    reviewed_answer: Optional[LiteratureReview] = None