import streamlit as st
from auth import login_required
from scraper import scrape_youtube_results
from utils import display_results

# Main app entry point
st.title("YouTube Partnership Finder")

if login_required():
    # Show the main app after successful login
    st.subheader("Enter Keywords")
    keywords_input = st.text_area(
        "Enter keywords (one per line):",
        placeholder="Type keywords here, one per line..."
    )

    # Input for result count
    max_results = st.number_input(
        "Enter the maximum number of results per keyword:",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )

    # Filter by minimum subscriber count
    min_subs = st.number_input(
        "Minimum Subscriber Count",
        min_value=0,
        value=0,
        step=1
    )

    # API Usage
    if "queries_used" not in st.session_state:
        st.session_state["queries_used"] = 0
    st.subheader("API Usage")
    st.write(f"Queries used this session: {st.session_state['queries_used']}")

    # Scrape button
    if st.button("Find Channels"):
        if not keywords_input.strip():
            st.error("Please enter at least one keyword.")
        else:
            keywords = [k.strip() for k in keywords_input.splitlines() if k.strip()]
            st.write(f"Scraping results for {len(keywords)} keywords...")

            # Call the scraper function
            results = scrape_youtube_results(keywords, max_results, min_subs)
            display_results(results)
