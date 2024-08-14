import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *
from app import *
from stt import *
float_init()

def initialize_session_state():
    if "message" not in st.session_state:
        st.session_state.message=[
            {"role":"assistant","content":"This is voice chat Chatbot"}
        ]
initialize_session_state()

st.header("VocoTalk")
st.subheader("Voice Conversational Bot", divider="green")
footer_container=st.container()
with footer_container:
    audio_bytes=audio_recorder(
        text="Tap here for start/stop recording",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="microphone-lines",
        icon_size="10x",
        pause_threshold=600.0,
    )

for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    with st.spinner("saving.."):
        webm_file_path="temp_audio.mp3"
        with open(webm_file_path,"wb") as f:
            f.write(audio_bytes)
        transcript=speech2text(webm_file_path)
        if transcript:
            st.session_state.message.append({"role":"user","content":transcript})
            os.remove(webm_file_path)

if st.session_state.message[-1]["role"]!="assistant":
    with st.chat_message("assistant"):
        final_resp = get_answer(st.session_state.message)
        audio_file = text2speech_deep(final_resp)
        autoplay_audio(audio_file)
        st.session_state.message.append({"role":"assistant","content":final_resp})
        os.remove(audio_file)

footer_container.float("bottom:0rem;")
