import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from ai_logic import generate_interview_questions

# Page setup
st.set_page_config(page_title="Smart Career Prep - AI Interview", layout="wide")

# UI styling
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        .block-container {padding-top: 1.2rem;}
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            background: linear-gradient(90deg, #004aad, #00aaff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subheading {
            text-align: left;
            font-size: 22px;
            color: #666;
            margin-bottom: 1rem;
        }
        .question-box {
            min-height: 80px;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>AI Mock Interview</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subheading'>Let's Get Started 🚀</h3>", unsafe_allow_html=True)

# Session state setup
position = st.session_state.get("position", "Not selected")
if "description" not in st.session_state: st.session_state["description"] = ""
if "years_experience" not in st.session_state: st.session_state["years_experience"] = None
if "details_filled" not in st.session_state: st.session_state["details_filled"] = False
if "interview_started" not in st.session_state: st.session_state["interview_started"] = False
if "question_index" not in st.session_state: st.session_state["question_index"] = 0
if "questions_list" not in st.session_state: st.session_state["questions_list"] = []

# Job detail input
if not st.session_state["details_filled"]:
    with st.expander("Enter Job Details to Proceed", expanded=True):
        temp_description = st.text_input("Skill set", value=st.session_state["description"])
        temp_years_experience = st.number_input("Years of Experience", min_value=0, step=1,
                                                value=st.session_state["years_experience"] or 0)
        if temp_description and temp_years_experience is not None:
            if st.button("Save Details"):
                st.session_state["description"] = temp_description
                st.session_state["years_experience"] = temp_years_experience
                st.session_state["details_filled"] = True
                st.success("✅ Details Saved!")
        else:
            st.warning("⚠️ Please enter both Job Description and Years of Experience.")

# Main columns
col1, col2 = st.columns(2)

# Left: Info / Question
with col1:
    if st.session_state["details_filled"]:
        if not st.session_state["interview_started"]:
            # Job info box
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
                    <p><b>Job Role/Job Position:</b> {position}</p>
                    <p><b>Job Description/Tech Stack:</b> {st.session_state["description"]}</p>
                    <p><b>Years of Experience:</b> {st.session_state["years_experience"]}</p>
                </div>
            """, unsafe_allow_html=True)

            # Note
            st.markdown("""
                <div style="background-color: #fff4d6; padding: 15px; border-radius: 8px; border-left: 5px solid #ffaa00;">
                    <p>⚡ <b>Information</b></p>
                    <p>Enable Video Web Cam and Microphone to Start your AI Generated Mock Interview.</p>
                    <p>It has 5 questions you can answer, and at the end, you will get a report based on your responses.</p>
                    <p><b>NOTE:</b> We never record your video. Web cam access can be disabled anytime.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Show interview question
            # Show interview question with progress
            q_index = st.session_state["question_index"]
            total_questions = len(st.session_state["questions_list"])
            st.markdown(f"#### Question {q_index + 1} of {total_questions}")
            st.markdown(f"<div class='question-box'>{st.session_state['questions_list'][q_index]}</div>", unsafe_allow_html=True)

            # Note
            st.markdown("""
                <div style="background-color: #e6f0ff; padding: 15px 20px; border-radius: 10px; border-left: 5px solid #0066ff; margin-top: 20px;">
                    <p style="margin: 0; font-size: 16px;">
                        <span style="font-weight: 600; font-size: 17px;">💡 Note:</span><br>
                        Click on <b>Record Answer</b> when you want to answer the question. At the end of interview we will give you the feedback along with correct answer for each of the question and your answer to compare it.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # Previous / Next with spacing
            st.markdown("<div style='margin-top: 20px'></div>", unsafe_allow_html=True)
            col_prev, col_next = st.columns(2)
            with col_prev:
                if st.button("⬅️ Previous", disabled=q_index == 0):
                    st.session_state["question_index"] -= 1
            with col_next:
                if st.button("Next ➡️", disabled=q_index == len(st.session_state["questions_list"]) - 1):
                    st.session_state["question_index"] += 1

# Right: Webcam + Start / Record
with col2:
    if st.session_state["details_filled"]:
        # Webcam stream
        class VideoProcessor(VideoProcessorBase):
            def recv(self, frame):
                return frame

        webrtc_streamer(
            key="webcam",
            video_processor_factory=VideoProcessor,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": {"width": 480, "height": 250}, "audio": True},
        )

        st.markdown("")

        if not st.session_state["interview_started"]:
            if st.button("🎤 Start Interview", use_container_width=True):
                st.session_state["questions_list"] = generate_interview_questions(
                    position,
                    st.session_state["description"],
                    st.session_state["years_experience"]
                ) or [
                    "Explain Spring Boot vs Node.js and which you prefer.",
                    "Describe the CIA triad in cybersecurity.",
                    "How do you protect a web app from SQL Injection?",
                    "Tell me about a time you debugged a complex issue.",
                    "Which tools do you use for backend development?"
                ]
                st.session_state["interview_started"] = True
                st.rerun()
        else:
            st.button("🎙️ Record Answer", use_container_width=True)
