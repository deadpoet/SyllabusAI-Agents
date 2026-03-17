#!/usr/bin/env python
import sys
import os
import time
from dotenv import load_dotenv

# 1. LOAD ENV FIRST
# This finds the directory where the terminal is currently standing
# which should be /Users/gerrysoco/Python/syllabus_ai_agents
current_dir = os.getcwd()
env_path = os.path.join(current_dir, '.env')

# Force load from the absolute path
load_dotenv(dotenv_path=env_path)

def run():
    # ... existing logic ...
    if not os.getenv("GOOGLE_API_KEY"):
        print(f"❌ Configuration Error: GOOGLE_API_KEY not found.")
        print(f"Attempted to load from: {env_path}") # This will tell us the truth
        print(f"File exists at that path: {os.path.exists(env_path)}")
        sys.exit(1)
        
# 2. IMPORT CREW SECOND
try:
    from syllabus_ai_agents.crew import SyllabusAiAgents
except ImportError as e:
    print(f"❌ Import Error: Could not find SyllabusAiAgents. {e}")
    sys.exit(1)

def run():
    """
    Run the SyllabusAI Crew.
    Usage: uv run run_crew <file_path> <training_type> <duration_days>
    Example: uv run run_crew requirements.txt VLT 3
    """
    try:
        # Check for required API key immediately after loading env
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in .env or system environment.")

        # 3. Capture inputs with defaults for SAM/ADDIE flexibility
        # Arg 1: File path or topic string
        file_path = sys.argv[1] if len(sys.argv) > 1 else "sample_requirements.txt"
        
        # Arg 2: Training Type (ILT, VLT, Self-Study, Microlearning)
        training_type = sys.argv[2] if len(sys.argv) > 2 else "ILT" 
        
        # Arg 3: Duration (1 to 5 days)
        duration_days = sys.argv[3] if len(sys.argv) > 3 else "1"

        # Check if the input is a valid file path on your system
        if os.path.exists(file_path):
            topic_content = f"the technical requirements documented in the file: {file_path}"
        else:
            topic_content = file_path

        # 4. Define the inputs for the tasks.yaml variables
        inputs = {
            'topic': topic_content,
            'training_type': training_type,
            'duration_days': duration_days
        }

        print(f"🚀 Initializing SyllabusAI Workflow...")
        print(f"📋 Target: {topic_content}")
        print(f"🛠  Format: {training_type} | Duration: {duration_days} Day(s)")
        
        # Initialize and kickoff the crew
        SyllabusAiAgents().crew().kickoff(inputs=inputs)
        
    except ValueError as ve:
        print(f"❌ Configuration Error: {ve}")
    except Exception as e:
        print(f"❌ An error occurred while running the crew: {e}")
        sys.exit(1)

def train():
    """
    Train the crew for a specific number of iterations.
    """
    inputs = {
        "topic": "Technical Documentation Modernization",
        "training_type": "ILT",
        "duration_days": "1"
    }
    try:
        SyllabusAiAgents().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        print(f"❌ Training error: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SyllabusAiAgents().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        print(f"❌ Replay error: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "Technical Documentation Modernization",
        "training_type": "ILT",
        "duration_days": "1"
    }
    try:
        SyllabusAiAgents().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        print(f"❌ Testing error: {e}")

if __name__ == "__main__":
    run()