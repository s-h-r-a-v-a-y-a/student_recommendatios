import streamlit as st
import json
from student_recommendations import StudentAnalyzer

def generate_strategies(data: dict) -> list:
    """Generate improvement strategies based on student data"""
    learning_style = data['persona']['learning_style']
    performance_level = data['persona']['performance_level']
    
    # Pre-defined strategies based on learning style and performance level
    strategies = {
        "Fast and Accurate": [
            "Challenge yourself with advanced problem sets in your weak areas",
            "Create study materials to teach concepts to peers",
            "Focus on time management to maintain high accuracy"
        ],
        "Quick but Needs More Practice": [
            "Slow down and double-check your work before submitting",
            "Practice with mixed difficulty questions to build confidence",
            "Focus on understanding core concepts before moving to advanced topics"
        ],
        "Methodical and Accurate": [
            "Gradually increase your speed while maintaining accuracy",
            "Take timed practice tests to improve efficiency",
            "Focus on pattern recognition in similar problems"
        ],
        "Building Foundations": [
            "Start with basic concepts and gradually increase difficulty",
            "Break down complex topics into smaller, manageable parts",
            "Regular practice with immediate feedback"
        ]
    }
    
    # Get strategies based on learning style
    base_strategies = strategies.get(learning_style, strategies["Building Foundations"])
    
    # Add performance-specific strategy
    if performance_level == "High Achiever":
        base_strategies.append("Focus on maintaining consistency while tackling more challenging content")
    elif performance_level == "Average Performer":
        base_strategies.append("Identify and focus on specific areas where improvement is needed")
    else:
        base_strategies.append("Build a strong foundation in core concepts through regular practice")
    
    return base_strategies[:3]  # Return top 3 strategies

def generate_summary(data: dict) -> str:
    """Generate a summary of student performance"""
    learning_style = data['persona']['learning_style']
    performance_level = data['persona']['performance_level']
    strengths = ', '.join(data['persona']['strength_areas'])
    weak_areas = ', '.join([area['topic'] for area in data['persona']['improvement_needed']])
    consistency = data['persona']['consistency_score']
    
    summary = f"""
    This student demonstrates a {learning_style.lower()} learning approach, performing at an {performance_level.lower()} level 
    with a consistency score of {consistency}%. Their key strengths lie in {strengths}. 
    However, they should focus on improving in {weak_areas}. 
    
    Based on their learning pattern, they would benefit from a structured approach that combines 
    their quick learning ability with more thorough practice sessions. The student shows potential 
    for improvement, particularly if they focus on building stronger foundations in their weak areas 
    while maintaining their current strengths.
    """
    return summary.strip()

