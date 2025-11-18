import streamlit as st
from streamlit_audio_recorder import st_audio_recorder  # pip install streamlit-audio-recorder
from gtts import gTTS
from io import BytesIO
import base64
import json
from pydub import AudioSegment
import speech_recognition as sr

st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

st.title("🎤 Trợ lý A.I Trưng Vương Garden")

# ---- Play intro button ----
if st.button("▶️ Phát lời chào"):
    play_audio_file("intro.mp3")

# ---- Audio recorder button ----
st.markdown("### 🎤 Bấm vào nút dưới đây để hỏi")
audio_bytes = st_audio_recorder()  # trả về WAV bytes
if audio_bytes is not None:
    # Chuyển bytes sang WAV để STT
    wav_io = BytesIO(audio_bytes)
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            user_text = recognizer.recognize_google(audio_data, language='vi-VN')
        except:
            user_text = "Tôi không nghe rõ, bạn nói lại nhé!"
    
    st.info(f"Bạn nói: {user_text}")
    
    # Tra cứu JSON
    answer_text = find_answer(user_text)
    st.success(f"Trợ lý trả lời: {answer_text}")
    
    # Phát audio TTS bằng trình duyệt
    tts = gTTS(text=answer_text, lang="vi")
    tts_io = BytesIO()
    tts.write_to_fp(tts_io)
    tts_io.seek(0)
    b64_audio = base64.b64encode(tts_io.read()).decode()
    st.markdown(f"""
    <audio autoplay="true" controls>
    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)
