# -*- coding: utf-8 -*-
"""
TVG Voice Assistant - Streamlit version hoàn chỉnh miễn phí
STT/TTS tự động, dùng JSON faq_garden.json để trả lời
"""

import streamlit as st
import json
import time
import tempfile
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO

# =================== Hàm tra cứu JSON ===================
def find_answer(user_text):
    """Tra cứu câu trả lời từ file JSON faq_garden.json"""
    try:
        with open("faq_garden.json", encoding="utf-8") as f:
            faq_data = json.load(f)
    except Exception:
        return "Xin lỗi, hiện tại tôi không thể truy cập dữ liệu tư vấn."
    
    for item in faq_data["faq"]:
        for keyword in item["question"]:
            if keyword.lower() in user_text.lower():
                return item["answer"]
    
    return ("Xin lỗi, tôi chưa hiểu câu hỏi của bạn. "
            "Bạn có thể hỏi về giờ mở cửa, giá vé, trải nghiệm, ẩm thực, khuyến mãi hoặc liên hệ.")

# =================== Hàm TTS ===================
def text_to_audio_bytes(text):
    """Chuyển text thành audio bytes mp3"""
    tts = gTTS(text=text, lang='vi')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

# =================== Streamlit UI ===================
st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)
st.markdown("Hướng dẫn ngắn: 1) Nhấn Phát lời chào để nghe giới thiệu. "
            "2) Nhấn Bấm để hỏi, nói câu hỏi. "
            "3) Trợ lý trả lời bằng âm thanh. "
            "4) Nhấn Kết thúc để chào tạm biệt.", unsafe_allow_html=True)

# Button columns
col1, col2, col3 = st.columns(3)

if 'assistant_running' not in st.session_state:
    st.session_state.assistant_running = False

if 'last_answer_audio' not in st.session_state:
    st.session_state.last_answer_audio = None

status_placeholder = st.empty()
user_text_placeholder = st.empty()

# =================== Phát lời chào ===================
with col1:
    if st.button("🎤 Phát lời chào"):
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
        audio_bytes = text_to_audio_bytes(intro_text)
        st.audio(audio_bytes, format="audio/mp3")
        status_placeholder.info("🎧 Lời chào đã phát xong.")

# =================== Nhập câu hỏi ===================
with col2:
    user_question = st.text_input("🎤 Vui lòng bấm để hỏi và nói câu hỏi của bạn", key="user_question")

    if st.button("Bấm để hỏi") and user_question:
        answer = find_answer(user_question)
        user_text_placeholder.info(f"Bạn nói: {user_question}")
        status_placeholder.info("⏳ Trợ lý đang trả lời...")
        audio_bytes = text_to_audio_bytes(answer)
        st.audio(audio_bytes, format="audio/mp3")
        st.session_state.last_answer_audio = audio_bytes
        status_placeholder.success("✅ Trợ lý đã trả lời.")

# =================== Kết thúc ===================
with col3:
    if st.button("⏹ Kết thúc") and st.session_state.assistant_running==False:
        bye_text = "Cảm ơn bạn đã tham quan Trưng Vương Garden. Chào tạm biệt!"
        audio_bytes = text_to_audio_bytes(bye_text)
        st.audio(audio_bytes, format="audio/mp3")
        status_placeholder.info("🛑 Trợ lý đã dừng. Chào tạm biệt!")
        st.session_state.user_question = ""
        st.session_state.last_answer_audio = None

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)
