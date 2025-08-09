#!/usr/bin/env python3
"""
Data Engineering Learning Agent - Ollama Version

A specialized AI agent powered by local Ollama models for learning data engineering.
Completely free and runs locally on your machine!

Repository: https://github.com/cookiee01/data-engineering-staff-learning-plan
"""

import streamlit as st
import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Data Engineering Learning Agent (Ollama)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class LearningProgress:
    """Track learning progress for each topic"""
    topic: str
    week: int
    day: int
    completion_percentage: float
    time_spent_hours: float
    confidence_level: int  # 1-10
    last_updated: str
    notes: str = ""
    
@dataclass
class SkillsAssessment:
    """Track skills assessment results"""
    category: str
    current_score: int
    max_score: int
    target_score: int
    last_assessed: str
    improvement_areas: List[str]

class OllamaLearningAgent:
    """Main learning agent class powered by Ollama"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.available_models = []
        self.selected_model = None
        self.progress_file = "learning_progress.json"
        self.curriculum_structure = self._load_curriculum_structure()
        
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and get available models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                self.available_models = [model['name'] for model in models_data.get('models', [])]
                return True
            return False
        except Exception as e:
            st.error(f"Ollama connection failed: {str(e)}")
            return False
    
    def query_ollama(self, prompt: str, model: str = None) -> str:
        """Query Ollama with a prompt"""
        if not model:
            model = self.selected_model
            
        if not model:
            return "❌ No model selected. Please select a model first."
            
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 3000
                    }
                },
                timeout=120  # 2 minute timeout for complex queries
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response received')
            else:
                return f"❌ Ollama error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "❌ Request timed out. Try a simpler question or use a faster model."
        except Exception as e:
            return f"❌ Error querying Ollama: {str(e)}"
    
    def _load_curriculum_structure(self) -> Dict[str, Any]:
        """Load the 6-week curriculum structure"""
        return {
            "Week 1": {
                "title": "Foundation & Modern Lakehouse",
                "days": {
                    1: "Environment Setup & Apache Iceberg Foundations",
                    2: "Advanced Iceberg Features",
                    3: "Delta Lake Fundamentals", 
                    4: "Delta Lake Advanced Features",
                    5: "AWS Glue Deep Dive",
                    6: "Integration Project - Lakehouse Platform",
                    7: "Week 1 Review & Assessment"
                },
                "technologies": ["Apache Iceberg", "Delta Lake", "AWS Glue", "Spark"],
                "key_concepts": ["ACID transactions", "Time travel", "Schema evolution", "Table formats"]
            },
            "Week 2": {
                "title": "Data Processing & Orchestration", 
                "days": {
                    8: "Apache Spark Performance Tuning",
                    9: "Spark Structured Streaming",
                    10: "Apache Airflow Advanced Patterns",
                    11: "dbt Analytics Engineering", 
                    12: "Kafka & Stream Processing",
                    13: "Integration Project - Real-time Analytics Pipeline",
                    14: "Week 2 Review & System Design Practice"
                },
                "technologies": ["Apache Spark", "Apache Airflow", "dbt", "Apache Kafka"],
                "key_concepts": ["Performance tuning", "Streaming", "Orchestration", "Analytics engineering"]
            },
            "Week 3": {
                "title": "Data Storage & Quality",
                "days": {
                    15: "Database Performance & Optimization",
                    16: "Object Storage & Data Lake Optimization", 
                    17: "Data Quality Frameworks",
                    18: "Data Governance & Compliance",
                    19: "Amazon EMR & Advanced Analytics",
                    20: "Amazon Athena Query Optimization", 
                    21: "Week 3 Review & Data Architecture Design"
                },
                "technologies": ["PostgreSQL", "S3", "Amazon EMR", "Amazon Athena"],
                "key_concepts": ["Data quality", "Governance", "Query optimization", "Storage optimization"]
            },
            "Week 4": {
                "title": "DevOps & Infrastructure",
                "days": {
                    22: "Infrastructure as Code with Terraform",
                    23: "Docker & Kubernetes for Data Workloads",
                    24: "CI/CD for Data Applications", 
                    25: "Monitoring & Observability",
                    26: "Cost Optimization & FinOps",
                    27: "Production Operations & SRE",
                    28: "Week 4 Review & Production Deployment"
                },
                "technologies": ["Terraform", "Docker", "Kubernetes", "CI/CD"],
                "key_concepts": ["Infrastructure as Code", "Containerization", "Monitoring", "Cost optimization"]
            },
            "Week 5": {
                "title": "Leadership & Advanced Topics",
                "days": {
                    29: "Technical Leadership & Mentoring",
                    30: "System Design at Scale",
                    31: "Emerging Technologies Research",
                    32: "Business Impact & Strategy",
                    33: "Open Source Contribution", 
                    34: "Industry Networking & Knowledge Sharing",
                    35: "Week 5 Review & Leadership Assessment"
                },
                "technologies": ["Leadership Skills", "System Design", "Emerging Tech"],
                "key_concepts": ["Technical leadership", "Scalability", "Business strategy", "Community contribution"]
            },
            "Week 6": {
                "title": "Interview Preparation & Portfolio",
                "days": {
                    36: "Technical Interview Preparation",
                    37: "System Design Interview Mastery",
                    38: "Behavioral Interview Preparation",
                    39: "Portfolio Development & Documentation",
                    40: "Mock Interviews & Final Preparation",
                    41: "Company Research & Application Strategy", 
                    42: "Program Completion & Final Assessment"
                },
                "technologies": ["Interview Skills", "Portfolio Development"],
                "key_concepts": ["Technical interviews", "System design", "Behavioral interviews", "Portfolio"]
            }
        }
    
    def analyze_learning_progress(self, topic: str, current_understanding: str, 
                                time_spent: str, week: int, day: int) -> str:
        """Analyze learning progress with curriculum context"""
        
        week_info = self.curriculum_structure.get(f"Week {week}", {})
        day_topic = week_info.get("days", {}).get(day, "Unknown")
        week_technologies = week_info.get("technologies", [])
        key_concepts = week_info.get("key_concepts", [])
        
        prompt = f"""You are an expert data engineering mentor working with a student following a structured 6-week staff-level curriculum.

