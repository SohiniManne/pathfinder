"""
Resume parsing and information extraction
"""
import PyPDF2
import io
import re
from typing import List, Dict, Tuple

class ResumeParser:
    """Parse resume and extract key information"""
    
    # Comprehensive skills database organized by category
    SKILLS_DATABASE = {
        "programming": [
            "Python", "Java", "JavaScript", "C++", "C#", "C", "Ruby", "PHP", 
            "Swift", "Kotlin", "Go", "Rust", "TypeScript", "R", "MATLAB", 
            "Scala", "Perl", "Shell", "Bash", "Dart", "Objective-C"
        ],
        "web": [
            "HTML", "CSS", "React", "Angular", "Vue.js", "Vue", "Node.js", 
            "Express", "Django", "Flask", "FastAPI", "Spring", "ASP.NET", 
            "jQuery", "Bootstrap", "Tailwind", "Next.js", "Nuxt.js", "Redux",
            "Webpack", "Sass", "SCSS", "Less"
        ],
        "databases": [
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", 
            "Oracle", "SQLite", "MariaDB", "DynamoDB", "Firebase", 
            "Elasticsearch", "Neo4j", "CouchDB"
        ],
        "cloud_devops": [
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Git", 
            "GitHub", "GitLab", "CI/CD", "Terraform", "Ansible", "Linux", 
            "Unix", "Nginx", "Apache", "CloudFormation", "Heroku"
        ],
        "data_ml": [
            "Machine Learning", "Deep Learning", "Data Analysis", "Data Science",
            "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "Pandas", "NumPy",
            "Matplotlib", "Seaborn", "Jupyter", "NLP", "Computer Vision", "MLOps",
            "XGBoost", "LightGBM", "NLTK", "SpaCy", "OpenCV"
        ],
        "analytics": [
            "Statistics", "Probability", "Excel", "Power BI", "Tableau", "Plotly",
            "Data Visualization", "Business Intelligence", "Analytics", "Looker",
            "Google Analytics", "Qlik"
        ],
        "other": [
            "Algorithms", "Data Structures", "System Design", "API", "REST", 
            "GraphQL", "Microservices", "Agile", "Scrum", "Testing", "Debugging", 
            "OOP", "Functional Programming", "Design Patterns", "Security",
            "Blockchain", "IoT", "AR/VR"
        ]
    }
    
    @staticmethod
    def get_all_skills() -> List[str]:
        """Get flattened list of all skills"""
        all_skills = []
        for category in ResumeParser.SKILLS_DATABASE.values():
            all_skills.extend(category)
        return all_skills
    
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF with error handling"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    @staticmethod
    def extract_skills(text: str) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Extract skills using comprehensive keyword matching
        Returns: (all_skills, skills_by_category)
        """
        if not text:
            return [], {}
        
        text_lower = text.lower()
        found_skills = []
        skills_by_category = {}
        
        all_skills = ResumeParser.get_all_skills()
        
        for skill in all_skills:
            skill_lower = skill.lower()
            
            # Check for exact match with word boundaries
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
                
                # Categorize skill
                for category, skills_list in ResumeParser.SKILLS_DATABASE.items():
                    if skill in skills_list:
                        if category not in skills_by_category:
                            skills_by_category[category] = []
                        skills_by_category[category].append(skill)
                        break
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in found_skills:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        return unique_skills, skills_by_category
    
    @staticmethod
    def extract_education(text: str) -> List[str]:
        """Extract education information"""
        education_patterns = {
            r'\bphd\b': "PhD",
            r'\bdoctorate\b': "PhD",
            r'\bmaster[\'s]*\b': "Master's",
            r'\bm\.?s\.?\b': "Master's",
            r'\bmsc\b': "Master's",
            r'\bm\.?tech\b': "Master's",
            r'\bmba\b': "MBA",
            r'\bbachelor[\'s]*\b': "Bachelor's",
            r'\bb\.?s\.?\b': "Bachelor's",
            r'\bbsc\b': "Bachelor's",
            r'\bb\.?tech\b': "Bachelor's",
            r'\bb\.?e\.?\b': "Bachelor's",
        }
        
        text_lower = text.lower()
        education = set()
        
        for pattern, degree in education_patterns.items():
            if re.search(pattern, text_lower):
                education.add(degree)
        
        return sorted(list(education))
    
    @staticmethod
    def extract_experience_years(text: str) -> int:
        """Estimate years of experience from resume"""
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s+(?:in|as)',
        ]
        
        text_lower = text.lower()
        years = []
        
        for pattern in patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                years.append(int(match.group(1)))
        
        return max(years) if years else 0
    
    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, str]:
        """Extract contact information"""
        contact = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone
        phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text.lower())
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(0)
        
        # GitHub
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, text.lower())
        if github_match:
            contact['github'] = github_match.group(0)
        
        return contact
    
    @staticmethod
    def parse_full_resume(file_bytes: bytes) -> Dict:
        """
        Complete resume parsing with all information extraction
        """
        text = ResumeParser.extract_text_from_pdf(file_bytes)
        
        if not text or len(text.strip()) < 50:
            return {
                "success": False,
                "error": "Could not extract sufficient text from PDF"
            }
        
        skills, skills_by_category = ResumeParser.extract_skills(text)
        education = ResumeParser.extract_education(text)
        experience_years = ResumeParser.extract_experience_years(text)
        contact = ResumeParser.extract_contact_info(text)
        
        return {
            "success": True,
            "text_length": len(text),
            "skills": skills,
            "skills_by_category": skills_by_category,
            "education": education,
            "experience_years": experience_years,
            "contact": contact,
            "text_preview": text[:500]
        }