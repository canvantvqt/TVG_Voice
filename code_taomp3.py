# -*- coding: utf-8 -*-
from gtts import gTTS

# Nội dung lời chào
intro_text = (
    "Xin chào! Tôi là trợ lý Voice AI Trưng Vương Garden. Rất vui vì bạn đã đến"
    "Bạn có thể hỏi tôi về giờ mở cửa, giá vé, trải nghiệm, khuyến mãi, ẩm thực hoặc liên hệ nhé. Vui lòng bấm nút để hỏi...  ."
)

# Tạo file MP3
tts = gTTS(text=intro_text, lang='vi')
tts.save("intro.mp3")

print("File intro.mp3 đã được tạo thành công!")
