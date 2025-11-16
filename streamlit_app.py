import streamlit as st
import json
import base64
from openai import OpenAI

client = OpenAI()

# ------------------------------------------------------------------------------------
# 1. LOAD JSON FAQ
# ------------------------------------------------------------------------------------
def load_faq():
    with open("faq_garden.json", "r", encoding="utf-8") as f:
        return json.load(f)

faq_data = load_faq()

def lookup_answer(user_text):
    """Tìm câu trả lời theo JSON như bản Python gốc"""
    for item in faq_data["faq"]:
        for key in item["question"]:
            if key.lower() in user_text.lower():
                return item["answer"]

    return ("Xin lỗi, tôi chưa hiểu câu hỏi của bạn. "
            "Bạn có thể hỏi về giờ mở cửa, giá vé, trải nghiệm, "
            "ẩm thực, khuyến mãi hoặc liên hệ.")


# ------------------------------------------------------------------------------------
# 2. TTS – CHUYỂN VĂN BẢN → GIỌNG NÓI GTS-1
# ------------------------------------------------------------------------------------
def text_to_speech(text):
    response = client.audio.speech.create(
        model="gts-1",
        voice="default",
        input=text
    )
    audio_bytes = response.read()
    return audio_bytes


# ------------------------------------------------------------------------------------
# 3. STT – NHẬN DIỆN GIỌNG NÓI (twilio / openai whisper)
# ------------------------------------------------------------------------------------
def speech_to_text(audio_file):
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-audio-preview",
        file=audio_file
    )
    return transcript.text


# ------------------------------------------------------------------------------------
# 4. PLAY AUDIO
# ------------------------------------------------------------------------------------
def play_audio(audio_bytes):
    st.audio(audio_bytes, format="audio/mp3")


# ------------------------------------------------------------------------------------
# 5. INTRO – PHÁT TỰ ĐỘNG LÚC KHỞI ĐỘNG
# ------------------------------------------------------------------------------------
INTRO_TEXT = """
Xin chào! Tôi là trợ lý Voice AI Trưng Vương Garden.
Khu trải nghiệm của chúng tôi có nhiều dịch vụ thú vị:
Vé tham quan, Vườn cây nhiệt đới, Vườn chim Aviary, Sở thú ăn chay,
Thác nước Apsara, Suối đá Mồ Côi, Bến Thiên Cầm, Nhà tre cộng đồng,
Vườn tượng cảnh quan, Hồ Thiên Nga, Cầu Kiều.
Các hoạt động trải nghiệm: cưỡi ngựa, Hồ bơi Pool Party, xe đạp đôi và đơn,
xe điện tham quan, thuyền Thiên Nga, thuyền SUP, Kayak,
Trượt phao cầu vồng, xe đua Gokart.
Ẩm thực tại nhà hàng Champa phục vụ ẩm thực địa phương,
bãi đỗ xe miễn phí và nhiều góc checkin.
Bạn có thể hỏi tôi về: giờ mở cửa, giá vé, trải nghiệm, khuyến mãi, ẩm thực hoặc liên hệ.
"""


# ------------------------------------------------------------------------------------
# 6. STREAMLIT UI
# ------------------------------------------------------------------------------------
st.set_page_config(page_title="Trợ lý A.I TVG", layout="centered")

st.title("🎧 TRỢ LÝ A.I BẰNG GIỌNG NÓI – TRƯNG VƯƠNG GARDEN")
st.subheader("Vui lòng bấm nút bên dưới để hỏi bằng giọng nói")

# Lưu trạng thái intro
if "intro_played" not in st.session_state:
    st.session_state.intro_played = False

# Lưu trạng thái kết thúc
if "ended" not in st.session_state:
    st.session_state.ended = False

# ------------------------------------------------------------------------------------
# PHÁT INTRO TỰ ĐỘNG KHI MỞ APP
# ------------------------------------------------------------------------------------
if not st.session_state.intro_played:
    st.session_state.intro_played = True
    intro_audio = text_to_speech(INTRO_TEXT)
    play_audio(intro_audio)
    st.info("👆 Đây là lời chào tự động. Mời bạn bấm nút bên dưới để đặt câu hỏi.")
    st.stop()


# ------------------------------------------------------------------------------------
# NÚT GHI ÂM – “BẤM ĐỂ HỎI”
# ------------------------------------------------------------------------------------
audio_uploaded = st.audio_input("🎤 **Bấm để hỏi** – nói câu hỏi của bạn", label_visibility="visible")


# ------------------------------------------------------------------------------------
# NÚT KẾT THÚC
# ------------------------------------------------------------------------------------
if st.button("⛔ KẾT THÚC TƯƠNG TÁC"):
    bye_audio = text_to_speech("Cảm ơn bạn đã ghé thăm Trưng Vương Garden. Hẹn gặp lại bạn.")
    play_audio(bye_audio)
    st.session_state.ended = True

if st.session_state.ended:
    st.warning("👉 Phiên tương tác đã kết thúc.")
    st.stop()


# ------------------------------------------------------------------------------------
# XỬ LÝ KHI CÓ ÂM THANH ĐẦU VÀO
# ------------------------------------------------------------------------------------
if audio_uploaded is not None:
    with st.spinner("⏳ Đang nhận diện giọng nói..."):
        user_text = speech_to_text(audio_uploaded)

    st.success(f"**Bạn hỏi:** {user_text}")

    # Tìm câu trả lời JSON
    answer = lookup_answer(user_text)

    # Hiển thị text
    st.write("### 📌 Trợ lý trả lời:")
    st.write(answer)

    # Nói bằng giọng
    audio_reply = text_to_speech(answer)
    play_audio(audio_reply)

    st.info("Bạn có thể tiếp tục bấm nút để hỏi thêm.")
