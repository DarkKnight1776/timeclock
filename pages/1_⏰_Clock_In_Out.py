import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Connect to the Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Your Clock-In Logic
if st.button("Submit Entry"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the row to send
    # Make sure keys match your column headers exactly!
    new_data = {
        "Timestamp": [current_time],
        "Employee": [st.session_state.current_user], # Or your selectbox variable
        "Action": [action_variable]
    }
    
    # Send to the sheet
    try:
        conn.create(spreadsheet="Timeclock_Database", data=new_data)
        st.success(f"Success! Data saved to Timeclock_Database.")
    except Exception as e:
        st.error(f"Failed to send data: {e}")