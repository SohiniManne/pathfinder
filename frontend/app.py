"""
Streamlit Dashboard - AI Career Mentor Frontend
"""
import streamlit as st
import requests
import sys
from pathlib import Path

# Add frontend to path
sys.path.append(str(Path(__file__).parent))

from components.sidebar import render_sidebar
from components.visualizations import (
    create_radar_chart,
    create_skills_gap_chart,
    create_timeline_chart
)
from components.career_cards import render_career_card

# Page config
st.set_page_config(
    page_title="AI Career Mentor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'extracted_skills' not in st.session_state:
        st.session_state['extracted_skills'] = []
    if 'resume_parsed' not in st.session_state:
        st.session_state['resume_parsed'] = False
    if 'education' not in st.session_state:
        st.session_state['education'] = []
    if 'experience_years' not in st.session_state:
        st.session_state['experience_years'] = 0
    if 'recommendations' not in st.session_state:
        st.session_state['recommendations'] = None

def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def render_welcome_screen():
    """Render welcome/intro screen"""
    st.markdown("""
    ## 👋 Welcome to AI Career Mentor!
    
    ### 🚀 How it works:
    1. **Upload your resume** (PDF format) or **enter your skills manually**
    2. **Click "Parse Resume"** to extract your skills automatically
    3. **Review and edit** the extracted information
    4. **Click "Get Career Recommendations"** to see your personalized career paths
    
    ### 🎯 What you'll get:
    - 📊 **Career Match Scores** - See which careers fit your profile best
    - 🔍 **Skills Gap Analysis** - Know exactly what to learn next
    - 📚 **Learning Roadmap** - Step-by-step plan to reach your goals
    - 💰 **Salary Insights** - Understand earning potential
    
    ---
    
    ### 🎓 Perfect for:
    - College students exploring career options
    - Career changers looking for new paths
    - Professionals planning skill development
    - Job seekers optimizing their profiles
    
    ---
    
    **Get started by uploading your resume or entering your skills in the sidebar!** 👈
    """)
    
    # Show sample careers
    with st.expander("📋 View Available Career Paths"):
        try:
            response = requests.get(f"{API_URL}/careers")
            if response.status_code == 200:
                careers = response.json()['careers']
                cols = st.columns(3)
                for idx, career in enumerate(careers):
                    with cols[idx % 3]:
                        st.write(f"✅ {career}")
        except:
            st.warning("Could not load careers. Make sure backend is running.")

def render_recommendations(recommendations):
    """Render career recommendations"""
    st.success("✨ Analysis Complete!")
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Top Match", recommendations[0]['career'])
    with col2:
        st.metric("Match Score", f"{recommendations[0]['match_score']}%")
    with col3:
        st.metric("Skills to Learn", len(recommendations[0]['skills_to_learn']))
    with col4:
        avg_match = sum(r['match_score'] for r in recommendations[:3]) / 3
        st.metric("Avg Top 3", f"{avg_match:.1f}%")
    
    st.divider()
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs([
        "📊 Career Matches", 
        "🎯 Skills Analysis", 
        "📚 Learning Path"
    ])
    
    with tab1:
        render_career_matches_tab(recommendations)
    
    with tab2:
        render_skills_analysis_tab(recommendations)
    
    with tab3:
        render_learning_path_tab()

def render_career_matches_tab(recommendations):
    """Render career matches visualization"""
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.plotly_chart(
            create_radar_chart(recommendations),
            use_container_width=True
        )
    
    with col_right:
        st.subheader("Top Career Recommendations")
        for i, rec in enumerate(recommendations[:5], 1):
            render_career_card(rec, i)

def render_skills_analysis_tab(recommendations):
    """Render skills gap analysis"""
    career_options = [rec['career'] for rec in recommendations]
    selected_career = st.selectbox(
        "Select a career to analyze skills gap:",
        career_options
    )
    
    # Get profile from session state
    profile = {
        "skills": st.session_state.get('current_skills', []),
        "interests": st.session_state.get('current_interests', []),
        "education_level": st.session_state.get('education_level', "Bachelor's"),
        "gpa": st.session_state.get('gpa', 3.5),
        "experience_years": st.session_state.get('experience_years', 0)
    }
    
    # Get skills gap analysis
    try:
        response = requests.post(
            f"{API_URL}/skills-gap-analysis",
            params={"target_career": selected_career},
            json=profile
        )
        
        if response.status_code == 200:
            gap_data = response.json()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Completion",
                    f"{gap_data['completion_percentage']}%"
                )
            with col2:
                st.metric(
                    "Skills Gap",
                    len(gap_data.get('missing_required', []))
                )
            with col3:
                st.metric(
                    "Bonus Skills",
                    len(gap_data.get('matching_nice', []))
                )
            
            # Skills breakdown
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("✅ Your Matching Skills")
                matching = gap_data.get('matching_required', [])
                if matching:
                    for skill in matching:
                        st.success(f"✓ {skill}")
                else:
                    st.info("No matching required skills yet")
            
            with col_right:
                st.subheader("📚 Skills to Learn")
                missing = gap_data.get('missing_required', [])
                if missing:
                    for skill in missing:
                        st.warning(f"→ {skill}")
                else:
                    st.success("You have all required skills!")
            
            # Visualization
            if missing or matching:
                st.plotly_chart(
                    create_skills_gap_chart(matching, missing),
                    use_container_width=True
                )
    except Exception as e:
        st.error(f"Error loading skills analysis: {str(e)}")

