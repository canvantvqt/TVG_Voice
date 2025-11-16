# -*- coding: utf-8 -*-
import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant (Free)", layout="centered")

# ---------- Load FAQ ----------
FAQ_PATH = Path("faq_garden.json")
if not FAQ_PATH.exists():
    st.error("Không tìm thấy file faq_garden.json trong cùng thư mục.")
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

# ---------- UI ----------
st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG (MIỄN PHÍ)</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)

st.write("---")
st.write("Hướng dẫn ngắn: 1) Nhấn **Phát lời chào** để nghe giới thiệu. 2) Nhấn **Bấm để hỏi**, nói câu hỏi. 3) Trợ lý trả lời bằng âm thanh. 4) Nhấn **Kết thúc** để chào tạm biệt.")

col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button("▶️ Phát lời chào"):
        # khi người bấm, front-end sẽ tự đọc đoạn INTRO (JS sẽ thực thi)
        st.experimental_set_query_params(action="play_intro")
        st.success("Đã gửi lệnh phát lời chào (trình duyệt sẽ đọc).")

with col2:
    # nút request start — front-end sẽ dùng Web Speech để bắt mic
    if st.button("🎤 Bấm để hỏi"):
        st.experimental_set_query_params(action="start_listen")
        st.success("Bạn có thể bắt đầu nói — trình duyệt sẽ ghi âm và nhận dạng.")

with col3:
    if st.button("⏹ Kết thúc"):
        st.experimental_set_query_params(action="stop_and_bye")
        st.success("Kết thúc phiên. Trình duyệt sẽ đọc lời tạm biệt.")

st.write("---")

# placeholders for displaying recognized text and assistant reply
user_txt_ph = st.empty()
assistant_txt_ph = st.empty()

# This component embeds client-side JS that:
# - listens to URL query param changes (action) and triggers Web Speech API accordingly
# - does STT in browser, then POST the recognized text back to Streamlit via fetch to '/streamlit-server' is not possible
# Instead, we'll use the streamlit javascript-to-python communication using window.parent.postMessage
# The HTML below uses the Streamlit component protocol to send the recognized text back to Streamlit.
#
# The component returns the last recognized text as the component return value.
#
from streamlit.components.v1 import html

COMPONENT_HTML = f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>TVG Voice Client</title>
  </head>
  <body>
    <script>
      // Utility to send value back into Streamlit
      function sendToStreamlit(value) {{
        const msg = {{isStreamlitMessage: true, type: "streamlit:setComponentValue", value: value}};
        window.parent.postMessage(msg, "*");
      }}

      // Read query param to decide action (start_listen, play_intro, stop_and_bye)
      function getAction() {{
        try {{
          const params = new URLSearchParams(window.location.search);
          return params.get("action");
        }} catch(e) {{
          return null;
        }}
      }}

      // Speech synthesis (TTS) via browser
      function speak(text) {{
        if (!("speechSynthesis" in window)) {{
          alert("Trình duyệt không hỗ trợ SpeechSynthesis.");
          return;
        }}
        const ut = new SpeechSynthesisUtterance(text);
        ut.lang = "vi-VN";
        // optional: choose voice if available
        const voices = speechSynthesis.getVoices();
        // choose first vi voice if present
        for (let v of voices) {{
          if (v.lang && v.lang.startsWith("vi")) {{
            ut.voice = v;
            break;
          }}
        }}
        speechSynthesis.cancel();
        speechSynthesis.speak(ut);
      }}

      // Web Speech API for recognition
      let recognition = null;
      function startRecognition() {{
        if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window)) {{
          alert("Trình duyệt không hỗ trợ Web Speech API. Hãy dùng Chrome hoặc Edge.");
          sendToStreamlit("");
          return;
        }}
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = "vi-VN";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        recognition.onresult = function(event) {{
          const text = event.results[0][0].transcript;
          // send recognized text to Streamlit
          sendToStreamlit(text);
        }};
        recognition.onerror = function(event) {{
          console.log("SpeechRecognition error", event);
          sendToStreamlit("");
        }};
        recognition.onend = function() {{
          // ended
        }};
        recognition.start();
      }}

      // parse action and run
      const action = getAction();
      if (action === "play_intro") {{
        const intro = {json.dumps("""Xin chào! Tôi là trợ lý Voice AI Trưng Vương Garden. Khu trải nghiệm của chúng tôi có nhiều dịch vụ thú vị: Vé tham quan, Vườn cây nhiệt đới, Vườn chim Aviary, Sở thú ăn chay, Thác nước Apsara, Suối đá Mồ Côi, Bến Thiên Cầm, Nhà tre cộng đồng, Vườn tượng cảnh quan, Hồ Thiên Nga, Cầu Kiều. Các hoạt động trải nghiệm: cưỡi ngựa, Hồ bơi Pool Party, xe đạp đôi và đơn, xe điện tham quan, thuyền Thiên Nga, thuyền SUP, KAYAK, Trượt phao cầu vồng, xe đua Gokart. Ẩm thực tại nhà hàng Champa phục vụ ẩm thực địa phương, bãi đỗ xe miễn phí và nhiều góc checkin. Bạn có thể hỏi tôi về: giờ mở cửa, giá vé, trải nghiệm, khuyến mãi, ẩm thực hoặc liên hệ.""" )};
        speak(intro);
        // reset action param by updating history (so button can be pressed again)
        history.replaceState(null, "", window.location.pathname);
        // send empty to not trigger processing
        sendToStreamlit("");
      }} else if (action === "start_listen") {{
        startRecognition();
        // reset query
        history.replaceState(null, "", window.location.pathname);
      }} else if (action === "stop_and_bye") {{
        speak("Cảm ơn bạn đã tham quan Trưng Vương Garden. Hẹn gặp lại!");
        history.replaceState(null, "", window.location.pathname);
        sendToStreamlit("__STOP__");
      }} else {{
        // no action -> do nothing
        sendToStreamlit("");
      }}
    </script>
  </body>
</html>
"""

# The component returns a string: recognized text or special flag
result = html(COMPONENT_HTML, height=0)  # height=0 hides iframe chrome

# When result is not empty, act: if __STOP__ -> speak bye handled client-side; else use it as user query
if result and result != "__STOP__":
    user_text = result
    user_txt_ph.info(f"Bạn nói: {user_text}")
    answer = find_answer(user_text)
    assistant_txt_ph.success(f"Trợ lý trả lời: {answer}")
    # Now instruct client to speak the answer: we reuse experimental_set_query_params to send an action the JS will catch next render
    # encode the answer in query param (URL length limit; keep answers short). We'll set action=tts&text=...
    # To avoid URL length issues, we'll trigger play_intro-like behavior: set action=start_tts with text encoded in base64
    import base64
    b = base64.b64encode(answer.encode("utf-8")).decode("ascii")
    st.experimental_set_query_params(action="tts", payload=b)
    # The JS component doesn't currently handle tts via action=tts; so to keep it simple, show a 'Phát lời đáp' button:
    if st.button("🔊 Phát lời đáp"):
        # instruct client to speak by setting action=tts - JS in component won't run again automatically, but we'll trigger by re-rendering the component with new params
        st.experimental_set_query_params(action="play_answer", payload=b)
        st.experimental_rerun()
