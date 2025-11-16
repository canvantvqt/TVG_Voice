# streamlit_app.py
# -*- coding: utf-8 -*-
import streamlit as st
import json

# ---- HÀM TRA CỨU JSON ----
def find_answer(user_text):
    """Tra cứu câu trả lời từ file JSON faq_garden.json"""
    try:
        with open("faq_garden.json", encoding="utf-8") as f:
            faq_data = json.load(f)
    except Exception:
        return "Xin lỗi, hiện tại tôi không thể truy cập dữ liệu tư vấn."

    for item in faq_data.get("faq", []):
        for kw in item.get("question", []):
            if kw.lower() in user_text.lower():
                return item.get("answer", "")
    return ("Xin lỗi, tôi chưa hiểu câu hỏi của bạn. "
            "Bạn có thể hỏi về giờ mở cửa, giá vé, trải nghiệm, ẩm thực, khuyến mãi hoặc liên hệ.")

# ---- HÀM TTS TRÊN TRÌNH DUYỆT ----
def tts_browser(text):
    """Dùng SpeechSynthesis API của trình duyệt để đọc text"""
    st.components.v1.html(f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.lang = "vi-VN";
    window.speechSynthesis.speak(msg);
    </script>
    """, height=0)

# ---- STREAMLIT UI ----
st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

st.markdown("""
**Hướng dẫn ngắn:**
1) Nhấn **Phát lời chào** để nghe giới thiệu.  
2) Nhấn **Bấm để hỏi**, nói câu hỏi hoặc nhập văn bản.  
3) Trợ lý trả lời bằng âm thanh.  
4) Nhấn **Kết thúc** để chào tạm biệt.
""")

col1, col2, col3 = st.columns(3)

if 'assistant_running' not in st.session_state:
    st.session_state.assistant_running = False

if 'user_question' not in st.session_state:
    st.session_state.user_question = ""

# ---- NÚT PHÁT LỜI CHÀO ----
with col1:
    if st.button("▶️ Phát lời chào"):
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
        tts_browser(intro_text)

# ---- NÚT BẤM ĐỂ HỎI ----
with col2:
    user_input = st.text_input("💬 Vui lòng bấm để hỏi và nhập câu hỏi:", st.session_state.user_question)
    if st.button("🎤 Hỏi"):
        if user_input.strip() != "":
            st.session_state.user_question = user_input
            answer = find_answer(user_input)
            st.markdown(f"**Trợ lý trả lời:** {answer}")
            tts_browser(answer)

# ---- NÚT KẾT THÚC ----
with col3:
    if st.button("⏹ Kết thúc"):
        goodbye_text = "Cảm ơn bạn đã tương tác. Chào tạm biệt!"
        tts_browser(goodbye_text)
        st.session_state.user_question = ""

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)
