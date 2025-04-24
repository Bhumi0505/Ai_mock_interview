import streamlit as st

# Streamlit UI
st.set_page_config(page_title="Smart Career Prep Dashboard", layout="wide")

# Hide sidebar completely
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        .block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# Centered Welcome Message and Quote
st.markdown(f"""
    <h1 style='text-align: center; font-size: 48px;'>🚀 Smart Career Preparation</h1>
    <p style='text-align: center; font-size: 20px; font-weight: bold; color: #555;'>🎯 Your limitation—it's only your imagination.</p>
""", unsafe_allow_html=True)

# Select target position
def validate_selection():
    if position == "Select Your Target Position":
        st.warning("Please choose a position before proceeding.")
        return 1
    else:
        st.success("Proceeding with: " + position)

position = st.selectbox("", ["Select Your Target Position", "Cybersecurity Analyst", "Software Developer", "Data Scientist", "AI Engineer", "Cloud Engineer", "DevOps Engineer", "Network Security Engineer", "Full Stack Developer", "Machine Learning Engineer", "IT Support Specialist"], index=0)
st.session_state["position"] = position

# Two buttons in the same row
col1, col2 = st.columns(2)

with col1:
    if st.button("🧑‍💼 Start Mock Interview", key="ai_interview", help="Start AI Interview", use_container_width=True):
        if validate_selection() !=1:
            st.switch_page("pages/interview.py")
with col2:
    if st.button("📊 View Interview Feedback", key="interview_feedback", help="View AI Interview Feedback", use_container_width=True):
        if validate_selection() !=1:
            st.switch_page("pages/feedback.py")

# Line separator before "Your Progress"
st.markdown("""
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)

# Centered Progress Section
st.markdown("""
    <h2 style='text-align: center; font-size: 27px; background-color: #004aad; color: white; padding: 10px; border-radius: 8px;'>📊 Your Progress</h2>
    <br>
""", unsafe_allow_html=True)

# Styled Progress Details (adjusted font sizes)
st.markdown("""
    <div style='display: flex; justify-content: space-around; text-align: center;'>
        <div>
            <h4 style='margin: 0; font-size: 18px;'>Mock Interviews Completed</h4>
            <p style='font-size: 18px; font-weight: bold; margin: 5px 0;'>5</p>
        </div>
        <div>
            <h4 style='margin: 0; font-size: 18px;'>Daily Streak</h4>
            <p style='font-size: 18px; font-weight: bold; margin: 5px 0;'>3 Days</p>
        </div>
    </div>
""", unsafe_allow_html=True)
