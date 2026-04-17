import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# ================== GATEKEEPER ==================
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login from the home page first.")
    st.stop()
# ===============================================

st.title("⏰ Clock In / Clock Out")

# Connect to Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Employee list (add/remove names here)
employees = ["Sarah", "Emma", "Mia", "Olivia", "Liam", "Noah"]

employee = st.selectbox("Employee Name", employees)

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 Clock In", type="primary", use_container_width=True):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = pd.DataFrame({
            "Timestamp": [timestamp],
            "Employee": [employee],
            "Action": ["Clock In"]
        })
        
        # Read current data + append new row + write back
        df = conn.read(worksheet="Timeclock_Database")
        df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Timeclock_Database", data=df)
        
        st.success(f"✅ {employee} clocked IN at {timestamp}")

with col2:
    if st.button("🔴 Clock Out", type="secondary", use_container_width=True):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = pd.DataFrame({
            "Timestamp": [timestamp],
            "Employee": [employee],
            "Action": ["Clock Out"]
        })
        
        df = conn.read(worksheet="Timeclock_Database")
        df = pd.concat([df, new_row], ignore_index=True)
        conn.update(worksheet="Timeclock_Database", data=df)
        
        st.success(f"✅ {employee} clocked OUT at {timestamp}")