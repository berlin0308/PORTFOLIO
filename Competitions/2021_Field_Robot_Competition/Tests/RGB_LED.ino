int R = 7;
int B = 6;
int G = 5;
int t = 1000;
void setup() {
  Serial.begin(9600); 
  pinMode(R,OUTPUT);
  pinMode(B,OUTPUT);
  pinMode(G,OUTPUT);
}

void loop() {
 int sensorValue = analogRead(A0); // read the input on analog pin 0
 Serial.println(sensorValue); 
 if(sensorValue<10){
  light(0,255,255);
 }
 else
  light(255,0,255);
 /*light(0,255,255);
 delay(t);
 light(255,0,255);
 delay(t);
 light(255,255,0);
 delay(t);
 light(0,0,0);
 delay(t);*/
}
void closelight(){
  analogWrite(R,0);
  analogWrite(G,0);
  analogWrite(B,0);
}
void light(int r,int g,int b){ // RGB 
  analogWrite(R,255-r);
  analogWrite(G,255-g);
  analogWrite(B,255-b);
}
