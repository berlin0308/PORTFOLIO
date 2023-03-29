/* 
 y=1023
-------
|     | x=1023
|     |
-------
 |||||
*/

const int Vry = A0;
const int Vrx = A1; 
const int SW = A2; // button on the Joystick

void setup() {
  pinMode(Vrx,INPUT);
  pinMode(Vry,INPUT);
  Serial.begin(9600);
}

void loop(){
  Serial.print("Vrx: ");
  Serial.println(analogRead(Vrx));
  Serial.print("Vry: ");
  Serial.println(analogRead(Vry));
  Serial.print("SW: ");
  Serial.println(analogRead(SW));

  
  Serial.println(" ");
  delay(500);
}