import sys
print("PYTHON USED:", sys.executable)

import streamlit as st
from Supervisor import run_meeting

st.title("Agentic Meeting Intelligence System")

audio = st.file_uploader("Upload Meeting Audio")
ppt = st.file_uploader("Upload Slides")
chat = st.text_area("Paste Chat Logs")

if st.button("Analyze Meeting"):
    tasks, decision, email = run_meeting(audio, ppt, chat)

    st.subheader("Action Items")
    st.write(tasks)

    st.subheader("Decision")
    st.write(decision)

    if email:
        st.subheader("Email Sent")
        st.write(email)
