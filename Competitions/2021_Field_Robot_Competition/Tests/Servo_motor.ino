#include <Servo.h>
Servo myservo;  // 建立一個 servo 物件，最多可建立 12個 servo
int pos = 0;    // 設定 Servo 位置的變數
char command;
#define relay1 7 // relay of motor 5V
void setup() {
  myservo.attach(9);  // 將 servo 物件連接到 pin 9
  Serial.begin(9600);
  pinMode(relay1,OUTPUT);
  Serial.println("Let's GO!");
}

void loop() {
  if(Serial.available()>0)
  {
    command = Serial.read();
    Serial.print("I received ");
    Serial.println(command);
    if(command == 'c') // c / close the relay
      {
        digitalWrite(relay1,HIGH); // open the relay of motor
        Serial.println("Open the relay");
      }
     if(command == 'g') // c / close the relay
      {
        myservo.write(180);
        Serial.println("right turn");
      }
      if(command == 'h') // c / close the relay
      {
        myservo.write(0);
        Serial.println("left turn");
      }
      if(command == 's') // c / close the relay
      {
        myservo.write(90);
        Serial.println("stop turn");
      }
    if(command == 'r')
    {
      for(pos=0;pos<90;pos++)
      {
        myservo.write(pos);
        delay(15); 
      }
    }
      if(command == 'l')
    {
      for(pos=180;pos>90;pos--)
      {
        myservo.write(pos);
        delay(15); 
      }
    }
    if(command == 'o') // o / open the load
      {
        digitalWrite(relay1,LOW);
        Serial.println("Close the power of motor");
      }
  }
  /*
  int sensorValue = analogRead(A0); // read the input on analog pin 0
  Serial.println(sensorValue); // print out the value you read
  if (sensorValue<300)
  {
      myservo.write(180);
      delay(20);
  }
  else
  {
    myservo.write(0);
    delay(20);
  }*/
}
