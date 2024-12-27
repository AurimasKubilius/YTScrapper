import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# Set a secure password for cookie encryption
COOKIE_PASSWORD = "your_secure_password_here"  # Replace with a secure key or load it from Streamlit secrets

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
    # Check if the user is already logged in via cookies
    if cookies.get("authenticated") == "true":
        st.session_state["authenticated"] = True
        st.session_state["username"] = cookies.get("username")
    else:
        # Initialize session state for first-time users
        if "authenticated" not in st.session_state:
            st.session_state["authenticated"] = False
        if "username" not in st.session_state:
            st.session_state["username"] = None

        # Display the login form
        st.title("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if authenticate(username, password):
                # Set session state and cookies on successful login
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                cookies["authenticated"] = "true"
                cookies["username"] = username
                cookies.save()
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")

def logout():
    """Log out the user."""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    cookies["authenticated"] = "false"
    cookies["username"] = ""
    cookies.save()
    st.info("You have been logged out.")
