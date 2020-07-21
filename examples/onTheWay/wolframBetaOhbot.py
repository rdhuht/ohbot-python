##  Example of ohbot intergrated with wolfram alpha and wikipedia web service
##  recognition voice and response by ohbot TODO

import wolframalpha
from ohbot import ohbot
from random import *
import threading
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

wiki = False

wolfclient = wolframalpha.Client('34YK5Q-QE9KPXKH35')

connectingPhrases = ['Let me think',
                     'Just a second',
                     'give me a moment',
                     'thats an easy one',
                     'thats tricky',
                     'i know this one',
                     'let me get you an answer']

ohbot.reset()


def handleInput():
    while True:
        text = input("Question:\n")
        ohbot.say(text)
        ohbot.setEyeColour(10, 5, 0, True)
        randIndex = randrange(0, len(connectingPhrases))

        choice = connectingPhrases[randIndex]
        ohbot.move(ohbot.HEADTURN, 5)
        ohbot.move(ohbot.EYETILT, 7)
        ohbot.move(ohbot.HEADNOD, 9)
        ohbot.say(choice)

        try:
            res = wolfclient.query(text)
            ans = next(res.results).text
            ans = ans.replace("|", ".")
            ohbot.say(ans)
            ohbot.setEyeColour(0, 10, 0, True)

        except:

            print('Answer not available')
            ohbot.say("Answer not available")
            ohbot.setEyeColour(10, 0, 0, True)

        ohbot.move(ohbot.HEADTURN, 5)


def handleInputWiki():
    while True:
        text = input("Define:\n")
        ohbot.say(text)
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
    # ohbot.say("I am ohbot. How may I help you?")


# microphone listen
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        audio = r.listen(source)
    print(type(audio))
    # try:
    print('Recognizing...')
    query = r.recognize_bing(audio, key="38d239c4c6174854b7fd666eedfd67d2")  # 1 bing
    # query = r.recognize_sphinx(audio)  # 2 环境搭建复杂，不实用
    # query = r.recognize_google(audio)  # 3 网络慢,speech_recognition.RequestError: recognition connection failed: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
    # query = r.recognize_ibm(audio, username="7ea013a0-f3c6-420f-b787-62eabc334a71", password='201205211314jC')  # 4 IBM不再提供username和pwd的配合使用服务，之恩那个用key，但rs库没更新
    print(f'user said: {query}\n')
    # TODO 识别失败，先尝试bing，再尝试shpinx离线识别
    # handleInput()
    # except Exception as e:
    #     print("Say that again please")


# ohbot.say("Initializing ohbot")
withMe()
while True:
    takeCommand()
# ohbot.say("Hello ohbot here, please type in a question")

