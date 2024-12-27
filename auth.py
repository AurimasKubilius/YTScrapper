import streamlit as st

def authenticate(username, password):
    """Authenticate user using Streamlit secrets."""
    users = st.secrets.get("users", {})
    return username in users and users[username] == password

def login_required():
    """Ensure the user is logged in before accessing the app."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None

    # If not authenticated, show the login form
    if not st.session_state["authenticated"]:
        st.title("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Welcome, {username}!")
                st.experimental_rerun()  # Reload the app after successful login
            else:
                st.error("Invalid username or password.")
        return False
    else:
        # Show a logout button if authenticated
        st.sidebar.write(f"Logged in as: **{st.session_state['username']}**")
        if st.sidebar.button("Logout"):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.experimental_rerun()  # Reload the app after logout
        return True
