
int pwm_L=400;
int pwm_R=400;
/* 
const int Lf = 5;  
const int Lb = 6;
const int Rf = 10;
const int Rb = 11; */

const int IN1 = 5;
const int IN2 = 6;
const int IN3 = 10;
const int IN4 = 11;

const int ENA = 9;
const int ENB = 3;


void setup() {
  /* 
  pinMode(Lf,OUTPUT);
  pinMode(Lb,OUTPUT);
  pinMode(Rf,OUTPUT);
  pinMode(Rb,OUTPUT); */
  
  
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
 
  Serial.begin(9600);
}

void loop() {
    Serial.println("Start");
    Serial.print("pwm L:");
    Serial.println(pwm_L);
    Serial.print("pwm R:");
    Serial.println(pwm_R);
    
    MotorAB_Direction1(1000);
}

/* 
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
} */


void MotorAB_Direction1(int milliseconds)
{
 analogWrite(IN1, 500);
 digitalWrite(IN2, LOW);
 analogWrite(IN3, 500);
 digitalWrite(IN4, LOW);
 if (milliseconds > 0)
 delay(milliseconds);
}
 
void MotorAB_Direction2(int milliseconds)
{
 digitalWrite(IN1, LOW);
 analogWrite(IN2, 500);
 digitalWrite(IN3, LOW);
 analogWrite(IN4, 500);
 if(milliseconds > 0)
 delay(milliseconds);
}
 
void MotorAB_Brake(int milliseconds)
{
 analogWrite(IN1, 500);
 analogWrite(IN2, 500);
 analogWrite(IN3, 500);
 analogWrite(IN4, 500);
 if(milliseconds > 0)
 delay(milliseconds); 
}
