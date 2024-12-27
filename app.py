import streamlit as st
from auth import login_page, logout

def main_app():
    """Render the main application interface."""
    st.sidebar.write(f"Logged in as: **{st.session_state['username']}**")
    if st.sidebar.button("Logout"):
        logout()

    st.title("YouTube Scrapper")

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
            st.write("Scraping results... (Placeholder)")
            st.session_state["queries_used"] += len(keywords_input.splitlines())

# Control Flow
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login_page()
else:
    main_app()
