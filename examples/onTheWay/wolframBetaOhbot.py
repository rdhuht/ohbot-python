##  Example of ohbot intergrated with wolfram alpha and wikipedia web service
##  recognition voice and response by ohbot TODO

import azure.cognitiveservices.speech as speechsdk
import wolframalpha
from ohbot import ohbot
from random import *
import threading
import pyttsx3
# import speech_recognition as sr 替换成azure方案
import datetime
import wikipedia
import webbrowser
import os
import smtplib

wiki = False

key = input('key:')
speech_key, service_region = key, "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
wolfclient = wolframalpha.Client('34YK5Q-QE9KPXKH35')

connectingPhrases = ['Let me think',
                     'Just a second',
                     'give me a moment',
                     'thats an easy one',
                     'thats tricky',
                     'i know this one',
                     'let me get you an answer']

ohbot.reset()


def handleInputWiki(text):
    if not text == None:
        ohbot.say("You ask this question to me " + text)
        ohbot.setEyeColour(10, 5, 0, True)
        randIndex = randrange(0, len(connectingPhrases))

        choice = connectingPhrases[randIndex]
        ohbot.move(ohbot.HEADTURN, 5)
        ohbot.move(ohbot.EYETILT, 7)
        ohbot.move(ohbot.HEADNOD, 9)
        ohbot.say(choice)

        try:
            res = wikipedia.summary(text)
            ohbot.say(res)
            ohbot.setEyeColour(0, 10, 0, True)

        except:

            print('Answer not available')
            ohbot.say("Answer not available")
            ohbot.setEyeColour(10, 0, 0, True)
            ohbot.move(ohbot.HEADTURN, 5)


def moveLoop():
    while True:
        ohbot.move(randint(0, 2), randint(0, 9))

        ohbot.wait(randint(0, 3))


def blinking():
    while True:
        ohbot.move(ohbot.LIDBLINK, 0, 10)

        ohbot.wait(random() / 3)

        ohbot.move(ohbot.LIDBLINK, 10, 10)

        ohbot.wait(randint(0, 6))


# 根据当前事件问候
def withMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        ohbot.say("Good morning!")
    elif hour >= 12 and hour < 18:
        ohbot.say("Good Afternoon")
    else:
        ohbot.say('Good Evening')
    ohbot.say("I am ohbot. How may I help you?")


# microphone listen
def takeCommand():
    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once()
    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


withMe()
while True:
    text = takeCommand()
    if not text is None:
        handleInputWiki(text)
