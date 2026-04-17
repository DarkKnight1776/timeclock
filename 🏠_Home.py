import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Boutique Time Clock", page_icon="⏰", layout="wide")

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def show_login():
    st.title("👋 Boutique Time Clock")
    st.subheader("Enter your personal passcode")
    
    passcode = st.text_input("Passcode", type="password", label_visibility="collapsed")
    
    if st.button("Login", type="primary", use_container_width=True):
        if passcode == "177698":          # ← change this if you want
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Incorrect passcode")

# Hide sidebar when not logged in
if not st.session_state.logged_in:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

if not st.session_state.logged_in:
    show_login()
else:
    st.title("✅ Welcome to the Boutique Time Clock")
    st.write("Use the sidebar to clock in/out or view logs.")
    
    # Logout button
    if st.sidebar.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.rerun()