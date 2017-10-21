/*
   ArduinoDeck program written to interact with main ArduinoDeck program.
   Allows user control system functions, interact with Twitch, and controll OBS.
   Tested with 2.8" TFT touchscreen and ArduinoMEGA.
   Please visit the Github in order to setup the files in order to run the program correctly.
   https://github.com/MikeJewski/ArduinoDeck
   
   By MikeJewski

   Note:  If using this program, an SD card MUST be inserted into the LCD screen in order
   for these images to be displayed. All files must be BMP files. If required, a bmp converter 
   can be found on the main Github page
   
   Much of this layout borrows from William Tavares numpad program,
   
   https://github.com/williamtavares/Arduino-Uno-NumPad
*/

#include <Adafruit_GFX.h>
#include <TouchScreen.h>
#include <Adafruit_TFTLCD.h>
#include <SPI.h>
#include <SD.h>
#include <string.h>

#define YP A3  // must be an analog pin, use "An" notation!
#define XM A2  // must be an analog pin, use "An" notation!
#define YM 9   // can be a digital pin
#define XP 8   // can be a digital pin

// calibration mins and max for raw data when touching edges of screen
// YOU CAN USE THIS SKETCH TO DETERMINE THE RAW X AND Y OF THE EDGES TO GET YOUR HIGHS AND LOWS FOR X AND Y
#define TS_MINX 130
#define TS_MINY 85
#define TS_MAXX 890
#define TS_MAXY 910

//SPI Communication
#define LCD_CS A3
#define LCD_CD A2
#define LCD_WR A1
#define LCD_RD A0
// optional
#define LCD_RESET A4

//Color Definitons
#define BLACK     0x0000
#define BLUE      0x001F
#define GREY      0xCE79
#define LIGHTGREY 0xDEDB
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define BROWN   0xA145
#define PURPLE  0x801F
#define WHITE   0xFFFF

#define MINPRESSURE 1
#define MAXPRESSURE 1000


//SD Card 
#define SD_CS 10 

// For better pressure precision, we need to know the resistance
// between X+ and X- Use any multimeter to read it
// For the one we're using, its 300 ohms across the X plate
// Pins A2-A6
TouchScreen ts = TouchScreen(XP, YP, XM, YM, 364);

//Size of key containers 70px
#define BOXSIZE 60
//2.4 = 240 x 320
//Height 319 to fit on screen

Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

//Import graphics
extern uint8_t crossout[];
extern uint8_t viewer[];
extern uint8_t analogClock[];


//Container variables for touch coordinates
int X, Y, Z;

//State for changing images
int Button1 = 0;
int Button2 = 0;
int Button3 = 0;
int Button4 = 0;
int Button5 = 0;
int Button6 = 0;
int Button7 = 0;
int Button8 = 0;
int Button9 = 0;
int Button10 = 0;
int Button11 = 0;
int Button12 = 0;
int Button13 = 0;
int Button14 = 0;
int Button15 = 0;

//Space between squares
double padding = 4;
double edge = padding/2;

double info = padding + BOXSIZE*2/3 + padding;

double C1 = edge;
double C2 = C1 + BOXSIZE + padding;
double C3 = C2 + BOXSIZE + padding;
double C4 = C3 + BOXSIZE + padding;
double C5 = C4 + BOXSIZE + padding;

double R1 = info + edge;
double R2 = R1 + BOXSIZE + padding;
double R3 = R2 + BOXSIZE + padding;

int col[] = {C1,C2,C3,C4,C5}; 
int row[] = {R1,R2,R3};

String files[] = {"Discord.bmp","Spotify.bmp","VolDown.bmp","VolUp.bmp","OBS.bmp","Mic0.bmp","Disabled.bmp","Disabled.bmp","Disabled.bmp","Disabled.bmp","Disabled.bmp","Disabled.bmp","Disabled.bmp","Disabled.bmp","Play.bmp"};
int Buttons[] = {Button1,Button2,Button3,Button4,Button5,Button6,Button7,Button8,Button9,Button10,Button11,Button12,Button13,Button14,Button15};

void setup() {
  Serial.begin(9600);

  tft.reset();
  uint16_t identifier = tft.readID();
  
  tft.begin(identifier);

  Serial.print(F("Initializing SD card..."));
  if (!SD.begin(SD_CS)) {
    Serial.println(F("failed!"));
    return;
  }
  Serial.println(F("OK!"));
  //Rotate 90 degrees
  tft.setRotation(1);

  //Background color
  tft.fillScreen(BLACK);

  drawBoxes();
  bmp();
  getState();
}
int button = 0;

void drawBoxes(){
  for(int j = 0; j<3; j++){
    for(int i = 0; i<5; i++){ 
      tft.drawRect(col[i],row[j],BOXSIZE,BOXSIZE,WHITE);
    }
  }

  tft.drawRect(edge,edge,tft.width()-padding,info-edge ,WHITE);
  
}

