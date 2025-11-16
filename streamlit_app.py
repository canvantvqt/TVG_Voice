# -*- coding: utf-8 -*-
import streamlit as st
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
from gtts import gTTS
import json
import base64
import os

st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

st.markdown("""
**Hướng dẫn ngắn:**
1) Trình duyệt sẽ tự phát **lời chào giới thiệu** khi mở app.
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

# ---- Phát audio bằng HTML5 (trình duyệt) ----
def play_audio_file(file_path):
    if not os.path.exists(file_path):
        st.error(f"Không tìm thấy file {file_path}")
        return
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

# ---- Phát TTS tự động ----
def speak_text(text, temp_file="temp_answer.mp3"):
    tts = gTTS(text=text, lang="vi")
    tts.save(temp_file)
    play_audio_file(temp_file)

# ---- AUTO PHÁT LỜI CHÀO KHI MỞ APP ----
if 'intro_played' not in st.session_state:
    st.session_state.intro_played = False

if not st.session_state.intro_played:
    intro_text = (
        "Xin chào! Tôi là trợ lý Voice AI Trưng Vương Garden. "
        "Khu trải nghiệm của chúng tôi có nhiều dịch vụ thú vị: "
        "Vé tham quan, Vườn cây nhiệt đới, Vườn chim Aviary, Sở thú ăn chay, "
        "Thác nước Apsara, Suối đá Mồ Côi, Bến Thiên Cầm, Nhà tre cộng đồng, "
        "Vườn tượng cảnh quan, Hồ Thiên Nga, Cầu Kiều. "
        "Các hoạt động trải nghiệm: cưỡi ngựa, Hồ bơi Pool Party, xe đạp đôi và đơn, "
        "xe điện tham quan, thuyền Thiên Nga, thuyền SUP, KAYAK, "
        "Trượt phao cầu vồng, xe đua Gokart. "
        "Ẩm thực tại nhà hàng Champa phục vụ ẩm thực địa phương, "
        "bãi đỗ xe miễn phí và nhiều góc checkin. "
        "Bạn có thể hỏi tôi về: giờ mở cửa, giá vé, trải nghiệm, khuyến mãi, ẩm thực hoặc liên hệ."
    )
    speak_text(intro_text, "intro.mp3")
    st.session_state.intro_played = True

# ---- UI ----
col1, col2, col3 = st.columns([1,1,1])

# Bấm để hỏi (upload audio)
uploaded_audio = col2.file_uploader("🎤 Bấm để hỏi", type=["wav","mp3","m4a","webm"], key="user_audio")

if uploaded_audio is not None:
    user_text = transcribe_audio(uploaded_audio)
    st.info(f"Bạn nói: {user_text}")
    answer_text = find_answer(user_text)
    st.success(f"Trợ lý trả lời: {answer_text}")
    speak_text(answer_text)

# Kết thúc
if col3.button("⏹ Kết thúc"):
    farewell_text = "Cảm ơn bạn đã sử dụng Trợ lý Trưng Vương Garden. Chào tạm biệt!"
    st.success(farewell_text)
    speak_text(farewell_text, "farewell.mp3")
