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

String MODE = "SHIFTING"; // MODE: "SHIFTING", "GRABBING";
String STATE = "STOP"; // STATE: "STOP", "FORWARD", "RIGHT", "LEFT", "BACKWARD", "CLOSING", "OPENING"


void setup() {
  pinMode(X_coord,INPUT);
  pinMode(Y_coord,INPUT);
  Serial.begin(9600);
}

void loop(){
    
  /* Serial.print("X_coord: ");
  Serial.println(analogRead(X_coord));
  Serial.print("Y_coord: ");
  Serial.println(analogRead(Y_coord));
  Serial.print("SW: ");
  Serial.println(analogRead(SW));
  Serial.println(" ");
  */
  
  while(MODE=="SHIFTING"){
      
      if(analogRead(X_coord)<20){ // X_coord=0 -> LEFT
          STATE = "LEFT";
      }
      else if(analogRead(X_coord)>1003){ // X_coord=1023 -> RIGHT
          STATE = "RIGHT";
      }
      else if(analogRead(Y_coord)<20){ // Y_coord=0 -> BACKWARD
          STATE = "BACKWARD";
      }
      else if(analogRead(Y_coord)>1003){ // Y_coord=1023 -> FORWARD
          STATE = "FORWARD";
      }
      else{
          STATE = "STOP";
      }
      
      if(analogRead(SW)==0){
          MODE = "GRABBING";
          STATE = "STOP";
          Serial.println("-----");
          Serial.println("MODE: GRABBING");
          Serial.println("-----");
          delay(1000);
      }
      
      Serial.print("STATE:");
      Serial.println(STATE);
      
      delay(500);
  }
  
  
  while(MODE=="GRABBING"){
      
      if(analogRead(X_coord)<20){ // X_coord=0 -> CLOSING
          STATE = "CLOSING";
      }
      else if(analogRead(X_coord)>1003){ // X_coord=1023 -> OPENING
          STATE = "OPENING";
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