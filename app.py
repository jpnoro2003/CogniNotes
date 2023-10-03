# Import Libraries
import streamlit as st
import requests

# Webpage Header
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.sidebar.image("Logo.png")
st.sidebar.write('Learn Faster with AI-Generated Study Guides from YouTube! Powered by GPT-3.5 by OpenAI.')
st.sidebar.write('---')

st.title(":robot_face: Welcome to CogniNotes!")
st.write("CogniNotes is a tool that leverages OpenAI's ChatGPT to generate study guides based on YouTube videos!")
st.write("To use the tool, copy the video id from the youtube url, paste it in the text box in the side bar, and press enter!")

# Generate Study Guide
def study_guide(vid_id):
    with st.spinner('Creating Guide...'):

        data = requests.get("http://ec2-3-136-116-97.us-east-2.compute.amazonaws.com/generate?vid_id="+str(vid_id)).json()
        try:
            ##### Show Content #####

            # Title with main topic
            st.header(data['main_title'])

            # Show Youtube video
            st.video(data['link'])

            # Summary Section
            st.subheader('Summary')
            st.write(data['summary'])
            st.write('---')

            # Key Points Section
            st.subheader('Key Points')
            st.write(data['key_points'])
            st.write('---')

            # Key Words Section
            st.subheader('Key Words')
            st.write(data['keywords'])
            st.write('---')

            # Study Questions
            st.subheader('Study Questions')
            st.write(data['questions'])
            st.write('---')

            # 
            # st.subheader('Study Questions')
            # st.write(data)
            # st.write('---')
        except Exception as e:

            st.write("ERROR: " + str(e))
            

# Get Video ID as input from user
input_col1, input_col2 = st.columns([4,1])
with input_col1:
    vid_id = st.sidebar.text_input('Enter the YouTube Video ID Below:')
with input_col2:
    st.write('##')
    submit = st.sidebar.button('Generate Study Guide')
if submit:
    study_guide(vid_id)
