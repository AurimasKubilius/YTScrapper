import pandas as pd
from googleapiclient.discovery import build
import streamlit as st

# YouTube API details
YOUTUBE_API_KEY = st.secrets["general"]["YOUTUBE_API_KEY"]
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Session state to track queries
if 'queries_used' not in st.session_state:
    st.session_state['queries_used'] = 0

# Function to get channel statistics
def get_channel_statistics(channel_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    request = youtube.channels().list(part="statistics", id=channel_id)
    response = request.execute()
    items = response.get('items', [])
    if items:
        return int(items[0]['statistics']['subscriberCount'])
    return None

# Function to scrape YouTube results
def scrape_youtube_results(keywords, max_results_per_keyword, min_subs):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    results = []
    total_queries = 0

    for keyword in keywords:
        next_page_token = None
        total_results = 0
        seen_channels = set()

        while total_results < max_results_per_keyword:
            request = youtube.search().list(
                q=keyword,
                part='snippet',
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            total_queries += 1  # Increment query count
            st.session_state['queries_used'] += 1  # Track in session state

            for item in response.get('items', []):
                channel_title = item['snippet']['channelTitle']
                channel_id = item['snippet']['channelId']

                # Skip if already seen
                if channel_title in seen_channels:
                    continue

                # Get subscriber count
                subs_count = get_channel_statistics(channel_id)
                if subs_count and subs_count < min_subs:
                    continue  # Skip channels below the subscriber count filter

                video_info = {
                    'Keyword': keyword,
                    'Video Title': item['snippet']['title'],
                    'Channel Title': channel_title,
                    'Subscriber Count': subs_count,
                    'Publish Time': item['snippet']['publishTime'],
                    'Video URL': f"https://www.youtube.com/watch?v={item['id'].get('videoId')}"
                }
                results.append(video_info)
                seen_channels.add(channel_title)

                # Stop collecting if we've hit the limit
                if len(seen_channels) >= max_results_per_keyword:
                    break

            # Update the total results and check for more pages
            total_results += len(response.get('items', []))
            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(seen_channels) >= max_results_per_keyword:
                break

    return results, total_queries

# Streamlit app interface
st.title("YouTube Scrapper")

# Input for keywords
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

# Show current session query usage
st.subheader("API Usage")
st.write(f"Queries used this session: {st.session_state['queries_used']}")

# Run scraper
if st.button("Find Channels"):
    if not keywords_input.strip():
        st.error("Please enter at least one keyword.")
    else:
        keywords = [k.strip() for k in keywords_input.splitlines() if k.strip()]
        st.write(f"Scraping results for {len(keywords)} keywords...")
        
        # Scrape results
        with st.spinner("Fetching data, please wait..."):
            results, total_queries = scrape_youtube_results(keywords, max_results, min_subs)
        st.write(f"Scraping complete! Total queries used: {total_queries}")
        df = pd.DataFrame(results)

        if not df.empty:
            st.dataframe(df)
            csv = df.to_csv(index=False)
            st.download_button("Download Results as CSV", data=csv, file_name="youtube_results.csv", mime="text/csv")
        else:
            st.warning("No results found. Try different keywords or adjust filters.")
