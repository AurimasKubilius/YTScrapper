import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# Initialize cookies manager
cookies = EncryptedCookieManager()

if not cookies.ready():
    st.stop()

def authenticate(username, password):
    """Authenticate user using Streamlit secrets."""
    users = st.secrets.get("users", {})
    return username in users and users[username] == password

def login_page():
    """Render the login page."""
    # Check for existing cookies
    if cookies.get("authenticated") == "true":
        st.session_state["authenticated"] = True
        st.session_state["username"] = cookies.get("username")
    else:
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
