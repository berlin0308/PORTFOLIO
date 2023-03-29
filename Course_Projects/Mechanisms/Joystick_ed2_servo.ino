#include <Servo.h>

const int Armmotor1 = 3; // the pin of arm motor1
const int Armmotor2 = 9; // the pin of arm motor2
Servo Armservo1; 
Servo Armservo2;

int servo1 = 90;
int servo2 = 90;

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
const int SW = A2; // button on the Joystick

const int LED_bi = 13; // built-in LED, ON if any button is pressed
const int LED_R = 4; // Green, ON if the motor is on
const int LED_L = 7; // Green, OFF if the motor is off
const int LED_Y = 8; // Yellow, ON if backward or the jaw is operating

int pwm_L=0;
int pwm_R=0;

const int IN1 = 5;
const int IN2 = 6;
const int IN3 = 10;
const int IN4 = 11;

const int ENA = 9;
const int ENB = 3;


String MODE = "SHIFTING"; // MODE: "SHIFTING", "GRABBING"
String STATE = "STOP"; // STATE: "STOP", "FORWARD", "RIGHT", "LEFT", "BACKWARD", "CLOSING", "OPENING", "DROPPING", "RISING"


void setup() {
  pinMode(X_coord,INPUT);
  pinMode(Y_coord,INPUT);
  
  pinMode(LED_bi,OUTPUT);
  pinMode(LED_L,OUTPUT);
  pinMode(LED_R,OUTPUT);
  pinMode(LED_Y,OUTPUT);
  digitalWrite(LED_bi,LOW);
  
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  analogWrite(ENA, 255);
  analogWrite(ENB, 255);
  
  
  Armservo1.attach(Armmotor1); // need PWM pin
  Armservo2.attach(Armmotor2); // need PWM pin
  
  Serial.begin(9600);
}

void loop(){
    
  
  while(MODE=="SHIFTING"){
      
      if(analogRead(X_coord)<20){ // X_coord=0 -> LEFT
          STATE = "LEFT";
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_bi,HIGH);
          
          digitalWrite(IN1, LOW);
          digitalWrite(IN2, LOW);
          digitalWrite(IN3, LOW);
          digitalWrite(IN4, HIGH);
         
      }
      else if(analogRead(X_coord)>1003){ // X_coord=1023 -> RIGHT
          STATE = "RIGHT";
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_bi,HIGH);
      
          digitalWrite(IN1, LOW);
          digitalWrite(IN2, HIGH);
          digitalWrite(IN3, LOW);
          digitalWrite(IN4, LOW);
      }
      else if(analogRead(Y_coord)<20){ // Y_coord=0 -> BACKWARD
          STATE = "BACKWARD";
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,HIGH);
          digitalWrite(LED_bi,HIGH);
      
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
          digitalWrite(LED_bi,HIGH);
          
          digitalWrite(IN1, LOW);
          digitalWrite(IN2, HIGH);
          digitalWrite(IN3, LOW);
          digitalWrite(IN4, HIGH);
      }
      else{
          STATE = "STOP";
          
          digitalWrite(LED_L,LOW);
          digitalWrite(LED_R,LOW);
          digitalWrite(LED_Y,LOW);
          digitalWrite(LED_bi,LOW);
            
          digitalWrite(IN1, HIGH);
          digitalWrite(IN2, HIGH);
          digitalWrite(IN3, HIGH);
          digitalWrite(IN4, HIGH);
      }
      
      if(analogRead(SW)==0){
          MODE = "GRABBING";
          STATE = "STOP";
          Serial.println("-----");
          Serial.println("MODE: GRABBING");
          Serial.println("-----");
          
          digitalWrite(LED_L,HIGH);
          digitalWrite(LED_R,HIGH);
          digitalWrite(LED_Y,HIGH);
          digitalWrite(LED_bi,HIGH);
          delay(1000);
      }
      
      Serial.print("STATE:");
      Serial.println(STATE);
      
      delay(500);
  }
  
  
  while(MODE=="GRABBING"){
      
      if(analogRead(X_coord)<20){ // X_coord=0 -> CLOSING
          STATE = "CLOSING";
          if(servo1!=180){
              servo1 -= 20;
          }
          Armservo1.write(servo1);
          Armservo2.write(servo2);
          
      }
      else if(analogRead(X_coord)>1003){ // X_coord=1023 -> OPENING
          STATE = "OPENING";
          if(servo1!=0){
              servo1 += 20;
          }
          Armservo1.write(servo1);
          Armservo2.write(servo2);
          
      }
      else if(analogRead(Y_coord)<20){ // Y_coord=0 -> DROPPING
          STATE = "DROPPING";
          if(servo2!=0){
              servo2 -= 20;
          }
          Armservo1.write(servo1);
          Armservo2.write(servo2);
          
      }
      else if(analogRead(Y_coord)>1003){ // Y_coord=1023 -> RISING
          STATE = "RISING";
          if(servo2!=180){
              servo2 += 20;
          }
          Armservo1.write(servo1);
          Armservo2.write(servo2);
      }
      else{
          STATE = "STOP";
      }
      
      if(analogRead(SW)==0){
          MODE = "SHIFTING";
          STATE = "STOP";
          Serial.println("-----");
          Serial.println("MODE: SHIFTING");
          Serial.println("-----");
          delay(1000);
      }
      
      Serial.print("STATE:");
      Serial.println(STATE);
      
      delay(500);
  }
  
  
  
}