
const int btn_STOP = A5;
String MODE = "STOP"; // MODE: STOP, FORWARD, RIGHT, LEFT, BACKWARD, JAW 


const int btn_F = A0; // Green
int delta_F_L = 60; 
int delta_F_R = 60;

const int btn_R = A1; // Orange
int delta_R_R = 60;

const int btn_L = A2; // Blue
int delta_L_L = 60;

const int btn_B = A3; // White
int delta_B_L = 40;
int delta_B_R = 40;

const int btn_Jaw_Open = 2;
const int btn_Jaw_Close = 12;

const int LED_bi = 13; // built-in LED, ON if any button is pressed
const int LED_R = 4; // Green, ON if the motor is on
const int LED_L = 7; // Green, OFF if the motor is off
const int LED_Y = 8; // Yellow, ON if backward or the jaw is operating

int pwm_L=0;
int pwm_R=0;

const int IN1 = 5;
const int IN2 = 6;
const int IN3 = 10;
const int IN4 = 11;

const int ENA = 9;
const int ENB = 3;


const int delay_time = 1000;


void setup() {
  pinMode(btn_STOP,INPUT);
  pinMode(btn_F,INPUT);
  pinMode(btn_R,INPUT);
  pinMode(btn_L,INPUT);
  pinMode(btn_B,INPUT);
  pinMode(btn_Jaw_Open,INPUT);
  pinMode(btn_Jaw_Close,INPUT);
  pinMode(LED_bi,OUTPUT);
  pinMode(LED_L,OUTPUT);
  pinMode(LED_R,OUTPUT);
  pinMode(LED_Y,OUTPUT);
  digitalWrite(LED_bi,LOW);
  
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  
  digitalWrite(ENA, HIGH);
  digitalWrite(ENB, HIGH);
  Serial.begin(9600);
  MODE = "STOP";
}

void loop() {
  Show_btn_status(digitalRead(btn_F),digitalRead(btn_L),digitalRead(btn_R),digitalRead(btn_B),digitalRead(btn_Jaw_Open),digitalRead(btn_Jaw_Close),digitalRead(btn_STOP));
  
  if(MODE == "STOP"){
      Close_all_LED();
      Serial.println("------ MODE: STOP ------");
      MODE = update_MODE();
      Serial.print("------ MODE: STOP -> ");
      Serial.print(MODE);
      Serial.println(" ------ ");
  }
  if(MODE == "FORWARD"){
      digitalWrite(LED_L,HIGH);
      digitalWrite(LED_R,HIGH);
      digitalWrite(LED_Y,LOW);
      digitalWrite(LED_bi,HIGH);
      Serial.println("------ MODE: FORWARD ------");
      if(checkIfSTOP() == true){
          MODE = "STOP";
          Serial.println("------ MODE: FORWARD -> STOP ------");
      }
  }
  if(MODE == "LEFT"){
      digitalWrite(LED_L,HIGH);
      digitalWrite(LED_R,LOW);
      digitalWrite(LED_Y,LOW);
      digitalWrite(LED_bi,HIGH);
      Serial.println("------ MODE: LEFT ------");
      if(checkIfSTOP() == true){
          MODE = "STOP";
          Serial.println("------ MODE: LEFT -> STOP ------");
      }
  }
  if(MODE == "RIGHT"){
      digitalWrite(LED_L,LOW);
      digitalWrite(LED_R,HIGH);
      digitalWrite(LED_Y,LOW);
      digitalWrite(LED_bi,HIGH);
      Serial.println("------ MODE: RIGHT ------");
      if(checkIfSTOP() == true){
          MODE = "STOP";
          Serial.println("------ MODE: RIGHT -> STOP ------");
      }
  }
  if(MODE == "BACKWARD"){
      digitalWrite(LED_L,LOW);
      digitalWrite(LED_R,LOW);
      digitalWrite(LED_Y,HIGH);
      digitalWrite(LED_bi,HIGH);
      Serial.println("------ MODE: BACKWARD ------");
      if(checkIfSTOP() == true){
          MODE = "STOP";
          Serial.println("------ MODE: BACKWARD -> STOP ------");
      }
  }
  if(MODE == "JAW"){
      digitalWrite(LED_L,HIGH);
      digitalWrite(LED_R,HIGH);
      digitalWrite(LED_Y,HIGH);
      digitalWrite(LED_bi,HIGH);
      Serial.println("------ MODE: JAW ------");
      if(checkIfSTOP() == true){
          MODE = "STOP";
          Serial.println("------ MODE: JAW -> STOP ------");
      }
      else{
          int count = digitalRead(btn_Jaw_Close)+digitalRead(btn_Jaw_Open);
          if(count==1){
              if(digitalRead(btn_Jaw_Open)==true){
                  Serial.println("------ Opening... ------");
                  // 伺服馬達轉動一小單位
              }
              if(digitalRead(btn_Jaw_Close)==true){
                  Serial.println("------ Closing... ------");
                  // 伺服馬達轉動一小單位
              }
          }
      }
  }
  
  delay(delay_time);
  
  
}