def render_learning_path_tab():
    """Render learning path"""
    st.subheader("🎓 Your Personalized Learning Path")
    
    # Get selected career
    if st.session_state.get('recommendations'):
        recommendations = st.session_state['recommendations']
        career_options = [rec['career'] for rec in recommendations]
        selected_career = st.selectbox(
            "Choose your target career:",
            career_options,
            key="learning_path_career"
        )
        
        profile = {
            "skills": st.session_state.get('current_skills', []),
            "interests": st.session_state.get('current_interests', []),
            "education_level": st.session_state.get('education_level', "Bachelor's"),
            "gpa": st.session_state.get('gpa', 3.5)
        }
        
        try:
            response = requests.post(
                f"{API_URL}/learning-path",
                params={"target_career": selected_career},
                json=profile
            )
            
            if response.status_code == 200:
                data = response.json()
                path = data['learning_path']
                
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Skills", data['total_skills'])
                with col2:
                    st.metric("Est. Duration", f"{data['total_weeks']} weeks")
                with col3:
                    st.metric("Target", selected_career)
                
                # Timeline
                st.plotly_chart(
                    create_timeline_chart(path),
                    use_container_width=True
                )
                
                # Detailed learning modules
                st.subheader("📖 Detailed Learning Plan")
                for module in path:
                    with st.expander(
                        f"Module {module['order']}: {module['skill']} "
                        f"({module['estimated_weeks']} weeks - {module['difficulty'].title()})"
                    ):
                        st.write(f"**Difficulty:** {module['difficulty'].title()}")
                        st.write(f"**Time Commitment:** {module['estimated_weeks']} weeks")
                        st.write("\n**Recommended Resources:**")
                        for resource in module['resources']:
                            st.write(f"- [{resource['name']}]({resource['url']}) ({resource['platform']})")
        except Exception as e:
            st.error(f"Error loading learning path: {str(e)}")

def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.title("🎯 AI-Powered Career Mentor")
    st.markdown("*Discover your ideal career path with AI-driven insights*")
    
    # Check backend status
    if not check_backend_status():
        st.error("""
        ⚠️ **Backend is not running!**
        
        Please start the backend server:
        ```bash
        cd backend
        uvicorn main:app --reload
        ```
        """)
        return
    
    st.divider()
    
    # Render sidebar and get user input
    analyze_button, profile_data = render_sidebar(API_URL)
    
    # Main content
    if analyze_button and profile_data:
        # Store current profile in session state
        st.session_state['current_skills'] = profile_data['skills']
        st.session_state['current_interests'] = profile_data['interests']
        st.session_state['education_level'] = profile_data['education_level']
        st.session_state['gpa'] = profile_data['gpa']
        
        with st.spinner("🤖 AI is analyzing your profile..."):
            try:
                response = requests.post(
                    f"{API_URL}/recommend-careers",
                    json=profile_data
                )
                
                if response.status_code == 200:
                    recommendations = response.json()
                    st.session_state['recommendations'] = recommendations
                    render_recommendations(recommendations)
                else:
                    st.error("Error getting recommendations. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the backend is running on http://localhost:8000")
    else:
        render_welcome_screen()

if __name__ == "__main__":
    main()