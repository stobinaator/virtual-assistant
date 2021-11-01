# -*- coding: utf-8 -*-
from __future__ import print_function

import requests
import json
import datetime
import pickle
import os.path
import webbrowser
import random
import wikipedia
import time
import os

from time import ctime
from configparser import ConfigParser
import speech_recognition as sr
from gtts import gTTS
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# accessing information from config.ini
apis = config_object["APIS"]
scopes = config_object["SCOPES"]
keys = config_object["KEYS"]


with open('greetings.json') as greet_f:
    data = json.load(greet_f)
    GREETING_RESPONSES = data['greeting responses']
    GREETING_NAMES = data['greeting names']

times = 0
listening = True

def listen():
    global times
    global listening

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("I am listening..." + "\n")
        audio = r.listen(source)
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data + "\n")
        times = 0
    except sr.UnknownValueError:
        if times < 4:
            print("Google Speech Recognition did not understand audio" + "\n")
            times += 1
        else:
            data = "stop listening"
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return data


def respond(audioString):
    print(audioString + "\n")
    tts = gTTS(text=audioString, lang='en')
    tts.save("speech.mp3")
    os.system("mpg321 -q speech.mp3")
    time.sleep(2)


def calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    try:
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config.ini', scopes["google_calendar"])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        print('Getting the upcoming 5 events...')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=5, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    except json.decoder.JSONDecodeError:
        print("whoops..something went wrong.")


def weather(data):
    listening = True
    data = data.split(" ")
    location = str(data[5])
    units = "metric"
    url = apis["weather_api"] + "appid=" + keys["weather_api_key"] + "&q=" + location + "&units=" + units
    js = requests.get(url).json()
    if js["cod"] != "404":
        weather = js["main"]
        temp = weather["temp"]
        temp_min = weather["temp_min"]
        temp_max = weather["temp_max"]
        temp_feels = weather["feels_like"]
        #hum = weather["humidity"]
        desc = js["weather"][0]["description"]
        resp_string = " The temperature in {0} in Celsius is ".format(location) \
            + str(temp) + "°C. But it really feels like " + str(temp_feels) \
            + "°C. Minimum is " + str(temp_min) + " and Maximum is " + str(temp_max) \
            + "°C. The weather description is: " + str(desc)
        respond(resp_string)
    else:
        respond("City not found")


def maps(data):
    listening = True
    data = data.split(" ")
    location_url = "https://www.google.com/maps/place/" + str(data[2]) + "," \
        + str(data[3])
    respond("Hold on Stoyan, I will show you where " + data[2] + "," +  data[3] + " is.")
    webbrowser.open(location_url)


def sites(s):
    listening=True
    respond("Redirecting to " + s.upper() + "\n")
    if s == "golem":
        webbrowser.open("https://www." + s + ".de", new=2)
    else:
        webbrowser.open("https://www." + s + ".com", new=2)


def search(data):
    listening = True
    data = data.split(" ")
    words = data[1:]
    sentence = ""
    for word in words:
        sentence += word
        sentence += "+"

    location_url = "https://www.google.com/search?q=" + sentence
    respond("Let me Google that for you..." + "\n")
    webbrowser.open(location_url, new=2)


def open(data):
    listening = True
    data = data.split(" ")
    app = str(data[1])
    if app == 'Messenger':
        arg = '/usr/bin/open -a  "/Applications/Messenger.app"'
        os.system(arg)
    elif app == 'Spotify' or app == 'spotify':
        arg = '/usr/bin/open -a  "/Applications/Spotify.app"'
        os.system(arg)


def choices():
    print("Which site would you like to visit?")
    print("1. Reddit")
    print("2. BBC")
    print("3. Golem")
    print("4. Polygon")


def chuck_norris_joke():
    listening = True
    json = requests.get(apis["chuck_api"]).json()
    print("Here is a joke.." + "\n")
    respond(json["value"])


def random_number_facts():
    listening = True
    js = requests.get(apis["trivia_api"])
    js2 = requests.get(apis["date_api"])
    respond(js.content.decode('utf-8'))
    print("\n")
    respond(js2.content.decode('utf-8'))


def random_advice():
    listening = True
    js = requests.get(apis["advice_api"]).json()
    print("Here is an advice.." + "\n")
    respond(js["slip"]["advice"])



# Function to get a person first and last name
def get_person(data):
    try:
        wordList = data.split(" ") # Split the text into a list of words
        for i in range(0, len(wordList)):
          if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':

                  person = wordList[i + 2] + ' ' + wordList[i + 3]

          wiki = wikipedia.summary(person, sentences=2)
          respond(wiki)
    except wikipedia.exceptions.PageError:
        print("wooops. didn't get that. can you repeat?")


def digital_assistant(data):

    global listening

    if "who is" in data:
        listening = True
        get_person(data)

    if "how are you" in data:
        listening = True
        respond("I am well")

    if "what time is it" in data:
        listening = True
        respond(ctime())

    if "where is" in data:
        maps(data)

    if "what is the weather in" in data:
        weather(data)

    if "search" in data:
        search(data)

    if "calendar" in data:
        calendar()

    if "open" in data:
        open(data)

    if "sites" in data:
        choices()

    if "Reddit" in data:
        sites("reddit")
    elif "BBC" in data:
        sites("bbc")
    elif  "golem" in data:
        sites("golem")
    elif "polygon" in data:
        sites("polygon")

    if "Chuck Norris" in data:
        chuck_norris_joke()

    if "numbers" in data:
        random_number_facts()

    if "advice" in data:
        random_advice()

    if "who made you" in data or "who created you" in data:
        listening = True
        respond("I was built by Stoyan.")


    if "stop listening" in data or "thank you" in data:
        listening = False
        print("Listening stopped")
        respond("Bye")
        return listening


    return listening



def main():
    global listening
    global times
    for key in apis:
        print(key)
    time.sleep(2)
    respond(random.choice(GREETING_RESPONSES) + " , " + random.choice(GREETING_NAMES) + "?")

    while listening == True:
        data = listen()
        listening = digital_assistant(data)


if __name__ == '__main__':
    main()
