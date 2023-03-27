#include <SoftwareSerial.h>
SoftwareSerial BTHC08Serial(0,1);// RX - TX
const int led = 13;
const int motorR1 = 5; // 右輪的馬達 pin 位 - 1
const int motorR2 = 6; // 右輪的馬達 pin 位 - 2
const int motorL1 = 10; // 左輪的馬達 pin 位 - 1
const int motorL2 = 11; // 左輪的馬達 pin 位 - 2
void setup() {
  Serial.begin(9600);
  Serial.println("Begin!");
  BTHC08Serial.begin(9600);  
  pinMode(led,OUTPUT);
  pinMode(motorR1,OUTPUT);
  pinMode(motorR2,OUTPUT);
  pinMode(motorL1,OUTPUT);
  pinMode(motorL2,OUTPUT);
}

void loop() {
  // keep reading from Arduino Serial Moniter and send to HC08
  if(Serial.available()) 
  {
    char data = Serial.read(); // reading the data recived from the Serial
    BTHC08Serial.write(Serial.read());
    digitalWrite(led,HIGH);
    switch(data)
    {
       case 'g':
      Serial.println("successed"); 
      analogWrite(motorR1,0);
      analogWrite(motorR2,175);
      analogWrite(motorL1,175);
      analogWrite(motorL2,0);
      break;
       case 's':
      Serial.println("success"); 
      analogWrite(motorR1,175); // R
      analogWrite(motorR2,0); // LR
      analogWrite(motorL1,0);
      analogWrite(motorL2,175);
      break;
       case 'd':
      Serial.println("success"); 
      analogWrite(motorR1,0); // R
      analogWrite(motorR2,175); // LR
      analogWrite(motorL1,0);
      analogWrite(motorL2,175);
      break;
       case 'a':
      Serial.println("success"); 
      analogWrite(motorR1,175); // R
      analogWrite(motorR2,0); // LR
      analogWrite(motorL1,175);
      analogWrite(motorL2,0);
      break;
    }
   
  }
  // HC08 default in AT command more
  if(BTHC08Serial.available()) 
  {
    Serial.write(BTHC08Serial.read());
    //Serial.println(BTHC08Serial.read());
    digitalWrite(led,HIGH);
   char data = BTHC08Serial.read(); // reading the data recived from the bluetooth module
   switch(data)
    {
       case 'g':
      Serial.println("success"); 
      analogWrite(motorR1,0); // R
      analogWrite(motorR2,175); // LR
      analogWrite(motorL1,175);
      analogWrite(motorL2,0);
      break;
      case 's':
      Serial.println("success"); 
      analogWrite(motorR1,175); // R
      analogWrite(motorR2,0); // LR
      analogWrite(motorL1,0);
      analogWrite(motorL2,175);
      break;
        case 'd':
      Serial.println("success"); 
      analogWrite(motorR1,0); // R
      analogWrite(motorR2,175); // LR
      analogWrite(motorL1,0);
      analogWrite(motorL2,175);
      break;
       case 'a':
      Serial.println("success"); 
      analogWrite(motorR1,175); // R
      analogWrite(motorR2,0); // LR
      analogWrite(motorL1,175);
      analogWrite(motorL2,0);
      break;
    }
  }
  delay(500);
  digitalWrite(led,LOW);
  analogWrite(motorR1,0);
  analogWrite(motorR2,0);
  analogWrite(motorL1,0);
  analogWrite(motorL2,0);
}
