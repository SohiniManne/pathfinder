"""
Visualization components using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict

def create_radar_chart(recommendations: List[Dict]) -> go.Figure:
    """
    Create radar chart showing career match scores
    """
    # Take top 5 careers
    top_careers = recommendations[:5]
    careers = [rec['career'] for rec in top_careers]
    scores = [rec['match_score'] for rec in top_careers]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=careers,
        fill='toself',
        name='Match Score',
        line_color='#4CAF50',
        fillcolor='rgba(76, 175, 80, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='%'
            )
        ),
        showlegend=False,
        title={
            'text': "Career Compatibility Radar",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=400
    )
    
    return fig

def create_skills_gap_chart(matching_skills: List[str], missing_skills: List[str]) -> go.Figure:
    """
    Create bar chart showing skills gap
    """
    # Prepare data
    skills = []
    status = []
    colors = []
    
    for skill in matching_skills:
        skills.append(skill)
        status.append('Have')
        colors.append('#4CAF50')
    
    for skill in missing_skills:
        skills.append(skill)
        status.append('Need')
        colors.append('#FF9800')
    
    if not skills:
        # Empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No skills data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        return fig
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=skills,
        x=[1] * len(skills),
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=2)
        ),
        text=status,
        textposition='inside',
        hovertemplate='%{y}<br>Status: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Skills Gap Analysis",
        xaxis_title="",
        yaxis_title="Skills",
        showlegend=False,
        height=max(400, len(skills) * 30),
        xaxis=dict(showticklabels=False),
        yaxis=dict(autorange="reversed")
    )
    
    return fig

def create_timeline_chart(learning_path: List[Dict]) -> go.Figure:
    """
    Create Gantt-style timeline for learning path
    """
    if not learning_path:
        fig = go.Figure()
        fig.add_annotation(
            text="No learning path available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        return fig
    
    # Calculate cumulative weeks for timeline
    start_week = 0
    timeline_data = []
    
    for module in learning_path:
        end_week = start_week + module['estimated_weeks']
        
        timeline_data.append({
            'Skill': module['skill'],
            'Start': start_week,
            'Finish': end_week,
            'Duration': module['estimated_weeks'],
            'Difficulty': module['difficulty']
        })
        
        start_week = end_week
    
    # Color mapping for difficulty
    color_map = {
        'beginner': '#4CAF50',
        'intermediate': '#FF9800',
        'advanced': '#F44336'
    }
    
    colors = [color_map.get(d['Difficulty'], '#2196F3') for d in timeline_data]
    
    fig = go.Figure()
    
    for idx, data in enumerate(timeline_data):
        fig.add_trace(go.Bar(
            y=[data['Skill']],
            x=[data['Duration']],
            base=data['Start'],
            orientation='h',
            name=data['Skill'],
            marker=dict(color=colors[idx]),
            text=f"{data['Duration']} weeks",
            textposition='inside',
            hovertemplate=(
                f"<b>{data['Skill']}</b><br>"
                f"Week {data['Start']} - {data['Finish']}<br>"
                f"Duration: {data['Duration']} weeks<br>"
                f"Difficulty: {data['Difficulty'].title()}"
                "<extra></extra>"
            )
        ))
    
    fig.update_layout(
        title="Learning Timeline (Gantt Chart)",
        xaxis_title="Weeks",
        yaxis_title="Skills",
        showlegend=False,
        height=max(400, len(timeline_data) * 50),
        barmode='overlay',
        yaxis=dict(autorange="reversed")
    )
    
    return fig

def create_salary_comparison_chart(recommendations: List[Dict]) -> go.Figure:
    """
    Create bar chart comparing salaries across careers
    """
    careers = []
    min_salaries = []
    max_salaries = []
    
    for rec in recommendations[:6]:
        careers.append(rec['career'])
        
        # Parse salary string (e.g., "$120,000 - $160,000")
        salary_str = rec.get('salary_info', '$0 - $0')
        try:
            parts = salary_str.replace('$', '').replace(',', '').split('-')
            min_sal = int(parts[0].strip())
            max_sal = int(parts[1].strip().split()[0]) if len(parts) > 1 else min_sal
        except:
            min_sal = 0
            max_sal = 0
        
        min_salaries.append(min_sal / 1000)  # Convert to thousands
        max_salaries.append(max_sal / 1000)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Min Salary',
        y=careers,
        x=min_salaries,
        orientation='h',
        marker=dict(color='#64B5F6')
    ))
    
    fig.add_trace(go.Bar(
        name='Max Salary',
        y=careers,
        x=max_salaries,
        orientation='h',
        marker=dict(color='#1976D2')
    ))
    
    fig.update_layout(
        title='Salary Comparison (in thousands)',
        xaxis_title='Salary ($K)',
        yaxis_title='Career',
        barmode='group',
        height=400,
        yaxis=dict(autorange="reversed")
    )
    
    return fig

def create_skills_distribution_pie(skills_by_category: Dict[str, List[str]]) -> go.Figure:
    """
    Create pie chart showing skills distribution by category
    """
    if not skills_by_category:
        fig = go.Figure()
        fig.add_annotation(
            text="No skills categorization available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        return fig
    
    categories = list(skills_by_category.keys())
    counts = [len(skills) for skills in skills_by_category.values()]
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=counts,
        hole=.3,
        marker=dict(
            colors=['#4CAF50', '#2196F3', '#FF9800', '#F44336', '#9C27B0', '#00BCD4']
        )
    )])
    
    fig.update_layout(
        title="Your Skills by Category",
        height=400
    )
    
    return fig