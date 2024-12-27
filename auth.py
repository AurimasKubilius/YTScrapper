import streamlit as st

def authenticate(username, password):
    """Authenticate user using Streamlit secrets."""
    users = st.secrets["users"]
    return username in users and users[username] == password

def login_required():
    """Ensure user is logged in before accessing the app."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state["authenticated"] = True
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
        return False
    return True
