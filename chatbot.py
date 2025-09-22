import streamlit as st
import google.generativeai as genai
import time

# ---------------------
# Configure Gemini
# ---------------------
genai.configure(api_key="AIzaSyBzLvhgcNzVAbZsxVX8LPtx-9amlKQEdrk")  # replace with your API key
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------
# Streamlit Setup
# ---------------------
st.set_page_config(page_title="Multi-Domain Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Multi-Domain Chatbot")

# Domain options
domains = {
    "Education": "You are an assistant that ONLY answers questions related to education (Python, programming, study tips, learning methods, etc.).",
    "Medical": "You are a helpful assistant that ONLY answers questions related to healthcare, common diseases, treatments, and healthy lifestyle. Do not give unrelated advice.",
    "Travel": "You are a helpful assistant that ONLY answers travel-related questions (places to visit, best food, travel tips, packing suggestions).",
    "Fitness Coach": "You are a professional fitness coach. ONLY answer questions related to workouts, diet, bodybuilding, fat loss, yoga, and fitness motivation."
}

# Domain selector
selected_domain = st.selectbox("Choose your chatbot domain:", list(domains.keys()))

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f"<div style='text-align:right; background:#DCF8C6; padding:8px; margin:5px; border-radius:10px; display:inline-block;'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left; background:#F1F0F0; padding:8px; margin:5px; border-radius:10px; display:inline-block;'><b>Bot:</b> {text}</div>", unsafe_allow_html=True)

# User input
user_input = st.chat_input(f"Ask your {selected_domain} related question...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    with st.spinner("Bot is typing..."):
        # Create domain-specific prompt
        prompt = f"""
        {domains[selected_domain]}
        
        If the user asks something unrelated to {selected_domain}, 
        politely decline by saying:
        'Sorry, I can only answer {selected_domain}-related questions.'

        User Question: {user_input}
        """

        response = model.generate_content(prompt)
        bot_reply = response.text

        # Typing animation
        placeholder = st.empty()
        reply_text = ""
        for char in bot_reply:
            reply_text += char
            placeholder.markdown(
                f"<div style='text-align:left; background:#F1F0F0; padding:8px; margin:5px; border-radius:10px; display:inline-block;'><b>Bot:</b> {reply_text}</div>",
                unsafe_allow_html=True
            )
            time.sleep(0.02)

        st.session_state.messages.append(("bot", bot_reply))
        st.rerun()
