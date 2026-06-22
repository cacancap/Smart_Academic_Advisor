import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import tools

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini client
# Note: It automatically picks up GEMINI_API_KEY from the environment
try:
    client = genai.Client()
except Exception as e:
    print(f"Failed to initialize Gemini client: {e}")
    print("Please make sure you have set GEMINI_API_KEY in your .env file.")
    exit(1)

# We use the recommended model for general tasks
MODEL_ID = 'gemini-2.5-flash'

# System prompt giving the agent its persona and instructions
SYSTEM_INSTRUCTION = """
You are a helpful and strict Academic Advisor for a University Computer Science department.
Your job is to help students plan their schedules and check if they can take certain classes.

ALWAYS use the provided tools to verify information before answering. 
Never guess a student's transcript or a course's prerequisites.
If a student wants to take a course, you MUST:
1. Check the course's prerequisites using get_course_info.
2. Check the student's transcript using get_student_transcript to ensure they have passed all prerequisites.
3. Check which semesters the course is offered to ensure they can take it.
4. If a student asks what courses they have left to take to graduate, use get_degree_requirements to find their major's curriculum, compare it against their transcript from get_student_transcript, and list the remaining required courses.

**DATA PRIVACY & SECURITY GUARDRAIL:**
You must treat the Student ID as a strict authentication token. If a user asks for personal academic information, grades, or degree progress without explicitly providing their Student ID (e.g., "S101"), you must refuse to answer and politely ask them to verify their identity by providing their Student ID first to protect student privacy.

Be polite, clear, and explain your reasoning based on the data you retrieve.
"""

def main():
    print("🎓 Welcome to the Smart Academic Advisor!")
    print("Type 'quit' or 'exit' to end the session.")
    print("-" * 50)
    
    # Create a chat session with the model, providing tools and system instructions
    chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            # Pass the python functions directly as tools
            tools=[tools.get_student_transcript, tools.get_course_info, tools.get_all_courses, tools.get_degree_requirements],
            temperature=0.2, # Keep it deterministic for advising
        )
    )

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit']:
                print("Academic Advisor: Have a great semester! Goodbye.")
                break
                
            if not user_input.strip():
                continue
                
            # Send message to the agent
            response = chat.send_message(user_input)
            print(f"\nAdvisor: {response.text}")
            
        except KeyboardInterrupt:
            print("\nAcademic Advisor: Session terminated. Goodbye.")
            break
        except Exception as e:
            print(f"\nError: An issue occurred communicating with the API. Ensure your API key is valid. Details: {e}")

if __name__ == "__main__":
    main()
