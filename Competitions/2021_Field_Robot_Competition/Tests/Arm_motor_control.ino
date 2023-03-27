#include <Servo.h>
const int relay1 = 35; // relay of motor 5V
const int relay2 = 37; // relay of magnet 12V
const int Armmotor1 = 7; // the pin of arm motor1 (手臂左邊的馬達)
const int Armmotor2 = 8; // the pin of arm motor2 (手臂右邊的馬達)
Servo Armservo1; // 定義伺服馬達物件
Servo Armservo2;
char command; // the command sended by Serial we input 
int pwm_L=0,pwm_R=0; // 這些都是關於車子馬達的宣告設定
const int Lf=10, Lb=11, Rf=12, Rb=13;  // Arduino mega pins (跟車子有關的宣告)

void setup() {
  Serial.begin(9600);
  Armservo1.attach(Armmotor1); // need PWM pin
  Armservo2.attach(Armmotor2); // need PWM pin
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  digitalWrite(relay1, LOW); // open the road of relay of motor
  digitalWrite(relay2, LOW); // open the road of relay of magnet
  Serial.println("Let's GO!"); // 這是用來確定 setup 已經跑完了
}

void loop() {
  if(Serial.available()>0)
  { // Read the incoming byte, and say what you got
    command = Serial.read();
    Serial.print("I received ");
    Serial.println(command); // use for debug
    // 判斷 command 並做出動作
    if(command == 'g') // grab
      {
        digitalWrite(relay1, HIGH); // open the relay of motor
        digitalWrite(relay2, HIGH); // open the relay of motor
        Armservo1.write(80);
        Armservo2.write(90);
        delay(500);
        Armservo1.write(90);
        Armservo2.write(90);
        delay(3000);
        Armservo1.write(120);
        Armservo2.write(60);
        delay(800);
        Armservo1.write(80);
        Armservo2.write(90);
        delay(500);
        Armservo1.write(90);
        Armservo2.write(90);
       }
      if(command == 'd') // drop
      {
        Armservo1.write(80);
        Armservo2.write(90);
        delay(500);
        Armservo1.write(90);
        Armservo2.write(90);
        delay(1000);
        digitalWrite(relay2, LOW); // open the relay of motor
        delay(500);
        Armservo1.write(110);
        Armservo2.write(70);
        delay(1700);
        Armservo1.write(85);
        Armservo2.write(95);
        delay(500);
        Armservo1.write(90);
        Armservo2.write(90);
        digitalWrite(relay1, LOW); // open the relay of motor
        }
    if(command == 'c') // c / close the circuit of relay
      {
        digitalWrite(relay1,HIGH); // open the relay of motor
        Serial.println("Open the relay of motor");
      }
    if(command == 'm') // m / close the circuit of magnet
      {
        digitalWrite(relay2,HIGH); // open the relay of motor
        Serial.println("Open the relay of magnet");
      }
    if(command == 's') // s / stop the Armmotor
      { // 數值 90 代表停止馬達轉動
        Armservo1.write(90);
        Armservo2.write(90);
        Serial.println("Stop work");
      }
    if(command == 'l') // l / turn left 手臂往左轉，往上轉
      {// 90 以上到 180 為順時針轉動，數字越大轉速越快
        //Armservo1.write(110);
        Armservo2.write(0);
        Serial.println("Go Left");
      }
    if(command == 'r') // r / turn right 手臂往右轉，往下動
      {// 90 以下到 0 為逆時針轉動，數字越小轉速越大
        Armservo1.write(80);
        Armservo2.write(90);
        Serial.println("Go Right");
      }
    if(command == 'o') // o / open the circuit of motor of relay 
      {
        digitalWrite(relay1,LOW); // open the relay of motor
        Serial.println("stop the power of motor(close the power source)");
      }
    if(command == 'p') // p / open the circuit of magnet of relay 
      {
        digitalWrite(relay2,LOW); // open the relay of motor
        Serial.println("stop the power of magnet (close the power source)");
      }
  }
}
/*// 這是車子馬達的函式
void runMotor(int pwm_L, int pwm_R){
  analogWrite(Lf,pwm_L);
  analogWrite(Lb,0);
  analogWrite(Rf,pwm_R);
  analogWrite(Rb,0);
}*/
