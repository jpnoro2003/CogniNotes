# Import Libraries
import streamlit as st
import requests

# Webpage Header
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title('CogniNotes -  Learn Faster with AI-Generated Study Guides from YouTube')
st.write('---')

# Generate Study Guide
def study_guide(vid_id):
    with st.spinner('Creating Guide...'):
        try:
            data = requests.get("http://ec2-3-136-116-97.us-east-2.compute.amazonaws.com/generate?vid_id="+str(vid_id)).json()
            ##### Show Content #####

            # Title with main topic
            st.header(data['main_title'])

            # Show Youtube Thumbnail
            st.image("https://img.youtube.com/vi/"+vid_id+"/maxresdefault.jpg")

            # Summary Section
            st.subheader('Summary')
            st.write(data['summary'])
            st.write('---')

            # Key Points Section
            st.subheader('5 Key Points')
            st.write(data['key_points'])
            st.write('---')

            # Key Words Section
            st.subheader('5 Key Words')
            st.write(data['keywords'])
            st.write('---')

            # Relevant Resources
            st.subheader('Resources')
            st.write('FIX ME')
            st.write('---')

            # Study Questions
            # st.subheader('Study Questions')
            # st.write(study_questions)
            # st.write('---')
        except Exception as e:
            st.write(str(e))

# Get Video ID as input from user
input_col1, input_col2 = st.columns([4,1])
with input_col1:
    vid_id = st.text_input('Enter the YouTube Video ID Below:')
with input_col2:
    st.write('##')
    submit = st.button('Generate Study Guide')
if submit:
    study_guide(vid_id)
