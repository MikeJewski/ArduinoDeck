# ArduinoDeck
Alternative method of controlling system functions using a touchscreen shield on an arduino. Mostly targeted towards streamers looking for a method to control OBS while streaming.

![Arduino Deck](https://github.com/MikeJewski/ArduinoDeck/blob/master/ArduinoDeck.jpg?raw=true)

## Contact

We have a discord if you have any question, need help with setup, or want to talk about a possible feature request: https://discord.gg/4FKdNYX

## Progress

A Trello board has been setup to monitor current features, as well as issues, feature requests, and current progress on the next version: https://trello.com/b/WWK25AX0/arduino-deck

## Hardware

1. Arduino MEGA
2. TFTLCD touchscreen (Currently has only been tested on 2.8" screens similar to: https://www.amazon.com/Elegoo-Inches-Screen-Technical-Arduino/dp/B01EUVJYME/ref=sr_1_1_sspa?ie=UTF8&qid=1508638064&sr=8-1-spons&keywords=elegoo+tft+touch&psc=1 )

##Setup Instructions

1. Download and install the Arduino IDE from the official website: https://www.arduino.cc/en/Main/Software

2. Place Adafruit_GFX, Adafruit_TFTLCD, and TouchScreen in the Arduino library folder located in ~/Documents/Arduino/libraries/

3. Open up the Arduino installation folder (default is ~\Program Files (x86)\Arduino\libraries\) and replace the folder SD (or where ever the main Arduino folder is located) with the folder with the same name located in ArduinoDeck\src\ArduinoDeck\libs.

4. Replace the SPI folder, the default is located at ~\Program Files (x86)\Arduino\hardware\arduino\avr\libraries\ with the one inside ArduinoDeck\src\ArduinoDeck\libs

5. As a precaution replace string.h located at ~\Program Files (x86)\Arduino\hardware\tools\avr\avr\include\string.h with the one in ArduinoDeck\src\ArduinoDeck\libs

6. Fill in the [setup file](https://github.com/MikeJewski/ArduinoDeck/blob/master/README.md#setup-file)

7. Install the OBS Websocket Plugin

8. Convert any icons that you want to use on your layouts, using the tool provides and copy the BMP files to the root of your SD card.

9. Compile the code in the Arduino IDE and let it run on to the Arduino board.

10. Setup your layouts, upload them and press start!


## Icons

Icons used for the ArduinoDeck as well as the main software. The icons originally used for this software are free to download and can be found at https://twitchtemple.com/product/elgato-stream-deck-key-icons-free/ . These were the best free icons that I could find, they did a great job on these.

To make them into usable icons, extract the zip file containing the icons anywhere on your computer and then launch IconConvert.exe. Choose the icons that you would like to convert and click open. This images will be placed into the correct folder. This program will convert any image file into a 58x58 bmp file for your ArduinoDeck to use.

To make the icons usable, the filename must be 8 characters or less, with no use of special characters. I am trying to work on using the SDfat library which supports the use of long filenames, but that will have to come later. If you would like an image to toggle (such as the mute mic icon), make sure that both icons have the same name, with the only difference being the last character as a 0 (off) or a 1 (on).

Ex. Mic0.bmp or Mic1.bmp

**In order for the images to be loaded, the file names in the icons folder and the SD card MUST be the exact same**


## Setup File

Included is a setup file, which contains vital information from each user of the software. This must not be edited beyond entering in the information required, or else the program will fail to run.  


**CurrentLayout**: Name of the layout to use. These can be found in the layouts folder (ex. "Blank.json")  
**TwitchChatKey**: Oauth key for the user. This allows the ArduinoDeck to send messages through Twitch chat, as well as get uptime information and viewer count. To get this value, you can use https://twitchapps.com/tmi/ to get your oauth token. Only paste the value after "oauth:" (ex. if the token is "ouath:0123456789abcdefghijABCDEFGHIJ", change the setup value to "0123456789abcdefghijABCDEFGHIJ"  
**ChannelName**: Lowercase name of your Channel. This value will determine what information is being presented with regards to the uptime of the channel, as well as the viewers, and what channel messages will be posted to. This will only work with the channel associated with the oauth token produced above.  
**obspswd**: Password for the OBS websocket plugin. If no password was used (I HIGHLY recommend doing this), the default is "admin"  
**port**: COM port that the Arduino is connected to. This value can be found by looking in the bottom right corner of the Arduino IDE. (ex. port = "COM8")  
**command**: Location of the initial Arduino install location, this is used to update the layout of the Arduino. (ex. command = "C:/Program Files (x86)/Arduino/arduino"). This should only be a matter of changing the C: location to whatever your file location, or the Program Files (x86) if you had chosen to install the Arduino software into a different location.

## OBS websocket plugin

Install the OBS plugin from https://obsproject.com/forum/resources/obs-websocket-remote-control-of-obs-studio-made-easy.466/. I have not added the new features that were made available in September, I will be doing this when I get the time.

## Using the software
Make sure not to move anything out of any of the folders/change names of files. To run the program launch ArduinoDeck.exe

Using a relatively blank layout:

![Layout](https://github.com/MikeJewski/ArduinoDeck/blob/master/ArduinoDeckLayout.png?raw=true)

1. Highlighted button: This is the current active button (Outlined in light grey). Any actions done in the right hand panel will be applied to this button.
2. Unhighlighted button: This is what the rest of the buttons will look like. If clicked on, these buttons will become the active button. This they are clicked and held, the button is able to be moved to a new location.
3. Disabled button: These buttons are disabled and unable to be clicked on.
4. Button Panel: Displays the button layout as it will be shown on the ArduinoDeck.
5. Add button: Pressing this button will add a new button until there is no space left. To remove a button, click and hold on a button, and a garbage icon will appear on the bottom of the Button Panel. Drag the button to the garbage and release to delete it.
6. Action Panel: Actions to apply to a button. Click on the arrow on the right side, or double click the bar to expand it. Clicking on an action will overwrite the current action applied to the Active Button (1). 
7. General Actions: These set of buttons govern the main use of the ArduinoDeck. 

**Save Layout/Save Layout As**: Will save the current layout to the active json file listed on the setup file, or make a new file respectively.  
**Load Layout**: Will allow you to load a previously saved layout file found in the Layouts folder.   
**Upload Layout**: Will save and load the current layout to the Arduino, but this will not start the program.  
**Start/Stop Deck**: This will start a separate program which connects your computer to the ArduinoDeck to allow the functions to run. Closing the ArduinoDeck program will also Stop the connection.  

## Current Issues

Starting and stopping the stream: currently does not work, but with the new update I will add this functionality once I get the time.

Initial state of toggle buttons: This does not currently work, this will be updated along with the stream functionality

## Contributions

Icon created by Dramcus: https://www.artstation.com/dramcus

## Donations

If you want to support me by buying me a coffee, I would be forever grateful!

[![Donate](https://az743702.vo.msecnd.net/cdn/kofi4.png?v=0 | width=36)](https://ko-fi.com/P5P37W6K)
