import os
import datetime
import random
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- TRAINING DATA ----------------
training_sentences = [
    # calculator
    "open calculator", "i want to calculate", "start calculator",

    # time
    "what is the time", "tell me the time", "current time please",

    # note
    "make a note", "save this note", "write this down",

    # joke
    "tell me a joke", "make me laugh", "joke please",

    # youtube
    "open youtube", "play youtube", "start youtube",

    # google search
    "search on google", "google this", "i want to search something",

    # music
    "play music", "start music", "i want to listen song"
]

intents = [
    "calculator","calculator","calculator",
    "time","time","time",
    "note","note","note",
    "joke","joke","joke",
    "youtube","youtube","youtube",
    "google","google","google",
    "music","music","music"
]

# ---------------- NLP MODEL ----------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="AI Intent Agent", layout="centered")
st.title("🤖 Smart AI Agent (Offline, No API)")
st.write("Type something & the AI will detect your intent and perform an action.")

user = st.text_input("Your Command:", placeholder="e.g., open calculator, tell me a joke, play music...")

if st.button("Run"):
    if user.strip() == "":
        st.warning("Please type something first!")
    else:
        user_vec = vectorizer.transform([user])
        similarity = cosine_similarity(user_vec, X)
        index = similarity.argmax()
        intent = intents[index]

        st.write(f"**Detected Intent:** `{intent}`")

        # Actions
        if intent == "calculator":
            st.write("Opening Calculator...")
            os.system("calc")

        elif intent == "time":
            now = datetime.datetime.now().strftime("%I:%M %p")
            st.success(f"Current Time: {now}")

        elif intent == "note":
            text = user.replace("note", "").strip()
            if text == "":
                st.write("Enter the note text below:")
                text = st.text_input("Note Text:")
            if text:
                with open("notes.txt", "a") as f:
                    f.write(text + "\n")
                st.success("Note Saved ✅")

        elif intent == "joke":
            jokes = [
                "Debugging: Removing the needles from the haystack 😂",
                "Programmers never die, they just go offline 💻"
            ]
            st.info(random.choice(jokes))

        elif intent == "youtube":
            st.write("Opening YouTube...")
            os.system("start https://www.youtube.com")

        elif intent == "google":
            st.write("Enter your search query:")
            query = st.text_input("Search Query:")
            if query:
                os.system(f"start https://www.google.com/search?q={query}")
                st.success(f"Searched: {query}")

        elif intent == "music":
            st.write("Playing Random Music 🎵")
            music_folder = "D:\\Music"   # CHANGE PATH IF NEEDED
            songs = os.listdir(music_folder)
            song = random.choice(songs)
            os.startfile(os.path.join(music_folder, song))
            st.success(f"Playing: {song}")

        else:
            st.error("Sorry, I didn't understand 😅")