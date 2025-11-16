# -*- coding: utf-8 -*-
import streamlit as st
import json
import base64
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import speech_recognition as sr

# ---- Page config ----
st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

# ---- Title ----
st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

st.markdown("""
**Hướng dẫn ngắn:**
1) Nhấn **▶️ Phát lời chào** để nghe giới thiệu.
2) Nhấn **🎤 Bấm để hỏi**, nói câu hỏi trực tiếp bằng micro.
3) Trợ lý trả lời bằng âm thanh.
4) Nhấn **⏹ Kết thúc** để chào tạm biệt.
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

# ---- Phát audio bằng HTML5 (trình duyệt) ----
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

def play_audio_bytes(audio_bytes):
    b64_audio = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio autoplay="true" controls>
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        Your browser does not support the audio element.
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# ---- Main UI ----
col1, col2, col3 = st.columns([1,2,1])

# ---- State ----
if 'stop' not in st.session_state:
    st.session_state.stop = False

# ---- Phát lời chào ----
with col1:
    if st.button("▶️ Phát lời chào"):
        play_audio_file("intro.mp3")  # cần file intro.mp3

# ---- Ghi âm trực tiếp + STT + TTS ----
with col2:
    st.markdown("### 🎤 Bấm để hỏi (ghi âm trực tiếp)")

    # Nút trigger
    if st.button("🎙 Bắt đầu ghi âm câu hỏi"):
        st.info("Đang lắng nghe, nói câu hỏi của bạn...")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                st.success("Đã ghi âm xong, đang nhận diện...")
                try:
                    user_text = recognizer.recognize_google(audio_data, language='vi-VN')
                    st.info(f"Bạn nói: {user_text}")
                    # Tra cứu câu trả lời
                    answer_text = find_answer(user_text)
                    st.success(f"Trợ lý trả lời: {answer_text}")
                    # Chuyển sang audio TTS
                    tts = gTTS(text=answer_text, lang="vi")
                    tts_bytes_io = BytesIO()
                    tts.write_to_fp(tts_bytes_io)
                    tts_bytes_io.seek(0)
                    play_audio_bytes(tts_bytes_io.read())
                except sr.UnknownValueError:
                    st.error("Tôi không nghe rõ, bạn vui lòng nói lại nhé!")
                except sr.RequestError:
                    st.error("Hiện tại không thể kết nối dịch vụ STT.")
            except Exception as e:
                st.error(f"Đã xảy ra lỗi khi ghi âm: {e}")

# ---- Kết thúc ----
with col3:
    if st.button("⏹ Kết thúc"):
        farewell_text = "Cảm ơn bạn đã sử dụng Trợ lý Trưng Vương Garden. Chào tạm biệt!"
        st.success(farewell_text)
        tts = gTTS(text=farewell_text, lang="vi")
        tts_bytes_io = BytesIO()
        tts.write_to_fp(tts_bytes_io)
        tts_bytes_io.seek(0)
        play_audio_bytes(tts_bytes_io.read())
        st.session_state.stop = True

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)
