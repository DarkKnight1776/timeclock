import streamlit as st
from datetime import datetime

st.subheader("Clock-In")

col1, col2 = st.columns(2)

with col1:
    employee = st.selectbox("Who is clocking in?", ["Letty A", "Hadley A", "Caroline", "Meghan", "Steve"])

with col2:
    action = st.radio("What are you doing?", ["Clocking In", "Clocking Out"])

if st.button("Submit Entry"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "Time": current_time,
        "Employee": employee,
        "Action": action
    }

    st.success(f"Verified! {employee} {action} at {current_time}")