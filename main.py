import streamlit as st
import pandas as pd
from bertopic import BERTopic
import requests
from googleapiclient.discovery import build
from groq import Groq

import os

groq_api_key = os.getenv("GROQ_API_KEY")#replace with your groq api key
# Groq LLaMA API call
def groq_model(prompt: str, max_tokens=300):
    client = Groq(api_key=groq_api_key)
    response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=700,
    )
    result=response.choices[0].message.content
    result=result.replace("**","")
    return result  

# BERTopic topic extraction
from bertopic import BERTopic
import hdbscan

def extract_topics(texts):
    if len(texts) < 5:
        raise ValueError("Please upload at least 5 titles to generate reliable topics.")
        
    hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=2, min_samples=1)
    topic_model = BERTopic(hdbscan_model=hdbscan_model, verbose=False)
    topics, probs = topic_model.fit_transform(texts)
    topic_info = topic_model.get_topic_info()
    return topic_info.head(10), topic_model

# YouTube API to find similar creators
def youtube_search_creators(query, max_results=5):
    api_key = os.getenv("YOUTUBE_API_KEY") # Replace with your YouTube API key
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=max_results,
            type='channel',
            order='relevance'
        ).execute()
    except Exception as e:
        st.error(f"YouTube API error: {e}")
        return []

    creators = []
    for item in search_response.get('items', []):
        channel = {
            "name": item['snippet']['channelTitle'],
            "channelId": item['snippet']['channelId'],
            "description": item['snippet']['description']
        }
        creators.append(channel)
    return creators

# Generate personalized content plan
def generate_content_plan(audience, niche, top_topics, sentiment_summary):
    prompt = f"""You are a content strategist AI.
    Audience: {audience}
    Niche: {niche}
    Top past topics: {', '.join(top_topics[:5])}
    Audience sentiment: Positive {sentiment_summary.get('positive', 0)*100:.1f}%, Negative {sentiment_summary.get('negative', 0)*100:.1f}%.
    Generate a personalized 1-month content plan with 2 posts for 4 weeks. Include post topics, formats, and suggested publishing days.
"""
    return groq_model(prompt)

# Analyze draft content
def analyze_draft(draft_text):
    prompt = f"""
    You are an expert content editor.
    Analyze this content draft and provide constructive feedback focused on engagement, tone, clarity, and audience appeal:{draft_text}
    Provide suggestions for improvement and highlight any potential issues."""
    return groq_model(prompt, max_tokens=200)

