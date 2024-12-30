import streamlit as st
from auth import login_page, logout, get_session_key
from scraper import scrape_youtube_results
import pandas as pd

def main(username):
    """Main app logic for a specific user."""
    st.title("YouTube Scraper")
    user_key = lambda key: get_session_key(username, key)

    keywords_input = st.text_area(
        "Enter keywords (one per line):",
        placeholder="Type keywords here, one per line...",
        key=user_key("keywords_input")
    )

    max_results = st.number_input(
        "Enter the maximum number of results per keyword:",
        min_value=1,
        max_value=50,
        value=10,
        step=1,
        key=user_key("max_results")
    )

    min_subs = st.number_input(
        "Minimum Subscriber Count",
        min_value=0,
        value=0,
        step=1,
        key=user_key("min_subs")
    )

    if st.button("Find Channels", key=user_key("find_channels")):
        if not keywords_input.strip():
            st.error("Please enter at least one keyword.")
        else:
            keywords = [k.strip() for k in keywords_input.splitlines() if k.strip()]
            st.write(f"Scraping results for {len(keywords)} keywords...")

            # Call the scraper function
            results = scrape_youtube_results(keywords, max_results, min_subs)

            # Convert results to a DataFrame for display
            if results:
                df = pd.DataFrame(results)
                st.success("Scraping complete!")
                st.dataframe(df)  # Display the table

                # Add a download button for CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name=f"{username}_youtube_results.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No results found.")

# Control flow
username = login_page()  # Handle login
if username:
    logout_button_clicked = st.sidebar.button("Logout")
    if logout_button_clicked:
        logout(username)
    else:
        main(username)
