# SyllabusAI Agents Crew 🎓

**SyllabusAI** is an agentic AI system designed to modernize legacy documentation and automate complex curriculum development. Built with the [crewAI](https://crewai.com) framework and powered by **Gemini 2.0 Flash**, it transforms technical requirements (PDF/DOCX) into structured, timed course outlines for ILT, VILT, and Self-Paced modalities.

# 🛠 Prerequisites

- **Python:** 3.12+ (Successfully tested on **Python 3.14**)
- **Rust Compiler:** Required for `tiktoken` and `pyo3` compilation on macOS Tahoe.
- **Dependency Manager:** [UV](https://docs.astral.sh/uv/) is used for seamless package handling.

# 🚀 Installation & Setup

1. **Install uv:**
   ```bash
   pip3 install uv

2. **Install Dependencies:**
If you are on Python 3.14+, use the ABI3 compatibility flag to ensure the Rust-based components build correctly:

PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 crewai install

3. Configure Environment Variables:
Create a .env file in the root directory (refer to .env.example for the template):

GOOGLE_API_KEY=your_api_key

# 🤖 Agentic Workflows
This crew utilizes a **Primary Designer + Auditor** loop based on the **ADDIE** and **Kirkpatrick** models while ensuring **pedagogical** quality and technical accuracy:
- **Lead Instructional Designer:** Transforms raw technical data into logical learning paths.
- **Technical Quality Auditor:** Enforces rigorous standards, including **Section 508** accessibility and specific federal training break-time regulations.

# 📁 Project Customization
- **Agents:** Modify <em>src/syllabus_ai_agents/config/agents.yaml</em> to refine the Instructional Designer and Auditor personas.
- **Tasks:** Modify <em>src/syllabus_ai_agents/config/tasks.yaml</em> to update drafting and auditing criteria.
- **Logic:** Enhance <em>src/syllabus_ai_agents/crew.py</em> to add custom tools (like the Duration Calculator) or specific arguments.

# 🏃 Running the Project
To initialize the crew and begin the curriculum generation process:

uv run run_crew **{REQUIREMENTS}** **{LEARNING}** **{DAYS}**

##KEYS
### **REQUIREMENTS** The PDF or TXT file containing the training requirements

#### **LEARNING** Choose from one of four Course Types
- **ILT** (Instructor-Led Training): Traditional classroom-based training led by a physical instructor.
- **VILT** (Virtual Instructor-Led Training): Online, instructor-led sessions (often referred to as VLT in your current command line arguments).
- **Self-Paced**: On-demand learning where the student progresses at their own speed without a live instructor.
- **Hybrid**: A blend of the above formats, typically combining self-paced modules with live virtual or in-person sessions.

#### **DAYS** By default, **SyllabusAI** calculates the number of days based on **REQUIREMENTS** and **LEARNING**.
- Optionally, the user can specify the number of days of the course.

- Example1:
*PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 uv run run_crew training1.pdf ILT
- This creates a syllabus from the training1.pdf technical requirements and creates a Instructor-Led Training course. **SyllabusAI** automatically calculates the number of days.

- Example2:
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 uv run run_crew training2.pdf Self-Paced 2
- This creates a syllabus from the training2.txt technical requirements and creates an On-demand learning course of 2-day duration.

- * I use the string PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 because I used Python >3.13.

#### Developed by Gerald Soco Senior Technical Writer & Instructional Design Specialist
