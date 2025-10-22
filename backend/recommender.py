"""
Career recommendation engine using ML algorithms
"""
import numpy as np
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from backend.database import CAREER_DATABASE
from backend.models import CareerRecommendation, StudentProfile

class CareerRecommender:
    """
    Recommendation engine that uses multiple algorithms:
    1. Skill matching (exact + partial)
    2. Interest alignment
    3. Experience level matching
    """
    
    def __init__(self):
        self.career_db = CAREER_DATABASE
    
    def calculate_skill_match_score(
        self, 
        user_skills: List[str], 
        career_skills: List[str],
        nice_to_have: List[str] = []
    ) -> float:
        """
        Calculate skill match percentage with weighted scoring
        Required skills: 70% weight
        Nice-to-have skills: 30% weight
        """
        if not career_skills:
            return 0.0
        
        user_skills_lower = {s.lower() for s in user_skills}
        required_lower = {s.lower() for s in career_skills}
        nice_lower = {s.lower() for s in nice_to_have}
        
        # Required skills matching
        required_matches = len(user_skills_lower & required_lower)
        required_score = (required_matches / len(required_lower)) * 70
        
        # Nice-to-have skills matching
        if nice_to_have:
            nice_matches = len(user_skills_lower & nice_lower)
            nice_score = (nice_matches / len(nice_lower)) * 30
        else:
            nice_score = 0
        
        total_score = required_score + nice_score
        return round(total_score, 2)
    
    def calculate_interest_boost(
        self, 
        interests: List[str], 
        career_name: str,
        career_details: Dict
    ) -> float:
        """
        Boost score if user's interests align with career
        """
        if not interests:
            return 0
        
        boost = 0
        interests_lower = [i.lower() for i in interests]
        career_lower = career_name.lower()
        
        # Check if interest matches career name or industry
        for interest in interests_lower:
            if interest in career_lower:
                boost += 5
            
            # Check industry match
            if 'industry' in career_details:
                for industry in career_details['industry']:
                    if interest in industry.lower():
                        boost += 3
        
        return min(boost, 10)  # Cap at 10% boost
    
    def calculate_experience_match(
        self,
        user_experience: int,
        career_details: Dict
    ) -> float:
        """
        Adjust score based on experience level
        """
        # This is a simplified version
        # In production, you'd have experience requirements per career
        if user_experience == 0:
            return 0
        elif user_experience < 2:
            return 2
        elif user_experience < 5:
            return 5
        else:
            return 8
    
    def recommend_careers(
        self, 
        profile: StudentProfile,
        top_n: int = 10
    ) -> List[CareerRecommendation]:
        """
        Generate personalized career recommendations
        """
        recommendations = []
        
        for career, details in self.career_db.items():
            # Base skill matching
            skill_score = self.calculate_skill_match_score(
                profile.skills,
                details['required_skills'],
                details['nice_to_have']
            )
            
            # Interest boost
            interest_boost = self.calculate_interest_boost(
                profile.interests,
                career,
                details
            )
            
            # Experience match
            experience_boost = self.calculate_experience_match(
                profile.experience_years or 0,
                details
            )
            
            # Final score
            final_score = min(skill_score + interest_boost + experience_boost, 100)
            
            # Identify matching and missing skills
            user_skills_lower = {s.lower() for s in profile.skills}
            required_lower = {s.lower(): s for s in details['required_skills']}
            
            matching_skills = [
                required_lower[skill] 
                for skill in user_skills_lower 
                if skill in required_lower
            ]
            
            skills_to_learn = [
                skill 
                for skill in details['required_skills']
                if skill.lower() not in user_skills_lower
            ]
            
            # Create recommendation
            recommendations.append(
                CareerRecommendation(
                    career=career,
                    match_score=final_score,
                    matching_skills=matching_skills,
                    skills_to_learn=skills_to_learn[:5],  # Top 5 priority skills
                    description=details['description'],
                    salary_info=details['avg_salary'],
                    growth_outlook=details['growth_outlook']
                )
            )
        
        # Sort by match score
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        
        return recommendations[:top_n]
    
    def analyze_skills_gap(
        self,
        profile: StudentProfile,
        target_career: str
    ) -> Dict:
        """
        Detailed skills gap analysis for a target career
        """
        if target_career not in self.career_db:
            return {"error": "Career not found"}
        
        career_details = self.career_db[target_career]
        user_skills_lower = {s.lower() for s in profile.skills}
        
        required_skills = career_details['required_skills']
        nice_to_have = career_details['nice_to_have']
        
        # Categorize skills
        required_lower = {s.lower(): s for s in required_skills}
        nice_lower = {s.lower(): s for s in nice_to_have}
        
        missing_required = [
            required_lower[skill]
            for skill in required_lower
            if skill not in user_skills_lower
        ]
        
        missing_nice = [
            nice_lower[skill]
            for skill in nice_lower
            if skill not in user_skills_lower
        ]
        
        matching_required = [
            required_lower[skill]
            for skill in user_skills_lower
            if skill in required_lower
        ]
        
        matching_nice = [
            nice_lower[skill]
            for skill in user_skills_lower
            if skill in nice_lower
        ]
        
        # Calculate completion percentage
        completion = (len(matching_required) / len(required_skills) * 100) if required_skills else 0
        
        # Priority ranking (missing required skills are highest priority)
        priority_skills = missing_required[:3] + missing_nice[:2]
        
        return {
            "target_career": target_career,
            "current_skills": profile.skills,
            "required_skills": required_skills,
            "nice_to_have": nice_to_have,
            "missing_required": missing_required,
            "missing_nice": missing_nice,
            "matching_required": matching_required,
            "matching_nice": matching_nice,
            "completion_percentage": round(completion, 2),
            "priority_skills": priority_skills
        }
    
    def get_learning_path(
        self,
        profile: StudentProfile,
        target_career: str
    ) -> List[Dict]:
        """
        Generate a structured learning path with timeline
        """
        gap_analysis = self.analyze_skills_gap(profile, target_career)
        
        if "error" in gap_analysis:
            return []
        
        learning_path = []
        
        # Estimate learning time for each skill (in weeks)
        skill_time_estimates = {
            "beginner": 8,
            "intermediate": 12,
            "advanced": 16
        }
        
        # Create learning modules
        for idx, skill in enumerate(gap_analysis['priority_skills'], 1):
            # Simplified difficulty estimation
            difficulty = "intermediate"
            if skill in ["Python", "JavaScript", "HTML", "CSS", "Git"]:
                difficulty = "beginner"
            elif skill in ["Machine Learning", "Deep Learning", "System Design"]:
                difficulty = "advanced"
            
            learning_path.append({
                "order": idx,
                "skill": skill,
                "difficulty": difficulty,
                "estimated_weeks": skill_time_estimates[difficulty],
                "resources": self._get_learning_resources(skill)
            })
        
        return learning_path
    
    def _get_learning_resources(self, skill: str) -> List[Dict]:
        """
        Get learning resources for a skill
        In production, this would query a real database
        """
        resources = [
            {
                "type": "Course",
                "name": f"{skill} Complete Course",
                "platform": "Coursera",
                "url": f"https://www.coursera.org/search?query={skill.replace(' ', '%20')}"
            },
            {
                "type": "Documentation",
                "name": f"Official {skill} Docs",
                "platform": "Official Website",
                "url": "#"
            },
            {
                "type": "Practice",
                "name": f"{skill} Exercises",
                "platform": "LeetCode/HackerRank",
                "url": "https://leetcode.com"
            }
        ]
        
        return resources