from flask import Flask, request
import pygame
import platform
from plyer import notification
import subprocess
import os
app = Flask(__name__)

# Initialize the mixer module for playing sound
pygame.mixer.init()
buzzer_sound = pygame.mixer.Sound("buzzer.wav")

def display_popup(message):
    if platform.system() == "Darwin":  # macOS
        applescript = f'display dialog "{message}" with title "System Popup" buttons {{"OK"}}'
        subprocess.call(f"osascript -e '{applescript}'", shell=True)
    elif platform.system() == "Windows":  # Windows
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, "System Popup", 1)
    else:  # Assuming Linux or other Unix-like OS
        subprocess.call(['zenity', '--info', '--text=' + message, '--title=System Popup'])

@app.route('/alert', methods=['GET'])
def alert():
    try:
        # Set maximum volume differs by OS
        if platform.system() == "Darwin":  # macOS
            os.system('osascript -e "set volume output volume 100"')
        elif platform.system() == "Windows":  # Windows
            os.system('nircmd.exe setsysvolume 65535')
        elif platform.system() == "Linux":  # Linux and derivatives
            os.system('amixer set Master 100%')

        buzzer_sound.play()
        notification.notify(
            title='Emergency',
            message='An emergency alert was triggered!',
            app_name='Emergency Alert System'
        )
        message = request.args.get('message', 'Default message')
        display_popup(message)
        return "Emergency alert activated!"
    except Exception as e:
        return str(e)

@app.route('/pop', methods=['GET'])
def pop():
   return "pop"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
