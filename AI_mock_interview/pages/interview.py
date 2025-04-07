import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from ai_logic import generate_interview_questions, generate_feedback, save_interview_history
from streamlit_webrtc import webrtc_streamer
import json

# Streamlit UI Config
st.set_page_config(page_title="Smart Career Prep - AI Interview", layout="wide")

# Hide sidebar completely
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
    </style>
""", unsafe_allow_html=True)

# Adjusted heading position with new emoji and space after text
st.markdown("<h1 class='title'>AI Mock Interview</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subheading'>Let's Get Started 🚀</h3>", unsafe_allow_html=True)

# Retrieve position from session_state (selected in dashboard.py)
position = st.session_state.get("position", "Not selected")

# Initialize session state variables if not already present
if "description" not in st.session_state:
    st.session_state["description"] = ""
if "years_experience" not in st.session_state:
    st.session_state["years_experience"] = None  # Changed to None to prevent auto-saving
if "details_filled" not in st.session_state:
    st.session_state["details_filled"] = False

# Job details input section
if not st.session_state["details_filled"]:
    with st.expander("Enter Job Details to Proceed", expanded=True):
        temp_description = st.text_input("Skill set", value=st.session_state["description"])
        temp_years_experience = st.number_input("Years of Experience", min_value=0, step=1, value=st.session_state["years_experience"] if st.session_state["years_experience"] else 0)

        # Save only if both fields are filled
        if temp_description and temp_years_experience is not None:
            if st.button("Save Details"):
                st.session_state["description"] = temp_description
                st.session_state["years_experience"] = temp_years_experience
                st.session_state["details_filled"] = True
                st.success("✅ Details Saved!")
        else:
            st.warning("⚠️ Please enter both Job Description and Years of Experience.")

# Two equal-sized columns
col1, col2 = st.columns(2)

# Left Section: Job Details
with col1:
    if st.session_state["details_filled"]:
        st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
                <p><b>Job Role/Job Position:</b> {position}</p>
                <p><b>Job Description/Tech Stack:</b> {st.session_state["description"]}</p>
                <p><b>Years of Experience:</b> {st.session_state["years_experience"]}</p>
            </div>
        """, unsafe_allow_html=True)

        # Information Box
        st.markdown("""
            <div style="background-color: #fff4d6; padding: 15px; border-radius: 8px; border-left: 5px solid #ffaa00;">
                <p>⚡ <b>Information</b></p>
                <p>Enable Video Web Cam and Microphone to Start your AI Generated Mock Interview.</p>
                <p>It has 5 questions you can answer, and at the end, you will get a report based on your responses.</p>
                <p><b>NOTE:</b> We never record your video. Web cam access can be disabled anytime.</p>
            </div>
        """, unsafe_allow_html=True)

# Right Section: Webcam & Mic Integration
with col2:
    if st.session_state["details_filled"]:
        

        class VideoProcessor(VideoProcessorBase):
            def recv(self, frame):
                return frame

        webrtc_streamer(key="webcam", video_processor_factory=VideoProcessor, rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        
        },
        media_stream_constraints={"video": {"width": 480, "height": 250}, "audio": True},
        )

        # Start Interview Button (Disabled Until Job Details Are Entered)
        if st.button("Start Interview", use_container_width=True):
            st.success(" Interview Started! Answer the AI-generated questions.")
    else:
        st.warning("⚠️ Please fill in the Skill set  acquired and Years of Experience before starting the interview.")


