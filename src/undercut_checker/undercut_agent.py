
import cv2 as cv
import numpy as np
import pyautogui
import time
from threading import Thread
import os
from random import randint
from undercut_checker.counter import increment_counter, reset_counter
from config import settings

class UndercutAgent:
    def __init__(self, main_agent):
        #make sure to set the correct keybinds as you use it ingame here, or change your ingame keybinds to these:
        self.auction_house_keybind = settings["auction_house_kb"]
        self.mailbox_keybind = settings["mailbox_kb"]
        self.bank_keybind = settings["bank_kb"]
        self.interact_keybind = settings["interact_kb"]

        self.got_undercut = False
        self.main_agent = main_agent
        
        # interpolate here_path to get the path to the assets
        here_path = os.path.dirname(os.path.realpath(__file__))

        self.post_scan = cv.imread(
            os.path.join(
                here_path,
                "assets", "post_scan.png"
            )
        )

        self.cancel_scan = cv.imread(
            os.path.join(
                here_path,
                "assets", "cancel_scan.png"
            )
        )

        self.cancel_auction = cv.imread(
            os.path.join(
                here_path,
                "assets", "cancel_auction.png"
            )
        )

        self.post_item_button = cv.imread(
            os.path.join(
                here_path,
                "assets", "post_item.png"
            )
        )

        self.mailbox = cv.imread(
            os.path.join(
                here_path,
                "assets", "open_mail.png"
            )
        )

        self.warbank_tab = cv.imread(
            os.path.join(
                here_path,
                "assets", "warbank_tab.png"
            )
        )

        self.restock = cv.imread(
            os.path.join(
                here_path,
                "assets", "restock_button.png"
            )
        )

        self.logout = cv.imread(
            os.path.join(
                here_path,
                "assets", "logout.png"
            )
        )

        self.healthbar = cv.imread(
            os.path.join(
                here_path,
                "assets", "healthbar.png"
            )
        )

        self.login = cv.imread(
            os.path.join(
                here_path,
                "assets", "login_button.png"
            )
        )

        self.undercut_thread = None
    
    def run_process(self):
        self.cancel_button_found = False
        self.post_button_found = False
        self.open_auction_house()
        self.open_cancel_scan()
        self.cancel_auctions()
        self.retrieve_mail()
        self.restock_items()
        self.open_post_scan()
        self.post_items()
        self.logout_process()

    # this is the identifier function that tells openCV to search for the button_asset on screen.
    # cases where the button can't be identified aren't handled well yet and need to be improved.
    def find_button(self, button_asset):
        threshold = 0.9 #if the program has trouble finding your buttons, lowering this number may help. going below 0.6 may give too many false results, however.
        found_button = cv.matchTemplate(self.main_agent.cur_img, button_asset, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(found_button)
        #print(max_val)
        if max_val >= threshold:
            return max_loc
        else:
            return None
        
    def navigate_to_button(self, coordinates: tuple):
        x = coordinates[0]
        y = coordinates[1]
        time.sleep(randint(50, 80)/100)
        pyautogui.moveTo(x+(randint(1,20)),y+(randint(1,5)),(randint(5,8)/10),pyautogui.easeOutQuad) # random numbers added to coordinates to make sure the exact coordinate isn't pressed over and over. first coordinate has more tolerance since buttons are horizontal rectangles
        time.sleep(randint(50, 80)/100)
        pyautogui.click()


    def open_auction_house(self):
        time.sleep(3)
        pyautogui.press(self.auction_house_keybind)
        time.sleep(randint(30, 40)/100)
        pyautogui.press(self.interact_keybind)
        time.sleep(randint(80, 100)/100)

    def open_cancel_scan(self):
        cancel_scan_button = self.find_button(self.cancel_scan)
        if cancel_scan_button:
            self.navigate_to_button(cancel_scan_button)
            time.sleep(randint(200, 250)/100)
        else:
            print("can't find cancel button, make sure the auction house tab is open!")
            print("type U after you opened the auction house to try again.")

    def cancel_auctions(self):
        cancel_auction_button = self.find_button(self.cancel_auction)
        if cancel_auction_button:
            self.cancel_button_found = True
            if pyautogui.position()[0]-cancel_auction_button[0] > 21 or pyautogui.position()[0]-cancel_auction_button[0] < 0: #since this function calls itself until there are no more items to cancel, this check ensures that the mouse doesn't constantly need to move
                self.navigate_to_button(cancel_auction_button)
                time.sleep(randint(20, 25)/100)
            pyautogui.click()
            time.sleep(randint(15, 20)/100)
            self.cancel_auctions()
        else:
            if self.cancel_button_found:
                print("All undercut actions cancelled, moving to retrieve mail")
            else:
                print("No items found to cancel, moving to retrieve mail")

    def retrieve_mail(self):
        pyautogui.press(self.mailbox_keybind)
        time.sleep(randint(30, 40)/100)
        pyautogui.press(self.interact_keybind)
        time.sleep(randint(50, 80)/100)
        retrieve_mail_button = self.find_button(self.mailbox)
        if retrieve_mail_button:
            self.navigate_to_button(retrieve_mail_button)
            time.sleep(randint(500, 550)/100)
            print("mail retrieved, moving to restock items")
        else:
            print("couldn't find mail button, make sure the mailbox opened or check if the NPC is too far or the keybind is wrong")
    
    def restock_items(self):
        pyautogui.press(self.bank_keybind)
        time.sleep(randint(30, 40)/100)
        pyautogui.press(self.interact_keybind)
        time.sleep(randint(50, 80)/100)
        warbank_button = self.find_button(self.warbank_tab)
        if warbank_button:
            self.navigate_to_button(warbank_button)
            restock_button = self.find_button(self.restock)
            if restock_button:
                self.navigate_to_button(restock_button)
                time.sleep(randint(400, 450)/100)
                print("items restocked, moving to post items")
            else:
                print("can't find restock bags button, make sure the window opened properly or type /tsm bankui in the wow chat window and try again")
        else:
            print("couldn't find warbank tab, make sure the bank opened correctly")

    def open_post_scan(self):
        pyautogui.press("1")
        time.sleep(randint(30, 40)/100)
        pyautogui.press("p")
        time.sleep(randint(100, 150)/100)
        post_button = self.find_button(self.post_scan)
        if post_button:
            self.navigate_to_button(post_button)
            time.sleep(randint(50, 80)/100)
            print("posting items now")
        else:
            print("could not find post scan button, try again and make sure the auction house window opens after the restocking process")

    def post_items(self):
        post_button = self.find_button(self.post_item_button)
        if post_button:
            self.post_button_found = True
            if pyautogui.position()[1]-post_button[1] > 12 or pyautogui.position()[1]-post_button[1] < 0: # another check for current mouse position to ensure cursor doesn't move upon multiple function repeats
                self.navigate_to_button(post_button)
                time.sleep(randint(20, 25)/100)
            pyautogui.click()
            time.sleep(randint(10, 15)/100)
            self.post_items()
        else:
            if self.post_button_found:
                print("posted all items!")
            else:
                print("can't find post button, make sure the post scan window opened properly and that there are items to restock in your bags!")

    def logout_process(self):
        if settings["cross_realm_logging"] == 1:
            print("all done, logging out now!")
            current_count = increment_counter()
            while True:
                pyautogui.press("esc")
                time.sleep(randint(100, 110)/100)
                logout_button = self.find_button(self.logout)
                if logout_button:
                    self.navigate_to_button(logout_button)
                    time.sleep(randint(30, 50)/100)
                    break
            if current_count <= settings["cross_characters"]:
                while True:
                    time.sleep(4)
                    login_button = self.find_button(self.login)
                    if login_button:
                        break    
                pyautogui.press("down")
                time.sleep(randint(10, 30)/100)
                pyautogui.press("enter")
            else:
                time.sleep(randint(400, 500)/100)
                for i in range(current_count-1):
                    pyautogui.press("up")
                    time.sleep(randint(10, 30)/100)
                pyautogui.press("enter")
                current_count = reset_counter()
                self.idle_process()
                

            while True: #checks if the character is loaded in by looking for the healthbar and ends the loops once the healthbar is visible
                time.sleep(4)
                character_load = self.find_button(self.healthbar)
                if character_load:
                    print("character load found")
                    break

            self.run_process()
        else:
            self.idle_process()

    def idle_process(self):
        afk_duration = time.time()
        idle_time = settings["idle_time"]
        max_time = 1500
        elapsed_time = time.time()
        print(f"idling, idle time set to {idle_time} seconds")
        while idle_time > 0:
            if time.time() - elapsed_time >= max_time:
                pyautogui.press("up")
                time.sleep(randint(10, 30)/100)
                pyautogui.press("down")
                elapsed_time = time.time()
            time.sleep(30)
            idle_time -= 30
            print(f"waking up in {idle_time} seconds")
        
        self.run()


    def run(self):
        if self.main_agent.cur_img is None:
            print("Image capture not found!  Did you start the screen capture thread?")
            return
        print("Undercut check in process...")
        
        self.undercut_thread = Thread(
            target=self.run_process, 
            args=(),
            name="undercut checker thread",
            daemon=True)    
        
        self.undercut_thread.start()