#  **TubeTactix.ai 📈** 
### Master your Youtube Content with AI-Driven Strategy
## Overview 

TubeTactix.ai is an AI-powered personalized content strategy advisor designed specifically for YouTube creators. By analyzing the latest videos and viewer comments from any YouTube channel, TubeTactix.ai provides data-driven insights and tailored content strategies to help creators boost engagement, understand their audience better, and grow their channels effectively.

The system leverages the **YouTube Data API v3** to fetch video metadata and comments, applies sentiment analysis on viewer feedback using **TextBlob**, and employs the powerful **LLaMA 3** model hosted on **Groq** to generate customized, actionable content strategies and suggested collaborations. All results are presented through a sleek and interactive Streamlit web application.

## 📌Features

✦ 📺 YouTube Channel Analysis: Fetches the latest videos and viewer comments for any public channel.

✦ 😊😡 Sentiment Classification: Classifies comments as positive or negative to gauge audience sentiment.

✦ 📊 AI-Powered Content Strategy: Utilizes Groq’s LLaMA 3 model to generate personalized content strategies based on video performance and audience feedback.

✦ Content draft analysis: Analyses the content draft and gives feedback

✦ Suggestions on collaborations: Gives personalized suggestions on collaborators creating similar content

✦ Interactive Visualization: Displays key video details, sentiment stats, and AI-generated recommendations in a user-friendly Streamlit interface.

✦ 🔗Flexible Input: Analyze any channel URL or ID with robust channel ID extraction logic.

✦ ⚡️Lightweight & Fast: Efficient data fetching and processing pipeline ensures quick responses.
      
## 🔧 Installation & Setup

1. Clone the Repository

       git clone https://github.com/Anughna04/TubeTactix.ai.git
       cd TubeTactix.ai

2. Install Required Libraries

       pip install -r requirements.txt

3. Set up API keys

   ・Get your YouTube Data API v3 key from Google Cloud Console.

   ・Get your Groq API credentials to access LLaMA 3.

   ・Create a .env file in the project root and add:

       YOUTUBE_API_KEY=your_youtube_api_key_here
       GROQ_API_KEY=your_groq_api_key_here

4. Run the Streamlit App

       streamlit run app.py

## Usage
✦ Enter a valid YouTube channel URL or ID in the app input box.

✦ The app fetches the latest 5 videos and their comments.

✦ Sentiment analysis breaks down viewer feedback into positive and negative comments.

✦ The Groq LLaMA 3 model generates a tailored content strategy to optimize your channel growth.

✦ Results are displayed with video titles, sentiment stats, and strategic recommendations.

## Tools & Technologies Used
✦ Programming Language☞: Python

✦ APIs🔗🌐: YouTube Data API v3, Groq API for LLaMA 3

✦ 💬NLP: TextBlob (sentiment analysis), LLaMA 3 (content strategy generation)

✦ Web Framework: Streamlit

✦ Data Processing: Pandas, Regex, Collections

## Code Snippets
Fetching Video Comments & Sentiment Analysis

    from textblob import TextBlob
    from googleapiclient.discovery import build
    
    def classify_sentiment(comments):
        positive, negative = 0, 0
        for comment in comments:
            polarity = TextBlob(comment).sentiment.polarity
            if polarity >= 0.1:
                positive += 1
            elif polarity <= -0.1:
                negative += 1
        return positive, negative
        
Generating Content Strategy via Groq LLaMA 3

    import requests
    
    def generate_content_strategy(analysis_summary):
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        payload = {
            "model": "llama3",
            "prompt": f"Generate a YouTube content strategy based on: {analysis_summary}",
            "max_tokens": 300
        }
        response = requests.post("https://api.groq.com/v1/generate", json=payload, headers=headers)
        strategy = response.json().get("text", "")
        return strategy

### 📧 For any queries, contact me at [anughnakandimalla11@gmail.com](anughnakandimalla11@gmail.com).

## 👩‍💻Author

Anughna
