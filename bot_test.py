import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import os
import time

class VoiceChatBot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.name = "Bot Response"
        self.get_time_response = lambda: f"ตอนนี้เวลา {time.strftime('%H:%M')}"
        self.responses = {
            "สวัสดี": "สวัสดี มีอะไรให้ช่วยไหม",
            "ชื่อ": f"ฉันชื่อ {self.name} ",
            "กี่โมง": self.get_time_response,
            "เวลา": self.get_time_response,
            "ขอบคุณ": "ยินดีมาก มีอะไรให้ช่วยอีกไหม",
            "ลาก่อน": "ลาก่อน"
        }

    def speak(self, text):
        print(f"{self.name}: {text}")
        tts = gTTS(text=text, lang='th', slow=False)
        tts.save("response.mp3")
        mixer.init()
        mixer.music.load("response.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        mixer.music.stop()
        mixer.quit()
        os.remove("response.mp3")

    def listen(self):
        with sr.Microphone() as source:
            self.speak("ฉันกำลังฟังอยู่ พูดมาเลย")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                user_input = self.recognizer.recognize_google(audio, language='th-TH')
                print(f"คุณ: {user_input}")
                return user_input.lower()
            except sr.WaitTimeoutError:
                self.speak("Time out ลองพูดใหม่")
                return ""
            except sr.UnknownValueError:
                self.speak("ไม่เข้าใจที่คุณพูด ลองพูดใหม่นะ")
                return ""


    def process_input(self, user_input):
        if not user_input:
            return "คุณไม่ได้พูดอะไรเลย มีอะไรให้ช่วยไหม"
        
        # รวบรวมคำตอบจากทุกคีย์เวิร์ดที่เจอ
        matched_responses = []
        for keyword, response in self.responses.items():
            if keyword in user_input:
                if callable(response):
                    matched_responses.append(response())
                else:
                    matched_responses.append(response)
        
        # ถ้ามีคำตอบมากกว่า 1 ให้รวมกัน (string)
        if matched_responses:
            if "ลาก่อน" in user_input:  
                return "ลาก่อน"
            return " ".join(matched_responses)  # รวมคำตอบด้วยช่องว่าง
        return "ขอโทษนะ ฉันไม่เข้าใจ"

    def run(self):
        self.speak(f"สวัสดี ฉันคือ {self.name}")
        self.speak("พูด 'ลาก่อน' ถ้าต้องการปิดระบบ")
        
        while True:
            try:
                user_input = self.listen()
                if user_input:
                    response = self.process_input(user_input)
                    self.speak(response)
                    if "ลาก่อน" in user_input:
                        break
            except KeyboardInterrupt:
                self.speak("ลาก่อนนะ")
                break

if __name__ == "__main__":
    bot = VoiceChatBot()
    bot.run()