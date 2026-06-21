# Smart Academic Advisor - Kaggle Vibe Coding Capstone

## 🎓 Overview
The **Smart Academic Advisor** is an autonomous AI agent designed to help university students plan their degree progress. Navigating course prerequisites, curriculum requirements, and semester availability can be overwhelming for students. This agent acts as a knowledgeable, strict academic advisor, utilizing the `gemini-2.5-flash` model to analyze student transcripts against university curriculums to provide accurate, data-driven academic advice.

## 🏗️ Technical Architecture & Workflow
The project implements a **Tool-Using Agent** architecture:
1. **User Input:** The user (student) inputs their student ID and an advising question (e.g., "What courses should I take next?").
2. **LLM Processing:** The Gemini model interprets the intent and determines which tools are required to answer the question.
3. **Tool Execution:** The agent autonomously calls bounded Python functions to fetch data from mock JSON databases (`courses.json`, `students.json`, `curriculum.json`).
4. **Synthesis:** The agent cross-references the student's transcript with course prerequisites and master graduation requirements to formulate an accurate, hallucination-free response.

## 🛠️ Tools & APIs Integrated
- **Google GenAI SDK:** Powers the core reasoning loop using `gemini-2.5-flash`.
- **`get_student_transcript(student_id)`**: Retrieves a specific student's passed courses and grades.
- **`get_all_courses()`**: Fetches the university's complete course catalog.
- **`get_course_info(course_id)`**: Retrieves specific details about a course, including its strict prerequisites and the semesters it is offered.
- **`get_degree_requirements(major)`**: Loads the master curriculum plan for specific majors (e.g., Computer Science, Data Science) to calculate remaining graduation credits.

## ⚙️ Setup & Installation
1. **Clone the repository** to your local machine.
2. **Create a Python Environment** (Conda recommended):
   ```bash
   conda create --name Smart_Academic_Advisor python=3.10
   conda activate Smart_Academic_Advisor
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configuration:**
   - Rename the `.env.example` file to `.env`.
   - Add your Gemini API Key to the file: `GEMINI_API_KEY=your_api_key_here`

## 🚀 How to Run
Execute the main agent script from your terminal:
```bash
python agent.py
```
You can then interact with the agent. 

**Example Prompt:**
> *"I am student S101 majoring in Computer Science. Can you list all remaining subjects that I must take to graduate?"*

## 🛡️ Edge Cases Handled (Safety & Guardrails)
- **Anti-Hallucination Guardrails:** If a student asks about graduation requirements but the agent does not have access to their specific major in the curriculum database, the agent will refuse to hallucinate a fake degree plan. It will politely inform the student of its limitations and advise them to speak to a human.
- **Prerequisite Enforcement:** The agent strictly enforces prerequisite chains (e.g., refusing to let a student take Deep Learning if they haven't passed Machine Learning).
- **Graceful Failures:** robust `try/except` blocks in `tools.py` ensure the system catches `FileNotFoundError` exceptions gracefully if the JSON databases are ever moved or deleted, preventing hard crashes.