void Close_all_LED(){
    digitalWrite(LED_L,LOW);
    digitalWrite(LED_R,LOW);
    digitalWrite(LED_Y,LOW);
    digitalWrite(LED_bi,LOW);
}

void Show_btn_status(boolean F,boolean L,boolean R,boolean B,boolean O,boolean C, boolean S){

  Serial.println(" ");
  Serial.println(" ");
  Serial.println("-L-F-R-");
  Serial.print(" ");
  Serial.print(L);
  Serial.print(" ");
  Serial.print(F);
  Serial.print(" ");
  Serial.print(R);
  Serial.println(" ");
  Serial.println(" ");
  Serial.println("-C-B-O- S ");
  Serial.print(" ");
  Serial.print(C);
  Serial.print(" ");
  Serial.print(B);
  Serial.print(" ");
  Serial.print(O);
  Serial.print("  ");
  Serial.print(S);
  Serial.println(" ");
  
  Serial.println(" ");
  
 
}

void runMotor(int pwm_L, int pwm_R){
  if(pwm_L>=0&&pwm_R>=0){
  analogWrite(Lf,pwm_L);
  analogWrite(Lb,0);
  analogWrite(Rf,pwm_R);
  analogWrite(Rb,0);
  }
  if(pwm_L<0&&pwm_R<0){
  analogWrite(Lf,0);
  analogWrite(Lb,pwm_L);
  analogWrite(Rf,0);
  analogWrite(Rb,pwm_R);
  }
}

boolean checkIfSTOP(){
    if(digitalRead(btn_STOP)==HIGH){
        Close_all_LED();
        Serial.println("checkIfSTOP: S T O P !!!!!!");
        return true;
    }
    else{
        Serial.println("checkIfSTOP: don't STOP");
        return false;
    }
}

String update_MODE(){
    if(checkIfSTOP()==true){
        return "STOP";
    }
    else if(digitalRead(btn_Jaw_Close)==true && digitalRead(btn_Jaw_Open)==true ){ 
        return "JAW";
    }
    else{
        if(count_btn_HIGH()>=2 || count_btn_HIGH()==0){
            return "STOP";
        }
        else{
            if(digitalRead(btn_F)==HIGH){
                return "FORWARD";
            }
            if(digitalRead(btn_R)==HIGH){
                return "RIGHT";
            }
            if(digitalRead(btn_L)==HIGH){
                return "LEFT";
            }
            if(digitalRead(btn_B)==HIGH){
                return "BACKWARD";
            }
            }
        }
    }


int count_btn_HIGH(){
    int count = digitalRead(btn_F)+digitalRead(btn_R)+digitalRead(btn_L)+digitalRead(btn_B);
    Serial.print("count_btn_HIGH: ");
    Serial.println(count);
    return count;
}