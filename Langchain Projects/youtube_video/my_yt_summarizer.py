import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the LLM (Updated to a more recent model)
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    temperature=0.3, 
    model="gpt-4o-mini" # Faster and cheaper than 3.5-turbo
)

# 2. Define the Prompt Template
summary_prompt = PromptTemplate(
    input_variables=["transcript"],  
    template="""
    You are an expert content summarizer.
    Here is a video transcript:
    {transcript}
    
    Please generate a clear and concise summary of the main points discussed in the video along with topics covered.
    """
)       

# 3. Create the Chain using LCEL (Fixes Deprecation Warning)
# This replaces LLMChain with the "Pipe" operator
chain = summary_prompt | llm

# Streamlit app UI
st.title("YouTube Video Summarizer")

video_url = st.text_input("Enter YouTube Video URL:")   

def get_video_id(url):
    """Extract the video ID from a YouTube URL."""
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        return parse_qs(parsed_url.query).get('v', [None])[0]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    return None

if st.button("Generate Video Summary"):
    if not video_url.strip():
        st.warning("Please enter a YouTube video URL.")
    else:
        with st.spinner("Fetching transcript and generating summary..."):
            video_id = get_video_id(video_url)
            if not video_id:
                st.error("Invalid YouTube URL. Please enter a valid URL.")
            else:
                try:
                    # Fix for YouTubeTranscriptApi: Ensure it's called correctly
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    transcript_text = " ".join([entry['text'] for entry in transcript_list])
                    
                    # Invoke using LCEL
                    response = chain.invoke({"transcript": transcript_text})

                    # ChatOpenAI returns a message object, content is accessed via .content
                    summary = response.content

                    st.subheader("Video Summary")
                    st.write(summary) # Use st.write for better formatting than st.text
                    
                except AttributeError:
                    # Fallback for newer versions/different structures
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    transcript= transcript_list.find_transcript(['en']).fetch()
                    transcript_text =  " ".join([entry['text'] for entry in transcript])

                    # ChatOpenAI returns a message object, content is accessed via .content
                    summary = response.content

                    st.subheader("Video Summary")
                    st.write(summary) # Use st.write for better formatting than st.text
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")