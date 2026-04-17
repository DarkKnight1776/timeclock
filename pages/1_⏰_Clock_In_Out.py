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
            
            # PULL existing data first
            df = conn.read(worksheet="Timeclock_Database", ttl=0)
            # ADD the new punch to the list
            updated_df = pd.concat([df, new_row], ignore_index=True)
            # SAVE it back (using .update so we don't try to create a duplicate tab)
            conn.update(worksheet="Timeclock_Database", data=updated_df)
            
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
            
            # PULL existing data first
            df = conn.read(worksheet="Timeclock_Database", ttl=0)
            # ADD the new punch to the list
            updated_df = pd.concat([df, new_row], ignore_index=True)
            # SAVE it back
            conn.update(worksheet="Timeclock_Database", data=updated_df)
            
            st.success(f"✅ {employee} clocked OUT at {timestamp}")
        except Exception as e:
            st.error(f"Error: {e}")