CURRICULUM CONTEXT:
- Week {week}: {week_info.get('title', 'Unknown')}
- Day {day}: {day_topic}
- Week Technologies: {', '.join(week_technologies)}
- Key Concepts: {', '.join(key_concepts)}

STUDENT STATUS:
- Current Topic: {topic}
- Understanding Level: {current_understanding}
- Time Spent: {time_spent}

Provide a comprehensive learning analysis including:

1. **Progress Assessment**: How well are they progressing for Day {day} of Week {week}?
2. **Curriculum Alignment**: How does their current understanding align with expected outcomes?
3. **Technology Mastery**: Specific guidance on {topic} within the broader curriculum context
4. **Next Steps**: Concrete actions for tomorrow and the rest of the week
5. **Integration Opportunities**: How this topic connects to other technologies in their curriculum
6. **Practice Recommendations**: Specific hands-on exercises aligned with their learning plan
7. **Potential Challenges**: Common pitfalls for this stage of learning
8. **Success Metrics**: How to measure progress and readiness for next topics

Be specific, encouraging, and provide actionable guidance that considers their position in the overall curriculum."""

        return self.query_ollama(prompt)
    
    def review_code_for_curriculum(self, code: str, technology: str, 
                                 week: int, learning_objective: str) -> str:
        """Review code with curriculum-specific guidance"""
        
        week_info = self.curriculum_structure.get(f"Week {week}", {})
        week_technologies = week_info.get("technologies", [])
        key_concepts = week_info.get("key_concepts", [])
        
        prompt = f"""As a senior data engineering mentor, review this {technology} code for a student in Week {week} of their staff-level curriculum.

