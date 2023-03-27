#include <Ultrasonic.h>
Ultrasonic ultrasonicHead(12,13); // 車子前面的 SR04, 用來測量終點距離 in cm
int GoalDistance; // 用來記錄測量終點距離 SR04 的數值
int pwm_L=0,pwm_R=0; // 馬達的 PWM 值
//int ledA_R=0, ledA_G=0, ledA_B=0; // LEDA 的 RGB 腳位
//int ledB_R=0, ledB_G=0, ledB_B=0; // LEDB 的 RGB 腳位
int Lf=5, Lb=6, Rf=10, Rb=11;  // 馬達接馬達驅動器的腳位

void setup() {
 //Serial.begin(9600);
 delay(3000);
 for(int n=0; n<20; n++){
  runMotor(40+10*n, 40+10*n);
  delay(50);
 }
 runMotor(255, 255);
 delay(7000);
 /*while(1){
   
 }*/
}

void loop() {
  GoalDistance= ultrasonicHead.read(); // 取得終點距離 cm
  //debug
  //Serial.print("Goal : ");
  //Serial.println(GoalDistance);
  
  if(GoalDistance < 15){
    while(1){
     runMotor(0, 0); 
    }
    //break;
  }
  else if(GoalDistance < 20){
    runMotor(100, 95);
  }
  else if(GoalDistance < 25){
    runMotor(150, 140);
  }
  else if(GoalDistance < 30){
    runMotor(200, 190);
  }
  else{
    runMotor(255, 250);
  }
}
void runMotor(int pwm_L, int pwm_R){ // 馬達行走的函式
  analogWrite(Lf, pwm_L);
  analogWrite(Lb, 0);
  analogWrite(Rf, pwm_R);
  analogWrite(Rb, 0);
}
