from shlex import quote
import subprocess
import pygame  # Updated import
import eel
import pvporcupine
import pyaudio
import pyautogui
from engine.config import ASSISTANT_NAME
import os
import pywhatkit as kit
from engine.command import speak
import re
import sqlite3
import webbrowser
import time
import struct
from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("kaido.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Keep script running until audio finishes
        pygame.time.Clock().tick(10)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on youtube")
    kit.playonyt(search_term)


#hotword detection
#done with pvporcupine and pyaudio
#pip install pvporcupine pyaudio
#pip install pyautogui , it is used for controlling the mouse and keyboard
#pip install pyttsx3 , it is used for text to speech conversion
#pip install pygame
#pip install pywhatkit , is used for sending messages on whatsapp and playing youtube videos
#pip install hugchat
#pip install eel
#pip install webbrowser
#pip install struct , it used for packing and unpacking binary data
#pip install sqlite3
#pip install re
#re is used for regular expression operations
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        # pre-trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length, keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detected or not
            if keyword_index >= 0:
                print("hotword detected")   
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

            
# find contacts
# it is used for finding contacts from the contact database , done by syntax analyzing the query 
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contact WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    

def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        kaido_message = "message sent successfully to " + name
    elif flag == 'call':
        target_tab = 7
        message = ''
        kaido_message = "calling " + name
    else:
        target_tab = 6
        message = ''
        kaido_message = "starting video call with " + name

    encoded_message = quote(message)
    print(encoded_message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')
    for i in range(1, target_tab):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')
    speak(kaido_message)


def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
