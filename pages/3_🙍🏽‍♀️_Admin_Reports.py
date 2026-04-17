import streamlit as st
import pandas as pd

def show_payroll_calculator(df):
    st.header("💰 2-Week Payroll Summary")
    
    # 1. Convert Timestamp column to actual 'Time' objects so Python can do math
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # 2. Get list of unique employees
    employees = df['Employee'].unique()
    
    payroll_data = []
    
    for person in employees:
        # Filter data for just this person
        person_df = df[df['Employee'] == person].sort_values('Timestamp')
        
        total_seconds = 0
        last_in_time = None
        
        # Loop through their punches to find pairs
        for index, row in person_df.iterrows():
            if row['Action'] == "Clock In":
                last_in_time = row['Timestamp']
            elif row['Action'] == "Clock Out" and last_in_time is not None:
                # Calculate difference
                duration = row['Timestamp'] - last_in_time
                total_seconds += duration.total_seconds()
                last_in_time = None # Reset for next pair
        
        # Convert seconds to hours
        total_hours = round(total_seconds / 3600, 2)
        
        # Calculate Pay (assuming a flat rate of $15/hr for now)
        hourly_rate = 15.00
        dollars_owed = round(total_hours * hourly_rate, 2)
        
        payroll_data.append({
            "Name": person,
            "Hours Worked": total_hours,
            "Dollars Owed": f"${dollars_owed:,.2f}"
        })

    # 3. Display the "Little Format" you wanted
    payroll_df = pd.DataFrame(payroll_data)
    st.table(payroll_df)