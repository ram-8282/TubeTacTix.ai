import re
from urllib.parse import urlparse

import googleapiclient.discovery
from textblob import TextBlob
import nltk

nltk.download('punkt')
nltk.download('stopwords')

YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY" #Replace with your youtube api key

#extracting channel id from the url
def extract_channel_id(url: str):
    parsed_url = urlparse(url)
    path = parsed_url.path

    if "youtube.com/channel/" in url:
        return path.split("/")[-1]

    elif "youtube.com/user/" in url:
        username = path.split("/")[-1]
        return get_channel_id_by_username(username)

    elif "youtube.com/@" in url:
        handle = path.split("/")[-1]
        if handle.startswith("@"):
            handle = handle[1:]
        return get_channel_id_by_handle(handle)

    else:
        return None

def get_channel_id_by_username(username):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.channels().list(part="id", forUsername=username)
    response = request.execute()
    if "items" in response and response["items"]:
        return response["items"][0]["id"]
    return None

#to return the channel handle for comment analysis
def get_channel_id_by_handle(handle):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(part="snippet", q=handle, type="channel", maxResults=5)
    response = request.execute()

    for item in response.get("items", []):
        channel_title = item["snippet"]["title"].lower()
        channel_id = item["snippet"]["channelId"]
        if handle.lower() in channel_title:
            return channel_id

    if response.get("items"):
        return response["items"][0]["snippet"]["channelId"]
    return None

#to extract latest video ids
def get_latest_video_ids(channel_id, max_results=5):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(part="snippet", channelId=channel_id, order="date", maxResults=max_results)
    response = request.execute()

    video_data = [
        {
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"]
        }
        for item in response["items"]
        if item["id"]["kind"] == "youtube#video"
    ]
    return video_data

#to return video comments
def get_video_comments(video_id, max_comments=50):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    comments = []
    try:
        request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=max_comments)
        response = request.execute()
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
    except Exception:
        pass
    return comments

#sentiment analysis of comments
def classify_sentiment(comments):
    positive, negative = 0, 0
    for comment in comments:
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity
        if polarity >= 0.1:
            positive += 1
        elif polarity <= -0.1:
            negative += 1
    return positive, negative

#to return brief analysis of comments as positive and negative
def get_youtube_analysis(channel_url):
    channel_id = extract_channel_id(channel_url)
    if not channel_id:
        return "Invalid YouTube channel URL", None

    try:
        video_data = get_latest_video_ids(channel_id)
        results = []

        for video in video_data:
            comments = get_video_comments(video["video_id"])
            pos, neg = 0, 0
            if comments:
                pos, neg = classify_sentiment(comments)

            results.append({
                "video_id": video["video_id"],
                "title": video["title"],
                "positive_comments": pos,
                "negative_comments": neg
            })

        return "Success", results

    except Exception as e:
        return f"Error: {str(e)}", None
