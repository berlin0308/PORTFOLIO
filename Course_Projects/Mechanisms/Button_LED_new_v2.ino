/* 

MODE: STOP, FORWARD, RIGHT, LEFT, BACKWARD, JAW 

*/

String MODE = "STOP"; // Default MODE

const int btn_STOP = A5;  // RED button

const int btn_F = A0; // GREEN button

const int btn_R = A1; // YELLOW button

const int btn_L = A2; // BLUE button

const int btn_B = A3; // BLACK button: Backward


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


const int delay_time = 10;
int checktime;

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
  
  analogWrite(ENA, 255);
  analogWrite(ENB, 255);
  Serial.begin(9600);
  MODE = "STOP";
}

void loop() {
    
  Show_btn_status(digitalRead(btn_F),digitalRead(btn_L),digitalRead(btn_R),digitalRead(btn_B),digitalRead(btn_Jaw_Open),digitalRead(btn_Jaw_Close),digitalRead(btn_STOP));
  
  if(MODE=" ")
      MODE = "STOP";
  
  if(MODE == "STOP"){
      
      Close_all_LED();
      Motor_Brake(500);
      
      Serial.println("------ MODE: STOP ------");
      MODE = update_MODE();
      
      if(MODE != "STOP"){
      Serial.print("------ MODE: STOP -> ");
      Serial.print(MODE);
      Serial.println(" ------ ");
      }
      
  }
  if(MODE == "FORWARD"){
      
      digitalWrite(LED_L,HIGH);
      digitalWrite(LED_R,HIGH);
      digitalWrite(LED_Y,LOW);
      digitalWrite(LED_bi,HIGH);
      
      delay(0);
      runMotor_Forward(2000);
      
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
      
      delay(200);
      runMotor_Left(500);
      
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
      
      delay(200);
      runMotor_Right(500);
      
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
      
      delay(200);
      runMotor_Backward(200);
      
      Serial.println("------ MODE: BACKWARD ------");
      
      if(checkIfSTOP() == true){
          MODE = "STOP";
          Serial.println("------ MODE: BACKWARD -> STOP ------");
      }
  }
  if(MODE == "JAW"){
      MODE = "STOP"; // the jaw haven't completed
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
  Serial.print("  ");
  Serial.println(F);
  Serial.print(L);
  Serial.print("   ");
  Serial.println(R);
  Serial.print("  ");
  Serial.println(B);
  Serial.println(" ");
  Serial.println(S);
  Serial.println(" ");
  
  /* Serial.println(" ");
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
   */
 
}




boolean checkIfSTOP(){
    if(digitalRead(btn_STOP)==HIGH){
        Close_all_LED();
        // Serial.println("checkIfSTOP: S T O P !!!!!!");
        return true;
    }
    else{
        // Serial.println("checkIfSTOP: don't STOP");
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
    // Serial.print("count_btn_HIGH: ");
    Serial.println(count);
    return count;
}

void runMotor_Forward(int milliseconds)
{
 checktime = milliseconds / 6;
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, HIGH);
 //analogWrite(IN2, 255);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, HIGH);
 //analogWrite(IN4, 255);
 delay(checktime);
 if(checkIfSTOP() == false){
     delay(checktime);
     Serial.println("111");
     if(checkIfSTOP() == false){
         delay(checktime);
         Serial.println("222");
         if(checkIfSTOP() == false){
             delay(checktime);
             Serial.println("333");
             if(checkIfSTOP() == false){
             delay(checktime);
             Serial.println("444");
             if(checkIfSTOP() == false){
             delay(checktime);
             Serial.println("555");
         }
         }
         }
   }
 }
 Motor_Brake(10);
}

void runMotor_Backward(int milliseconds)
{
 digitalWrite(IN1, HIGH);
 // analogWrite(IN1, 500);
 digitalWrite(IN2, LOW);
 digitalWrite(IN3, HIGH);
 //analogWrite(IN3, 500);
 digitalWrite(IN4, LOW);
 if (milliseconds > 0)
 delay(milliseconds);
}
 
 
void runMotor_Right(int milliseconds) // untested
{
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, HIGH);
 //analogWrite(IN2, 500);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, LOW);
 //analogWrite(IN4, 0);
 if(milliseconds > 0)
 delay(milliseconds);
}


void runMotor_Left(int milliseconds) // untested
{
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, LOW);
 //analogWrite(IN2, 0);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, HIGH);
 //analogWrite(IN4, 500);
 if(milliseconds > 0)
 delay(milliseconds);
}

void Motor_Brake(int milliseconds)
{
 digitalWrite(IN1, HIGH);
 digitalWrite(IN2, HIGH);
 digitalWrite(IN3, HIGH); 
 digitalWrite(IN4, HIGH);
 /*analogWrite(IN2, 500);
 analogWrite(IN3, 500);
 analogWrite(IN4, 500);*/
 if(milliseconds > 0)
 delay(milliseconds); 
}