from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st
import uuid

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

def get_session_key(key):
    """Get session key unique to the user."""
    session_id = st.session_state.get("session_id", "default")
    return f"{session_id}_{key}"

def login_page():
    """Render the login page."""
    # Generate a session ID for the user if not already present
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = generate_session_id()

    session_key_authenticated = get_session_key("authenticated")
    session_key_username = get_session_key("username")

    # Restore login state if cookies indicate user is already logged in
    if cookies.get("authenticated") == "true":
        st.session_state[session_key_authenticated] = True
        st.session_state[session_key_username] = cookies.get("username")
        return st.session_state[session_key_username]

    # Render login form
    st.title("Login")
    username = st.text_input("Username", key=get_session_key("login_username"))
    password = st.text_input("Password", type="password", key=get_session_key("login_password"))
    if st.button("Login", key=get_session_key("login_button")):
        if authenticate(username, password):
            st.session_state[session_key_authenticated] = True
            st.session_state[session_key_username] = username
            cookies["authenticated"] = "true"
            cookies["username"] = username
            cookies.save()
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")
    return None

def logout():
    """Log out the current user."""
    session_key_authenticated = get_session_key("authenticated")
    session_key_username = get_session_key("username")

    st.session_state[session_key_authenticated] = False
    st.session_state[session_key_username] = None
    cookies["authenticated"] = "false"
    cookies["username"] = ""
    cookies.save()
    st.info("You have been logged out.")
    st.rerun()
