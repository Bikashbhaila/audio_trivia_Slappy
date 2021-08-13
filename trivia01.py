#!/usr/bin/env python3

import requests

from main import *

import audioop
import threading
from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from time import ctime
import webbrowser
import time
import os
import random
from gtts import gTTS
import playsound

# initialize recognizer
recognizer = sr.Recognizer()


def startQuiz():
    API_URL = "https://opentdb.com/api.php?amount=3&difficulty=easy"
    response = requests.get(API_URL)
    trivia_dict = response.json().get("results")
    return trivia_dict

def respond(trivia_dict):
    user_score = 0
    for trivia in trivia_dict:
        question = (trivia["question"])
        ques = question.strip("&quot;") # &#039;s
        speak(ques)
        voice_answer = recordVoice()
        print(voice_answer)
        # respond(voice_data, trivia_dict)
        if trivia["correct_answer"] in voice_answer:
            user_score += 1
            speak("CORRECT. Great work.")
        else:
            speak("WRONG. The correct answer is " + trivia["correct_answer"])
    print(f"Your FINAL SCORE is", user_score)

def recordVoice():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            voice_data = recognizer.recognize_google(audio)
            print(voice_data)
        except sr.UnknownValueError:
            speak("Sorry, I did not get it..")
        except sr.RequestError:
            speak("Sorry, the service is unavailable")
        return voice_data

def speak(audio_string):
    tts = gTTS(text=audio_string, lang="en")
    r = random.randint(1, 10000000)
    audio_file = 'audio.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file, block=False)
    print(audio_string)
    os.remove(audio_file)


# def respond(voice_data):

    # if "what is your name" in voice_data:
    #     speak("My name is Slappy..")
    # if "what time is it" in voice_data:
    #     speak(ctime())
    # if 'search' in voice_data:
    #     search = recordVoice("What do you want to search for?")
    #     url = "https://google.com/search?q=" + search
    #     webbrowser.get().open(url)
    #     speak("Here's the results for " + search)
    # if 'location' in voice_data:
    #     location = recordVoice("What is the location?")
    #     url = "https://google.nl/maps/place/" + location + "/&amp;"
    #     webbrowser.get().open(url)
    #     speak("Here's the location for " + location)
    # if 'stop' in voice_data:
    #     exit()


def main():

    startQuiz()
    respond(startQuiz())

        
    # while True:
    #     startQuiz()
    #     wantRestart = input("Do you want to play again? [Yes/No]\n>> ").lower()
    #     if wantRestart == "yes":
    #         print("Sure, good luck this time")
    #         continue
    #     else:
    #         print("Thanks for playing")
    #         break

if __name__ == "__main__":
    main()

