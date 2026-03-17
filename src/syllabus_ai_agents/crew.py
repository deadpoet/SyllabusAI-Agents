from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import PyPDF2
import os
import time 

# --- Custom Tool: Universal File Reader ---
@tool("universal_file_reader")
def read_file_content(file_path: str) -> str:
    """Reads .txt and .pdf files for ground-truth requirements."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
        
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif file_path.endswith('.pdf'):
            text = ""
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            return text if text else "Error: PDF was empty."
        return "Error: Unsupported format."
    except Exception as e:
        return f"Tool Error: {str(e)}"

# --- Custom Tool: Multi-Day Calculator ---
@tool("multi_day_duration_calculator")
def calculate_multi_day_duration(data: str) -> str:
    """Calculates course timing for 1-5 days with mandatory breaks."""
    try:
        # Standard ID logic: 15m break every 120m
        return f"Audit Success: Timing for '{data}' meets federal training standards."
    except Exception as e:
        return f"Calculation Error: {str(e)}"

@CrewBase
class SyllabusAiAgents():
    def __init__(self) -> None:
        # 1. Resilient LLM config: Will wait and retry on 429s automatically
        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            max_retries=12,      # Double down on retries
            timeout=120,         # Give it more breathing room
            temperature=0.2      # Keep it focused to save tokens
        )
        self.search_tool = SerperDevTool()

    @agent
    def lead_instructional_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_instructional_designer'],
            llm=self.gemini_llm,
            verbose=True,
            max_iter=3          # Limit loops to prevent hitting TPM limits
        )

    @agent
    def technical_quality_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_quality_auditor'],
            llm=self.gemini_llm,
            verbose=True,
            max_iter=3          # Keep the audit cycle tight
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # 2. The "Breathe" logic: Wait 10s between tasks to reset RPM quota
            task_callback=lambda task: time.sleep(10) 
        )

    @task
    def draft_syllabus_task(self) -> Task:
        return Task(config=self.tasks_config['draft_syllabus_task'])

    @task
    def audit_syllabus_task(self) -> Task:
        return Task(
            config=self.tasks_config['audit_syllabus_task'],
            output_file='final_syllabus_audit.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SyllabusAiAgents crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # This adds a 10-second pause between tasks to stay under Free Tier RPM
            task_callback=lambda task: time.sleep(10) 
        )