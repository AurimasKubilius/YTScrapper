import streamlit as st
import uuid
from streamlit_cookies_manager import EncryptedCookieManager

# Set a secure password for cookie encryption
COOKIE_PASSWORD = st.secrets["general"]["COOKIE_PASSWORD"]

# Initialize the cookie manager
cookies = EncryptedCookieManager(password=COOKIE_PASSWORD)

if not cookies.ready():
    st.stop()

def authenticate(username, password):
    """Authenticate user using Streamlit secrets."""
    users = st.secrets.get("users", {})
    return username in users and users[username] == password

def generate_session_id():
    """Generate a unique session ID."""
    return str(uuid.uuid4())

def login_page():
    """Render the login page."""
    # Restore login state if session ID exists and matches
    session_id = cookies.get("session_id")
    if session_id and cookies.get("authenticated") == "true":
        st.session_state["authenticated"] = True
        st.session_state["username"] = cookies.get("username")
        st.session_state["session_id"] = session_id
        return st.session_state["username"]  # Skip rendering login form

    # Initialize session state for the current user
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if authenticate(username, password):
            session_id = generate_session_id()
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["session_id"] = session_id
            cookies["authenticated"] = "true"
            cookies["username"] = username
            cookies["session_id"] = session_id
            cookies.save()
            st.success(f"Welcome, {username}!")
            st.rerun()  # Ensure the main app renders after login
            return username
        else:
            st.error("Invalid username or password.")
    return None

def validate_session():
    """Validate if the session ID in cookies matches the session state."""
    session_id = cookies.get("session_id")
    if not session_id or session_id != st.session_state.get("session_id"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.session_state["session_id"] = None
        cookies["authenticated"] = "false"
        cookies["username"] = ""
        cookies["session_id"] = ""
        cookies.save()
        return False
    return True

def logout(username):
    """Log out the current user."""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["session_id"] = None
    cookies["authenticated"] = "false"
    cookies["username"] = ""
    cookies["session_id"] = ""
    cookies.save()
    st.info("You have been logged out.")
    st.rerun()
