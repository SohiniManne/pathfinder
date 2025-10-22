"""
Sidebar component for user input
"""
import streamlit as st
import requests

def render_sidebar(api_url):
    """
    Render sidebar with resume upload and profile input
    Returns: (analyze_button_clicked, profile_data)
    """
    with st.sidebar:
        st.header("📝 Your Profile")
        
        # Resume upload section
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF)",
            type=['pdf'],
            help="Upload your resume for automatic skill extraction"
        )
        
        if uploaded_file is not None:
            st.info(f"📄 {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
            
            if st.button("🔍 Parse Resume", type="primary", use_container_width=True):
                with st.spinner("🤖 Analyzing your resume..."):
                    try:
                        files = {
                            'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')
                        }
                        response = requests.post(f"{api_url}/parse-resume", files=files)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            if data['status'] == 'success':
                                st.session_state['extracted_skills'] = data.get('extracted_skills', [])
                                st.session_state['education'] = data.get('education', [])
                                st.session_state['experience_years'] = data.get('experience_years', 0)
                                st.session_state['resume_parsed'] = True
                                
                                st.success(f"✅ Found {len(st.session_state['extracted_skills'])} skills!")
                                
                                # Show extracted info
                                with st.expander("📊 Extracted Information", expanded=True):
                                    st.write(f"**Skills Found:** {len(st.session_state['extracted_skills'])}")
                                    if st.session_state['extracted_skills']:
                                        skills_preview = st.session_state['extracted_skills'][:10]
                                        st.write(", ".join(skills_preview))
                                        if len(st.session_state['extracted_skills']) > 10:
                                            remaining = len(st.session_state['extracted_skills']) - 10
                                            st.write(f"*...and {remaining} more*")
                                    
                                    if st.session_state['education']:
                                        st.write(f"**Education:** {', '.join(st.session_state['education'])}")
                                    if st.session_state['experience_years'] > 0:
                                        st.write(f"**Experience:** {st.session_state['experience_years']} years")
                            else:
                                st.error(f"❌ {data.get('message', 'Unknown error')}")
                        else:
                            st.error("❌ Error connecting to API")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("💡 Make sure backend is running: `uvicorn main:app --reload`")
        
        st.divider()
        
        # Manual input section
        st.subheader("✏️ Manual Input")
        
        # Skills input with extracted skills as default
        default_skills = ", ".join(st.session_state.get('extracted_skills', []))
        
        skills_input = st.text_area(
            "Your Skills (comma-separated)",
            value=default_skills,
            placeholder="Python, Machine Learning, SQL, Git...",
            height=100,
            help="Edit or add skills manually"
        )
        
        interests_input = st.text_input(
            "Interests",
            placeholder="Data Science, AI, Web Development...",
            help="What fields interest you?"
        )
        
        education = st.selectbox(
            "Education Level",
            ["High School", "Bachelor's", "Master's", "PhD"],
            index=1
        )
        
        gpa = st.slider(
            "GPA (optional)", 
            0.0, 4.0, 3.5, 0.1,
            help="Your current GPA"
        )
        
        experience_years = st.number_input(
            "Years of Experience",
            min_value=0,
            max_value=50,
            value=st.session_state.get('experience_years', 0),
            help="Total years of professional experience"
        )
        
        st.divider()
        
        # Analyze button
        analyze_button = st.button(
            "🚀 Get Career Recommendations", 
            type="primary", 
            use_container_width=True
        )
        
        # Prepare profile data
        profile_data = None
        if skills_input.strip():
            skills = [s.strip() for s in skills_input.split(',') if s.strip()]
            interests = [i.strip() for i in interests_input.split(',') if i.strip()]
            
            profile_data = {
                "skills": skills,
                "interests": interests,
                "education_level": education,
                "gpa": gpa,
                "experience_years": experience_years
            }
        elif analyze_button:
            st.warning("⚠️ Please enter your skills or upload a resume!")
        
        # Additional info
        st.divider()
        st.caption("💡 **Tips:**")
        st.caption("• Upload PDF for auto-extraction")
        st.caption("• Add all relevant skills")
        st.caption("• Be specific with interests")
        
    return analyze_button, profile_data