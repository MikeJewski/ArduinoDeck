# ArduinoDeck
Alternative method of controlling system functions using a touchscreen shield on an arduino. Mostly targeted towards streamers looking for a method to control OBS while streaming.

# Icons

Icons used for the ArduinoDeck as well as the main software. The icons originally used for this software are free to download and can be found at https://twitchtemple.com/product/elgato-stream-deck-key-icons-free/ . These were the best free icons that I could find, they did a great job on these.

To make them into usable icons, extract the zip file containing the icons anywhere on your computer and then launch IconConvert.exe. Choose the icons that you would like to convert and click open. This images will be placed into the correct folder. This program will convert any image file into a 58x58 bmp file for your ArduinoDeck to use.

To make the icons usable, the filename must be 8 characters or less, with no use of special characters. I am trying to work on using the SDfat library which supports the use of long filenames, but that will have to come later. If you would like an image to toggle (such as the mute mic icon), make sure that both icons have the same name, with the only difference being the last character as a 0 (off) or a 1 (on).

Ex. Mic0.bmp or Mic1.bmp

# Setup File

Included is a setup file, which contains vital information from each user of the software. This must not be edited beyond entering in the information required, or else the program will fail to run.

CurrentLayout: Name of the layout to use. These can be found in the layouts folder (ex. "Blank.json")
TwitchChatKey: Oauth key for the user. This allows the ArduinoDeck to send messages through Twitch chat, as well as get uptime information and viewer count. To get this value, you can use https://twitchapps.com/tmi/ to get your oauth token. Only paste the value after "oauth:" (ex. if the token is "ouath:0123456789abcdefghijABCDEFGHIJ", change the setup value to "0123456789abcdefghijABCDEFGHIJ"
ChannelName: Lowercase name of your Channel. This value will determine what information is being presented with regards to the uptime of the channel, as well as the viewers, and what channel messages will be posted to. This will only work with the channel associated with the oauth token produced above.
obspswd: Password for the OBS websocket plugin. If no password was used (I HIGHLY recommend doing this), the default is "admin"

# OBS websocket plugin

Install the OBS plugin from https://obsproject.com/forum/resources/obs-websocket-remote-control-of-obs-studio-made-easy.466/. I have not added the new features that were made available in September, I will be doing this when I get the time.

# Using the software

Assuming you are starting from the 

![Layout](https://github.com/MikeJewski/ArduinoDeck/edit/master/ArduinoDeckLayout.png?raw=true)
