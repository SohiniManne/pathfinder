"""
Career and skills database
Expand this with real data from O*NET, LinkedIn, etc.
"""

CAREER_DATABASE = {
    "Data Scientist": {
        "required_skills": [
            "Python", "Machine Learning", "Statistics", "SQL", "Data Visualization",
            "Pandas", "NumPy", "Scikit-learn", "Deep Learning", "Data Analysis"
        ],
        "nice_to_have": ["TensorFlow", "PyTorch", "Spark", "AWS", "R", "Tableau"],
        "description": "Analyze complex data to help companies make data-driven decisions",
        "avg_salary": "$120,000 - $160,000",
        "growth_outlook": "22% (Much faster than average)",
        "education_required": "Bachelor's or Master's in Computer Science, Statistics, or related field",
        "industry": ["Technology", "Finance", "Healthcare", "E-commerce"]
    },
    
    "Software Engineer": {
        "required_skills": [
            "Python", "Java", "Algorithms", "Data Structures", "System Design",
            "Git", "Testing", "Debugging", "API", "Databases"
        ],
        "nice_to_have": ["Docker", "Kubernetes", "AWS", "Microservices", "CI/CD"],
        "description": "Design, develop, and maintain software applications and systems",
        "avg_salary": "$110,000 - $150,000",
        "growth_outlook": "25% (Much faster than average)",
        "education_required": "Bachelor's in Computer Science or related field",
        "industry": ["Technology", "Finance", "Healthcare", "Entertainment"]
    },
    
    "Machine Learning Engineer": {
        "required_skills": [
            "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
            "MLOps", "Docker", "Kubernetes", "Cloud", "Algorithms"
        ],
        "nice_to_have": ["Spark", "AWS", "Azure", "Model Optimization", "Edge Computing"],
        "description": "Build and deploy machine learning models at scale in production",
        "avg_salary": "$140,000 - $180,000",
        "growth_outlook": "21% (Much faster than average)",
        "education_required": "Bachelor's or Master's in CS, ML, or related field",
        "industry": ["Technology", "AI Companies", "Research", "Autonomous Vehicles"]
    },
    
    "Full Stack Developer": {
        "required_skills": [
            "JavaScript", "React", "Node.js", "HTML", "CSS", "SQL",
            "Git", "API", "REST", "Express"
        ],
        "nice_to_have": ["TypeScript", "Next.js", "MongoDB", "Docker", "AWS"],
        "description": "Develop both front-end and back-end of web applications",
        "avg_salary": "$100,000 - $140,000",
        "growth_outlook": "23% (Much faster than average)",
        "education_required": "Bachelor's in Computer Science or self-taught with portfolio",
        "industry": ["Technology", "Startups", "E-commerce", "Media"]
    },
    
    "Data Engineer": {
        "required_skills": [
            "Python", "SQL", "Spark", "Kafka", "ETL", "Data Pipelines",
            "AWS", "Airflow", "Databases", "Big Data"
        ],
        "nice_to_have": ["Snowflake", "Databricks", "Kubernetes", "Terraform"],
        "description": "Build and maintain data infrastructure and pipelines",
        "avg_salary": "$115,000 - $155,000",
        "growth_outlook": "20% (Much faster than average)",
        "education_required": "Bachelor's in Computer Science or Data Engineering",
        "industry": ["Technology", "Finance", "E-commerce", "Healthcare"]
    },
    
    "DevOps Engineer": {
        "required_skills": [
            "Linux", "Docker", "Kubernetes", "CI/CD", "AWS", "Jenkins",
            "Terraform", "Ansible", "Git", "Monitoring"
        ],
        "nice_to_have": ["Python", "Shell", "Azure", "GCP", "Security"],
        "description": "Automate and optimize software development and deployment processes",
        "avg_salary": "$110,000 - $145,000",
        "growth_outlook": "20% (Much faster than average)",
        "education_required": "Bachelor's in Computer Science or System Administration",
        "industry": ["Technology", "Cloud Services", "Finance", "All Industries"]
    },
    
    "Frontend Developer": {
        "required_skills": [
            "JavaScript", "React", "HTML", "CSS", "TypeScript",
            "Git", "Responsive Design", "API", "Testing"
        ],
        "nice_to_have": ["Vue.js", "Angular", "Redux", "Webpack", "Performance Optimization"],
        "description": "Create user interfaces and experiences for web applications",
        "avg_salary": "$90,000 - $130,000",
        "growth_outlook": "23% (Much faster than average)",
        "education_required": "Bachelor's in CS or self-taught with strong portfolio",
        "industry": ["Technology", "Design Agencies", "E-commerce", "Media"]
    },
    
    "Backend Developer": {
        "required_skills": [
            "Python", "Java", "Node.js", "SQL", "API", "REST",
            "Databases", "System Design", "Git", "Security"
        ],
        "nice_to_have": ["Microservices", "GraphQL", "Docker", "AWS", "Caching"],
        "description": "Develop server-side logic and database management",
        "avg_salary": "$105,000 - $140,000",
        "growth_outlook": "22% (Much faster than average)",
        "education_required": "Bachelor's in Computer Science",
        "industry": ["Technology", "Finance", "SaaS", "E-commerce"]
    },
    
    "Cloud Architect": {
        "required_skills": [
            "AWS", "Azure", "GCP", "System Design", "Networking",
            "Security", "Docker", "Kubernetes", "Terraform", "Microservices"
        ],
        "nice_to_have": ["Multi-Cloud", "Cost Optimization", "Compliance", "Serverless"],
        "description": "Design and oversee cloud computing strategies",
        "avg_salary": "$135,000 - $175,000",
        "growth_outlook": "19% (Much faster than average)",
        "education_required": "Bachelor's + Cloud Certifications",
        "industry": ["Technology", "Consulting", "Enterprise", "All Industries"]
    },
    
    "AI Research Scientist": {
        "required_skills": [
            "Machine Learning", "Deep Learning", "Python", "Mathematics",
            "Research", "PyTorch", "TensorFlow", "NLP", "Computer Vision", "Statistics"
        ],
        "nice_to_have": ["Publications", "PhD", "Reinforcement Learning", "Transformers"],
        "description": "Conduct cutting-edge research in artificial intelligence",
        "avg_salary": "$150,000 - $200,000+",
        "growth_outlook": "24% (Much faster than average)",
        "education_required": "Master's or PhD in CS, AI, or related field",
        "industry": ["Research Labs", "Big Tech", "AI Startups", "Academia"]
    },
    
    "Business Analyst": {
        "required_skills": [
            "Data Analysis", "Excel", "SQL", "Business Intelligence",
            "Communication", "Problem Solving", "Requirements Gathering", "Analytics"
        ],
        "nice_to_have": ["Python", "Tableau", "Power BI", "Agile", "Project Management"],
        "description": "Bridge business needs and technical solutions through data analysis",
        "avg_salary": "$80,000 - $110,000",
        "growth_outlook": "14% (Faster than average)",
        "education_required": "Bachelor's in Business, Economics, or related field",
        "industry": ["Consulting", "Finance", "Technology", "Healthcare"]
    },
    
    "Product Manager": {
        "required_skills": [
            "Product Strategy", "Communication", "Agile", "User Research",
            "Analytics", "Roadmap Planning", "Stakeholder Management", "Problem Solving"
        ],
        "nice_to_have": ["Technical Background", "SQL", "A/B Testing", "Design Thinking"],
        "description": "Define product vision and strategy, working with engineering and design",
        "avg_salary": "$120,000 - $160,000",
        "growth_outlook": "18% (Much faster than average)",
        "education_required": "Bachelor's in any field + product experience",
        "industry": ["Technology", "SaaS", "E-commerce", "Finance"]
    }
}

def get_all_careers():
    """Get list of all career titles"""
    return list(CAREER_DATABASE.keys())

def get_career_details(career_name: str):
    """Get details for a specific career"""
    return CAREER_DATABASE.get(career_name)

def search_careers_by_skill(skill: str):
    """Find careers that require a specific skill"""
    matching_careers = []
    skill_lower = skill.lower()
    
    for career, details in CAREER_DATABASE.items():
        all_skills = details['required_skills'] + details['nice_to_have']
        if any(skill_lower in s.lower() for s in all_skills):
            matching_careers.append(career)
    
    return matching_careers