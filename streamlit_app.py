import streamlit as st
import json
import tempfile
import speech_recognition as sr

# =========================
# 1. LOAD DATA JSON
# =========================
def load_faq():
    try:
        with open("faq_garden.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"faq": []}

faq_data = load_faq()

def find_answer(user_text):
    for item in faq_data["faq"]:
        for keyword in item["question"]:
            if keyword.lower() in user_text.lower():
                return item["answer"]
    return "Xin lỗi, tôi chưa hiểu câu hỏi. Bạn có thể hỏi: giờ mở cửa, giá vé, khuyến mãi, trải nghiệm…"

# =========================
# 2. SPEECH TO TEXT
# =========================
recognizer = sr.Recognizer()

def speech_to_text(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="vi-VN")
            return text
        except:
            return None

# =========================
# 3. UI
# =========================
st.set_page_config(page_title="Trợ lý A.I Trưng Vương Garden", layout="centered")

st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

st.subheader("🎧 Tương tác với trợ lý")
st.write("Vui lòng **bấm nút để hỏi** và nói câu hỏi của bạn bằng micro.")

# --- NÚT GHI ÂM ---
audio_data = st.audio_input("🎤 **Bấm để hỏi**")

user_question = None
assistant_answer = None

# Nếu người dùng ghi âm
if audio_data:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_data.getvalue())
        tmp_path = tmp.name

    text = speech_to_text(tmp_path)

    if text:
        user_question = text
        assistant_answer = find_answer(text)
    else:
        user_question = "Không nhận dạng được giọng nói."
        assistant_answer = "Bạn nói chưa rõ, vui lòng bấm để hỏi lại."

# --- Upload file audio ---
st.write("Hoặc tải file âm thanh lên (wav/mp3/m4a/webm)")

uploaded = st.file_uploader(" ", type=["wav", "mp3", "m4a", "webm"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    text = speech_to_text(tmp_path)

    if text:
        user_question = text
        assistant_answer = find_answer(text)
    else:
        user_question = "Không nhận dạng được âm thanh."
        assistant_answer = "Bạn vui lòng thử lại."

# Hiển thị kết quả
if user_question:
    st.info(f"**Bạn hỏi:** {user_question}")

if assistant_answer:
    st.success(f"**Trợ lý trả lời:** {assistant_answer}")

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)
