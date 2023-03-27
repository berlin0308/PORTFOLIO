String cmd;
int pwm_L=0,pwm_R=0;
int ledA_R=3, ledA_G=5, ledA_B=6;
char pwmL[4],pwmR[4],sender,state,power,motion;
char ledA, ledB, ledC, ledD;
int Lf=9, Lb=10, Rf=11, Rb=13;

void setup() {
  pinMode(ledA_R, OUTPUT);
  pinMode(ledA_G, OUTPUT);
  pinMode(ledA_B, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  turnoffLED(ledA_R,ledA_G,ledA_B);
  if (Serial.available()) {
    Serial.println("serial available");
    // 讀取傳入的字串直到'e'結尾 不包括e
    cmd = Serial.readStringUntil('e');
    Serial.println(cmd); 

    sender = cmd[0];
    //Serial.println(sender);
    
    state = cmd[1];
    //Serial.println(state);
    
    power = cmd[2];
    //Serial.println(power);
 
    motion = cmd[3];
    //Serial.println(motion);
    
    if(sender=='0'){   //the signal is from python
      if(state=='1'){  //甲關
        Serial.println(cmd);
        ledA = cmd[10];
        ledB = cmd[11];
        ledC = cmd[12];
        ledD = cmd[13];
        
        igniteLED(ledA_R,ledA_G,ledA_B,ledA);
        
        if(power=='1'){  // power on, read pwm for motor
            pwmL[0] = cmd[4];
            pwmL[1] = cmd[5];
            pwmL[2] = cmd[6];
            pwmL[3] = '\0';
            pwm_L = atoi(pwmL);
            //Serial.println(pwm_L);
    
            pwmR[0] = cmd[7];
            pwmR[1] = cmd[8];
            pwmR[2] = cmd[9];
            pwmR[3] = '\0';
            pwm_R = atoi(pwmR);
            //Serial.println(pwm_R);
        }
        else{               // power off
           pwm_L = 0;
           pwm_R = 0;
        }

        runMotor(pwm_L,pwm_R);
        delay(100);
        turnoffLED(ledA_R,ledA_G,ledA_B);
      }
      
      
    }
    
  }
}

void igniteLED(int R,int G,int B,char choice){
  switch(choice){
    case '0':
      light(R,G,B,0,0,0);  // light off
      break;
      
    case '1':
      light(R,G,B,255,255,255);  // white
      break;
 
    case 'R':
      light(R,G,B,255,0,0);  // Red
      break;

    case 'G':
      light(R,G,B,0,255,0);  // Green
      break;
     
    case 'B':
      light(R,G,B,0,0,255);  // Blue
      break;
    
    case 'C':
      light(R,G,B,0,255,255);  // Cyan
      break;
      
    case 'Y':
      light(R,G,B,255,255,0);  // Yellow
      break;
      
    case 'M':
      light(R,G,B,255,0,255);  // Megenta
      break;
      
  }
}

void turnoffLED(int R,int G,int B){
  pinMode(R,INPUT);
  pinMode(G,INPUT);
  pinMode(B,INPUT);
}

void runMotor(int pwm_L, int pwm_R){
  analogWrite(Lf,pwm_L);
  analogWrite(Lb,0);
  analogWrite(Rf,pwm_R);
  analogWrite(Rb,0);
}

void light(int R,int G,int B,int r,int g,int b){
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  analogWrite(R,255-r);
  analogWrite(G,255-g);
  analogWrite(B,255-b);
}

 
 
