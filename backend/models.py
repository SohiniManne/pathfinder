"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class StudentProfile(BaseModel):
    """Student profile input"""
    skills: List[str] = Field(..., min_items=1, description="List of student's skills")
    interests: List[str] = Field(default=[], description="Areas of interest")
    education_level: str = Field(..., description="Current education level")
    gpa: Optional[float] = Field(default=None, ge=0.0, le=4.0, description="GPA score")
    experience_years: Optional[int] = Field(default=0, ge=0, description="Years of experience")

class CareerRecommendation(BaseModel):
    """Career recommendation output"""
    career: str = Field(..., description="Career title")
    match_score: float = Field(..., ge=0, le=100, description="Match percentage")
    matching_skills: List[str] = Field(default=[], description="Skills that match")
    skills_to_learn: List[str] = Field(default=[], description="Skills needed")
    description: str = Field(..., description="Career description")
    salary_info: str = Field(..., description="Salary information")
    growth_outlook: str = Field(..., description="Job growth outlook")

class ResumeParseResponse(BaseModel):
    """Resume parsing response"""
    status: str = Field(..., description="Success or error status")
    message: Optional[str] = Field(default=None, description="Error message if any")
    extracted_skills: List[str] = Field(default=[], description="Extracted skills")
    education: List[str] = Field(default=[], description="Education information")
    experience_years: int = Field(default=0, description="Estimated years of experience")
    text_length: Optional[int] = Field(default=None, description="Length of extracted text")
    text_preview: Optional[str] = Field(default=None, description="Preview of extracted text")

class SkillsGapAnalysis(BaseModel):
    """Skills gap analysis output"""
    target_career: str
    current_skills: List[str]
    required_skills: List[str]
    missing_skills: List[str]
    extra_skills: List[str]
    completion_percentage: float
    priority_skills: List[str] = Field(default=[], description="Top priority skills to learn")

class LearningResource(BaseModel):
    """Learning resource recommendation"""
    skill: str
    resources: List[dict]
    estimated_time_weeks: int
    difficulty: str  # Beginner, Intermediate, Advanced