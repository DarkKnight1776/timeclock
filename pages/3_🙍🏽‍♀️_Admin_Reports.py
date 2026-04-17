import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- GATEKEEPER ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login from the home page first.")
    st.stop()

st.title("💰 Payroll & Hours Report")

# 1. Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)
URL = "https://docs.google.com/spreadsheets/d/1-IqIw7WqDFa1sXIQHhrgIn0edyTPRk4ZJ73IELlzo7Y/edit"

try:
    # 2. Read the data
    df = conn.read(spreadsheet=URL, worksheet="Timeclock_Database", ttl=0)
    
    if df.empty:
        st.info("The database is currently empty.")
    else:
        # Display raw logs first to verify connection
        with st.expander("View Raw Logs"):
            st.dataframe(df)

        # 3. Process Hours
        # Ensure the column name matches EXACTLY what you see in the sheet
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Simple Logic to show total entries per person
        st.subheader("Summary by Employee")
        summary = df.groupby('Employee')['Action'].count().reset_index()
        summary.columns = ['Employee', 'Total Punches']
        st.table(summary)

        # 4. Detailed Calculation (Name: Hours Worked: Dollars Owed)
        st.subheader("Payroll Breakdown")
        results = []
        for employee in df['Employee'].unique():
            person_df = df[df['Employee'] == employee].sort_values('Timestamp')
            
            total_hours = 0
            last_in = None
            
            for i, row in person_df.iterrows():
                if row['Action'] == "Clock In":
                    last_in = row['Timestamp']
                elif row['Action'] == "Clock Out" and last_in is not None:
                    duration = row['Timestamp'] - last_in
                    total_hours += duration.total_seconds() / 3600
                    last_in = None
            
            pay_rate = 15.00 # You can change this
            results.append({
                "Employee": employee,
                "Hours Worked": round(total_hours, 2),
                "Dollars Owed": f"${round(total_hours * pay_rate, 2):,.2f}"
            })
            
        st.table(pd.DataFrame(results))

except Exception as e:
    st.error(f"Error loading report: {e}")