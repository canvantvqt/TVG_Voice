# -*- coding: utf-8 -*-
import streamlit as st
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
import json
import base64

st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

st.markdown("""
**Hướng dẫn ngắn:**
1) Nhấn **Phát lời chào** để nghe giới thiệu.
2) Nhấn **Bấm để hỏi**, ghi âm câu hỏi (upload file audio).
3) Trợ lý trả lời bằng âm thanh.
4) Nhấn **Kết thúc** để chào tạm biệt.
""")

# ---- Load FAQ JSON ----
def find_answer(user_text):
    try:
        with open("faq_garden.json", encoding="utf-8") as f:
            faq_data = json.load(f)
    except Exception:
        return "Xin lỗi, hiện tại tôi không thể truy cập dữ liệu tư vấn."

    for item in faq_data.get("faq", []):
        for keyword in item.get("question", []):
            if keyword.lower() in user_text.lower():
                return item.get("answer", "")
    return ("Xin lỗi, tôi chưa hiểu câu hỏi của bạn. "
            "Bạn có thể hỏi về giờ mở cửa, giá vé, trải nghiệm, ẩm thực, khuyến mãi hoặc liên hệ.")

# ---- Phát lời chào bằng HTML5 audio (miễn phí, trình duyệt) ----
def play_audio_file(file_path):
    audio_file = open(file_path, "rb").read()
    b64_audio = base64.b64encode(audio_file).decode()
    audio_html = f"""
        <audio autoplay="true" controls>
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        Your browser does not support the audio element.
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# ---- STT từ file audio ----
def transcribe_audio(uploaded_file):
    if uploaded_file is None:
        return None
    # Chuyển audio về WAV nếu cần
    file_bytes = uploaded_file.read()
    audio = AudioSegment.from_file(BytesIO(file_bytes))
    wav_io = BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='vi-VN')
            return text
        except sr.UnknownValueError:
            return "Tôi không nghe rõ, bạn vui lòng nói lại nhé!"
        except sr.RequestError:
            return "Hiện tại không thể kết nối dịch vụ STT."

# ---- MAIN UI ----
col1, col2, col3 = st.columns([1,1,1])

# State
if 'stop' not in st.session_state:
    st.session_state.stop = False

with col1:
    if st.button("▶️ Phát lời chào"):
        # intro.mp3 phải có trong repo
        play_audio_file("intro.mp3")

with col2:
    uploaded_audio = st.file_uploader("🎤 Bấm để hỏi", type=["wav", "mp3", "m4a", "webm"])
    if uploaded_audio is not None:
        user_text = transcribe_audio(uploaded_audio)
        st.info(f"Bạn nói: {user_text}")
        answer_text = find_answer(user_text)
        st.success(f"Trợ lý trả lời: {answer_text}")
        # Phát bằng TTS trình duyệt
        tts_file = "temp_answer.mp3"
        from gtts import gTTS
        tts = gTTS(text=answer_text, lang="vi")
        tts.save(tts_file)
        play_audio_file(tts_file)

with col3:
    if st.button("⏹ Kết thúc"):
        farewell_text = "Cảm ơn bạn đã sử dụng Trợ lý Trưng Vương Garden. Chào tạm biệt!"
        st.success(farewell_text)
        tts = gTTS(text=farewell_text, lang="vi")
        tts.save("farewell.mp3")
        play_audio_file("farewell.mp3")
        st.session_state.stop = True

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)
