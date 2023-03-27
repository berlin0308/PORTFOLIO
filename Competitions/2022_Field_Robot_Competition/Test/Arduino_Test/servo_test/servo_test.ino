#include <Servo.h>

const int Armmotor_claw = 8; // the pin of arm motor1
Servo Armservo_claw;

void setup() {
    Serial.begin(9600);
    Armservo_claw.attach(Armmotor_claw); // need PWM pin
    Armservo_claw.write(0);
    delay(500);
}

void loop() {
    Serial.println("Let's GO!");

    runServoMotor(Armservo_claw,0,20,2000);
    Serial.println("Completed!");     
}

void runServoMotor(Servo Armservo,int init_pos,int fin_pos,int timeInterval){

    if(fin_pos>=init_pos){
        int cur_pos = init_pos;
        while(cur_pos<init_pos){
            Armservo.write(cur_pos);
            cur_pos += ((fin_pos-init_pos)/20);
            delay(timeInterval/20);
        }
        Armservo.write(fin_pos);
    }
    else if(fin_pos<=init_pos){
        int cur_pos = init_pos;
        while(cur_pos<init_pos){
            Armservo.write(cur_pos);
            cur_pos -= ((init_pos-fin_pos)/20);
            delay(timeInterval/20);
        }
        Armservo.write(fin_pos);
    }
}
