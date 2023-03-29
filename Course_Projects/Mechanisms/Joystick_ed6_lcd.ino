#include <Servo.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27,20,4); 

const int Armmotor1 = 9; // the pin of arm motor1: direction
const int Armmotor2 = 3; // the pin of arm motor2: arm
const int Armmotor3 = A3; // the pin of arm motor3: claw

Servo Armservo1; 
Servo Armservo2;
Servo Armservo3;

int servo1 = 90;
int servo2 = 120;
int servo3 = 90;

/* 
 y=1023
-------
|     | x=1023
|     |                                 
-------
 |||||
*/

const int Y_coord = A0; // VrX pin
const int X_coord = A1; // VrY pin
const int SW = A2; // RED button

//const int LED_bi = 13; // built-in LED, ON if "STOP"
const int LED_R = 7; // Green, ON if "SHIFTING"
const int LED_L = 13; // Green, ON if "SHIFTING"
const int LED_B = 4; // Blue, ON if "SPINNING"
const int LED_Y = 8; // Yellow, ON if "GRABBING"

int pwm_L=0;
int pwm_R=0;

const int IN1 = 5;
const int IN2 = 6;
const int IN3 = 10;
const int IN4 = 11;

const int ENA = 12;
const int ENB = 2;


String MODE = "SHIFTING"; // MODE: "SHIFTING", "SPINNING", "GRABBING"
String STATE = "STOP"; // STATE: "STOP", "FORWARD", "RIGHT", "LEFT", "BACKWARD", "CLOSING", "OPENING", "DROPPING", "RISING"


void setup() {
    
  lcd.init();
  lcd.backlight();
  
  
  pinMode(X_coord,INPUT);
  pinMode(Y_coord,INPUT);
  pinMode(SW,INPUT);
  
  pinMode(LED_L,OUTPUT);
  pinMode(LED_R,OUTPUT);
  pinMode(LED_B,OUTPUT);
  pinMode(LED_Y,OUTPUT);
   
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  digitalWrite(ENA, HIGH);
  digitalWrite(ENB, HIGH);
  
  digitalWrite(LED_B,LOW);
  
  Armservo1.attach(Armmotor1);
  Armservo2.attach(Armmotor2);
  Armservo3.attach(Armmotor3);
  
  
 /*  Armservo1.write(servo1);
  Armservo2.write(servo2);
  Armservo3.write(servo3);
  */ 
  Serial.begin(9600);
}

