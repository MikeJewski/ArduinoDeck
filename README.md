# ArduinoDeck
Alternative method of controlling system functions using a touchscreen shield on an arduino. Mostly targeted towards streamers looking for a method to control OBS while streaming.

# Icons

Icons used for the ArduinoDeck as well as the main software. The icons originally used for this software are free to download and can be found at https://twitchtemple.com/product/elgato-stream-deck-key-icons-free/ . These were the best free icons that I could find, they did a great job on these.

To make them into usable icons, extract the zip file containing the icons anywhere on your computer and then launch IconConvert.exe. Choose the icons that you would like to convert and click open. This images will be placed into the correct folder. This program will convert any image file into a 58x58 bmp file for your ArduinoDeck to use.

To make the icons usable, the filename must be 8 characters or less, with no use of special characters. I am trying to work on using the SDfat library which supports the use of long filenames, but that will have to come later. If you would like an image to toggle (such as the mute mic icon), make sure that both icons have the same name, with the only difference being the last character as a 0 (off) or a 1 (on).

Ex. Mic0.bmp or Mic1.bmp
