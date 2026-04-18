import streamlit as st

# --- 1. PAGE CONFIG & HIDING SIDEBAR ---
st.set_page_config(page_title="The Pink Tulip", page_icon="🌷", layout="centered")

# Initialize the notebook (session state)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Hide sidebar ONLY if not logged in
if not st.session_state.logged_in:
    st.markdown("""
        <style> [data-testid="stSidebar"] { display: none; } </style>
    """, unsafe_allow_html=True)

# --- 2. THE LOGIN SCREEN (Shows only if NOT logged in) ---
if not st.session_state.logged_in:
    st.title("Welcome to The Pink Tulip!🌷💐")
    
    passcode = st.text_input("Please enter your 6-digit employee ID", type="password", key="user_passcode")
    login_button = st.button("Log In", use_container_width=True)

    # Check the code if either the button is pressed OR if they hit enter (passcode has 6 chars)
    if login_button or (passcode and len(passcode) == 6):
        all_codes = st.secrets["employee_codes"]
        
        if passcode in all_codes:
            st.session_state.logged_in = True
            st.session_state.employee_name = all_codes[passcode]
            # No success message here yet—we want to jump to the portal first!
            st.rerun() 
        elif len(passcode) == 6:
            st.error("Invalid Employee ID. Please try again.")

    # --- 3. THE ACTUAL APP (Shows only IF logged in) ---
else:
    # This shows up on the main screen
    st.success(f"Welcome {st.session_state.employee_name}! You are now logged in.")
    st.write("Please use the sidebar to navigate.")

    # --- THE LOGOUT BUTTON (In the Sidebar) ---
    st.sidebar.header(f"Logged in as: {st.session_state.employee_name}")
    st.sidebar.divider() # Optional: adds a clean line
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.employee_name = None 
        st.rerun()