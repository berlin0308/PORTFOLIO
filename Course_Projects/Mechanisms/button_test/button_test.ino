const int btn_F = 2; // Green
int delta_F_L = 60; 
int delta_F_R = 60;

const int btn_R = 3; // Orange
int delta_R_R = 60;

const int btn_L = 4; // Blue
int delta_L_L = 60;

const int btn_B = 5; // White
int delta_B_L = 40;
int delta_B_R = 40;

const int LED = 13; // built-in LED
int pwm_L=0;
int pwm_R=0;


void setup() {
  
  pinMode(btn_F,INPUT);
  pinMode(btn_R,INPUT);
  pinMode(btn_L,INPUT);
  pinMode(btn_B,INPUT);
  pinMode(LED,OUTPUT);
  digitalWrite(LED,LOW);
  Serial.begin(9600);
}

void loop() {

  pwm_L = 0;
  pwm_R = 0;

  Show_btn_status(digitalRead(btn_F),digitalRead(btn_L),digitalRead(btn_R),digitalRead(btn_B));
  
  if(digitalRead(btn_F)==HIGH){
    pwm_L += delta_F_L;
    pwm_R += delta_F_R;  
  }
  if(digitalRead(btn_L)==HIGH){
    pwm_L += delta_L_L;  
  }
  if(digitalRead(btn_R)==HIGH){
    pwm_R += delta_R_R;  
  }
  if(digitalRead(btn_B)==HIGH){
    pwm_L -= delta_B_L;  
    pwm_R -= delta_B_R;
  }
  
  Serial.print("pwm_L:");
  Serial.println(pwm_L);
  Serial.print("pwm_R:");
  Serial.println(pwm_R);
  digitalWrite(LED,HIGH);
  delay(500);
  digitalWrite(LED,LOW);
  delay(1000);
  
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
