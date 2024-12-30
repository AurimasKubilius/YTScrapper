import streamlit as st
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

def get_session_key(username, key):
    """Generate a user-specific session key."""
    return f"{username}_{key}"

def login_page():
    """Render the login page."""
    # Restore login state if cookies indicate user is already logged in
    username = cookies.get("username")
    if username and cookies.get(f"{username}_authenticated") == "true":
        st.session_state[get_session_key(username, "authenticated")] = True
        st.session_state[get_session_key(username, "username")] = username
        return username  # Skip rendering login form

    # Initialize session state for the current user
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if authenticate(username, password):
            user_session_key = get_session_key(username, "authenticated")
            st.session_state[user_session_key] = True
            st.session_state[get_session_key(username, "username")] = username
            cookies[f"{username}_authenticated"] = "true"
            cookies["username"] = username
            cookies.save()
            st.success(f"Welcome, {username}!")
            st.rerun()  # Ensure the main app renders after login
            return username
        else:
            st.error("Invalid username or password.")
    return None

def logout(username):
    """Log out the current user."""
    user_session_key = get_session_key(username, "authenticated")
    st.session_state[user_session_key] = False
    st.session_state[get_session_key(username, "username")] = None
    cookies[f"{username}_authenticated"] = "false"
    cookies["username"] = ""
    cookies.save()
    st.info("You have been logged out.")
    st.rerun()
