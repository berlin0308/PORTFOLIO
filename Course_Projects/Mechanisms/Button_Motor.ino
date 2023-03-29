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

const int LED_bi = 13; // built-in LED, ON if any button is pressed
const int LED_R = 4; // Green, ON if the motor is on
const int LED_L = 7; // Green, OFF if the motor is off
const int LED_Y = 8; // Yellow, ON if backward or the jaw is operating

int pwm_L=0;
int pwm_R=0;

const int Lf = 5;  
const int Lb = 6;
const int Rf = 10;
const int Rb = 11;


void setup() {
  
  pinMode(btn_F,INPUT);
  pinMode(btn_R,INPUT);
  pinMode(btn_L,INPUT);
  pinMode(btn_B,INPUT);
  pinMode(LED_bi,OUTPUT);
  pinMode(LED_L,OUTPUT);
  pinMode(LED_R,OUTPUT);
  pinMode(LED_Y,OUTPUT);
  digitalWrite(LED_bi,LOW);
  Serial.begin(9600);
}

void loop() {

  pwm_L = 0;
  pwm_R = 0;
  
  Close_all_LED();
  Show_btn_status(digitalRead(btn_F),digitalRead(btn_L),digitalRead(btn_R),digitalRead(btn_B));
  
  if(digitalRead(btn_F)==HIGH || digitalRead(btn_L)==HIGH || digitalRead(btn_R)==HIGH || digitalRead(btn_B)==HIGH){
      digitalWrite(LED_bi,HIGH); // the built-in LED is ON if any button is pressed
      if(digitalRead(btn_F)==HIGH){
        pwm_L += delta_F_L;
        pwm_R += delta_F_R;  
        digitalWrite(LED_L,HIGH);
        digitalWrite(LED_R,HIGH);
      }
      if(digitalRead(btn_L)==HIGH){
        pwm_L += delta_L_L; 
        digitalWrite(LED_L,HIGH);        
      }
      if(digitalRead(btn_R)==HIGH){
        pwm_R += delta_R_R;
        digitalWrite(LED_R,HIGH);        
      }
      if(digitalRead(btn_B)==HIGH){
        pwm_L -= delta_B_L;  
        pwm_R -= delta_B_R;
        digitalWrite(LED_Y,HIGH);
      }
      runMotor(pwm_L,pwm_R);
      delay(500);
      Close_all_LED();
      runMotor(0,0);
  }
  
  
  
  Serial.print("pwm_L:");
  Serial.println(pwm_L);
  Serial.print("pwm_R:");
  Serial.println(pwm_R);
  Serial.println(" ");
  
  
}

void Close_all_LED(){
    digitalWrite(LED_L,LOW);
    digitalWrite(LED_R,LOW);
    digitalWrite(LED_Y,LOW);
    digitalWrite(LED_bi,LOW);
}

void Show_btn_status(boolean F,boolean L,boolean R,boolean B){

  Serial.println("-----");
  Serial.print("  ");
  Serial.println(F);
  Serial.print(L);
  Serial.print("   ");
  Serial.println(R);
  Serial.print("  ");
  Serial.println(B);
  Serial.println("-----");
  
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
