import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- GATEKEEPER ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login from the home page to access this feature.")
    st.stop()

st.sidebar.header(f"Logged in as: {st.session_state.employee_name}")
st.sidebar.divider()

if st.sidebar.button("Log Out", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.employee_name = None
    st.switch_page("Home.py")

# 1. Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)
URL = "https://docs.google.com/spreadsheets/d/1-IqIw7WqDFa1sXIQHhrgIn0edyTPRk4ZJ73IELlzo7Y/edit"
# We look up the name automatically based on the ID
employee_name = st.session_state.employee_name

st.subheader(f"Ready to clock in, {employee_name}?")

col1, col2 = st.columns(2)

with col1:
    if st.button("Clock In", type="primary", use_container_width=True):
        if not employee_name:
            st.error("Invalid Employee ID. Please try again.")
        else:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{
                    "Timestamp": timestamp,
                    "Employee": employee_name, # Automatically uses the name tied to the ID
                    "Action": "Clock In"
                }])
                
                # Using UPDATE logic to avoid the "Already Exists" 400 error
                df = conn.read(worksheet="Timeclock_Database", ttl=0)
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Timeclock_Database", data=updated_df)
                
                st.success(f"✅ {employee_name} clocked IN at {timestamp}")
            except Exception as e:
                st.error(f"Error: {e}")

with col2:
    if st.button("Clock Out", type="secondary", use_container_width=True):
        if not employee_name:
            st.error("Invalid Employee ID. Please try again.")
        else:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{
                    "Timestamp": timestamp,
                    "Employee": employee_name,
                    "Action": "Clock Out"
                }])
                
                df = conn.read(worksheet="Timeclock_Database", ttl=0)
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(worksheet="Timeclock_Database", data=updated_df)
                
                st.success(f"✅ {employee_name} clocked OUT at {timestamp}")
            except Exception as e:
                st.error(f"Error: {e}")