#include <Servo.h>
#include <Ultrasonic.h>

const int relay1 = 35; // relay of motor 5V
const int relay2 = 37; // relay of magnet 12V
const int Armmotor1 = 7; // the pin of arm motor1 (手臂左邊的馬達)
const int Armmotor2 = 8; // the pin of arm motor2 (手臂右邊的馬達)
Servo Armservo1; // 定義伺服馬達物件
Servo Armservo2;
String cmd;
int pwm_L=0,pwm_R=0;

// int ledA_R=46, ledA_G=36, ledA_B=38;   // left-front light, pwm pins
int ledA_R=34, ledA_G=46, ledA_B=36; 
// int ledB_R=40, ledB_G=42, ledB_B=44;   // right-front light, pwm pins
int ledB_R=38, ledB_G=40, ledB_B=42;
int ledC_R=29, ledC_G=31, ledC_B=33;  // left-rear light, digital pins
int ledD_R=28, ledD_G=30, ledD_B=32;  // right-rear light, digital pins

char pwmL[4],pwmR[4],sender,state,power,motion,command;
char ledA, ledB, ledC, ledD;
int Lf=10, Lb=11, Rf=12, Rb=13;  // Arduino mega pins

char color;

Ultrasonic ultrasonicF(45,47); // Front ultra - Trig 45, Echo 47
int distanceD,distanceF;

void setup() {
  Serial.begin(9600);
  Serial.println("Let's GO!"); // 這是用來確定 setup 已經跑完了
}

void loop() {

     resetLED();
     delay(400);
     color = '7';
     igniteLED(ledA_R,ledA_G,ledA_B,color);
     igniteLED(ledB_R,ledB_G,ledB_B,color);
     igniteLED(ledC_R,ledC_G,ledC_B,color);
     igniteLED(ledD_R,ledD_G,ledD_B,color);
     delay(1000);
}

void resetLED(){
     
     igniteLED(ledA_R,ledA_G,ledA_B,'0');
     igniteLED(ledB_R,ledB_G,ledB_B,'0');
     igniteLED(ledC_R,ledC_G,ledC_B,'1');
     igniteLED(ledD_R,ledD_G,ledD_B,'1');
}

void igniteLED(int R,int G,int B,char choice){
  switch(choice){
    case '0':
      light(R,G,B,0,0,0);  // light off
      break;
      
    case '1':
      light(R,G,B,255,255,255);  // white
      break;
 
    case '2':
      light(R,G,B,255,0,0);  // Red
      break;

    case '3':
      light(R,G,B,0,255,0);  // Green
      break;
     
    case '4':
      light(R,G,B,0,0,255);  // Blue
      break;
    
    case '5':
      light(R,G,B,0,255,255);  // Cyan
      break;
      
    case '6':
      light(R,G,B,255,255,0);  // Yellow
      break;
      
    case '7':
      light(R,G,B,255,0,255);  // Megenta
      break;
      
  }
}


void light(int R,int G,int B,int r,int g,int b){
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  if(R==ledA_R || R==ledB_R){
    digitalWrite(R,255-r);
    digitalWrite(G,255-g);
    digitalWrite(B,255-b);
    
  }
  else{
    
    digitalWrite(R,255-r);
    digitalWrite(G,255-g);
    digitalWrite(B,255-b);
  }

}
