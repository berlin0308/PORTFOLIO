#include <SoftwareSerial.h>
SoftwareSerial BTHC08Serial(0,1); // (RX - TX)
const int motorL1 = 10; // 左輪的馬達 pin 位 - 1
const int motorL2 = 11; // 左輪的馬達 pin 位 - 2
const int motorR1 = 12; // 右輪的馬達 pin 位 - 1
const int motorR2 = 13; // 右輪的馬達 pin 位 - 2
//const int led = 13; // 用來測試(確認)指令有沒有傳輸到

long premillis = 0; // will store last time that was updated
long interval = 500; // delay time

void setup() {
  Serial.begin(9600);
  BTHC08Serial.begin(9600); 
  Serial.println("Begin!");
  pinMode(led,OUTPUT);
  pinMode(motorR1,OUTPUT);
  pinMode(motorR2,OUTPUT);
  pinMode(motorL1,OUTPUT);
  pinMode(motorL2,OUTPUT);
}

void loop() {
unsigned long curmillis = millis();
if(Serial.available()) // keep reading from Arduino Serial Moniter and send to HC08
{
  char data = Serial.read(); // reading the data recived from the bluetooth module
  BTHC08Serial.write(Serial.read());
  digitalWrite(led,HIGH);
  switch(data)
  {
    case 'w': 
      go(); 
      break;
    case 'a':
      left();
      
      break;
    case's':
      back();
      break;
    case'd':
      right();
      break;
    case'r':
       stopcar();
      break;
  }
}
if(BTHC08Serial.available()) // HC08 default in AT command more
  {
   Serial.write(BTHC08Serial.read());
   digitalWrite(led,HIGH);
   char data = BTHC08Serial.read(); // reading the data recived from the bluetooth module
   switch(data)
    {
        case 'w': 
      go(); 
      break;
    case 'a':
      left();
      break;
    case's':
      back();
      break;
    case'd':
      right();
      break;
     case'r':
      stopcar();
      break;
    }
  }
 /* if(curmillis - premillis > interval){
    premillis = curmillis;
    digitalWrite(led,LOW);
    stopcar(); // 把馬達都停止( 歸零: analogWrite(motor,0) )
  }*/
  delay(interval);
  digitalWrite(led,LOW);
  stopcar();
}

void go() { // 用來設定往前進的函式
  analogWrite(motorR1,100);
  analogWrite(motorR2,0);
  analogWrite(motorL1,0);
  analogWrite(motorL2,100);
}

void back() { // 用來設定往後退的函式
  analogWrite(motorR1,0);
  analogWrite(motorR2,100);
  analogWrite(motorL1,100);
  analogWrite(motorL2,0);
}

void right() { // 用來設定往右轉的函式
  analogWrite(motorR1,0);
  analogWrite(motorR2,100);
  analogWrite(motorL1,0);
  analogWrite(motorL2,100);
}

void left() { // 用來設定往左轉的函式
  analogWrite(motorR1,100);
  analogWrite(motorR2,0);
  analogWrite(motorL1,100);
  analogWrite(motorL2,0);
}
void stopcar(){ // 讓馬達停止的函式
  analogWrite(motorR1,0);
  analogWrite(motorR2,0);
  analogWrite(motorL1,0);
  analogWrite(motorL2,0);
}

/*int angle () { // 用來計算轉彎時要轉多少的函式(進階的函式看後面會不會用到)
  
}*/

/*int IRvalue(IR){ // 讀取 IR sensor 數值的函式
  return analogRead(IR);
  Serial.println(analogRead(IR));
}*/

/*int DMSvalue(DMS){ // 讀取 DMS sensor 數值的函式
  return analogRead(DMS);
  Serial.println(analogRead(DMS));
}*/
