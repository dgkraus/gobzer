# gobzer - An Auction House Bot Based on wowzer
gobzer is a Python and OpenCV-based bot designed to automate auction house interactions in World of Warcraft, such as cancelling undercut items, retrieving mail, and reposting stock.

This bot is based on [wowzer](https://github.com/fjpereny/wowzer) made by [fjpereny](https://github.com/fjpereny)! Make sure to check out the project and especially the tutorial video because it is amazing and very educational:

[![Tutorial Youtube Video Link](https://img.youtube.com/vi/TCzMkWkpMS4/0.jpg)](https://www.youtube.com/watch?v=TCzMkWkpMS4)


> **Warning**  
> Using this bot may result in reports and account bans, as it directly interacts with other players' gameplay. Use at your own risk.

## Required setup

1. Install the TSM WoW addon and configure ingame it for posting and cancelling auctions. Ensure minimum prices are set correctly, as the bot will not verify them.
2. Position your character in a location where the auction house, bank, and mailbox are within reach without moving. For best results without modifications, I recommend Valley of Wisdom in Ogrimmar (for the "open-air" bank NPC Tatepi at 40.0 46.6) using the newest store-bought auction house mount.
   Modifying the code to use mailbox toys etc. should be easy and straightforward but is not yet implemented.
3. Set up WoW macros and keybinds as detailed below.

### Macros and Keybinds
The bot uses the following default keybinds (modifiable in `undercut_agent.py`):
- "1" button keybind macro: Auction house NPC  
- "2" button keybind macro: Mailbox NPC  
- "3" button keybind macro: Bank NPC  
- Interact button: **p**  

So, in order to use this bot with the new store-bought auction house mount and standing next to the bank NPC Tatepi in Orgrimmar (40.0 46.6 on the Ogrimmar map) , the macros need to be set up as follows:
- Macro 1: "/tar Killia"
- Macro 2: "/tar Melanie Morten"
- Macro 3: "/tar Tatepi"


## Features
- Automates auction house interactions, including:
  - Canceling undercut auctions
  - Retrieving items from the mailbox
  - Restocking items from the warbank for cross-realm posting
  - Reposting items in the auction house
- Designed for use with TSM addon
- Human-like behavior adjustments for reduced detection


## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). 

It is based on [wowzer](https://github.com/fjpereny/wowzer) by [fjpereny](https://github.com/fjpereny), which is also licensed under the GPL v3.0.  
A copy of the full license text is available in this repository as `LICENSE`.


## Contributing
This project is primarily for personal learning, but contributions, feedback, or feature requests are welcome! Please feel free to submit issues or pull requests.