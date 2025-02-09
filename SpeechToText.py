import speech_recognition as sr

mic_index = 3  # เลขlistของmicrophone
mic = sr.Microphone(device_index=mic_index)
recog = sr.Recognizer()
recog.pause_threshold = 2

with mic as source:
    print("Listening......🎙️")
    recog.adjust_for_ambient_noise(source)  # ลดnoise
    try:
        audio = recog.listen(source)
        text = recog.recognize_google(audio, language='th')
        print("Result:", text)
    except sr.UnknownValueError:
        print("Can not use mic⚠️")
    except sr.WaitTimeoutError:
        print("Time out nobody speak❌")
