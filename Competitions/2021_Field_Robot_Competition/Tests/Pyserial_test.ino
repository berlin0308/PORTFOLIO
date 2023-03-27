int x;
void setup() {
 Serial.begin(9600);
 Serial.setTimeout(1);
 pinMode(10,OUTPUT);
 pinMode(11,OUTPUT);
 pinMode(12,OUTPUT);
 pinMode(13,OUTPUT);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 if(x == 1){
  analogWrite(10,100);
  analogWrite(11,0);
  Serial.println(x + 1);
  delay(1000);
 }
 if(x == 2){
  analogWrite(10,0);
  analogWrite(11,0);
  Serial.println(x + 1);
  delay(1000);
 }
  if(x == 3){
  analogWrite(12,100);
  analogWrite(13,0);
  Serial.println(x + 1);
  delay(1000);
 }
 Serial.println(x + 1);
}
