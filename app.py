import streamlit as st
from googleapiclient.discovery import build
import pandas as pd

# Initialize session state keys
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# Authentication logic
def authenticate(username, password):
    """Authenticate user using Streamlit secrets."""
    users = st.secrets.get("users", {})
    return username in users and users[username] == password

# Login page
def login_page():
    """Render the login form."""
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

# Logout function
def logout():
    """Reset session state and reload the app."""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.experimental_rerun()

# Main app functionality
def main_app():
    """Render the main app."""
    st.sidebar.write(f"Logged in as: **{st.session_state['username']}**")
    if st.sidebar.button("Logout"):
        logout()

    # Main app interface
    st.title("YouTube Partnership Finder")

    st.subheader("Enter Keywords")
    keywords_input = st.text_area(
        "Enter keywords (one per line):",
        placeholder="Type keywords here, one per line..."
    )

    max_results = st.number_input(
        "Enter the maximum number of results per keyword:",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )

    min_subs = st.number_input(
        "Minimum Subscriber Count",
        min_value=0,
        value=0,
        step=1
    )

    if "queries_used" not in st.session_state:
        st.session_state["queries_used"] = 0
    st.subheader("API Usage")
    st.write(f"Queries used this session: {st.session_state['queries_used']}")

    if st.button("Find Channels"):
        if not keywords_input.strip():
            st.error("Please enter at least one keyword.")
        else:
            keywords = [k.strip() for k in keywords_input.splitlines() if k.strip()]
            st.write(f"Scraping results for {len(keywords)} keywords...")

            # Placeholder for scraper function
            st.write("Scraping complete! (Simulated for demo)")
            st.session_state["queries_used"] += len(keywords)

# Render the app
if not st.session_state["authenticated"]:
    login_page()
else:
    main_app()
