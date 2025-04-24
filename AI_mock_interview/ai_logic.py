import google.generativeai as genai
import mysql.connector
import json
import os
from dotenv import load_dotenv
import io
import re



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
    Generate 5 technical interview questions(questions that are actually asked during interviews) for a {position} with expertise in {skills} 
    and {experience} years of experience. Just return plain questions line by line without numbering or bullet points.
    """
    model = genai.GenerativeModel("gemini-1.5-pro-002")
    response = model.generate_content(prompt)

    if response.text:
        lines = response.text.strip().split("\n")
        questions = [line.strip("0123456789. ").strip() for line in lines if line.strip()]
        return questions
    return []
def store_answers_in_db(user_id, question_id, question, user_answer,position):
    cursor = db.cursor()

    
    cursor.execute("""
        INSERT INTO interview_feedback(user_id, question_id, question, user_answer,position) 
        VALUES (%s, %s, %s,%s,%s)
    """, (user_id, question_id, question,user_answer,position))

    db.commit()
    cursor.close()
    
   

# Function to store answers in the database
def get_user_feedback_and_rating(user_id, position):
   
     
    # Query to get the feedback data for the user based on their position
    query = """
    SELECT question, user_answer, correct_answer, feedback, rating, question_id
    FROM interview_feedback
    WHERE user_id = %s AND position = %s
    ORDER BY question_id ASC
    """
    cursor = db.cursor()
    cursor.execute(query, (user_id, position))
    feedback_data = cursor.fetchall()
    
    # Calculate overall rating (average of the ratings)
    query_avg_rating = """
    SELECT AVG(rating) AS average_rating
    FROM interview_feedback
    WHERE user_id = %s AND position = %s
    """
    cursor.execute(query_avg_rating, (user_id, position))
    avg_rating_result = cursor.fetchone()
    overall_rating = round(avg_rating_result['average_rating'], 2)  # rounding to 2 decimal places

    cursor.close()
    
    
    return feedback_data, overall_rating


# Process AI Feedback (Using Gemini)
def generate_feedback(user_id, questions_answers, position):
   
    feedback_blocks = []
    for idx, (q, a) in enumerate(questions_answers):
        feedback_blocks.append(f"Question {idx+1}: {q}\nAnswer: {a}")
    
    joined_prompt = "\n\n".join(feedback_blocks)
    final_prompt = f"""
You are an expert interview evaluator. Analyze the following responses to interview questions.

{joined_prompt}

For each question, return the feedback in this format:
---
Rating: (number out of 3)
Corrected Answer: (ideal version)
Feedback: (constructive advice)
and after all 5 questions give overall rating out of 10 in format 
Overall Rating: (number out of 10)
---
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(final_prompt)

    # Split feedback into parts
    blocks = re.split(r'---+', response.text)
    feedbacks = []
    for idx, block in enumerate(blocks):
        rating = re.search(r'Rating:\s*(\d+)', block)
        corrected = re.search(r'Corrected Answer:\s*(.+?)\n', block, re.DOTALL)
        fb = re.search(r'Feedback:\s*(.+)', block, re.DOTALL)

        feedbacks.append({
            "question_id": idx + 1,
            "question": questions_answers[idx][0],
            "user_answer": questions_answers[idx][1],
            "rating": rating.group(1).strip() if rating else "N/A",
            "corrected_answer": corrected.group(1).strip() if corrected else "N/A",
            "feedback": fb.group(1).strip() if fb else "N/A"
        })

    # Save all feedbacks to DB
    # Save all feedbacks to DB by updating existing rows
    cursor = db.cursor()
    for f in feedbacks:
        cursor.execute("""
            UPDATE interview_feedback
            SET correct_answer = %s,
                feedback = %s,
                rating = %s
            WHERE user_id = %s AND question_id = %s AND position = %s
        """, (f["corrected_answer"], f["feedback"], f["rating"], user_id, f["question_id"], position))


    db.commit()
    cursor.close()

def get_all_answered_questions(user_id, position):
    query = """
        SELECT question_id, question, user_answer
        FROM interview_feedback
        WHERE user_id = %s AND position = %s AND user_answer IS NOT NULL
        ORDER BY question_id
    """
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, (user_id, position))
    results = cursor.fetchall()
    cursor.close()

    # Return as list of (question, answer)
    return [(row['question'], row['user_answer']) for row in results]

    

