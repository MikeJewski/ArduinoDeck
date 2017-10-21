In order for this program to run on the ArduinoMEGA, extra libraries are needed to be downloaded, and present libraries are required to be edited in order for the touchscreen to work with the MEGA.

It is recommended that any file that you are replacing is backed up, in case you need to revert back to using an ArduinoUNO.

Adafruit_GFX, Adafruit_TFTLCD, and TouchScreen can all be placed in the Arduino library folder located in ~/Documents/Arduino/libraries/

SD needs to replace the folder located in ~\Program Files (x86)\Arduino\libraries\ (or where ever the main Arduino folder is located)

SPI needs to replace the folder located in ~\Program Files (x86)\Arduino\hardware\arduino\avr\libraries\

Finally, as a precaution string.h replaces the file located at ~\Program Files (x86)\Arduino\hardware\tools\avr\avr\include\string.h
