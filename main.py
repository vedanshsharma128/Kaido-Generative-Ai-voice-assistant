import os
import eel
import subprocess
from engine.features import *
from engine.command import *
from engine.auth import recognize

def start():
    eel.init("www")

    playAssistantSound()

    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")

        recognized_name = recognize.AuthenticateFace()  # Get recognized name

        if recognized_name != "unknown":
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak(f"Hello, Welcome {recognized_name}, How can I help you?")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Failed")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)
