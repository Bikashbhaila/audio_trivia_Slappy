from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import webbrowser
from datetime import datetime
import os
import time
import random
from gtts import gTTS
import playsound
import requests
import html


app = Flask(__name__)

# initialize recognizer
recognizer = sr.Recognizer()


def recordVoice(ask = False):
    # use speech recog's microphone to record response
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = recognizer.listen(source)
        # pass recorded voice recognize google to return voice data
        try:
            voice_data = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            voice_data = recognizer.recognize_google(audio)
            speak("Sorry, I did not get it..")
        except sr.RequestError:
            speak("Sorry, the service is unavailable")
        return voice_data

def speak(audio_string):
    print(audio_string)
    # use google text to speech to convert text to audio file
    tts = gTTS(text=audio_string, lang="en")
    # use random to generate and save file name as mp3
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save("C:\\AmazonSDE\\4-python\\python_atlas\\self_study_project - Copy\\"+ audio_file)
    # use playsound to play the stored audio file
    playsound.playsound("C:\\AmazonSDE\\4-python\\python_atlas\\self_study_project - Copy\\" + audio_file)
    # remove audio once read by playsound
    os.remove("C:\\AmazonSDE\\4-python\\python_atlas\\self_study_project - Copy\\" + audio_file)


def respond(voice_data):
    # based on inputs from voice recording respond accordingly 
    if "your name" in voice_data:
        speak("My name is Slappy..")
    if "what day is it" in voice_data:
        current_day = str(datetime.now().strftime("%A"))
        speak(f"Today is {current_day}")
    if "what time is it" in voice_data:
        current_time = str(datetime.now().strftime("%H:%M"))
        speak(f"It's {current_time}")
    if "search" in voice_data:
        search = recordVoice("What do you want to search for?")
        # prompt user for search term and open browsrt for search results
        url = "https://google.com/search?q=" + search
        webbrowser.get().open(url)
        speak("Here's the results for " + search)
    if "location" in voice_data:
         # prompt user for search location and open browsrt for search results
        location = recordVoice("What is the location?")
        url = "https://google.nl/maps/place/" + location + "/&amp;"
        webbrowser.get().open(url)
    if "trivia" in voice_data:
        # call playtrivia method to start trivia
        speak("Good Luck...")
        playTrivia(getQuestions())
    if "stop" in voice_data:
        speak("Goodbye...")
        exit()

    print("Listening ....")


def getQuestions():
    # if user input includes trivia, fetch 5 trivia questions from open trivia db and return results
    API_URL = "https://opentdb.com/api.php?amount=5&difficulty=easy"
    response = requests.get(API_URL)
    trivia_dict = response.json().get("results")
    return trivia_dict

def playTrivia(trivia_dict):
    # track user score
    user_score = 0
    # loop through each questions from trivia api questions
    for trivia in trivia_dict:
        question = trivia["question"]
        correct_answer = trivia["correct_answer"].strip().lower()
        # use html unescape to remove escaping chars from trivia questions returned
        ques = html.unescape(question)
        # pass questions to speak function
        speak(ques)
        print("API ANSWER: " + correct_answer)
        voice_answer = recordVoice().strip().lower()
        print("You said: " + voice_answer)

        # check for answer and update user score and respond
        if correct_answer in voice_answer:
            user_score += 1
            speak("CORRECT. Great work.")
        else:
            speak("WRONG. The correct answer is " + correct_answer)
    speak(f"Your FINAL SCORE is {user_score}")
    speak("What else can I do for you?")

def main():
    time.sleep(1)
    speak('Hello, How can I help you?')
    while 1:        
        voice_data = recordVoice()
        respond(voice_data)

if __name__ == "__main__":
    main()


