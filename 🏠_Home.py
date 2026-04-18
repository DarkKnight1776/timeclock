def show_login():
    st.title("🌷 The Pink Tulip")
    st.subheader("Enter your personal passcode")
    
    # Use the same layout you already have
    passcode = st.text_input("Passcode", type="password", label_visibility="collapsed")
    
    if passcode: # Only run this if they've actually typed something
        # 1. THE ADMIN FORK
        if passcode == "177698": # Your current Admin Pin
            st.info("Admin Access Detected")
            admin_password = st.text_input("Enter Manager Password", type="password")
            
            if st.button("Unlock Admin Dashboard", type="primary", use_container_width=True):
                if admin_password == "Tulip2026!": # Set your actual password here
                    st.session_state.logged_in = True
                    st.session_state.role = "admin" # Label them as Admin
                    st.rerun()
                else:
                    st.error("❌ Incorrect Password")
                    
        # 2. THE EMPLOYEE FORK
        elif len(passcode) == 6: # If they entered a 6-digit code that ISN'T the admin one
            if st.button("Clock In/Out", type="primary", use_container_width=True):
                # Later, we will check this code against your Google Sheet list
                st.session_state.logged_in = True
                st.session_state.role = "employee"
                st.rerun()