import streamlit as st
import chatBotBackend as glib
from datetime import datetime
import urllib.parse
from gtts import gTTS
import time

st.set_page_config(page_title="Chatbot")

if "is_button_active" not in st.session_state:
    st.session_state.is_button_active = False

st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <h1 style="flex: 1; margin: 0; font-family: Roboto;">Neutron</h1>
        <img src="https://firebasestorage.googleapis.com/v0/b/procoachconnect-92db3.appspot.com/o/ChatBotNeuron%2FNeuron.png?alt=media&token=ad5bb8f7-4e43-45f9-930b-fa907f48d48a" 
             alt="Neuron Logo" style="height: 50px; margin-left: 0px;">
    </div>
    """,
    unsafe_allow_html=True,
)

if 'memory' not in st.session_state:
    st.session_state.memory = glib.create_memory()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

def toggle_button():
    st.session_state.is_button_active = not st.session_state.is_button_active
    if st.session_state.is_button_active and "latest_bot_response" in st.session_state:
        def generate_audio(text):
            tts = gTTS(text, lang='en')
            tts.save("response.mp3")
            return "response.mp3"

        st.session_state.session_audio_file = generate_audio(st.session_state.latest_bot_response)

input_text = st.chat_input("Chat with Neutron here")

if input_text:
    with st.chat_message("user"):
        st.markdown(input_text)
    st.session_state.chat_history.append({"role": "user", "text": input_text})
    st.session_state.chat_response = glib.get_chat_response(
        user_message=input_text, 
        memory=st.session_state.memory
    )
    st.session_state.latest_bot_response = st.session_state.chat_response
    st.session_state.chat_history.append({"role": "assistant", "text": st.session_state.chat_response})
    with st.chat_message("assistant"):
        st.markdown(st.session_state.chat_response)

if "is_button_active" in st.session_state and st.session_state.is_button_active:
    if "session_audio_file" in st.session_state:
        st.audio(st.session_state.session_audio_file, format="audio/mp3")

def format_chat_history(chat_history):
    formatted_history = ""
    for message in chat_history:
        role = "You" if message["role"] == "user" else "Bot"
        formatted_history += f"{role}: {message['text']}\n"
    return formatted_history

conversation_text = format_chat_history(st.session_state.chat_history)

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

encoded_message = urllib.parse.quote(conversation_text)

whatsapp_link = f"https://api.whatsapp.com/send?text={encoded_message}"
messenger_link = f"https://www.messenger.com/t/?text={encoded_message}"

button_text = "🔊 Activate" if not st.session_state.is_button_active else "🔇 Deactivate"

col1, col2= st.columns([1, 1])
if st.session_state.chat_history:
    with st.spinner("Processing... Please wait!"):
        time.sleep(0.5)
    with col1:
        st.markdown(
            f"""
            <div style="display: flex; gap: 20px; align-items: center;">
                <a href="{whatsapp_link}" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" width="34" style="vertical-align: middle;">
                </a>
                <a href="{messenger_link}" target="_blank">
                    <img src="https://firebasestorage.googleapis.com/v0/b/procoachconnect-92db3.appspot.com/o/ChatBotNeuron%2FFacebook_Messenger_logo_2020.svg.png?alt=media&token=247a32ac-9ae7-4d09-b4ec-5e2b64f3b50c" alt="Messenger" width="30" style="vertical-align: middle;">
                </a>
                <a href="data:text/plain;charset=utf-8,{urllib.parse.quote(conversation_text)}" download="conversation_text_{current_time}" style="text-decoration: none;">
                <img src="https://firebasestorage.googleapis.com/v0/b/procoachconnect-92db3.appspot.com/o/ChatBotNeuron%2Fdownload-icon.webp?alt=media&token=20429318-2865-4101-bcb6-8e75829369c6" alt="Download" width="30" style="vertical-align: middle;">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="margin-top: 20px; display: flex; align-items: center; color: transparent">
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.button(button_text, on_click=toggle_button)



