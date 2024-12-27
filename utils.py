import pandas as pd
import streamlit as st

def display_results(results):
    """Display results in a table and allow download."""
    if results:
        df = pd.DataFrame(results)
        st.write("Scraping complete!")
        st.dataframe(df)
        csv = df.to_csv(index=False)
        st.download_button("Download Results as CSV", data=csv, file_name="youtube_results.csv", mime="text/csv")
    else:
        st.warning("No results found. Try different keywords or adjust filters.")