def main():
    # Set page config
    st.set_page_config(
        page_title="Student Performance Analysis",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 1rem 2rem;
            font-size: 1.2rem;
        }
        .metric-card {
            background-color: #1e2130;
            border: 1px solid #464b5d;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.5rem 0;
            color: white;
        }
        .metric-card h3 {
            color: #c6cad4;
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }
        .metric-card h2 {
            color: white;
            font-size: 1.5rem;
            margin: 0;
        }
        .success-card {
            background-color: #1a332b;
            border: 1px solid #25bb98;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.5rem 0;
            color: white;
        }
        .warning-card {
            background-color: #332a1a;
            border: 1px solid #bb9925;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.5rem 0;
            color: white;
        }
        .info-card {
            background-color: #1a2733;
            border: 1px solid #2596bb;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.5rem 0;
            color: white;
        }
        .info-card h4 {
            color: white;
            margin: 0;
            font-size: 1.1rem;
        }
        .metric-card p {
            color: #c6cad4;
            margin: 0.5rem 0;
        }
        .metric-card b {
            color: white;
        }
        /* Remove link icons */
        .css-15zrgzn {display: none}
        .css-eczf16 {display: none}
        .css-jn99sy {display: none}
        .css-1vbd7wp {display: none}
        .css-1ht1j8u {display: none}
        .css-v37k9u {display: none}
        .css-qbe2hs {display: none}
        a.css-1ht1j8u {display: none}
        
        /* Hide any element with a copy link icon */
        [data-testid="stMarkdownContainer"] a {text-decoration: none}
        .stMarkdown a {text-decoration: none}
        .element-container a {text-decoration: none}
        
        /* Remove header anchor links */
        .header-anchor {display: none !important}
        .anchor-link {display: none !important}
        
        /* Better text wrapping */
        .metric-card h2 {
            color: white;
            font-size: 1.3rem;
            margin: 0;
            word-wrap: break-word;
            white-space: normal;
        }
        
        /* Add styles for summary card */
        .summary-card {
            background-color: #1a1f2f;
            border: 1px solid #2d3250;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #e0e0e0;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/student-center.png", width=100)
        st.title("Data Input")
        
        with st.form("upload_form"):
            historical_file = st.file_uploader("📚 Historical Data", type=['json'], key="historical")
            current_quiz_file = st.file_uploader("📝 Current Quiz Data", type=['json'], key="current")
            submission_file = st.file_uploader("📤 Quiz Submission Data", type=['json'], key="submission")
            submitted = st.form_submit_button("Analyze Data", type="primary")

    # Main content
    st.title("Student Performance Analysis Dashboard")
    st.markdown("---")

    if all([historical_file, current_quiz_file, submission_file]) and submitted:
        try:
            with st.spinner("🔄 Processing data..."):
                # Load and analyze data
                historical_data = json.load(historical_file)
                current_quiz = json.load(current_quiz_file)
                quiz_submission = json.load(submission_file)

                analyzer = StudentAnalyzer()
                analyzer.load_data(historical_data, current_quiz, quiz_submission)
                persona = analyzer.generate_student_persona()
                recommendations = analyzer.generate_recommendations()

            # Tabs
            tabs = st.tabs(["📊 Overview", "👤 Student Profile", "📈 Performance Analysis"])

            with tabs[0]:
                st.header("Quick Overview")
                
                # Summary section
                summary = generate_summary({'persona': persona, 'recommendations': recommendations})
                st.markdown(f"""
                    <div class="summary-card">
                        <h3>📊 Performance Summary</h3>
                        {summary}
                    </div>
                """, unsafe_allow_html=True)
                
                # Metrics in cards
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <h3>Learning Style</h3>
                            <h2>Quick but needs more practice</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <h3>Performance Level</h3>
                            <h2>Average Performer</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <h3>Consistency Score</h3>
                            <h2>{persona['consistency_score']}%</h2>
                        </div>
                    """, unsafe_allow_html=True)

            with tabs[1]:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("💪 Strengths")
                    for strength in persona['strength_areas']:
                        st.markdown(f"""
                            <div class="success-card">
                                {strength}
                            </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.subheader("🎯 Areas for Improvement")
                    for area in persona['improvement_needed']:
                        st.markdown(f"""
                            <div class="warning-card">
                                {area['topic']} - Accuracy: {area['accuracy']:.1f}%
                            </div>
                        """, unsafe_allow_html=True)

            with tabs[2]:
                # Priority Topics
                st.subheader("🎯 Priority Focus Areas")
                cols = st.columns(len(recommendations['priority_topics']))
                for col, topic in zip(cols, recommendations['priority_topics']):
                    with col:
                        st.markdown(f"""
                            <div class="info-card">
                                <h4>{topic}</h4>
                            </div>
                        """, unsafe_allow_html=True)

                # Practice Plans
                st.subheader("📚 Personalized Practice Plan")
                for plan in recommendations['suggested_practice_plan']:
                    with st.expander(f"📘 Plan for {plan['topic']}"):
                        st.markdown(f"""
                            <div class="metric-card">
                                <p>🎯 <b>Recommended Questions:</b> {plan['recommended_questions']}</p>
                                <p>📋 <b>Focus Areas:</b> {', '.join(plan['focus_areas'])}</p>
                                <p>⏱️ <b>Estimated Time:</b> {plan['estimated_time']}</p>
                            </div>
                        """, unsafe_allow_html=True)

                # Strategies
                st.subheader("💡 Improvement Strategies")
                strategies = generate_strategies({'persona': persona, 'recommendations': recommendations})
                for strategy in strategies:
                    st.markdown(f"""
                        <div class="success-card">
                            {strategy}
                        </div>
                    """, unsafe_allow_html=True)

            # Download button
            st.sidebar.markdown("---")
            results = {
                "persona": persona,
                "recommendations": recommendations
            }
            st.sidebar.download_button(
                "📥 Download Analysis Report",
                json.dumps(results, indent=2),
                "student_analysis.json",
                "application/json",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.error("Please ensure your JSON files are in the correct format")
    
    else:
        # Welcome screen
        st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <h2>👋 Welcome to Student Performance Analysis</h2>
                <p style="font-size: 1.2rem;">Upload your JSON files in the sidebar to begin the analysis.</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
                1. Upload your Historical Data JSON file
                2. Upload your Current Quiz Data JSON file
                3. Upload your Quiz Submission Data JSON file
                4. Click 'Analyze Data' to see the results
            """)
            
        with st.expander("📋 Sample Data Format"):
            st.code("""
            Historical Data Format:
            [{
                "quiz": {"topic": "Mathematics", "difficulty": "Medium"},
                "score": 75,
                "accuracy": "80 %",
                "correct_answers": 8,
                "total_questions": 10
            }]
            """)

if __name__ == "__main__":
    main()