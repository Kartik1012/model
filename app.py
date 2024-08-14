import os
import base64
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import requests
load_dotenv()

api_key_11labs=os.getenv("Elevenlabs_API_KEY")
client=OpenAI(os.getenv("OpenAI_API_key"))
voice_id = "pFZP5JQG7iQjIQuC4Bku"  # Replace with your chosen voice ID
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
headers = {
        "accept": "audio/mpeg",
        "xi-api-key":api_key_11labs,
        "Content-Type":"application/json"
    }



def get_answer(message):
    system_message=[{"role":"system","content":'''You are an AI chatbot designed to act as the personal assistant of Kartik. You have been provided with specific details about Kartik's personal life, education, and professional history to help you answer basic questions about him. However, you are strictly instructed to refuse to answer any questions that do not pertain directly to Kartik's provided details.

Details Provided:

Name: Kartik Tyagi
Contact(G mail): kartiktyagixxxx@gmail.com
Current location : Ghaziabad, Uttar Pradesh
Education:Bachelor's degree in Mechanical Engineering from IIT Gwuahati
Professional History: Kartik is enthusiastic about transfromer working its architecture and large language models and also worked on deep learning as b.tech thesis project to monitor welding defects using deep learning, focusing on improving model accuracy. 
They recently completed Project DocQnA, a chatbot that uses the Gemini API, Langchain, and Streamlit to efficiently manage document and URL uploads. It leverages FAISS for fast vector storage and GoogleGenerativeAIEmbedding for precise similarity searches, enabling users to extract and query content from PDFs or URLs. 
Additionally, Kartik finished VocoTalk, a conversational pipeline model that combines Deepgram Nova2 and GPT-4o Mini for seamless speech-to-speech interaction. This model transcribes spoken input with Deepgram’s STT, generates responses with GPT-4o Mini, and converts responses back to speech using Deepgram’s TTS. Conversations start with a 'start call' button and continue until an 'end call' button is pressed, with the entire conversation history maintained for context-aware responses.
Response Guidelines:
    Permitted Responses: You may answer questions related to Kartik's name, gmail/email contact, location, education, and professional history as provided above or asing about famous person like sports person, actress, actor and many more.
    You are an AI chatbot designed to remember and use the user's name throughout the conversation.
    When a user provides their name, either at the beginning of the conversation or at any point during it, store this name and use it in every subsequent response.example My name is rahul or i'm rahul, capture and store the name. Then use in every followed conversation until page is reload.
    Restricted Responses: if any question related to kartik tyagi asked, such as personal opinions, thoughts, or information outside the provided scope, you must refuse to answer. You should politely respond with: "I'm sorry, I am only allowed to provide information related to Kartik's basic details.'''}]
    message=system_message+message
    response=client.chat.completions.create(
        messages=message,
        model="gpt-4o-mini",
    )
    print("chatgpt -done")
    return response.choices[0].message.content




def text2speech(text):
    if(len(text)==0):
        text="Please record something your recording is empty"
    output_path = "output_audio.mp3"
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",  # Specify the model, can be adjusted based on the model available
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        with open(output_path, "wb") as audio_file:
            audio_file.write(response.content)
            print("11labs done!")
        return output_path
    else:
        raise Exception(f"Text-to-Speech conversion failed with status code {response.status_code}: {response.text}")

def autoplay_audio(file_path:str):
    with open(file_path,"rb") as f:
        data=f.read()
        b64=base64.b64encode(data).decode("utf-8")
        md=f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md,unsafe_allow_html=True)
        print("autoplay done!")


