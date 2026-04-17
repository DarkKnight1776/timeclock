import streamlit as st
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Setup the connection
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Clock In / Out")

# 2. Create the ACTUAL input boxes so they appear on screen
# We use a 'form' so the page doesn't refresh until you hit submit
with st.form("time_clock_form"):
    # Pull names from your session_state list we made earlier
    # Change your line 14 to this:
if not st.session_state.get('logged_in', False):
    show_login()
    action = st.radio("What are you doing?", ["Clock In", "Clock Out"])
    
    submitted = st.form_submit_button("Submit Entry")

    if submitted:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 3. Use the variables from the selectbox and radio button
        new_data = {
            "Timestamp": [current_time],
            "Employee": [employee],  # Matches the variable from the selectbox above
            "Action": [action]       # Matches the variable from the radio above
        }
        
        try:
            conn.create(data=new_data)
            st.success(f"Verified! {employee} {action}ed at {current_time}")
        except Exception as e:
            st.error(f"Error sending to Sheets: {e}")