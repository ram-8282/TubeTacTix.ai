from main import extract_topics, generate_content_plan, analyze_draft, youtube_search_creators
import streamlit as st
import pandas as pd
from comment_analysis import get_youtube_analysis

def main():
    col1, col2 = st.columns([1.5,2])
    with col1:
        st.image("logo.jpg", width=200)

    # Project Name and Tagline
    with col2:
        
        st.markdown(
        """
        <h1 style='text-align: center;'>
            <span style='color: red;'>Tube</span><span style='color: white;'>Tactix.ai</span>
        </h1>
        <h3 style='text-align: center; color: white; font-style: italic;'>Master Your Youtube Content with AI-Driven Strategy
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("Upload Past Content Data")
    uploaded_file = st.sidebar.file_uploader("Upload CSV with past content (titles, engagement, comments)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Preview of Uploaded Content Data")
        st.dataframe(df.head())

        # Basic sanity check
        if 'title' not in df.columns:
            st.error("CSV must have a 'title' column for topic extraction.")
            return

        # Step 1: Extract Topics from Titles
        topic_info, topic_model = extract_topics(df['title'].tolist())
        st.subheader("Identified Content Topics")
        st.dataframe(topic_info)

        # Step 2: Basic sentiment summary from comments if available
        sentiment_summary = {'positive': 0.6, 'negative': 0.4}  # Mock for now
        if 'comments' in df.columns:
            st.info("Sentiment analysis of comments can be integrated here (placeholder).")

        # Step 3: User inputs for audience and niche
        st.sidebar.header("Your Content Info")
        audience = st.sidebar.text_input("Describe your audience", "Tech enthusiasts, millennials")
        niche = st.sidebar.text_input("Your content niche", "Technology reviews")

        if st.sidebar.button("Generate Content Plan"):
            top_topics = topic_info['Name'].tolist()
            st.subheader("Generated Content Plan")
            content_plan = generate_content_plan(audience, niche, top_topics, sentiment_summary)
            st.text_area("Content Plan", content_plan, height=300)

        st.sidebar.header("Enter your channel url to anlayse comments")
        channel_url = st.sidebar.text_input("YouTube Channel URL", "https://www.youtube.com/@..")
            # Placeholder for comments analysis
        if channel_url and st.sidebar.button("Analyze Comments"):
            st.subheader("Channel Comments Analysis")
            status, analysis = get_youtube_analysis(channel_url)
            if status == "Success":
                for i, item in enumerate(analysis):
                    st.markdown(f"### Video {i+1} - ID: {item['video_id']}")
                    st.write(f"**Video Title:** {item['title']}")
                    st.write(f"**Positive Comments:** {item['positive_comments']}")
                    st.write(f"**Negative Comments:** {item['negative_comments']}")
                    st.markdown("---")
            else:
                st.error(status)


        # Step 4: Analyze draft content
        st.subheader("Analyze Draft Content")
        draft_text = st.text_area("Paste your content draft here for feedback")
        if st.button("Get Draft Feedback") and draft_text.strip() != "":
            feedback = analyze_draft(draft_text)
            st.text_area("Editor Feedback", feedback, height=200)

        # Step 5: Suggest Collaborations
        st.subheader("Suggested Collaborators Based on Your Niche")
        if niche:
            creators = youtube_search_creators(niche)
            if creators:
                for c in creators:
                    st.markdown(f"**{c['name']}**")
                    st.markdown(f"{c['description'][:200]}...")
                    st.markdown(f"https://www.youtube.com/channel/{c['channelId']}")
                    st.markdown("---")
            else:
                st.info("No collaborators found or YouTube API issue.")

    else:
        st.info("Please upload a CSV file with your past content data to get started.")

if __name__ == "__main__":
    main()