void loop(){
    
  lcd.init();
  delay(100);
  lcd.setCursor(0, 0);
  lcd.print(MODE);
  lcd.setCursor(0, 1);
  lcd.print(STATE);

  Armservo1.write(servo1);
  Armservo2.write(servo2);
  Armservo3.write(servo3);
  
  Serial.println(analogRead(SW));
  Serial.println(digitalRead(SW));
  
  while(MODE=="SHIFTING"){
      
      if(analogRead(X_coord)<20){ // X_coord=0 -> LEFT
          STATE = "LEFT";
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_B,LOW);
           

          digitalWrite(IN1, LOW);
          digitalWrite(IN2, HIGH);
          digitalWrite(IN3, HIGH);
          digitalWrite(IN4, LOW);
         
      }
      else if(analogRead(X_coord)>1003){ // X_coord=1023 -> RIGHT
          STATE = "RIGHT";
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_B,LOW);
           
          
          digitalWrite(IN1, HIGH);
          digitalWrite(IN2, LOW);
          digitalWrite(IN3, LOW);
          digitalWrite(IN4, HIGH);
      }
      else if(analogRead(Y_coord)<20){ // Y_coord=0 -> BACKWARD
          STATE = "BACKWARD";
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_B,LOW);
           
      
          digitalWrite(IN1, HIGH);
          digitalWrite(IN2, LOW);
          digitalWrite(IN3, HIGH);
          digitalWrite(IN4, LOW);
      }
      else if(analogRead(Y_coord)>1003){ // Y_coord=1023 -> FORWARD
          STATE = "FORWARD";
              
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_B,LOW);
           
          
          digitalWrite(IN1, LOW);
          digitalWrite(IN4, HIGH);
          digitalWrite(IN3, LOW);
          digitalWrite(IN2, HIGH);
      }
      else{
          STATE = "STOP";
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_B,LOW);
           
            
          digitalWrite(IN1, HIGH);
          digitalWrite(IN2, HIGH);
          digitalWrite(IN3, HIGH);
          digitalWrite(IN4, HIGH);
      }
      
      //if(digitalRead(SW)==0){
      if(analogRead(SW)>0){
          MODE = "SPINNING";
          STATE = "STOP";
          Serial.println("-----");
          Serial.println("MODE: SPINNING");
          Serial.println("-----");
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,HIGH);
          digitalWrite(LED_B,HIGH);
           
          delay(500);
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_B,LOW);
           
          delay(500);
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,HIGH);
          digitalWrite(LED_B,HIGH);
           
          delay(500);
      }
      
      Serial.print("STATE:");
      Serial.println(STATE);
      
      delay(200);
  }
  
  while(MODE=="SPINNING"){
      
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, HIGH);
      
      digitalWrite(LED_L,LOW);
      digitalWrite(LED_R,LOW);
      digitalWrite(LED_Y,LOW);
      digitalWrite(LED_B,HIGH);
       
      
      Armservo1.write(servo1);
      Armservo2.write(servo2);
      Armservo3.write(servo3);
                  
      if(analogRead(X_coord)<20){ // X_coord=0 -> LEFTTURN
          STATE = "LEFTTURN";
          if(servo3+20<180){
              for(int delta=0; delta<=20; delta+=1){
                  servo3 += 1;
                  Armservo1.write(servo1);
                  Armservo2.write(servo2);
                  Armservo3.write(servo3);
                  delay(25);
              } 
          }
          else{
              Serial.print("LEFTTURN: reach the servo limit");
          }
             
      }
      else if(analogRead(X_coord)>1003){ // X_coord=1023 -> RIGHTTURN
          STATE = "RIGHTTURN";
          if(servo3-20>0){ 
              for(int delta=0; delta<=20; delta+=1){
                      servo3 -= 1;
                      Armservo1.write(servo1);
                      Armservo2.write(servo2);
                      Armservo3.write(servo3);
                      delay(25);
                  } 
          }
          else{
               Serial.print("RIGHTTURN: reach the servo limit");
          }
      }
      else{
          STATE = "STOP";
      }
      
      //if(digitalRead(SW)==0){
      if(analogRead(SW)==0){
          MODE = "GRABBING";
          STATE = "STOP";
          Serial.println("-----");
          Serial.println("MODE: GRABBING");
          Serial.println("-----");
          
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,HIGH);
          digitalWrite(LED_B,HIGH);
           
          delay(500);
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_B,LOW);
           
          delay(500);
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,HIGH);
          digitalWrite(LED_B,HIGH);
           
          delay(500);
      }
      
      Serial.print("STATE:");
      Serial.println(STATE);
      
      delay(20);
      
      }
      
  
  while(MODE=="GRABBING"){
      
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, HIGH);
      
      digitalWrite(LED_L,LOW);
      digitalWrite(LED_R,LOW);
      digitalWrite(LED_Y,HIGH);
      digitalWrite(LED_B,LOW);
       
      
      Armservo1.write(servo1);
      Armservo2.write(servo2);
      Armservo3.write(servo3);
                  
      if(analogRead(X_coord)<20){ // X_coord=0 -> CLOSING
          STATE = "CLOSING";
          if(servo1+20<180){
              for(int delta=0; delta<=20; delta+=1){
                  servo1 += 1;
                  Armservo1.write(servo1);
                  Armservo2.write(servo2);
                  delay(25);
              } 
          }
          else{
              Serial.print("CLOSING: reach the servo limit");
          }
             
      }
      else if(analogRead(X_coord)>1003){ // X_coord=1023 -> OPENING
          STATE = "OPENING";
          if(servo1-20>0){ 
              for(int delta=0; delta<=20; delta+=1){
                      servo1 -= 1;
                      Armservo1.write(servo1);
                      Armservo2.write(servo2);
                      delay(25);
                  } 
          }
          else{
               Serial.print("OPENING: reach the servo limit");
          }
           
      }
      else if(analogRead(Y_coord)<20){ // Y_coord=0 -> DROPPING
          STATE = "DROPPING";
          if(servo2-20>=0){
              for(int delta=0; delta<=20; delta+=1){
                  servo2 -= 1;
                  Armservo1.write(servo1);
                  Armservo2.write(servo2);
                  delay(25);
              } 
          }
          else{
              Serial.print("DROPPING: reach the servo limit");
          }
          
          
      }
      else if(analogRead(Y_coord)>1003){ // Y_coord=1023 -> RISING
          STATE = "RISING";
          if(servo2+20<=180){ 
              for(int delta=0; delta<=20; delta+=1){
                      servo2 += 1;
                      Armservo1.write(servo1);
                      Armservo2.write(servo2);
                      delay(25);
                  } 
          }
          else{
               Serial.print("RISING: reach the servo limit");
          }
      }
      else{
          STATE = "STOP";
      }
      
      
      //if(digitalRead(SW)==0){
      if(analogRead(SW)==0){
          MODE = "SHIFTING";
          STATE = "STOP";
          Serial.println("-----");
          Serial.println("MODE: SHIFTING");
          Serial.println("-----");
          
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,HIGH);
          digitalWrite(LED_B,HIGH);
           
          delay(500);
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_B,LOW);
           
          delay(500);
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,HIGH);
          digitalWrite(LED_B,HIGH);
           
          delay(500);
          
      }
      
      Serial.print("STATE:");
      Serial.println(STATE);
      
      delay(200);
  }
  
  
}