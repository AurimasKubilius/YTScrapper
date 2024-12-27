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

def login_page():
    """Render the login page."""
    # Restore login state if cookies indicate user is already logged in
    if cookies.get("authenticated") == "true":
        st.session_state["authenticated"] = True
        st.session_state["username"] = cookies.get("username")
        return  # Skip rendering login form

    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None

    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            cookies["authenticated"] = "true"
            cookies["username"] = username
            cookies.save()
            st.success(f"Welcome, {username}!")
            st.rerun()  # Ensure the main app renders after login
        else:
            st.error("Invalid username or password.")

def authenticated_page(logout_callback):
    """Render the authenticated page with a logout option."""
    st.sidebar.write(f"Logged in as: **{st.session_state['username']}**")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        cookies["authenticated"] = "false"
        cookies["username"] = ""
        cookies.save()
        st.info("You have been logged out.")
        st.rerun()  # Ensure the login page renders after logout
    logout_callback()