char fileName[100];
 
void bmp(){
  button = 0;
  for(int j = 0; j<3; j++){
    for(int i = 0; i<5; i++){
      files[button].toCharArray(fileName,100); 
      bmpDraw(fileName,col[i]+1,row[j]+1);
      button = button+1;
    }
  }
}

int first = 0;

void loop() {
  retrieveTouch();
  if (first = 1);
    chooseButton();
  first = 1;
  updateInfo();
}

void setRotation(uint8_t rotation);

String temp;
String val;
char newVal[100];

void getState(){
  for( int i = 0; i<15; i++){
    val = files[i].charAt(files[i].length()-5);
    if(val == "1"){
      Buttons[i] = 1;    
    }
  }
}

void retrieveTouch()
{
  digitalWrite(13, HIGH);
  TSPoint p = ts.getPoint();
  digitalWrite(13, LOW);

  //If sharing pins, you'll need to fix the directions of the touchscreen pins
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);

  // on my tft the numbers are reversed so this is used instead of the above
  X = map(p.y, TS_MAXY, TS_MINY, 0, tft.width());
  Y = map(p.x, TS_MAXX, TS_MINX, 0, tft.height());
  Z = p.z;
  
}

void chooseButton(){
  if (Z > MINPRESSURE && Z < MAXPRESSURE){
    for(int j = 0; j<3; j++){
      for(int i = 0; i<5; i++){
        if(X > col[i] &&  X < col[i] + BOXSIZE){
          if(Y > row[j] && Y < row[j] + BOXSIZE){
            
            drawBoxes();
            tft.drawRect(col[i],row[j],BOXSIZE,BOXSIZE,RED);
            Serial.println((j*5)+i+1);
            val = files[(j*5)+i].charAt(files[(j*5)+i].length()-5);
            if(val == "1"){
              Buttons[(j*5)+i] = 0;
              files[(j*5)+i].replace("1","0");
              files[(j*5)+i].toCharArray(fileName,100);
              bmpDraw(fileName,col[i]+1,row[j]+1);
            }
            if(val == "0"){
              Buttons[(j*5)+i] = 1;
              files[(j*5)+i].replace("0","1");
              files[(j*5)+i].toCharArray(fileName,100);
              bmpDraw(fileName,col[i]+1,row[j]+1);
            }
            memset(fileName, 0, sizeof newVal);
            temp = ""; 
            delay(50);
          }
        }
      }
    }
  }
}

void updateInfo(){
  if(Serial.available() > 0) {
     // display each character to the LCD
    String currentTime = Serial.readStringUntil(',');
    String viewers = Serial.readStringUntil(',');
    String uptime = Serial.readStringUntil(',');
    tft.fillRect(edge,edge,tft.width()-padding,info-edge ,BLACK);
    tft.drawRect(edge,edge,tft.width()-padding,info-edge ,WHITE);
    tft.drawBitmap(col[1]+BOXSIZE*3/4,info/5 + 2*padding,viewer,20,20,RED);
    tft.drawBitmap(col[3]+BOXSIZE/2,info/5 + 2*padding,analogClock,20,20,LIGHTGREY);
    tft.setTextSize(2);
    tft.setTextColor(WHITE);
    tft.setCursor(padding*2 ,20);
    tft.println(currentTime);
    tft.setCursor((tft.width()*2)/5+(BOXSIZE*1/4),20);
    tft.println(viewers);
    tft.setCursor((tft.width()*4)/5,20);
    tft.println(uptime);
  }
}

// This function opens a Windows Bitmap (BMP) file and
// displays it at the given coordinates.  It's sped up
// by reading many pixels worth of data at a time
// (rather than pixel by pixel).  Increasing the buffer
// size takes more of the Arduino's precious RAM but
// makes loading a little faster.  20 pixels seems a
// good balance.

#define BUFFPIXEL 20

