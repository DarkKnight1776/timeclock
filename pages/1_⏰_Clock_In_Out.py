import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. GATEKEEPER ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login from the home page to access this feature.")
    st.stop()

# Sidebar Setup
st.sidebar.header(f"👤 {st.session_state.employee_name}")
st.sidebar.divider()
if st.sidebar.button("Log Out", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.employee_name = None
    st.switch_page("Home.py")

# --- 2. DATABASE & STATUS CHECK ---
conn = st.connection("gsheets", type=GSheetsConnection)
employee_name = st.session_state.employee_name

# Read the sheet with a safety net for errors/empty sheets
try:
    df = conn.read(worksheet="Timeclock_Database", ttl=0)
except Exception:
    df = pd.DataFrame(columns=["Timestamp", "Employee", "Action"])

# Find THIS specific user's last action in the history
user_history = df[df["Employee"] == employee_name]

if not user_history.empty:
    last_action = user_history.iloc[-1]["Action"]
    is_clocked_in = (last_action == "Clock In")
else:
    # If they have never clocked in before, they are "Clocked Out"
    is_clocked_in = False

# --- 3. THE SINGLE DYNAMIC INTERFACE ---
st.title("⏰ Time Clock")
st.subheader(f"Ready to clock in, {employee_name}?")

# This logic gate ensures ONLY one status and ONE button exist on the page
if is_clocked_in:
    # --- UI FOR CLOCK OUT ---
    st.info("🟢 **Status:** You are currently **Clocked In**")
    
    if st.button("Clock Out", type="secondary", use_container_width=True):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{"Timestamp": timestamp, "Employee": employee_name, "Action": "Clock Out"}])
            
            # Combine the old data with the new entry
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # Push back to Google Sheets
            conn.update(worksheet="Timeclock_Database", data=updated_df)
            
            st.toast("Shift ended! Great work.")
            st.rerun() # Forces the page to refresh and swap the button
        except Exception as e:
            st.error(f"Error: {e}")

else:
    # --- UI FOR CLOCK IN ---
    st.warning("🔴 **Status:** You are currently **Clocked Out**")
    
    if st.button("Clock In", type="primary", use_container_width=True):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{"Timestamp": timestamp, "Employee": employee_name, "Action": "Clock In"}])
            
            # Combine and Update
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(worksheet="Timeclock_Database", data=updated_df)
            
            st.toast("Shift started! Have a good one.")
            st.rerun() # Forces the page to refresh and swap the button
        except Exception as e:
            st.error(f"Error: {e}")