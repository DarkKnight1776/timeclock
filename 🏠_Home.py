import streamlit as st
import time

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="The Pink Tulip", page_icon="🌷", layout="wide")

# Hide sidebar when not logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'show_admin_pass' not in st.session_state:
    st.session_state.show_admin_pass = False

# --- 3. THE LOGIN FUNCTION ---
def show_login():
    st.title("🌷 The Pink Tulip")
    st.subheader("Enter your personal passcode")
    
    # The PIN input
    passcode = st.text_input("Passcode", type="password", label_visibility="collapsed", key="pin_input")
    
    # CHECK PIN: This logic forces the password box to stay visible
    if passcode == "177698":
        st.session_state.show_admin_pass = True
    else:
        # If they backspace or enter something else, hide the admin password box
        st.session_state.show_admin_pass = False

    # FORK 1: ADMIN PATH
    if st.session_state.show_admin_pass:
        st.info("🔓 Admin PIN recognized.")
        admin_password = st.text_input("Manager Password", type="password", key="admin_pass_input")
        
        if st.button("Unlock Admin Dashboard", type="primary", use_container_width=True):
            if admin_password == "Tulip2026!": # Your secure password
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("❌ Incorrect Password")
                
    # FORK 2: EMPLOYEE PATH
    elif len(passcode) == 6:
        if st.button("Clock In/Out", type="primary", use_container_width=True):
            # This is where we'll eventually check the Google Sheet list
            st.session_state.logged_in = True
            st.session_state.role = "employee"
            st.rerun()

# --- 4. MAIN APP LOGIC ---
if not st.session_state.logged_in:
    show_login()
else:
    # --- LOGGED IN AREA ---
    if st.session_state.role == "admin":
        st.title("📊 Manager Dashboard")
        st.write("Welcome back! Here are the store stats.")
        # Place your Sales Stats and Employee Overviews here
    else:
        st.title("🕒 Employee Portal")