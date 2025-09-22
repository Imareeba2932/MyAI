import streamlit as st
import google.generativeai as genai
import time

# ---------------------
# Configure Gemini
# ---------------------
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # 🔑 Replace with your key
model = genai.GenerativeModel("gemini-pro")

# ---------------------
# Streamlit UI Setup
# ---------------------
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini Chatbot")

# Store messages in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------
# Display chat history
# ---------------------
for msg in st.session_state.messages:
    role, text = msg
    if role == "user":
        st.markdown(f"""
        <div style="text-align:right; background:#DCF8C6; padding:8px; margin:5px; border-radius:10px; display:inline-block;">
            <b>You:</b> {text}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:left; background:#F1F0F0; padding:8px; margin:5px; border-radius:10px; display:inline-block;">
            <b>Bot:</b> {text}
        </div>
        """, unsafe_allow_html=True)

# ---------------------
# Input box
# ---------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.messages.append(("user", user_input))

    # Show typing effect
    with st.spinner("Bot is typing..."):
        response = model.generate_content(user_input)
        bot_reply = response.text

        # Typing animation
        placeholder = st.empty()
        reply_text = ""
        for char in bot_reply:
            reply_text += char
            placeholder.markdown(f"""
            <div style="text-align:left; background:#F1F0F0; padding:8px; margin:5px; border-radius:10px; display:inline-block;">
                <b>Bot:</b> {reply_text}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.02)  # Adjust speed here

        # Save bot reply
        st.session_state.messages.append(("bot", bot_reply))

        # Refresh UI
        st.rerun()
