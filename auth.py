import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# Set a secure password for cookie encryption (load from Streamlit secrets)
COOKIE_PASSWORD = st.secrets["general"]["COOKIE_PASSWORD"]

# Initialize the cookie manager
cookies = EncryptedCookieManager(password=COOKIE_PASSWORD)

if not cookies.ready():
    st.stop()

def authenticate(username, password):
    """Authenticate user using Streamlit secrets."""
    users = st.secrets.get("users", {})  # Retrieve users from Streamlit secrets
    return username in users and users[username] == password

def login_page():
    """Render the login page and manage login flow."""
    # Restore state if already logged in via cookies
    if cookies.get("authenticated") == "true":
        st.session_state["authenticated"] = True
        st.session_state["username"] = cookies.get("username")
        return  # Skip rendering the login page if already logged in

    # Initialize session state for first-time users
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("username", None)

    # Display login form
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if authenticate(username, password):
            # Update session state and cookies upon successful login
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            cookies["authenticated"] = "true"
            cookies["username"] = username
            cookies.save()
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

def logout():
    """Log out the user and reset session state."""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    cookies["authenticated"] = "false"
    cookies["username"] = ""
    cookies.save()
    st.info("You have been logged out.")