CURRICULUM CONTEXT:
- Week Focus: {week_info.get('title', 'Unknown')}
- Week Technologies: {', '.join(week_technologies)}
- Key Concepts: {', '.join(key_concepts)}
- Learning Objective: {learning_objective}

CODE TO REVIEW:
```{technology.lower()}
{code}
```

Provide comprehensive feedback:

1. **Code Quality Assessment**: 
   - Syntax and structure
   - Best practices adherence
   - Staff-level expectations

2. **Curriculum Alignment**:
   - How well does this demonstrate Week {week} concepts?
   - Integration with other technologies in their learning path

3. **Performance & Optimization**:
   - Specific to {technology} best practices
   - Scalability considerations for staff-level work

4. **Learning Enhancement**:
   - Concepts they should understand from this code
   - Connections to other curriculum topics
   - Areas for deeper exploration

5. **Next Level Challenges**:
   - How to extend this code for advanced learning
   - Integration opportunities with other Week {week} technologies

6. **Interview Readiness**:
   - How this code demonstrates staff-level skills
   - Potential interview questions about this implementation

Be detailed, educational, and connect feedback to their overall learning journey."""

        # Use DeepSeek-Coder for code review if available
        code_model = None
        for model in self.available_models:
            if 'deepseek-coder' in model or 'codellama' in model:
                code_model = model
                break
        
        return self.query_ollama(prompt, model=code_model or self.selected_model)
    
    def generate_practice_scenario(self, week: int, day: int, 
                                 skill_level: str, available_time: str) -> str:
        """Generate practice scenarios based on curriculum position"""
        
        week_info = self.curriculum_structure.get(f"Week {week}", {})
        day_topic = week_info.get("days", {}).get(day, "Unknown")
        technologies = week_info.get("technologies", [])
        key_concepts = week_info.get("key_concepts", [])
        
        prompt = f"""Create a hands-on practice scenario for a student on Day {day} of Week {week} in their data engineering curriculum.

CURRICULUM CONTEXT:
- Week Theme: {week_info.get('title', 'Unknown')}
- Today's Focus: {day_topic}
- Technologies: {', '.join(technologies)}
- Key Concepts: {', '.join(key_concepts)}
- Student Level: {skill_level}
- Available Time: {available_time}

Create a realistic scenario that includes:

1. **Business Context**: 
   - Realistic company scenario requiring today's technologies
   - Clear business requirements and constraints

2. **Technical Challenge**:
   - Specific use of Day {day} technologies
   - Integration with previous week's learning
   - Appropriate complexity for {skill_level} level

3. **Step-by-Step Implementation**:
   - Detailed tasks that can be completed in {available_time}
   - Progressive difficulty building on curriculum foundation

4. **Learning Objectives**:
   - Specific skills this scenario will reinforce
   - Connections to upcoming curriculum topics

5. **Validation & Testing**:
   - How to verify successful implementation
   - Performance benchmarks appropriate for staff-level work

6. **Extension Opportunities**:
   - How to expand this scenario for deeper learning
   - Integration with other curriculum technologies

7. **Real-World Application**:
   - How this scenario reflects actual staff-level responsibilities
   - Interview talking points from this exercise

Make it engaging, practical, and directly aligned with their curriculum progression."""

        return self.query_ollama(prompt)
    
    def explain_concept_in_context(self, concept: str, week: int, 
                                 current_level: str, learning_style: str) -> str:
        """Explain concepts with curriculum context"""
        
        week_info = self.curriculum_structure.get(f"Week {week}", {})
        technologies = week_info.get("technologies", [])
        key_concepts = week_info.get("key_concepts", [])
        
        prompt = f"""Explain {concept} to a {current_level} student in Week {week} of their data engineering curriculum, using {learning_style} approach.

