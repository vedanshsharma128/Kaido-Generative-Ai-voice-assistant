import pyttsx3
import speech_recognition as sr
import eel
import time
from engine import volume_control
import os
import webbrowser

#used to speak and display message
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

#used to take command from user
#it uses speech recognition to take command from user and return the command in string format
def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)

        else:
            if "take screenshot" in query:
                from engine.screenshot import take_screenshot
                filename = take_screenshot()
                speak("Screenshot taken")
    
            elif "open notepad" in query:
                os.system("notepad.exe")
                speak("Opening Notepad")

            elif "what time is it" in query or "current time" in query:
                from datetime import datetime
                now = datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {now}")

            elif "take a note" in query:
                speak("What should I write?")
                note = takecommand()
                with open("notes.txt", "a") as f:
                    f.write(f"{note}\n")
                speak("Note saved.")

            elif "open browser" in query:
                import webbrowser
                webbrowser.open("https://www.google.com")
                speak("Opening browser")

            elif "shut down the system" in query:
                speak("Shutting down the system")
                os.system("shutdown /s /t 5")

            elif "volume" in query:
                handle_command(query)

            else:
                from engine.features import chatBot
                chatBot(query)


    except:
        print("error")



def handle_command(command):
    if "set volume to" in command:
        try:
            level = int(command.split("set volume to")[-1].strip().replace("%", ""))
            volume_control.set_volume(level)
            speak(f"Volume set to {level} percent")
        except ValueError:
            speak("Sorry, I didn't understand the volume level.")
    
    elif "mute volume" in command:
        volume_control.mute_volume()
        speak("Volume muted")

    elif "unmute volume" in command:
        volume_control.unmute_volume()
        speak("Volume unmuted")

    
    eel.ShowHood()