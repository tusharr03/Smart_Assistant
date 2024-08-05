import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import time
import os

#pip install speech recognition
#pip install setuptools
#pip install gTTS (if you are making this project on a large scale then use)
#pip install pygame (to play mp3)

recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi = "78ec7d3e77d7414281db6d599c743516"

def speak_old(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts=gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the script running until the music finishes
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(
    api_key="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",
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in General Tasks like Alexa and Google Cloud. Give short responses"},
            {"role": "user", "content": "What is coding"}
        ]
    )

    return completion.choices[0].message



def ProcessCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=music_library.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        #here r stands for response
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
        # Parse the JSON response
            data = r.json()
    
            # Check if the response contains articles
            if 'articles' in data:
            # Loop through the articles and print the headlines
                for article in data['articles']:
                    speak(article['title'])
            else:
                print("No articles found")
        else:
            print(f"Failed to retrieve news: {r.status_code}")
        
    else:
        #let open ai handle the request
        aiProcess(c)

    


if __name__=="__main__":
    speak("Initializing Jarvis....")

    #Listen for the wake word Jarvis

    # obtain audio from the microphone
    r = sr.Recognizer()
    

    
while True:
    # recognize speech using Sphinx
    print("Recognizing..")
    try:
        with sr.Microphone() as source:
            print("Listening..")
            audio = r.listen(source,timeout=3,phrase_time_limit=3)
        word=r.recognize_google(audio)

        if(word.lower()=="jarvis"):
            speak("Ya")
            #Listen for command
            
            with sr.Microphone() as source:
                print("Jarvis Active.")
                audio = r.listen(source)
                command=r.recognize_google(audio)

                ProcessCommand(command)


        
    except Exception as e:
        print("error; {0}".format(e))
