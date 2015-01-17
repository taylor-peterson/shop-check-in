/*
Richard Piersall - rpiersall@g.hmc.edu
Taylor Peterson  - tpeterson@g.hmc.edu

Arduino 


*/


// Include the LiquidCrystal Library for writing to LCD:
#include <LiquidCrystal.h>

// Pinout
#define SIG0  0 // Signal Input Pins
#define SIG1  1 
#define SEL0  5 // Signal Select Pins
#define SEL1  4
#define SEL2  3
#define SEL3  2
#define in0   9 // Button Pins
#define in1  10
#define in2  11
#define in3  12

// Constants
const int STRLEN = 16;      // Character-width of LCD row
const int INITDELAY = 1000; // Multiplexer post-reset delay
const int SHIFTTIME = 62;   // Time between multiplexer shifts

// Initializing Variables
int lcdCursor;
int buttonState[4];
int buttonRead[4];
int matrixState[32];
int selectPins;
boolean mux0, mux1;
unsigned long nextShift;
unsigned long currentTime;
unsigned long difference;

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(18, 19, 20, 21, 22, 23);



void setup() {
  Serial.begin(115200);
  
  initButtons();
  initMuxer();  
  resetMuxer();
  lcd.begin(STRLEN, 2);
  
  nextShift = micros() + INITDELAY;  
  currentTime = micros();
}

void loop() {
  readButtons();
  readMuxer();
  lcdScroll();
}
  




void initButtons(){
  pinMode(in0, INPUT_PULLUP);
  pinMode(in1, INPUT_PULLUP);
  pinMode(in2, INPUT_PULLUP);
  pinMode(in3, INPUT_PULLUP);
}



void readButtons(){
  buttonRead[0] = !digitalRead(in0);
  buttonRead[1] = !digitalRead(in1);
  buttonRead[2] = !digitalRead(in2);
  buttonRead[3] = !digitalRead(in3);
  
  for(int i=0; i<4; i++){
    if (buttonRead[i] != buttonState[i]){
      Serial.print("B");
      Serial.print(i);
      Serial.print(",");
      Serial.println(buttonRead[i]);
      buttonState[i] = buttonRead[i];
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
    
    if (mux0 != matrixState[selectPins]){
      Serial.print(selectPins);
      Serial.print(",");
      Serial.println(mux0);
    }      
    if (mux1 > matrixState[selectPins + 16]){
      Serial.print(selectPins);
      Serial.print(",");
      Serial.println(mux1);
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