CURRICULUM CONTEXT:
- Week Theme: {week_info.get('title', 'Unknown')}
- Week Technologies: {', '.join(technologies)}
- Week Key Concepts: {', '.join(key_concepts)}

Provide comprehensive explanation:

1. **Core Concept**:
   - Clear definition tailored to {current_level} level
   - Why this concept matters in Week {week} context

2. **Curriculum Integration**:
   - How {concept} connects to current week's technologies
   - Relationships to previous learning
   - Foundation for upcoming concepts

3. **Practical Application**:
   - Real-world examples using {', '.join(technologies)}
   - Hands-on demonstrations appropriate for their level

4. **Learning Style Adaptation**:
   - Explanation optimized for {learning_style} learning
   - Multiple perspectives and approaches

5. **Common Misconceptions**:
   - Typical misunderstandings at {current_level} level
   - Clear clarifications and corrections

6. **Progression Path**:
   - What to master first vs. advanced topics
   - Connection to staff-level responsibilities

7. **Practice Opportunities**:
   - Specific exercises using curriculum technologies
   - Integration with current week's learning objectives

Make it comprehensive yet accessible, with clear connections to their learning journey."""

        return self.query_ollama(prompt)
    
    def assess_skills_for_week(self, week: int, self_assessment: Dict[str, int]) -> str:
        """Assess skills specific to curriculum week"""
        
        week_info = self.curriculum_structure.get(f"Week {week}", {})
        technologies = week_info.get("technologies", [])
        key_concepts = week_info.get("key_concepts", [])
        
        prompt = f"""Assess skills for Week {week} of the data engineering curriculum based on self-assessment scores.

WEEK CONTEXT:
- Week Theme: {week_info.get('title', 'Unknown')}
- Expected Technologies: {', '.join(technologies)}
- Key Concepts: {', '.join(key_concepts)}

SELF-ASSESSMENT SCORES (1-10 scale):
{json.dumps(self_assessment, indent=2)}

Provide detailed assessment:

1. **Readiness Analysis**:
   - Are they ready for Week {week} challenges?
   - Specific skill gaps that need attention

2. **Technology Alignment**:
   - How well prepared are they for {', '.join(technologies)}?
   - Priority areas for skill development

3. **Learning Strategy**:
   - Recommended focus areas for this week
   - Time allocation suggestions

4. **Risk Assessment**:
   - Potential challenges based on current skills
   - Mitigation strategies

5. **Acceleration Opportunities**:
   - Areas where they could move faster
   - Advanced topics they could explore

6. **Support Recommendations**:
   - Additional resources needed
   - Community engagement suggestions

7. **Success Metrics**:
   - How to measure progress this week
   - Target skill levels by week end

Be honest about readiness while providing actionable improvement strategies."""

        return self.query_ollama(prompt)
    
    def generate_interview_questions(self, week: int, focus_area: str) -> str:
        """Generate interview questions based on curriculum progress"""
        
        completed_weeks = list(range(1, week + 1))
        all_technologies = []
        all_concepts = []
        
        for w in completed_weeks:
            week_info = self.curriculum_structure.get(f"Week {w}", {})
            all_technologies.extend(week_info.get("technologies", []))
            all_concepts.extend(week_info.get("key_concepts", []))
        
        prompt = f"""Generate staff-level interview questions for someone who has completed {week} weeks of the data engineering curriculum.

COMPLETED LEARNING:
- Technologies Covered: {', '.join(set(all_technologies))}
- Concepts Mastered: {', '.join(set(all_concepts))}
- Focus Area: {focus_area}

Create interview questions in these categories:

1. **Technical Deep Dive** (3-4 questions):
   - Advanced questions about technologies they've learned
   - Staff-level complexity and depth

2. **System Design** (2-3 scenarios):
   - Use technologies from their curriculum
   - Scale and complexity appropriate for staff-level

