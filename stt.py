import os

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
    SpeakOptions,
)
from dotenv import load_dotenv
load_dotenv()


deepgram = DeepgramClient(os.getenv("API_DEEPGRAM"))

def speech2text(AUDIO_FILE):
    try:
        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        user_text = response['results']['channels'][0]['alternatives'][0]['transcript']
        print(user_text)
        return user_text

    except Exception as e:
        print(f"Exception: {e}")

def text2speech_deep(text):
    if (len(text) == 0):
        text = "Please record something your recording is empty"
    SPEAK_OPTIONS = {"text": text}
    filename = "output.wav"
    try:
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        print("Deepgram done!")
        return filename

    except Exception as e:
        print(f"Exception: {e}")
