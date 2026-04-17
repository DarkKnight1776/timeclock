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

    st.markdown("""
                <style>
                    [data-testid="stSidebar"] {
                        display: none;
                }
                """, unsafe_allow_html=True)

else:
    st.title("Welcome to 🌷 The Pink Tulip Time Tracker!")
    st.write("Please use the sidebar to navigate.")

    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()