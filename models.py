from typing import List, Optional
from pydantic import BaseModel, Field

class ResearchPaper(BaseModel):
    title: str
    authors: List[str]
    url: str
    year: Optional[int]
    key_points: List[str] = Field(description="Main findings")
    limitations: List[str] = Field(description="Research gaps")
    bibtex: Optional[str] = None