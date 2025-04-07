import google.generativeai as genai
import mysql.connector
import json
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ai_mock_interview"
)
cursor = db.cursor()

# Generate AI Interview Questions (Using Gemini)
def generate_interview_questions(position, skills, experience):
    prompt = f"""
    Generate 5 technical interview questions for a {position} with expertise in {skills} 
    and {experience} years of experience. Just return plain questions line by line without numbering or bullet points.
    """
    model = genai.GenerativeModel("gemini-1.5-pro-002")
    response = model.generate_content(prompt)

    if response.text:
        lines = response.text.strip().split("\n")
        questions = [line.strip("0123456789. ").strip() for line in lines if line.strip()]
        return questions
    return []

# Process AI Feedback (Using Gemini)
def generate_feedback(question, answer):
    prompt = f"Evaluate the following interview answer:\n\nQuestion: {question}\nAnswer: {answer}\n\nProvide constructive feedback."

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text.strip()  # Returns AI feedback

# Save Interview History
def save_interview_history(user_id, questions, answers, feedback):
    interview_data = json.dumps({"questions": questions, "answers": answers, "feedback": feedback})
    
    query = "INSERT INTO interview_history (user_id, interview_data) VALUES (%s, %s)"
    values = (user_id, interview_data)
    cursor.execute(query, values)
    db.commit()