void bmpDraw(char *filename, int x, int y) {

  File     bmpFile;
  int      bmpWidth, bmpHeight;   // W+H in pixels
  uint8_t  bmpDepth;              // Bit depth (currently must be 24)
  uint32_t bmpImageoffset;        // Start of image data in file
  uint32_t rowSize;               // Not always = bmpWidth; may have padding
  uint8_t  sdbuffer[3*BUFFPIXEL]; // pixel in buffer (R+G+B per pixel)
  uint16_t lcdbuffer[BUFFPIXEL];  // pixel out buffer (16-bit per pixel)
  uint8_t  buffidx = sizeof(sdbuffer); // Current position in sdbuffer
  boolean  goodBmp = false;       // Set to true on valid header parse
  boolean  flip    = true;        // BMP is stored bottom-to-top
  int      w, h, row, col;
  uint8_t  r, g, b;
  uint32_t pos = 0, startTime = millis();
  uint8_t  lcdidx = 0;
  boolean  first = true;

  if((x >= tft.width()) || (y >= tft.height())) return;

  //Serial.println();
  //Serial.print(F("Loading image '"));
  //Serial.print(filename);
  //Serial.println('\'');
  // Open requested file on SD card
  if ((bmpFile = SD.open(filename)) == NULL) {
    //Serial.println(F("File not found"));
    return;
  }

  // Parse BMP header
  if(read16(bmpFile) == 0x4D42) { // BMP signature
    //Serial.println(F("File size: ")); 
    read32(bmpFile);
    (void)read32(bmpFile); // Read & ignore creator bytes
    bmpImageoffset = read32(bmpFile); // Start of image data
    //Serial.print(F("Image Offset: ")); 
    (bmpImageoffset, DEC);
    // Read DIB header
    //Serial.print(F("Header size: ")); 
    read32(bmpFile);
    bmpWidth  = read32(bmpFile);
    bmpHeight = read32(bmpFile);
    if(read16(bmpFile) == 1) { // # planes -- must be '1'
      bmpDepth = read16(bmpFile); // bits per pixel
      //Serial.print(F("Bit Depth: ")); Serial.println(bmpDepth);
      if((bmpDepth == 24) && (read32(bmpFile) == 0)) { // 0 = uncompressed

        goodBmp = true; // Supported BMP format -- proceed!
        //Serial.print(F("Image size: "));
        //Serial.print(bmpWidth);
        //Serial.print('x');
        //Serial.println(bmpHeight);

        // BMP rows are padded (if needed) to 4-byte boundary
        rowSize = (bmpWidth * 3 + 3) & ~3;

        // If bmpHeight is negative, image is in top-down order.
        // This is not canon but has been observed in the wild.
        if(bmpHeight < 0) {
          bmpHeight = -bmpHeight;
          flip      = false;
        }

        // Crop area to be loaded
        w = bmpWidth;
        h = bmpHeight;
        if((x+w-1) >= tft.width())  w = tft.width()  - x;
        if((y+h-1) >= tft.height()) h = tft.height() - y;

        // Set TFT address window to clipped image bounds
        tft.setAddrWindow(x, y, x+w-1, y+h-1);

        for (row=0; row<h; row++) { // For each scanline...
          // Seek to start of scan line.  It might seem labor-
          // intensive to be doing this on every line, but this
          // method covers a lot of gritty details like cropping
          // and scanline padding.  Also, the seek only takes
          // place if the file position actually needs to change
          // (avoids a lot of cluster math in SD library).
          if(flip) // Bitmap is stored bottom-to-top order (normal BMP)
            pos = bmpImageoffset + (bmpHeight - 1 - row) * rowSize;
          else     // Bitmap is stored top-to-bottom
            pos = bmpImageoffset + row * rowSize;
          if(bmpFile.position() != pos) { // Need seek?
            bmpFile.seek(pos);
            buffidx = sizeof(sdbuffer); // Force buffer reload
          }

          for (col=0; col<w; col++) { // For each column...
            // Time to read more pixel data?
            if (buffidx >= sizeof(sdbuffer)) { // Indeed
              // Push LCD buffer to the display first
              if(lcdidx > 0) {
                tft.pushColors(lcdbuffer, lcdidx, first);
                lcdidx = 0;
                first  = false;
              }
              bmpFile.read(sdbuffer, sizeof(sdbuffer));
              buffidx = 0; // Set index to beginning
            }

            // Convert pixel from BMP to TFT format
            b = sdbuffer[buffidx++];
            g = sdbuffer[buffidx++];
            r = sdbuffer[buffidx++];
            lcdbuffer[lcdidx++] = tft.color565(r,g,b);
          } // end pixel
        } // end scanline
        // Write any remaining data to LCD
        if(lcdidx > 0) {
          tft.pushColors(lcdbuffer, lcdidx, first);
        } 
        //Serial.print(F("Loaded in "));
        //Serial.print(millis() - startTime);
        //Serial.println(" ms");
      } // end goodBmp
    }
  }

  bmpFile.close();
  if(!goodBmp) Serial.println(F("BMP format not recognized."));
}

// These read 16- and 32-bit types from the SD card file.
// BMP data is stored little-endian, Arduino is little-endian too.
// May need to reverse subscript order if porting elsewhere.

uint16_t read16(File f) {
  uint16_t result;
  ((uint8_t *)&result)[0] = f.read(); // LSB
  ((uint8_t *)&result)[1] = f.read(); // MSB
  return result;
}

uint32_t read32(File f) {
  uint32_t result;
  ((uint8_t *)&result)[0] = f.read(); // LSB
  ((uint8_t *)&result)[1] = f.read();
  ((uint8_t *)&result)[2] = f.read();
  ((uint8_t *)&result)[3] = f.read(); // MSB
  return result;
}
