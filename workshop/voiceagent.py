import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import uuid
import webbrowser
import datetime
import random
import subprocess

# ======== Text to Speech ========
def speak(text):
    file = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)

# ======== Speech to Text ========
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        st.write(f"🗣️ You said: **{command}**")
        return command.lower()
    except:
        st.write("❌ Sorry, I couldn't understand.")
        return None

# ======== Command Logic ========
def process_command(command):
    if "hello" in command:
        response = "Hello! How can I assist you?"

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {now}."

    elif "open google" in command:
        webbrowser.open("https://google.com")
        response = "Opening Google."

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube."

    elif "open calculator" in command:
        os.system("calc")
        response = "Opening Calculator."

    elif "open vs code" in command or "open vscode" in command:
        try:
            subprocess.Popen(["code"])
            response = "Opening Visual Studio Code."
        except:
            response = "VS Code not found. Make sure it is installed properly."

    elif "play music" in command:
        music_folder = os.path.expanduser("~/Music")
        try:
            songs = [song for song in os.listdir(music_folder) if song.endswith(".mp3")]
            if songs:
                random_song = os.path.join(music_folder, random.choice(songs))
                playsound.playsound(random_song)
                response = "Playing Music."
            else:
                response = "No mp3 songs found in your Music folder."
        except:
            response = "Unable to play music. Please check your Music folder."

    elif "exit" in command or "stop" in command:
        response = "Goodbye!"
        speak(response)
        raise SystemExit()

    else:
        response = "I didn't understand that command."

    st.success(response)
    speak(response)

# ======== Streamlit UI ========
st.title("🎙️ Voice Controlled AI Agent")

if st.button("🎤 Speak Now"):
    cmd = listen()
    if cmd:
        process_command(cmd)
