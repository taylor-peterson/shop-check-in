/*
Richard Piersall - rpiersall@g.hmc.edu
Taylor Peterson  - tpeterson@g.hmc.edu

Arduino code to communicate over USB serial with computer
Read in strings and write to LCD
Read in switch states and write out to serial

*/


// Include the LiquidCrystal Library for writing to LCD:
#include <LiquidCrystal.h>

// Pinout
#define LED  13 // LED pin
#define SIG0 15 // Signal Input Pins
#define SIG1 18 
#define SEL0 22 // Signal Select Pins
#define SEL1 21
#define SEL2 20
#define SEL3 19
#define PWR  14 // Power Switch Pin
#define in0   0 // Button Pins
#define in1   1
#define in2   2
#define in3   3
#define in4   4 

// Constants
const int STRLEN = 16;          // Character-width of LCD row
const int INITDELAY = 1000;     // Multiplexer post-reset delay
const int SHIFTTIME = 620;   // Time between multiplexer shifts
const int LEDTIMER = 1000;      // One half period of led blink
const int SWITCHDEBOUNCE = 10;  // Switch Debounce delay in milliseconds
const int BUTTONDEBOUNCE = 30;  // Button Debounce delay in milliseconds
const int MUXERDEBOUNCE  = 30;  // Muxer Debounce delay in milliseconds

// Initializing Variables
int lcdCursor;
int buttonState[5];
int buttonRead[5];
int switchRead;
int switchState;
int matrixState[32];
int selectPins;
int blinkTimer;
boolean mux0, mux1;
unsigned long nextShift;
unsigned long currentTime;
unsigned long difference;
unsigned long debounceTimer;

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 10, 9, 8, 7);


void setup() {
  Serial.begin(115200);

  initLED();
  initSwitch();
  initButtons();
  initMuxer();  
  resetMuxer();
  lcd.begin(STRLEN, 2);
  
  nextShift = micros() + INITDELAY;  
  currentTime = micros();
}

void loop() {
  blinkLED();
  readSwitch();
  readButtons();
  readMuxer();
  lcdScroll();
}
  



void initLED(){
  pinMode(LED, OUTPUT);
}

void blinkLED(){
  if ((millis()%(2*LEDTIMER)) > LEDTIMER){
    digitalWrite(LED,HIGH);
  } else {
    digitalWrite(LED, LOW);
  }
}

void initSwitch(){
  pinMode(PWR, INPUT);
}

void readSwitch(){
  switchRead = digitalRead(PWR);
  if (switchState != switchRead && millis() - debounceTimer > SWITCHDEBOUNCE){
    Serial.print("S");
    Serial.println(switchRead);
    switchState = switchRead;
    debounceTimer = millis();
  }
}
  


void initButtons(){
  pinMode(in0, INPUT_PULLUP);
  pinMode(in1, INPUT_PULLUP);
  pinMode(in2, INPUT_PULLUP);
  pinMode(in3, INPUT_PULLUP);
  pinMode(in4, INPUT_PULLUP);
}



void readButtons(){
  buttonRead[0] = !digitalRead(in0);
  buttonRead[1] = !digitalRead(in1);
  buttonRead[2] = !digitalRead(in2);
  buttonRead[3] = !digitalRead(in3);
  buttonRead[4] = !digitalRead(in4);  
  
  for(int i=0; i<5; i++){
    if (buttonRead[i] > buttonState[i] && millis() - debounceTimer > BUTTONDEBOUNCE){
      Serial.print("B");
      Serial.println(i);
      buttonState[i] = buttonRead[i];
      debounceTimer = millis();
    } else if (buttonRead[i] < buttonState[i] && millis() - debounceTimer > BUTTONDEBOUNCE){
      buttonState[i] = buttonRead[i];
      debounceTimer = millis();
    }
  }
}



void initMuxer(){
  pinMode(SIG0, INPUT);
  pinMode(SIG1, INPUT);
  pinMode(SEL0, OUTPUT);
  pinMode(SEL1, OUTPUT);
  pinMode(SEL2, OUTPUT);
  pinMode(SEL3, OUTPUT);
}



void resetMuxer(){
  selectPins = 0;
  digitalWrite(SEL0, LOW);
  digitalWrite(SEL1, LOW);
  digitalWrite(SEL2, LOW);
  digitalWrite(SEL3, LOW);
}



void readMuxer(){
  currentTime = micros();
  difference = currentTime - nextShift;
  if (difference > SHIFTTIME && difference < 10*SHIFTTIME){
    mux0 = digitalRead(SIG0);
    mux1 = digitalRead(SIG1);
    
    if (mux0 != matrixState[selectPins] && millis() - debounceTimer > MUXERDEBOUNCE){
      Serial.print("M");
      Serial.print(mux0);
      Serial.println(selectPins);
      debounceTimer = millis();
    }      
    if (mux1 != matrixState[selectPins + 16] && millis() - debounceTimer > MUXERDEBOUNCE){
      Serial.print("M");
      Serial.print(mux1);
      Serial.println(selectPins + 16);
      debounceTimer = millis();
    }       
      
    matrixState[selectPins]      = mux0;
    matrixState[selectPins + 16] = mux1;
    selectPins = (selectPins + 1) % 16;
    
    digitalWrite(SEL0, (selectPins & 1) >> 0);
    digitalWrite(SEL1, (selectPins & 2) >> 1);
    digitalWrite(SEL2, (selectPins & 4) >> 2);
    digitalWrite(SEL3, (selectPins & 8) >> 3);
          
    nextShift = nextShift+SHIFTTIME;   
  } 
}



void lcdScroll(){
  if (Serial.available()) {
    if (lcdCursor > 2*STRLEN-1) {
      lcdCursor = 0;
      lcd.clear();
    }
    else lcd.setCursor(lcdCursor%STRLEN, lcdCursor/STRLEN);
    
    char c = Serial.read();
    if      (c == '\0') lcdCursor = 2*STRLEN;
    else if (c == '\n') lcdCursor = lcdCursor + STRLEN;
    else if (c == '\r') lcdCursor = (lcdCursor/STRLEN)*STRLEN;
    else {
      lcd.write(c);
      lcdCursor++;  
    }
  }
}



