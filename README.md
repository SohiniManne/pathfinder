# 🎯 AI-Powered Career Mentor

An intelligent career guidance system that uses AI to analyze student resumes, skills, and interests to recommend ideal career paths and personalized learning plans.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **📄 Resume Parsing**: Automatically extract skills, education, and experience from PDF resumes
- **🤖 AI Recommendations**: Get personalized career suggestions based on your profile
- **📊 Skills Gap Analysis**: Identify exactly what skills you need for your target career
- **📚 Learning Paths**: Receive structured learning roadmaps with timelines
- **💰 Salary Insights**: Compare salary ranges across different careers
- **📈 Visual Analytics**: Interactive charts and dashboards

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │ ◄─────► │   Backend    │ ◄─────► │  Database   │
│  Streamlit  │  REST   │   FastAPI    │         │   (JSON)    │
└─────────────┘   API   └──────────────┘         └─────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  ML Components  │
                     │  - Resume Parser│
                     │  - Recommender  │
                     └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/pathfinder.git
cd pathfinder
```

2. **Set up Backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up Frontend**
```bash
cd ../frontend
pip install -r requirements.txt
```

### Running the Application

1. **Start Backend Server** (Terminal 1)
```bash
cd backend
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

2. **Start Frontend** (Terminal 2)
```bash
cd frontend
streamlit run app.py
```
The dashboard will open at `http://localhost:8501`

## 📁 Project Structure

```
PathFinder/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic data models
│   ├── parser.py            # Resume parsing logic
│   ├── recommender.py       # Recommendation engine
│   ├── database.py          # Career database
│   └── requirements.txt
│
├── frontend/
│   ├── app.py               # Main Streamlit app
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py       # Sidebar component
│   │   ├── visualizations.py # Chart components
│   │   └── career_cards.py  # Career display cards
│   └── requirements.txt
│
├── data/
│   └── careers.json         # Career information
│
├── tests/
│   ├── test_parser.py
│   ├── test_recommender.py
│   └── test_api.py
│
└── README.md
```

## 🎯 Usage

### 1. Upload Resume
- Click "Upload Resume (PDF)" in the sidebar
- Click "Parse Resume" to extract information
- Review and edit extracted skills

### 2. Enter Profile Information
- Manually add or edit skills
- Specify interests and education level
- Add years of experience

### 3. Get Recommendations
- Click "Get Career Recommendations"
- View match scores and career details
- Analyze skills gaps

### 4. Plan Your Learning
- Select a target career
- View personalized learning path
- Access recommended resources

## 🔧 API Endpoints

### Resume Parsing
```http
POST /parse-resume
Content-Type: multipart/form-data

Upload PDF file
```

### Career Recommendations
```http
POST /recommend-careers
Content-Type: application/json

{
  "skills": ["Python", "Machine Learning"],
  "interests": ["Data Science"],
  "education_level": "Bachelor's",
  "gpa": 3.5
}
```

### Skills Gap Analysis
```http
POST /skills-gap-analysis?target_career=Data%20Scientist
Content-Type: application/json

{
  "skills": ["Python", "SQL"],
  "interests": ["Data"],
  "education_level": "Bachelor's"
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend tests/

# Run specific test file
pytest tests/test_parser.py -v
```

## 📊 Tech Stack

### Backend
- **FastAPI**: Modern web framework for APIs
- **PyPDF2**: PDF text extraction
- **scikit-learn**: Machine learning algorithms
- **Pydantic**: Data validation

### Frontend
- **Streamlit**: Interactive dashboards
- **Plotly**: Data visualizations
- **Requests**: HTTP client

## 🎨 Features in Detail

### Resume Parser
- Extracts skills using keyword matching with 100+ skills database
- Identifies education level and years of experience
- Categorizes skills by domain (Programming, Cloud, Data, etc.)
- Handles various PDF formats

### Recommendation Engine
- Calculates match scores based on multiple factors:
  - Skill alignment (70% weight)
  - Nice-to-have skills (30% weight)
  - Interest matching (+10% boost)
  - Experience level consideration
- Provides top 10 personalized recommendations

### Skills Gap Analysis
- Identifies required vs. current skills
- Prioritizes missing skills by importance
- Calculates completion percentage
- Suggests learning order

## 🚧 Future Enhancements

- [ ] OCR support for scanned PDFs
- [ ] Real-time job market data integration
- [ ] User authentication and profile saving
- [ ] Collaborative filtering recommendations
- [ ] Integration with LinkedIn API
- [ ] Mobile app version
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - [GitHub](https://github.com/SohiniManne)

## 🙏 Acknowledgments

- Career data inspired by O*NET Database
- Skills taxonomy from industry standards
- UI design inspired by modern career platforms


⭐ If you find this project helpful, please give it a star!