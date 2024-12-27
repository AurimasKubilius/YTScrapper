from googleapiclient.discovery import build
import streamlit as st

YOUTUBE_API_KEY = st.secrets["general"]["YOUTUBE_API_KEY"]

def get_channel_statistics(channel_id):
    """Fetch subscriber count for a channel."""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.channels().list(part="statistics", id=channel_id)
    response = request.execute()
    items = response.get("items", [])
    if items:
        return int(items[0]["statistics"]["subscriberCount"])
    return None

def scrape_youtube_results(keywords, max_results_per_keyword, min_subs):
    """Scrape YouTube results with filtering."""
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    results = []

    for keyword in keywords:
        next_page_token = None
        seen_channels = set()

        while len(seen_channels) < max_results_per_keyword:
            request = youtube.search().list(
                q=keyword,
                part="snippet",
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                channel_title = item["snippet"]["channelTitle"]
                channel_id = item["snippet"]["channelId"]

                if channel_title in seen_channels:
                    continue

                subs_count = get_channel_statistics(channel_id)
                if subs_count and subs_count >= min_subs:
                    results.append({
                        "Keyword": keyword,
                        "Video Title": item["snippet"]["title"],
                        "Channel Title": channel_title,
                        "Subscriber Count": subs_count,
                        "Video URL": f"https://www.youtube.com/watch?v={item['id'].get('videoId')}"
                    })
                    seen_channels.add(channel_title)

                if len(seen_channels) >= max_results_per_keyword:
                    break

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    return results
