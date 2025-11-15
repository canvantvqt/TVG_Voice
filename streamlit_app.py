# streamlit_app.py
# -*- coding: utf-8 -*-
import streamlit as st
import json
import tempfile
from pathlib import Path
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
import os
import speech_recognition as sr

# ---------- Config ----------
st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

# ---------- Load FAQ ----------
FAQ_PATH = Path("faq_garden.json")
if not FAQ_PATH.exists():
    st.error("Không tìm thấy file faq_garden.json. Vui lòng đặt file JSON vào cùng thư mục.")
    st.stop()

with open(FAQ_PATH, encoding="utf-8") as f:
    faq_data = json.load(f)

def find_answer(user_text: str) -> str:
    for item in faq_data.get("faq", []):
        for kw in item.get("question", []):
            if kw.lower() in user_text.lower():
                return item.get("answer", "")
    return ("Xin lỗi, tôi chưa hiểu câu hỏi của bạn. "
            "Bạn có thể hỏi về giờ mở cửa, giá vé, trải nghiệm, ẩm thực, khuyến mãi hoặc liên hệ.")

# ---------- Helpers ----------
def save_audio_bytes_to_wav(audio_bytes: bytes) -> str:
    """Convert audio bytes to wav file."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
    audio = AudioSegment.from_file(BytesIO(audio_bytes))
    audio.export(tmp_path, format="wav")
    return tmp_path

def transcribe_audio(wav_path: str) -> str:
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language="vi-VN")
    except:
        return ""

def tts_bytes(text: str) -> bytes:
    """Tạo mp3 bytes từ văn bản bằng gTTS."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp_mp3 = f.name
    tts = gTTS(text=text, lang="vi")
    tts.save(tmp_mp3)
    data = Path(tmp_mp3).read_bytes()
    os.remove(tmp_mp3)
    return data

# ---------- UI ----------
st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# ---------- Giới thiệu và lời chào ----------
with col1:
    if st.button("🎵 Phát lời chào"):
        if Path("intro.mp3").exists():
            st.audio("intro.mp3", format="audio/mp3")
        else:
            st.warning("Chưa có file intro.mp3. Vui lòng tạo file lời chào trước.")

# ---------- Tương tác giọng nói ----------
st.divider()
st.subheader("Tương tác với trợ lý")
st.markdown("**Vui lòng bấm nút để hỏi** và nói câu hỏi của bạn bằng micro.")

# Record audio component
try:
    from audio_recorder_streamlit import audio_recorder
    recorder_available = True
except ImportError:
    recorder_available = False

audio_bytes = None
if recorder_available:
    audio_bytes = audio_recorder()
else:
    uploaded = st.file_uploader("Hoặc tải file âm thanh lên (wav/mp3/m4a/webm)", type=["wav","mp3","m4a","webm"])
    if uploaded:
        audio_bytes = uploaded.read()

if audio_bytes:
    st.info("Đang xử lý âm thanh...")
    wav_path = save_audio_bytes_to_wav(audio_bytes)
    user_text = transcribe_audio(wav_path)
    if not user_text:
        st.warning("Không nhận diện được giọng nói. Hãy thử lại.")
    else:
        st.success(f"Bạn nói: {user_text}")
        answer = find_answer(user_text)
        st.success(f"Trợ lý trả lời: {answer}")
        if st.button("🔊 Phát lời đáp"):
            tts_data = tts_bytes(answer)
            st.audio(tts_data, format="audio/mp3")

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)
