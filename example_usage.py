#!/usr/bin/env python3
"""
Example usage of the Data Engineering Learning Agent

This script demonstrates how to use the agent programmatically
for automated learning sessions, batch analysis, or integration
with other tools.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_engineering_agent import DataEngineeringLearningAgent, LearningProgress

def example_learning_session():
    """Example of a complete learning session with the agent"""
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ Please set ANTHROPIC_API_KEY in your .env file")
        return
    
    # Initialize agent
    print("🚀 Initializing Data Engineering Learning Agent...")
    agent = DataEngineeringLearningAgent()
    
    if not agent.initialize_claude(api_key):
        print("❌ Failed to initialize Claude")
        return
    
    print("✅ Agent initialized successfully!")
    print()
    
    # Example 1: Learning Analysis
    print("📈 Example 1: Learning Analysis")
    print("-" * 40)
    
    analysis = agent.analyze_learning_progress(
        topic="Apache Iceberg table evolution",
        current_understanding="I understand the basics of table formats but struggling with schema evolution and branching features",
        time_spent="4 hours over 2 days",
        week=1,
        day=2
    )
    
    print("Agent Analysis:")
    print(analysis)
    print()
    
    # Example 2: Code Review
    print("👨‍💻 Example 2: Code Review")
    print("-" * 40)
    
    sample_code = """
    from pyspark.sql import SparkSession
    from delta.tables import DeltaTable
    
    spark = SparkSession.builder.appName("DeltaExample").getOrCreate()
    
    # Read data
    df = spark.read.format("delta").load("/path/to/delta-table")
    
    # Simple transformation
    result = df.groupBy("category").sum("amount")
    
    # Write back
    result.write.format("delta").mode("overwrite").save("/path/to/output")
    """
    
    review = agent.review_code_for_curriculum(
        code=sample_code,
        technology="PySpark",
        week=1,
        learning_objective="Learn Delta Lake operations and performance optimization"
    )
    
    print("Code Review:")
    print(review)
    print()
    
    # Example 3: Practice Scenario Generation
    print("🎯 Example 3: Practice Scenario")
    print("-" * 40)
    
    scenario = agent.generate_practice_scenario(
        week=2,
        day=3,
        skill_level="Intermediate",
        available_time="2-3 hours"
    )
    
    print("Practice Scenario:")
    print(scenario)
    print()
    
    # Example 4: Concept Explanation
    print("💡 Example 4: Concept Explanation")
    print("-" * 40)
    
    explanation = agent.explain_concept_in_context(
        concept="ACID transactions in data lakes",
        week=1,
        current_level="Some familiarity",
        learning_style="Real-world examples"
    )
    
    print("Concept Explanation:")
    print(explanation)
    print()
    
    # Example 5: Skills Assessment
    print("🏆 Example 5: Skills Assessment")
    print("-" * 40)
    
    # Mock self-assessment scores
    self_assessment = {
        "Apache Iceberg": 6,
        "Delta Lake": 7,
        "AWS Glue": 4,
        "Spark": 8,
        "ACID transactions": 5,
        "Time travel": 3,
        "Schema evolution": 4,
        "Table formats": 6
    }
    
    assessment = agent.assess_skills_for_week(1, self_assessment)
    
    print("Skills Assessment:")
    print(assessment)
    print()
    
    # Example 6: Progress Tracking
    print("📊 Example 6: Progress Tracking")
    print("-" * 40)
    
    # Create and save progress entry
    progress = LearningProgress(
        topic="Apache Iceberg advanced features",
        week=1,
        day=2,
        completion_percentage=75,
        time_spent_hours=3.5,
        confidence_level=7,
        last_updated=datetime.now().isoformat(),
        notes="Completed time travel and schema evolution labs. Need more practice with branching."
    )
    
    agent.save_progress(progress)
    print("✅ Progress saved successfully!")
    
    # Load and display progress
    all_progress = agent.load_progress()
    print(f"📈 Total logged sessions: {len(all_progress)}")
    
    if all_progress:
        total_hours = sum(p.time_spent_hours for p in all_progress)
        avg_confidence = sum(p.confidence_level for p in all_progress) / len(all_progress)
        print(f"⏱️  Total study time: {total_hours:.1f} hours")
        print(f"🎯 Average confidence: {avg_confidence:.1f}/10")
    
    print()
    print("🎉 Example session completed!")

def batch_analysis_example():
    """Example of batch analysis for multiple topics"""
    
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ Please set ANTHROPIC_API_KEY in your .env file")
        return
    
    agent = DataEngineeringLearningAgent()
    agent.initialize_claude(api_key)
    
    # Topics to analyze
    topics = [
        ("Apache Kafka basics", "Understanding producers and consumers", "2 hours", 2, 5),
        ("Airflow DAG design", "Creating complex workflows with dependencies", "3 hours", 2, 3),
        ("dbt models", "Building incremental models and tests", "2.5 hours", 2, 4)
    ]
    
    print("📊 Batch Learning Analysis")
    print("=" * 50)
    
    for i, (topic, understanding, time_spent, week, day) in enumerate(topics, 1):
        print(f"\n🔍 Analysis {i}: {topic}")
        print("-" * 30)
        
        analysis = agent.analyze_learning_progress(topic, understanding, time_spent, week, day)
        
        # Extract key recommendations (simplified)
        lines = analysis.split('\n')
        key_points = [line for line in lines if any(keyword in line.lower() 
                     for keyword in ['next step', 'recommend', 'focus', 'practice'])]
        
        print("Key Recommendations:")
        for point in key_points[:3]:  # Show top 3 recommendations
            if point.strip():
                print(f"  • {point.strip()}")
        
        print()

def interview_prep_example():
    """Example of interview preparation workflow"""
    
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ Please set ANTHROPIC_API_KEY in your .env file")
        return
    
    agent = DataEngineeringLearningAgent()
    agent.initialize_claude(api_key)
    
    print("💼 Interview Preparation Example")
    print("=" * 40)
    
    # Generate questions for someone who completed 3 weeks
    questions = agent.generate_interview_questions(
        week=3,
        focus_area="System Design"
    )
    
    print("Generated Interview Questions:")
    print(questions)

if __name__ == "__main__":
    print("🎯 Data Engineering Learning Agent - Example Usage")
    print("=" * 60)
    print()
    
    # Check if API key is available
    load_dotenv()
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  To run these examples, please:")
        print("1. Copy .env.template to .env")
        print("2. Add your Claude API key to the .env file")
        print("3. Run this script again")
        print()
        sys.exit(1)
    
    choice = input("Choose an example to run:\n"
                  "1. Complete learning session\n"
                  "2. Batch analysis\n"
                  "3. Interview preparation\n"
                  "Enter choice (1-3): ")
    
    print()
    
    if choice == "1":
        example_learning_session()
    elif choice == "2":
        batch_analysis_example()
    elif choice == "3":
        interview_prep_example()
    else:
        print("Invalid choice. Running complete learning session...")
        example_learning_session()