3. **Trade-offs & Decision Making** (2-3 questions):
   - When to use different technologies they've learned
   - Real-world decision-making scenarios

4. **Problem Solving** (2-3 scenarios):
   - Debugging and optimization challenges
   - Based on their curriculum technologies

5. **Leadership & Communication** (2-3 questions):
   - Technical mentoring scenarios
   - Explaining complex concepts

For each question, provide:
- The question itself
- Key points expected in a strong answer
- Follow-up questions
- How this relates to their curriculum learning

Focus on questions that would be asked in actual staff-level data engineering interviews."""

        return self.query_ollama(prompt)
    
    def save_progress(self, progress: LearningProgress):
        """Save learning progress to file"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"progress": []}
            
            # Update or add progress
            updated = False
            for i, p in enumerate(data["progress"]):
                if p["topic"] == progress.topic and p["week"] == progress.week and p["day"] == progress.day:
                    data["progress"][i] = asdict(progress)
                    updated = True
                    break
            
            if not updated:
                data["progress"].append(asdict(progress))
            
            with open(self.progress_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            st.error(f"Error saving progress: {str(e)}")
    
    def load_progress(self) -> List[LearningProgress]:
        """Load learning progress from file"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                return [LearningProgress(**p) for p in data.get("progress", [])]
            return []
        except Exception as e:
            st.error(f"Error loading progress: {str(e)}")
            return []

def main():
    """Main Streamlit application"""
    
    # Initialize agent
    if 'agent' not in st.session_state:
        st.session_state.agent = OllamaLearningAgent()
    
    agent = st.session_state.agent
    
    # Header
    st.title("🤖 Data Engineering Learning Agent (Ollama)")
    st.markdown("*Powered by your local Ollama models - completely free!*")
    
    # Sidebar setup
    with st.sidebar:
        st.header("🔧 Ollama Setup")
        
        # Check Ollama connection
        if st.button("🔍 Check Ollama Connection"):
            if agent.check_ollama_connection():
                st.success(f"✅ Connected! Found {len(agent.available_models)} models")
            else:
                st.error("❌ Cannot connect to Ollama")
                st.info("Make sure Ollama is running: `ollama serve`")
        
        # Model selection
        if agent.available_models:
            st.subheader("🧠 Select Model")
            
            # Model recommendations
            model_info = {
                'deepseek-coder': '🚀 Best for code review',
                'codellama': '💻 Great for coding tasks', 
                'llama3.2': '🎯 Good all-around choice',
                'mistral': '⚡ Fast and efficient'
            }
            
            model_options = []
            for model in agent.available_models:
                info = ""
                for key, desc in model_info.items():
                    if key in model:
                        info = f" {desc}"
                        break
                model_options.append(f"{model}{info}")
            
            selected_option = st.selectbox("Choose model:", model_options, index=0)
            agent.selected_model = selected_option.split(' ')[0]  # Extract model name
            
            st.info(f"Using: **{agent.selected_model}**")
        else:
            st.warning("No models found. Check Ollama connection.")
            
        st.markdown("---")
        
        # Navigation
        st.header("🧭 Navigation")
        page = st.selectbox("Choose your learning tool:", [
            "📊 Progress Dashboard",
            "📈 Learning Analysis", 
            "👨‍💻 Code Review",
            "🎯 Practice Scenarios",
            "💡 Concept Explanation",
            "🏆 Skills Assessment",
            "💼 Interview Prep"
        ])
        
        st.markdown("---")
        
        # Quick stats
        st.header("📈 Quick Stats")
        progress_data = agent.load_progress()
        if progress_data:
            total_hours = sum(p.time_spent_hours for p in progress_data)
            avg_confidence = sum(p.confidence_level for p in progress_data) / len(progress_data)
            completed_topics = len([p for p in progress_data if p.completion_percentage >= 80])
            
            st.metric("Total Study Hours", f"{total_hours:.1f}")
            st.metric("Average Confidence", f"{avg_confidence:.1f}/10")
            st.metric("Completed Topics", completed_topics)
        else:
            st.info("Start tracking your progress to see stats!")
    
    # Main content area
    if not agent.available_models:
        st.warning("⚠️ Please check your Ollama connection first.")
        st.markdown("""
        ### Getting Started with Ollama
        
        1. **Make sure Ollama is running:**
           ```bash
           ollama serve
           ```
        
        2. **Click "Check Ollama Connection"** in the sidebar
        
        3. **Select a model** and start learning!
        
        ### Your Available Models
        You have these great models installed:
        - **deepseek-coder** - Excellent for code review and programming tasks
        - **codellama** - Great for coding and technical explanations  
        - **llama3.2** - Good all-around model for learning guidance
        - **mistral** - Fast and efficient for quick questions
        
        ### About This Agent
        This AI learning agent is specifically designed to enhance your experience with the 
        [Data Engineering Staff Learning Plan](https://github.com/cookiee01/data-engineering-staff-learning-plan).
        
        **Features:**
        - 📊 Progress tracking aligned with the 6-week curriculum
        - 🧠 Intelligent analysis based on your current week/day
        - 👨‍💻 Code review for curriculum technologies
        - 🎯 Practice scenarios tailored to your learning stage
        - 💡 Concept explanations with curriculum context
        - 🏆 Skills assessment for interview readiness
        - 🆓 **Completely free** - runs on your local machine!
        """)
        return
    
    if not agent.selected_model:
        st.info("Please select a model in the sidebar to get started.")
        return
    
    # Page content
    if page == "📊 Progress Dashboard":
        show_progress_dashboard(agent)
    elif page == "📈 Learning Analysis":
        show_learning_analysis(agent)
    elif page == "👨‍💻 Code Review":
        show_code_review(agent)
    elif page == "🎯 Practice Scenarios":
        show_practice_scenarios(agent)
    elif page == "💡 Concept Explanation":
        show_concept_explanation(agent)
    elif page == "🏆 Skills Assessment":
        show_skills_assessment(agent)
    elif page == "💼 Interview Prep":
        show_interview_prep(agent)

# Copy all the show_ functions from the original file with minor modifications for Ollama
def show_progress_dashboard(agent):
    """Show progress dashboard"""
    st.header("📊 Learning Progress Dashboard")
    
    progress_data = agent.load_progress()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📅 Curriculum Overview")
        
        # Show curriculum structure
        for week_num in range(1, 7):
            week_key = f"Week {week_num}"
            week_info = agent.curriculum_structure.get(week_key, {})
            
            with st.expander(f"**{week_key}: {week_info.get('title', 'Unknown')}**"):
                days = week_info.get('days', {})
                technologies = week_info.get('technologies', [])
                
                st.write(f"**Technologies:** {', '.join(technologies)}")
                st.write("**Daily Schedule:**")
                for day, topic in days.items():
                    # Check if this day is completed
                    day_progress = [p for p in progress_data 
                                  if p.week == week_num and p.day == day]
                    status = "✅" if day_progress and day_progress[0].completion_percentage >= 80 else "⏳"
                    st.write(f"  {status} Day {day}: {topic}")
    
    with col2:
        st.subheader("📊 Progress Summary")
        
        if progress_data:
            # Create progress visualization
            df = pd.DataFrame([asdict(p) for p in progress_data])
            
            # Weekly progress chart
            weekly_progress = df.groupby('week')['completion_percentage'].mean()
            fig = px.bar(
                x=weekly_progress.index, 
                y=weekly_progress.values,
                title="Weekly Completion %",
                labels={'x': 'Week', 'y': 'Completion %'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Confidence levels
            confidence_by_week = df.groupby('week')['confidence_level'].mean()
            fig2 = px.line(
                x=confidence_by_week.index,
                y=confidence_by_week.values,
                title="Confidence Level by Week",
                labels={'x': 'Week', 'y': 'Confidence (1-10)'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No progress data yet. Start logging your learning!")
    
    # Add new progress entry
    st.markdown("---")
    st.subheader("➕ Log Learning Progress")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        week = st.selectbox("Week", list(range(1, 7)))
        day = st.selectbox("Day", list(range(1, 8)))
        
    with col2:
        topic = st.text_input("Topic/Technology", 
                            placeholder="e.g., Apache Iceberg basics")
        completion = st.slider("Completion %", 0, 100, 50)
        
    with col3:
        hours = st.number_input("Hours Spent", 0.0, 24.0, 2.0, 0.5)
        confidence = st.slider("Confidence Level", 1, 10, 5)
    
    notes = st.text_area("Notes (optional)", 
                        placeholder="Key learnings, challenges, next steps...")
    
    if st.button("💾 Save Progress"):
        progress = LearningProgress(
            topic=topic,
            week=week,
            day=day,
            completion_percentage=completion,
            time_spent_hours=hours,
            confidence_level=confidence,
            last_updated=datetime.now().isoformat(),
            notes=notes
        )
        agent.save_progress(progress)
        st.success("✅ Progress saved!")
        st.rerun()

def show_learning_analysis(agent):
    """Show learning analysis page"""
    st.header("📈 Personalized Learning Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        week = st.selectbox("Current Week", list(range(1, 7)), index=0)
        day = st.selectbox("Current Day", list(range(1, 8)), index=0)
        
    with col2:
        topic = st.text_input("What are you learning today?",
                            placeholder="e.g., Delta Lake time travel")
        time_spent = st.text_input("Time spent so far",
                                 placeholder="e.g., 3 hours over 2 days")
    
    understanding = st.text_area("Describe your current understanding:",
                                placeholder="What you've learned, what's confusing, specific challenges...")
    
    if st.button("🧠 Get Personalized Analysis"):
        if topic and understanding:
            with st.spinner(f"🤖 {agent.selected_model} is analyzing your learning progress..."):
                analysis = agent.analyze_learning_progress(
                    topic, understanding, time_spent, week + 1, day + 1
                )
                st.markdown(analysis)
        else:
            st.warning("Please fill in the topic and understanding fields.")

def show_code_review(agent):
    """Show code review page"""
    st.header("👨‍💻 Code Review & Learning")
    
    # Show which model will be used for code review
    code_model = None
    for model in agent.available_models:
        if 'deepseek-coder' in model or 'codellama' in model:
            code_model = model
            break
    
    if code_model:
        st.info(f"🚀 Using **{code_model}** for enhanced code review")
    else:
        st.info(f"Using **{agent.selected_model}** for code review")
    
    col1, col2 = st.columns(2)
    
    with col1:
        technology = st.selectbox("Technology/Language:", [
            "PySpark", "SQL", "Python ETL", "Scala Spark",
            "Airflow DAG", "dbt", "Terraform", "Docker",
            "Delta Lake", "Apache Iceberg", "Kafka", "Flink"
        ])
        week = st.selectbox("Current Week", list(range(1, 7)), index=0)
        
    with col2:
        learning_objective = st.text_input("Learning Objective",
                                         placeholder="e.g., Optimize Spark job performance")
    
    code = st.text_area("Paste your code here:", 
                       height=300,
                       placeholder="# Your code here...\n# Be sure to include relevant context")
    
    if st.button("🔍 Get Code Review"):
        if code and technology:
            model_name = code_model or agent.selected_model
            with st.spinner(f"🤖 {model_name} is reviewing your code..."):
                review = agent.review_code_for_curriculum(
                    code, technology, week + 1, learning_objective
                )
                st.markdown(review)
        else:
            st.warning("Please provide both code and technology selection.")

def show_practice_scenarios(agent):
    """Show practice scenarios page"""
    st.header("🎯 Hands-on Practice Scenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        week = st.selectbox("Week", list(range(1, 7)), index=0)
        day = st.selectbox("Day", list(range(1, 8)), index=0)
        
    with col2:
        skill_level = st.selectbox("Your Skill Level:", [
            "Beginner", "Intermediate", "Advanced", "Expert"
        ], index=1)
        available_time = st.selectbox("Available Time:", [
            "30 minutes", "1 hour", "2-3 hours", "Half day", "Full day"
        ], index=1)
    
    if st.button("🎯 Generate Practice Scenario"):
        with st.spinner(f"🤖 {agent.selected_model} is creating your personalized scenario..."):
            scenario = agent.generate_practice_scenario(
                week + 1, day + 1, skill_level, available_time
            )
            st.markdown(scenario)

def show_concept_explanation(agent):
    """Show concept explanation page"""
    st.header("💡 Concept Explanation with Context")
    
    col1, col2 = st.columns(2)
    
    with col1:
        concept = st.text_input("Concept to explain:",
                              placeholder="e.g., ACID transactions in Delta Lake")
        week = st.selectbox("Current Week", list(range(1, 7)), index=0)
        
    with col2:
        current_level = st.selectbox("Your current level with this concept:", [
            "Complete beginner", "Some familiarity", "Intermediate", "Advanced"
        ], index=1)
        learning_style = st.selectbox("Preferred learning style:", [
            "Visual with diagrams", "Step-by-step logical", "Real-world examples",
            "Hands-on practical", "Theoretical deep-dive"
        ], index=2)
    
    if st.button("💡 Get Explanation"):
        if concept:
            with st.spinner(f"🤖 {agent.selected_model} is crafting your explanation..."):
                explanation = agent.explain_concept_in_context(
                    concept, week + 1, current_level, learning_style
                )
                st.markdown(explanation)
        else:
            st.warning("Please enter a concept to explain.")

def show_skills_assessment(agent):
    """Show skills assessment page"""
    st.header("🏆 Skills Assessment for Current Week")
    
    week = st.selectbox("Assess skills for Week", list(range(1, 7)), index=0)
    week_info = agent.curriculum_structure.get(f"Week {week + 1}", {})
    
    st.write(f"**Week {week + 1}: {week_info.get('title', 'Unknown')}**")
    st.write(f"**Technologies**: {', '.join(week_info.get('technologies', []))}")
    
    st.subheader("Rate your current skills (1-10 scale):")
    
    # Dynamic skill assessment based on week
    skills = {}
    technologies = week_info.get('technologies', [])
    key_concepts = week_info.get('key_concepts', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Technologies:**")
        for tech in technologies:
            skills[tech] = st.slider(f"{tech}", 1, 10, 5, key=f"tech_{tech}")
    
    with col2:
        st.write("**Key Concepts:**")
        for concept in key_concepts:
            skills[concept] = st.slider(f"{concept}", 1, 10, 5, key=f"concept_{concept}")
    
    if st.button("📊 Get Skills Assessment"):
        with st.spinner(f"🤖 {agent.selected_model} is assessing your skills..."):
            assessment = agent.assess_skills_for_week(week + 1, skills)
            st.markdown(assessment)

def show_interview_prep(agent):
    """Show interview preparation page"""
    st.header("💼 Interview Preparation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weeks_completed = st.selectbox("Weeks of curriculum completed", 
                                     list(range(1, 7)), index=2)
        
    with col2:
        focus_area = st.selectbox("Interview focus area:", [
            "Technical Deep Dive", "System Design", "Behavioral Questions",
            "Code Review", "Architecture Decisions", "Leadership Scenarios"
        ])
    
    if st.button("🎯 Generate Interview Questions"):
        with st.spinner(f"🤖 {agent.selected_model} is creating interview questions..."):
            questions = agent.generate_interview_questions(weeks_completed, focus_area)
            st.markdown(questions)

if __name__ == "__main__":
    main()
