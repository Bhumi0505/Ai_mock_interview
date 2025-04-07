import streamlit as st
import mysql.connector
import time
# Hide Sidebar Completely & Use Full Screen
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-1f391y8 {
            display: none !important;
        }
        /* Full-screen layout */
        .main-container {
            display: flex;
            height: 100vh; /* Full viewport height */
        }
        .left-half, .right-half {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        /* Fixing Font & Color of "Login" */
        .login-title {
            color: #004aad !important;
            font-size: 28px !important;
            font-weight: bold !important;
            font-family: 'Poppins', sans-serif !important;
            margin-bottom: 10px !important;
            padding: 0px !important;
        }
        /* Style Login Button */
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

# Right Half - Login Form
with col2:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='login-title'>Login</h2>", unsafe_allow_html=True)  

    username = st.text_input("Username", placeholder="Enter your username")  
    password = st.text_input("Password", type="password", placeholder="Enter your password")  

    if st.button("Login"):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="ai_mock_interview"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.session_state["user_id"] = user[0]
            st.session_state["username"] = user[1]
            st.session_state["email"] = user[2]
            st.success("✅ Login Successful!")
            time.sleep(2)
            st.switch_page("pages/dashboard.py")
        else:
            st.error("❌ Invalid Credentials!")

    # Signup Link
    col1, col2 = st.columns([0.5, 1])  
    with col1:
        st.write("Don't have an account?")
    with col2:
        st.page_link("pages/signup.py", label="Create an account")

    st.markdown("</div>", unsafe_allow_html=True)  # Close login container
