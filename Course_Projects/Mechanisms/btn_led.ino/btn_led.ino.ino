
int pwm_L=40;
int pwm_R=40;

const int Lf = 5;  
const int Lb = 6;
const int Rf = 10;
const int Rb = 11;
const int ENA = 9;
const int ENB = 3;



void setup() {
  
  pinMode(Lf,OUTPUT);
  pinMode(Lb,OUTPUT);
  pinMode(ENA,OUTPUT);
  pinMode(Rf,OUTPUT);
  pinMode(Rb,OUTPUT);
  pinMode(ENB,OUTPUT);
  Serial.println("Start");
  Serial.begin(9600);
}

void loop() {
    
    Serial.print("pwm L:");
    Serial.println(pwm_L);
    Serial.print("pwm R:");
    Serial.println(pwm_R);
    
}

void runMotor(int pwm_L, int pwm_R){
  if(pwm_L>=0&&pwm_R>=0){
  analogWrite(ENA,pwm_L);
  analogWrite(Lf,pwm_L);
  analogWrite(Lb,0);
  analogWrite(Rf,pwm_R);
  analogWrite(ENB,pwm_R);
  analogWrite(Rb,0);
  }
  if(pwm_L<0&&pwm_R<0){
  analogWrite(Lf,0);
  analogWrite(Lb,pwm_L);
  analogWrite(ENA,pwm_L);
  analogWrite(Rf,0);
  analogWrite(Rb,pwm_R);
  analogWrite(ENB,pwm_R);
  }
}
