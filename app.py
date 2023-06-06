# Import Libraries
import streamlit as st
import pickle
from youtube_transcript_api import YouTubeTranscriptApi as yta
import spacy
import pytextrank
import pickle
import openai

# Load SpaCy NLP processing Model

# Set up OpenAI API Key
openai.api_key = st.secrets["key"]

# Webpage Header
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title('CogniNotes -  Learn Faster with AI-Generated Study Guides from YouTube')
st.write('---')

# Generate Study Guide
def study_guide(vid_id):
    with st.spinner('Creating Guide...'):
            # Convert transcript into string
            data = yta.get_transcript(vid_id)
            transcript = ''
            for value in data:
                for key,val in value.items():
                    if key == 'text':
                        transcript += val + ' '

            nlp = spacy.load('en_core_web_sm')

            # Transform transcript with SpaCy model
            doc = nlp(transcript)

            # Get most relevant key sentences
            test = ''
            for sentence in doc._.textrank.summary(limit_sentences=50):
                test = test + str(sentence) + " "
                # print(len(test))
                if len(test) >= 10000:
                    break

            # Summary
            messages = [ {"role": "system", "content": "You are a intelligent assistant"}]

            message = """
            Summarize this youtube video for a study guide, keep all important details relevant for studying, at least 250 words
            """+test

            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            summary = chat.choices[0].message.content

            # Key Points
            messages = [ {"role": "system", "content": "You are a intelligent assistant"}]

            message = """
            Provide 5 key points relevant for a study guide from the youtube video listed below, only respond with the points
            """+test

            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            key_points = chat.choices[0].message.content

            # Study Questions
            messages = [ {"role": "system", "content": "You are a intelligent assistant"}]

            message = """
            Provide 5 study questions (can be open-ended) based on the content from the youtube video listed below, only respond with the questions
            """+test

            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            study_questions = chat.choices[0].message.content

            # Main Topic
            messages = [ {"role": "system", "content": "You are a intelligent assistant"}]

            message = """
            Provide a title describing the main topic of a video with the transcript below. This title should be appropriate for a study guide.
            """+test

            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            main_topic = chat.choices[0].message.content

            # Key Words
            messages = [ {"role": "system", "content": "You are a intelligent assistant"}]

            message = """
            Provide a list of 5 key words including a definition based on the video transcript below. These words should be important, and avoid including common words in your list. Try to tie in content from the video where appropriate
            """+test

            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            key_words = chat.choices[0].message.content

            # Relevant Resources
            messages = [ {"role": "system", "content": "You are a intelligent assistant"}]

            message = """
            Where can I learn more about """+main_topic+"""Only reply with a list of resources and nothing else
            """

            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            resources = chat.choices[0].message.content

            ##### Show Content #####

            # Title with main topic
            st.header(main_topic)

            # Show Youtube Thumbnail
            st.image("https://img.youtube.com/vi/"+vid_id+"/maxresdefault.jpg")

            # Summary Section
            st.subheader('Summary')
            st.write(summary)
            st.write('---')

            # Key Points Section
            st.subheader('5 Key Points')
            st.write(key_points)
            st.write('---')

            # Key Words Section
            st.subheader('5 Key Words')
            st.write(key_words)
            st.write('---')

            # Relevant Resources
            st.subheader('Resources')
            st.write('FIX ME')
            st.write(resources)
            st.write('---')

            # Study Questions
            st.subheader('Study Questions')
            st.write(study_questions)
            st.write('---')

# Get Video ID as input from user
input_col1, input_col2 = st.columns([4,1])
with input_col1:
    vid_id = st.text_input('Enter the YouTube Video ID Below:')
with input_col2:
    st.write('##')
    submit = st.button('Generate Study Guide')
if submit:
    study_guide(vid_id)
