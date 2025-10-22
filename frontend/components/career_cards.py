"""
Career card components for displaying recommendations
"""
import streamlit as st

def render_career_card(recommendation: dict, rank: int):
    """
    Render a single career recommendation card
    """
    with st.expander(
        f"#{rank} {recommendation['career']} - {recommendation['match_score']}% Match",
        expanded=(rank == 1)
    ):
        # Match score indicator
        match_score = recommendation['match_score']
        if match_score >= 80:
            score_color = "🟢"
            score_text = "Excellent Match"
        elif match_score >= 60:
            score_color = "🟡"
            score_text = "Good Match"
        elif match_score >= 40:
            score_color = "🟠"
            score_text = "Moderate Match"
        else:
            score_color = "🔴"
            score_text = "Needs Development"
        
        st.markdown(f"### {score_color} {score_text}")
        
        # Description
        st.write(f"**Description:** {recommendation['description']}")
        
        # Salary and growth in columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💰 Salary Range", recommendation['salary_info'])
        with col2:
            st.metric("📈 Growth Outlook", recommendation['growth_outlook'])
        
        st.divider()
        
        # Matching skills
        if recommendation.get('matching_skills'):
            st.write("**✅ Your Matching Skills:**")
            skills_html = " ".join([
                f'<span style="background-color: #d4edda; padding: 4px 8px; '
                f'border-radius: 4px; margin: 2px; display: inline-block;">{skill}</span>'
                for skill in recommendation['matching_skills'][:10]
            ])
            st.markdown(skills_html, unsafe_allow_html=True)
            
            if len(recommendation['matching_skills']) > 10:
                with st.expander(f"View all {len(recommendation['matching_skills'])} matching skills"):
                    st.write(", ".join(recommendation['matching_skills']))
        
        # Skills to learn
        if recommendation.get('skills_to_learn'):
            st.write("**📚 Skills You Need to Learn:**")
            skills_html = " ".join([
                f'<span style="background-color: #fff3cd; padding: 4px 8px; '
                f'border-radius: 4px; margin: 2px; display: inline-block;">{skill}</span>'
                for skill in recommendation['skills_to_learn']
            ])
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.success("🎉 You already have all the required skills!")
        
        # Action buttons
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📊 Analyze Skills Gap", key=f"gap_{rank}"):
                st.session_state['selected_career_for_gap'] = recommendation['career']
                st.rerun()
        with col2:
            if st.button(f"🎓 View Learning Path", key=f"path_{rank}"):
                st.session_state['selected_career_for_path'] = recommendation['career']
                st.rerun()

def render_compact_career_card(recommendation: dict):
    """
    Render a compact version of career card (for lists)
    """
    score = recommendation['match_score']
    
    # Progress bar color based on score
    if score >= 80:
        color = "#4CAF50"
    elif score >= 60:
        color = "#FF9800"
    else:
        color = "#F44336"
    
    st.markdown(f"""
    <div style="
        border: 1px solid #ddd;
        border-left: 4px solid {color};
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        background-color: #f9f9f9;
    ">
        <h4 style="margin: 0 0 0.5rem 0;">{recommendation['career']}</h4>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>Match Score: <strong>{score}%</strong></span>
            <span>Salary: {recommendation['salary_info']}</span>
        </div>
        <div style="
            background-color: #e0e0e0;
            height: 8px;
            border-radius: 4px;
            margin-top: 0.5rem;
            overflow: hidden;
        ">
            <div style="
                background-color: {color};
                height: 100%;
                width: {score}%;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_career_comparison_table(recommendations: list):
    """
    Render a comparison table for multiple careers
    """
    import pandas as pd
    
    # Prepare data
    data = []
    for rec in recommendations:
        data.append({
            'Career': rec['career'],
            'Match Score': f"{rec['match_score']}%",
            'Skills Match': len(rec.get('matching_skills', [])),
            'Skills Needed': len(rec.get('skills_to_learn', [])),
            'Salary': rec['salary_info'],
            'Growth': rec['growth_outlook']
        })
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )