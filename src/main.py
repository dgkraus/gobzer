
from PIL import Image, ImageGrab
import time
from threading import Thread
import numpy as np
import cv2 as cv
import keyboard
from gui import app

import undercut_checker.undercut_agent as undercut_agent
from undercut_checker.counter import log_amount

update_screen_thread = None
cancel_button = "c"

class MainAgent:
    def __init__(self):
        self.agents = []

        self.cur_img = None
        self.cur_imgHSV = None

def update_screen(agent,root):
    cancel = False
    print("Starting computer vision screen update...")

    while not cancel:
        if keyboard.is_pressed(cancel_button):
            cancel = True
        screenshot = ImageGrab.grab()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        screenshotHSV = cv.cvtColor(screenshot, cv.COLOR_BGR2HSV)
        agent.cur_img = screenshot
        agent.cur_imgHSV = screenshotHSV
    print("done")
    root.destroy()

def print_menu():
    print('Enter a command:')
    print('\tS\tStart main AI agent screen capture.')
    print('\tU\tStart checking your auctions.')
    print('\tQ\tQuit gobzer.')

def run_main_agent(main_agent):
    global update_screen_thread
    if update_screen_thread is None or not update_screen_thread.is_alive():
        update_screen_thread = Thread(
            target=update_screen, 
            args=(main_agent,app), 
            name="update screen thread",
            daemon=True)
        update_screen_thread.start()
        app.after(2000, lambda: run_undercut_agent(main_agent))


def run_undercut_agent(main_agent):
        agent = undercut_agent.UndercutAgent(main_agent)
        agent.run()

def run():
    main_agent = MainAgent()

    run_main_agent(main_agent)

    # print_menu()
    # while True:
    #     user_input = input()
    #     user_input = str.lower(user_input).strip()

    #     if user_input == 's':
    #         if update_screen_thread is None or not update_screen_thread.is_alive():
    #             update_screen_thread = Thread(
    #                 target=update_screen, 
    #                 args=(main_agent,), 
    #                 name="update screen thread",
    #                 daemon=True)
    #             update_screen_thread.start()
    #         else:
    #             print("Screen capture is already running! Enter ""U"" to start the auction bot.")

    #     elif user_input == 'u':
    #         print("Starting undercutting check in 3 seconds, make sure to focus your WoW window now!")
    #         time.sleep(3) 
    #         agent = undercut_agent.UndercutAgent(main_agent)
    #         agent.run()

    #     elif user_input == 'q':
    #         print("Shutting down gobzer.")
    #         break       
        
    #     else:
    #         print("Invalid entry.")
    #         print_menu()

    # print("Done.")
    
if __name__ == '__main__':
    app.mainloop()
