import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- GATEKEEPER ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login from the home page first.")
    st.stop()

st.title("⏰ Clock In / Clock Out")

# 1. Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. UI for Clocking
employees = ["Sarah", "Emma", "Mia", "Olivia", "Liam", "Noah"]
employee = st.selectbox("Employee Name", employees)

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 Clock In", type="primary", use_container_width=True):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{
                "Timestamp": timestamp,
                "Employee": employee,
                "Action": "Clock In"
            }])
            
            # Using your exact tab name: Timeclock_Database
            conn.create(
                worksheet="Timeclock_Database", 
                data=new_row
            )
            st.success(f"✅ {employee} clocked IN at {timestamp}")
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    if st.button("🔴 Clock Out", type="secondary", use_container_width=True):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{
                "Timestamp": timestamp,
                "Employee": employee,
                "Action": "Clock Out"
            }])
            
            # Using your exact tab name: Timeclock_Database
            conn.create(
                worksheet="Timeclock_Database", 
                data=new_row
            )
            st.success(f"✅ {employee} clocked OUT at {timestamp}")
        except Exception as e:
            st.error(f"Error: {e}")