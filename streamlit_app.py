# -*- coding: utf-8 -*-
import streamlit as st
import json

st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

# ---- HÀM TRA CỨU JSON ----
def find_answer(user_text):
    """Tra cứu câu trả lời từ file JSON faq_garden.json"""
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

# ---- GIAO DIỆN ----
st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

st.markdown("""
Hướng dẫn ngắn:  
1) Nhấn 🎤 Phát lời chào để nghe giới thiệu.  
2) Nhấn 💬 Bấm để hỏi, nhập câu hỏi hoặc upload file audio.  
3) Trợ lý trả lời bằng âm thanh và văn bản.  
4) Nhấn ⏹ Kết thúc để chào tạm biệt.
""")

# ---- BUTTONS ----
col1, col2, col3 = st.columns([1,1,1])

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# ---- Lời chào và tạm biệt ----
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

bye_text = "Cảm ơn bạn đã tham quan Trưng Vương Garden. Chào tạm biệt!"

# ---- PHÁT LỜI CHÀO ----
with col1:
    if st.button("🎤 Phát lời chào"):
        st.session_state.conversation.append(("TVG", intro_text))
        st.markdown(f"**Trợ lý:** {intro_text}")
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{intro_text}");
        msg.lang = "vi-VN";
        window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

# ---- BẤM ĐỂ HỎI ----
with col2:
    user_input = st.text_input("💬 Bấm để hỏi", key="user_input")
    if st.button("Gửi câu hỏi") and user_input:
        answer = find_answer(user_input)
        st.session_state.conversation.append(("Bạn", user_input))
        st.session_state.conversation.append(("TVG", answer))
        st.markdown(f"**Bạn:** {user_input}")
        st.markdown(f"**Trợ lý:** {answer}")
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{answer}");
        msg.lang = "vi-VN";
        window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

# ---- KẾT THÚC ----
with col3:
    if st.button("⏹ Kết thúc"):
        st.session_state.conversation.append(("TVG", bye_text))
        st.markdown(f"**Trợ lý:** {bye_text}")
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{bye_text}");
        msg.lang = "vi-VN";
        window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)
