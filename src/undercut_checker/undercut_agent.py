
import cv2 as cv
import numpy as np
import pyautogui
import time
from threading import Thread
import os
from random import randint
from undercut_checker.counter import increment_counter, reset_counter

class UndercutAgent:
    def __init__(self, main_agent):
        #make sure to set the correct keybinds as you use it ingame here, or change your ingame keybinds to these:
        self.auction_house_keybind = "1"
        self.mailbox_keybind = "2"
        self.bank_keybind = "3"
        self.interact_keybind = "p"

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
        self.idle_process() #this currently clashes with self.logout_process and will be integrated into that
        #self.logout_process() #enable this to log between characters to post items not on the regional auction house, will clean this up later

    def find_button(self, button_asset):
        threshold = 0.8 #if the program has trouble finding your buttons, lowering this number may help. going below 0.6 may give too many false results, however.
        found_button = cv.matchTemplate(self.main_agent.cur_img, button_asset, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(found_button)
        print(max_val)
        if max_val >= threshold:
            return max_loc
        else:
            return None

    def open_auction_house(self):
        time.sleep(3)
        pyautogui.press(self.auction_house_keybind)
        time.sleep(randint(30, 40)/100)
        pyautogui.press(self.interact_keybind)
        time.sleep(randint(80, 100)/100)

    def open_cancel_scan(self):
        cancel_scan_button = self.find_button(self.cancel_scan)
        if cancel_scan_button:
            time.sleep(randint(50, 80)/100)
            pyautogui.moveTo(cancel_scan_button[0]+(randint(1,20)),cancel_scan_button[1]+(randint(1,5)),(randint(5,8)/10),pyautogui.easeOutQuad)
            time.sleep(randint(50, 80)/100)
            pyautogui.click()
            time.sleep(randint(200, 250)/100)
        else:
            print("can't find cancel button, make sure the auction house tab is open!")
            print("type U after you opened the auction house to try again.")

    def cancel_auctions(self):
        cancel_auction_button = self.find_button(self.cancel_auction)
        if cancel_auction_button:
            self.cancel_button_found = True
            if pyautogui.position()[0]-cancel_auction_button[0] > 21 or pyautogui.position()[0]-cancel_auction_button[0] < 0:
                pyautogui.moveTo(cancel_auction_button[0]+(randint(1,20)),cancel_auction_button[1]+(randint(1,5)),(randint(5,8)/10),pyautogui.easeOutQuad)
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
            pyautogui.moveTo(retrieve_mail_button[0]+(randint(1,20)),retrieve_mail_button[1]+(randint(5,8)/10),(randint(5,8)/10),pyautogui.easeOutQuad)
            time.sleep(randint(50, 80)/100)
            pyautogui.click()
            time.sleep(randint(500, 550)/100)
            print("mail retrieved, moving to restock items")
    
    def restock_items(self):
        pyautogui.press(self.bank_keybind)
        time.sleep(randint(30, 40)/100)
        pyautogui.press(self.interact_keybind)
        time.sleep(randint(50, 80)/100)
        warbank_button = self.find_button(self.warbank_tab)
        if warbank_button:
            pyautogui.moveTo(warbank_button[0]+(randint(1,20)),warbank_button[1]+(randint(1,5)),(randint(4,6)/10),pyautogui.easeOutQuad)
            time.sleep(randint(50, 80)/100)
            pyautogui.click()
            restock_button = self.find_button(self.restock)
            if restock_button:
                pyautogui.moveTo(restock_button[0]+(randint(1,20)),restock_button[1]+(randint(1,5)),(randint(5,8)/10),pyautogui.easeOutQuad)
                time.sleep(randint(50, 80)/100)
                pyautogui.click()
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
        threshold = 0.95
        post_button = self.find_button(self.post_scan)
        if post_button:
            pyautogui.moveTo(post_button[0]+(randint(1,20)),post_button[1]+(randint(1,5)),(randint(5,8)/10),pyautogui.easeOutQuad)
            time.sleep(randint(30, 50)/100)
            pyautogui.click()
            time.sleep(randint(50, 80)/100)
            print("posting items now")
        else:
            print("could not find post scan button, try again and make sure the auction house window opens after the restocking process")

    def post_items(self):
        threshold = 0.9
        post_button = self.find_button(self.post_item_button)
        if post_button:
            self.post_button_found = True
            if pyautogui.position()[1]-post_button[1] > 12 or pyautogui.position()[1]-post_button[1] < 0:
                pyautogui.moveTo(post_button[0]+(randint(1,20)),post_button[1]+(randint(1,5)),(randint(5,8)/10),pyautogui.easeOutQuad)
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
        print("all done, logging out now!")
        current_count = increment_counter()
        #print(current_count)
        pyautogui.press("esc")
        time.sleep(randint(10, 15)/100)
        pyautogui.press("esc")
        time.sleep(randint(10, 15)/100)
        pyautogui.press("esc")
        time.sleep(randint(10, 15)/100)
        logout_button = self.find_button(self.logout)
        if logout_button:
            pyautogui.moveTo(logout_button[0]+(randint(1,20)),logout_button[1]+(randint(1,5)),(randint(5,8)/10),pyautogui.easeOutQuad)
            time.sleep(randint(30, 50)/100)
            pyautogui.click()
        if current_count <= 4:
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
            current_count = reset_counter()
            pyautogui.press("enter")
            time.sleep(100)
            pyautogui.press("1")
            time.sleep(100)
            pyautogui.press("2")
            time.sleep(100)
            pyautogui.press("1")
            time.sleep(100)

        time.sleep(12)
        while True:
            time.sleep(4)
            character_load = self.find_button(self.healthbar)
            if character_load:
                break

        self.run()

    def idle_process(self):
        afk_duration = time.time()
        idle_time = 600
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