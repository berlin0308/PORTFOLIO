#include <Ultrasonic.h>
int ultra_trig_pin[2] = {22,24};
int ultra_echo_pin[2] = {23,25};
char Receiver, STAGE, STATE, pwmL[4], pwmR[4];
int PWM_L=0, PWM_R=0;
String commandStr;

Ultrasonic Ultra_F(ultra_trig_pin[0],ultra_echo_pin[0]);
Ultrasonic Ultra_B(ultra_trig_pin[1],ultra_echo_pin[1]);

int TRACK_ultra_LED[3] = {26,27,28};

void setup(){
    
    pinMode(22,OUTPUT);
    pinMode(24,OUTPUT);
    pinMode(23,INPUT);
    pinMode(25,INPUT);

    pinMode(TRACK_ultra_LED[0],OUTPUT);
    pinMode(TRACK_ultra_LED[1],OUTPUT);
    pinMode(TRACK_ultra_LED[2],OUTPUT);


    Serial.begin(9600);
}


void loop(){

    //Serial.println("A039898e");
    if(Serial.available()){
        commandStr = Serial.readStringUntil('e');
        Receiver = commandStr[0];
        STAGE = commandStr[1];
        STATE = commandStr[2];
    }

    int F_read=0, B_read=0;
    for(int i=0;i<20;i++){
        F_read += Ultra_F.read();
        B_read += Ultra_B.read();
        delay(10);
    }
    
    Serial.print("\nF: ");
    Serial.println(F_read/20);
    Serial.print("B: ");
    Serial.println(B_read/20);

    TRACK_ultra2pwm(PWM_L,PWM_R,F_read/20,B_read/20);

    Serial.print("PWM_L:");
    Serial.println(PWM_L);
    Serial.print("PWM_R:");
    Serial.println(PWM_R);

    delay(1000);
    
}



void TRACK_ultra2pwm(int& L,int& R, int dist_F,int dist_B){

    int default_PWM = 60;
    int dist_Bound = 60;
    int dist_target = 30;
    int pwm_delta;
    double pwm_delta_const = 1.0;
    double dist_offset_const = 1.0;

    if(dist_F > dist_Bound && dist_B > dist_Bound){
        Serial.println("\nTRACK_ultra2pwm: no valid ultra value\n");
        L = default_PWM;
        R = default_PWM;
        igniteLED(TRACK_ultra_LED,'2'); // red
    }
    else if(dist_F < dist_Bound && dist_B > dist_Bound){
        Serial.println("\nTRACK_ultra2pwm: Front ultra only\n");
        pwm_delta = dist_F-dist_target;
        L = default_PWM + pwm_delta*pwm_delta_const;
        R = default_PWM - pwm_delta*pwm_delta_const;
        igniteLED(TRACK_ultra_LED,'6'); // yellow
    }
    else if(dist_F > dist_Bound && dist_B < dist_Bound){
        Serial.println("\nTRACK_ultra2pwm: Backward ultra only\n");
        pwm_delta = dist_B-dist_target;
        L = default_PWM + pwm_delta*pwm_delta_const;
        R = default_PWM - pwm_delta*pwm_delta_const;
        igniteLED(TRACK_ultra_LED,'3'); // blue
    }else{
        Serial.println("\nTRACK_ultra2pwm: Consider both ultras\n");
        
        // average distance, offset distance
        int dist_avg = (dist_F + dist_B)/2;
        int dist_offset = dist_F - dist_B;
        pwm_delta = dist_avg-dist_target;

        if(abs(pwm_delta)<10){
            Serial.println("\nTRACK_ultra2pwm: Consider both ultras: offset adjust\n");
            L = default_PWM + dist_offset*dist_offset_const;
            R = default_PWM - dist_offset*dist_offset_const;
            igniteLED(TRACK_ultra_LED,'7'); // megenta

        }else{
            Serial.println("\nTRACK_ultra2pwm: Consider both ultras: dist_avg adjust\n");
            L = default_PWM + pwm_delta*pwm_delta_const;
            R = default_PWM - pwm_delta*pwm_delta_const;
            igniteLED(TRACK_ultra_LED,'5'); // cyan
        }

    }



}



void igniteLED(int LEDpins[] ,char choice){
  int R = LEDpins[0];  
  int G = LEDpins[1];  
  int B = LEDpins[2];
  
  switch(choice){
    case '0':
      light(R,G,B,0,0,0);  // light off
      break;
      
    case '1':
      light(R,G,B,255,255,255);  // white
      break;
 
    case '2':
      light(R,G,B,255,0,0);  // Red
      break;

    case '3':
      light(R,G,B,0,255,0);  // Green
      break;
     
    case '4':
      light(R,G,B,0,0,255);  // Blue
      break;
    
    case '5':
      light(R,G,B,0,255,255);  // Cyan
      break;
      
    case '6':
      light(R,G,B,255,255,0);  // Yellow
      break;
      
    case '7':
      light(R,G,B,255,0,255);  // Megenta
      break;
      
  }
}


void light(int R,int G,int B,int r,int g,int b){
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  
    if(r==0){
      digitalWrite(R,LOW);
    }
    else{
      digitalWrite(R,HIGH);
    }
    if(g==0){
      digitalWrite(G,LOW);
    }
    else{
      digitalWrite(G,HIGH);
    }
    if(b==0){
      digitalWrite(B,LOW);
    }
    else{
      digitalWrite(B,HIGH);
    }
    
  }

