import streamlit_authenticator as stauth

# 1. List your passwords here
passwords = ['moms_password', 'employee_password']

# 2. Hash them one by one manually
for pw in passwords:
    hashed_pw = stauth.Hasher([pw]).generate()[0]
    print(f"Password: {pw} \nHash: {hashed_pw}\n")