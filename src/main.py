
from PIL import Image, ImageGrab
import time
from threading import Thread
import gobzer
import tkinter as tk
import numpy as np
import cv2 as cv    

import undercut_checker.undercut_agent as undercut_agent
from undercut_checker.counter import log_amount


class MainAgent:
    def __init__(self):
        self.agents = []
        self.fishing_thread = None

        self.cur_img = None
        self.cur_imgHSV = None

        self.zone = "Feralas"
        self.time = "day"

def update_screen(agent):
    print("Starting computer vision screen update...")

    # root = tk.Tk()
    # width = root.winfo_screenwidth()
    # height = root.winfo_screenheight()

    while True:
        screenshot = ImageGrab.grab()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        screenshotHSV = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
        agent.cur_img = screenshot
        agent.cur_imgHSV = screenshotHSV

def print_menu():
    print('Enter a command:')
    print('\tS\tStart main AI agent screen capture.')
    print('\tU\tStart checking your auctions.')
    print('\tQ\tQuit wowzer.')

def run():
    main_agent = MainAgent()

    print_menu()
    while True:
        user_input = input()
        user_input = str.lower(user_input).strip()

        if user_input == 's':
            update_screen_thread = Thread(
                target=update_screen, 
                args=(main_agent,), 
                name="update screen thread",
                daemon=True)
            update_screen_thread.start()

        elif user_input == 'u':
            print("Starting undercutting check in 3 seconds, make sure to focus your WoW window now!")
            time.sleep(3) 
            agent = undercut_agent.UndercutAgent(main_agent)
            agent.run()

        elif user_input == 'q':
            print("Shutting down wowzer.")
            break       
        
        else:
            print("Invalid entry.")
            print_menu()

    print("Done.")
    
if __name__ == '__main__':
    gobzer.run()
