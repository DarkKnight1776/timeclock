import streamlit as st

st.set_page_config(page_title="Boutique Portal", page_icon="🛍️")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


def show_login():
    st.title("👋 Hi! Please login below")

    passcode = st.text_input("Enter your personal ID code here", type = "password")

    if st.button("login"):
        if passcode == "177698":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect passcode. Please try again.")

if not st.session_state.logged_in:
    show_login()
else:
    st.title("Welcome to the Boutique Portal!")
    st.write("This is where you can manage your boutique operations.")

    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()