from pydantic import BaseModel, Field, validator
from typing import List

class Feedback(BaseModel):
    skill_gaps: List[str] = Field(default_factory=list)
    formatting: List[str] = Field(default_factory=list)
    ats_keywords: List[str] = Field(default_factory=list)

class ResumeAnalysis(BaseModel):
    skills: str = Field(..., description="Comma-separated list of skills")
    experience: str = Field(..., description="Experience in years, e.g., '2.0 years'")
    education: str = Field(..., description="Comma-separated education details")
    rating: float = Field(..., ge=0, le=100, description="Rating from 0 to 100")
    recommendations: str = Field(..., description="Recommendations for improvement")
    feedback: Feedback = Field(..., description="Detailed feedback")

    @validator('experience')
    def validate_experience(cls, value):
        if not value.endswith('years') or not any(char.isdigit() for char in value):
            raise ValueError("Experience must be in format 'X.Y years'")
        return value

    @validator('skills')
    def validate_skills(cls, value):
        if not value or len(value.split(', ')) < 1:
            raise ValueError("Skills must be a non-empty comma-separated list")
        return value

    @validator('rating')
    def validate_rating(cls, value):
        if value < 0 or value > 100:
            raise ValueError("Rating must be between 0 and 100")
        return value