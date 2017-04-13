Thank you for taking the time to view my Risk simulation I built in Python to practice programming, version 2.0! I hope you enjoy it! 

If you have any questions, comments, concerns, or would like to hire me, please feel free to contact me. 

WHAT’S NEW

The entire source code has been reworked to follow OOP principles. The code is now spread between a number of files, making it easier to read through and understand. 

The map and color changing now works via indexed palettes and is much faster. Territories will now highlight when clicked. 

Attacking now allows the player to choose the number of units to attack with (default is always set to the maximum amount) and following a successful invasion, the attacking units must move into the territory, which is more in line with the game. 

Clicking the player token brings up a menu which shows the connecting lines between territories and allows the player to restart the game or view the tutorial or hints. 

HOW TO INSTALL

I have placed the executable (and hope to get the .app as well) in a ZIP folder in this repository that you can download. Run RiskMain.exe to play the game. 

If you plan to use the source code to make the executable (or app for Mac users), you will need the Pygame and cx_Freeze libraries, which can be installed with pip. 
I am including the cx_Freeze setup file. You will need to make sure that all the appropriate files are all in the same directory: RiskRaw.py, RiskData.py, RiskGUI.py, RiskIntro.py, RiskMoves.py, RiskMain.py, Map.gif, and RedR.png (or you can delete RedR.png and the lines pertaining to RedR.png from RiskGUI.py). 
Additionally, you will also need the .ttf files for freesansbold in the directory. Once you have installed Pygame, you can find it at C:/path/to/python/Lib/Site-packages/pygame. Copy the file freesansbold.ttf and place it in the same directory as the other files.
You will need to alter a few lines in the cx_FreezeSetup.py file. Where it says "path/to/python" use the path to where Python is on your machine.
Then from the command line/terminal, once you've cd'd into the directory with the files, execute "python cx_FreezeSetup.py build" ("python cx_FreezeSetup.py bdist_mac" for Mac users). If you have multiple versions of python on your machine, you may have to specify which one. 
This will create a build folder with all the necessary files and folders. However, there are a number of folders and files that cx_Freeze will create that are simply unnecessary and can be deleted (not sure if they're the same on Mac). 
The necessary folders are: collections, encodings, logging, and pygame. The necessary files are freesansbold.ttf, Map.gif, python35.dll, python35.zip (these may be different depending on your version of Python. I used 3.5.2), README.txt (not completely necessary but good to have), RedR.png, RiskMain.exe, and VCRUNTIME140.dll.
As far as I know, everything else can be deleted. And with that you should be ready to play!

HOW TO PLAY

This Risk simulation functions much like the classic board game Risk (with a few exceptions). If you are unfamiliar with the rules of Risk, please visit: http://www.hasbro.com/common/instruct/risk.pdf

Please take note of the changes I have made that deviate from the original rules:

Initial territory and troop placement is randomized.
Cards have been simplified. You may cash your cards when you have 3 or 4. Cards are automatically cashed when you have 5 or more.
Attacking territories will default to use the maximum number of dice, but can be changed.
Defending territories will automatically use the maximum number of dice.

PRO TIP: When placing units, the left click will place them 1 at a time while the right click will place them 5 at a time (10 at a time if there are more than 50 units to place). If the right click is pressed when there are less than 5 units, the remaining units will be placed. 

PLEASE NOTE: the button to advance to the next phase of your turn will have the next available action written on it. It will be red when active (meaning available to use) or grey if action must be taken (such as placing units).

HOW IT WORKS

RiskRaw.py holds raw data including color values, coordinates, and connecting territories, which are used by a number of other files. It has no other classes or methods.

RiskData.py initializes and holds the data structures for the game. There are classes for players, territories, and an overarching data class that will set up arrays for all the territories as well as the players and randomize the territories/units at the start of the game. However, it won’t do this until it is passed a number of players, which is obtained from RiskIntro.py. Since a number of other files make alterations to this data (such as adding new troops, conquering a territory, etc.), it is initialized at the bottom of the file and imported by a number of other files, but the actual data for the game is not initialized until it is called in RiskMain.py. 

RiskGUI.py initializes pygame and sets up the GUI and user interface (UI), which are separate classes. GUI is primarily concerned with the display of the map, including units, connection lines, and changing colors. UI mostly focuses on the user interface below the map and is responsible for updating it when changes occur, including to the number of units/territories/cards, output to the user, and the current player token. It relies on being able to make changes to the data in RiskData.py and other files in turn rely on RiskGUI.py to make changes to the display, so a GUI and UI class are initialized at the end of the file. 

RiskIntro.py handles both the introductory messages and the menu once the player token has been clicked. The final page of the intro allows the user to select a number of players, and this number is used by a method in RiskData.py to initialize the player and territory list. However, to make updates to the display, it is reliant on RiskGUI.py, which in turn is reliant on RiskData.py. Thus, an empty RiskData.py data structure is initialized, followed by a GUI and UI class, and then the introduction is shown to the user, allowing him or her to select the number of players, which is passed to the data structure and used to initialize the player list, territory list, and starting board. Since RiskIntro.py is also used by RiskMoves.py for the menu, it is initialized at the bottom of the file. 

RiskMoves.py controls all the moves a player can make in a turn, including placing units, attacking, and fortifying. It requires that the data, GUI, and intro all be initialized and imported in order to function, as it will make calls and updates to all of these. The menu (which is handled in RiskIntro.py) allows for a restart option. To handle this potential scenario, every sub-function handles for this case and will allow the program to pass through, break the main game loop in RiskMain.py, and allow the user to pick a number of players and start the game over. 

RiskMain.py holds the main function and is the file which must be run once all the other files are in the same directory to produce the game. It holds a game loop which will allow the game to be played to completion or if a user opts for a restart, will allow the game to be reset.

RedR.png is just a logo for the game that can be seen at the top left of the display window (this may be different for Mac users). It won't affect the game in any meaningful way and can be deleted. A few lines must be removed from the __init__ function in RiskGUI.py so that the program won't crash. 

Map.gif, the main map photo, has very specific RGB values. For the countries, the G value is 150, the B value is 100, and the R value is a number between 1 and 42 (corresponding to the 42 risk territories). The code uses these RGB values (plus (0, 0, 0) for the black outlines and (162, 232, 232) for the water) to create a color-indexed palette, which then alters the values for territories to the color of their owner (or if clicked their owners’ highlight color). A second copy of Map.gif is saved unaltered and used to correctly get the appropriate territory from the player clicking the display, since the RGB values still correspond to their initial values. Please note: if Map.gif is altered in any way, the map may not display properly. 

LEGAL DISCLAIMER

Risk is a registered trademark of Parker Brothers. This simulation is for educational purposes only. I do not claim to own any of Parker Brothers’ intellectual property. Please don’t sue me!

Join the chat at https://gitter.im/Risk2-0/Lobby
