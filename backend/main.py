"""
Main FastAPI application - AI Career Mentor Backend
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from backend.models import (
    StudentProfile, 
    CareerRecommendation, 
    ResumeParseResponse
)
from backend.parser import ResumeParser
from backend.recommender import CareerRecommender
from backend.database import get_all_careers, get_career_details

# Initialize FastAPI app
app = FastAPI(
    title="AI Career Mentor API",
    description="AI-powered career guidance system for students",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommender
recommender = CareerRecommender()

@app.get("/")
def root():
    """API health check"""
    return {
        "message": "AI Career Mentor API - Ready to guide your career journey!",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "parse_resume": "/parse-resume",
            "recommend": "/recommend-careers",
            "careers": "/careers"
        }
    }

@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "careers_loaded": len(get_all_careers()),
        "api_version": "1.0.0"
    }

@app.post("/parse-resume", response_model=ResumeParseResponse)
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse uploaded resume and extract information
    
    - **file**: PDF resume file (max 200MB)
    
    Returns extracted skills, education, and experience
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Read file
        contents = await file.read()
        
        # Parse resume
        result = ResumeParser.parse_full_resume(contents)
        
        if not result.get("success"):
            return ResumeParseResponse(
                status="error",
                message=result.get("error", "Could not parse resume")
            )
        
        return ResumeParseResponse(
            status="success",
            extracted_skills=result['skills'],
            education=result['education'],
            experience_years=result['experience_years'],
            text_length=result['text_length'],
            text_preview=result['text_preview']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return ResumeParseResponse(
            status="error",
            message=f"Error processing resume: {str(e)}"
        )

@app.post("/recommend-careers", response_model=List[CareerRecommendation])
def recommend_careers(profile: StudentProfile):
    """
    Get personalized career recommendations
    
    - **profile**: Student profile with skills, interests, education
    
    Returns list of career recommendations sorted by match score
    """
    try:
        recommendations = recommender.recommend_careers(profile)
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )

@app.post("/skills-gap-analysis")
def analyze_skills_gap(profile: StudentProfile, target_career: str):
    """
    Analyze skills gap for a target career
    
    - **profile**: Student profile
    - **target_career**: Name of target career
    
    Returns detailed gap analysis with missing and matching skills
    """
    try:
        analysis = recommender.analyze_skills_gap(profile, target_career)
        
        if "error" in analysis:
            raise HTTPException(status_code=404, detail=analysis["error"])
        
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing skills gap: {str(e)}"
        )

@app.post("/learning-path")
def get_learning_path(profile: StudentProfile, target_career: str):
    """
    Generate structured learning path for target career
    
    - **profile**: Student profile
    - **target_career**: Name of target career
    
    Returns ordered list of skills to learn with resources and timeline
    """
    try:
        path = recommender.get_learning_path(profile, target_career)
        
        if not path:
            raise HTTPException(
                status_code=404,
                detail="Career not found or no learning path needed"
            )
        
        return {
            "target_career": target_career,
            "learning_path": path,
            "total_weeks": sum(item['estimated_weeks'] for item in path),
            "total_skills": len(path)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating learning path: {str(e)}"
        )

@app.get("/careers")
def list_careers():
    """Get list of all available careers"""
    return {
        "careers": get_all_careers(),
        "total": len(get_all_careers())
    }

@app.get("/careers/{career_name}")
def get_career_info(career_name: str):
    """
    Get detailed information about a specific career
    
    - **career_name**: Name of the career
    """
    details = get_career_details(career_name)
    
    if not details:
        raise HTTPException(
            status_code=404,
            detail=f"Career '{career_name}' not found"
        )
    
    return {
        "career": career_name,
        "details": details
    }

@app.post("/test-skill-extraction")
def test_skill_extraction(text: str):
    """
    Test skill extraction with sample text
    Useful for debugging
    """
    skills, skills_by_category = ResumeParser.extract_skills(text)
    
    return {
        "input_length": len(text),
        "skills_found": len(skills),
        "skills": skills,
        "skills_by_category": skills_by_category
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)