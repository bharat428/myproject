import pyttsx3
import pythonwin.win32ui
import datetime
import speech_recognition as sr
import wikipedia 
import smtplib
import webbrowser as wb
import psutil 
import pyjokes
import os
import pyautogui
import random
import json
import requests
from urllib.request import urlopen
import wolframalpha
engine = pyttsx3.init()
wolframalpha_app_id = 'wolfram alpha id will go here'


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time=datetime.datetime.now().strftime("%H:%M:%S")
    speak("The current time is")
    speak(Time) 

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak("The current date is")
    speak(date)
    speak(month)
    speak(year)

def wishme():
    speak("Welcome back bharat")
    time_()
    date_()


    hour = datetime.datetime.now().hour

    if hour>=6 and hour<12:
        speak("Good Morning sir!")
    elif hour>=12 and hour<18:
        speak("Good afternoon sir!")
    elif hour>=18 and hour<24:
        speak("Good evening sir!")
    else:
        speak("Good Night sir!")

    speak("Jarvis at your service. please tell me how can I help you")        


def TakeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_thershold = 1
        audio = r.listen(source)

    try:
         print("Recognizing")
         query = r.recognize_google(audio,language='en-US')
         print(query) 

    except Exception as e:
         print(e)
         print("Say that again please.....")
         return "None"

    return query

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()    

    server.login('bharatsharma.bs50521@gmail.com','shivanilovebharat')
    server.sendmail('username@gmail.com',to,content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save('C:/Users/bhara/Desktop/screenshot.png')    


def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at'+usage) 

    battery = psutil.sensors_battery()
    speak('Battery is at')
    speak(battery.percent)   


def joke():
    speak(pyjokes.get_joke())    

if __name__ == "__main__":

    wishme()

    while True:
        query = TakeCommand().lower()

        if 'time' in query: 
            time_()
        elif 'date' in query:
            date_()

        elif 'wikipedia' in query:
            speak("searching...")
            query=query.replace('wikipedia','')
            result=wikipedia.summary(query,sentences=3)
            speak('According to wikipedia')
            print(result)
            speak(result)   

        elif 'send email' in query:
            try:
                speak("what should I say")
                content=TakeCommand()
                
                speak("who is the Reciever")
                reciever=input("Enter Reciever's Email : ")
                to = reciever
                sendEmail(to,content)
                speak(content)
                speak('Email has been sent..')

            except Exception as e:
                print(e)
                speak("unable to send Email.")    

        elif 'search in chrome' in query:
            speak('What should I search?')
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com')


        elif 'search youtube' in query:
            speak('what should I search?')
            search_Term = TakeCommand().lower()
            speak('here we go to youtube')
            wb.open('https://www.youtube.com/results?search_query='+search_Term)

        elif 'search google' in query:
            speak('what should I search')
            search_Term = TakeCommand().lower()
            speak('seaerching...')
            wb.open('https://www.google.com/search?q='+search_Term) 


        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()   


        elif 'go offline' in query:
            speak('Going offline sir!')
            quit()   

        elif 'word' in query:
            speak('opening MS word')
            ms_word = r'C:/ProgramData/Microsoft/Windows/StartMenu/programs/Word 2016.EXE'
            os.startfile(ms_word)   

        elif 'write a note' in query:
            speak("what should i write , sir")
            notes = TakeCommand()
            file = open('notes.txt','w')
            speak("sir should i indlcude date and time")
            ans = TakeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(':-')
                file.write(notes)
                speak('Done Taking Notes Sir')  
            else:
                file.write(notes)  

        elif 'show note' in query:
            speak('showing Notes')
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())   
            
        elif 'screenshot' in query:
            screenshot()

        elif 'play music' in query:
            songs_dir = 'D:/Songs'  
            music = os.listdir(songs_dir) 
            speak('what should I play')
            speak('select a number..')
            ans = TakeCommand().lower()
            if 'number' in ans:
                no = int(ans.replace('number',''))
            elif 'random' or 'you choose' in ans:
                no = random.randint(1,100)  
            
            os.startfile(os.path.join(songs_dir,music[no]))

        elif 'remember that' in query:
            speak("what should I remember")
            memory = TakeCommand()
            speak("You asked me to remember that") 
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()

        elif "do you remember anyhitng" in query:
            remember = open('memory.txt','r')
            speak('You asked me to remember that'+remember.read())  

        elif 'news' in query:
            try:
                jsonObj = urlopen("http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=43829a569723423da4aabc57e3844cd1")
                data = json.load(jsonObj)
                i = 1

                speak('Here are some top headlines from bussiness')
                print('========Top headlines=======')
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['title'])
                    i += 1

            except Exception as e:
                      print(str(e))     


        elif 'where is' in query:
            query = query.replace("where is","")
            location = query
            speak("user asked to locate"+ location)
            wb.open_new_tab("https://www.google.com/maps/places/"+location)
                            
        elif 'calculate' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(''.join(query))
            answer = next(res.results).text
            print('The answer is : '+answer)
            speak('The answer is '+ answer)





              



                   



                          
