import pygame
from gtts import gTTS as tts

pygame.mixer.init()

while True:
    langcode = input("Language code: ")
    text = input("Text: ")
    
    # if text.lower() == "exit":
    #     print("Exiting program.")
    #     break
    
    namef = input("file name: ") + ".mp3"
    
    audio = tts(text, lang=langcode)
    audio.save(namef)

    print("Playing audio file...")
    pygame.mixer.music.load(namef)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

