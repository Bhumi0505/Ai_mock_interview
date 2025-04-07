import streamlit as st
import mysql.connector
from otp_auth import verify_otp, send_otp
import time

# Hide Sidebar Completely & Use Full Screen
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none !important;
        }
        /* Full-screen layout */
        .main-container {
            display: flex;
            height: 100vh;
        }
        .left-half, .right-half {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        /* Fixing Font & Color of "Verify OTP" */
        .otp-title {
            color: #004aad !important;
            font-size: 28px !important;
            font-weight: bold !important;
            font-family: 'Poppins', sans-serif !important;
            margin-bottom: 10px !important;
            padding: 0px !important;
        }
        /* Style Buttons */
        .stButton>button {
            background-color: #004aad !important;
            color: white !important;
            width: 100%;
            padding: 12px;
            font-size: 18px;
            font-weight: bold;
            font-family: 'Poppins', sans-serif;
            border-radius: 8px;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #00338c !important;
        }
        /* Fix Textbox Behavior */
        .stTextInput>div>div>input {
            border-radius: 8px !important;
            font-size: 16px !important;
            padding: 10px !important;
            border: 1px solid #cccccc !important;
        }
        /* Hide Extra Eye Icon */
        input::-ms-reveal,
        input::-webkit-contacts-auto-fill-button,
        input::-webkit-credentials-auto-fill-button {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Full-Screen Layout: Two Equal Columns
col1, col2 = st.columns(2)

# Left Half - Image
with col1:
    st.image("images/login.jpg", use_container_width=True)  # Add your image path

# Right Half - OTP Verification Form
with col2:
    st.markdown("<div class='otp-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='otp-title'>Verify OTP</h2>", unsafe_allow_html=True)

    if "signup_email" not in st.session_state:
        st.error("⚠️ No signup data found. Please sign up again.")
        st.switch_page("pages/signup.py")

    email = st.session_state["signup_email"]
    username = st.session_state["signup_username"]
    password = st.session_state["signup_password"]

    st.success(f"✅ OTP sent successfully to {email}!")

    otp_input = st.text_input("Enter OTP", placeholder="Enter the OTP received", type="password", autocomplete="off")

    # Buttons Layout
    col1, col2 = st.columns([1, 1])  
    with col1:
        verify_clicked = st.button("Verify OTP")
    with col2:
        resend_clicked = st.button("Resend OTP")

    # Handle Verify OTP
    if verify_clicked:
        if verify_otp(email, otp_input):
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="ai_mock_interview"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                        (username, email, password))
            conn.commit()
            conn.close()

            st.success("✅ Account Created Successfully!")
            time.sleep(2)
            st.switch_page("login.py")  # Redirect to login page
        else:
            st.error("❌ Invalid OTP!")

    # Handle Resend OTP
    if resend_clicked:
        send_otp(email)
        st.markdown("<div style='text-align: center; width: 100%;'><span style='color: green; font-weight: bold;'>✅ New OTP Sent!</span></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Close OTP container
