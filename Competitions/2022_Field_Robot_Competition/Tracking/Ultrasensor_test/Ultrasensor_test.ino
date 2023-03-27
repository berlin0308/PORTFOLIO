
#include <Ultrasonic.h>
int ultra_trig_pin[4] = {16,18,22,24};
int ultra_echo_pin[4] = {17,19,23,25};
const int a_b_boundary=10,b_c_boundary=30,c_d_boundary=60;
char Receiver, STAGE, STATE, pwmL[4], pwmR[4];
int PWM_L, PWM_R;
String commandStr;

Ultrasonic Ultra_A(ultra_trig_pin[0],ultra_echo_pin[0]);
Ultrasonic Ultra_B(ultra_trig_pin[1],ultra_echo_pin[1]);
Ultrasonic Ultra_C(ultra_trig_pin[2],ultra_echo_pin[2]);
Ultrasonic Ultra_D(ultra_trig_pin[3],ultra_echo_pin[3]);


void setup(){

    
    pinMode(16,OUTPUT);
    pinMode(18,OUTPUT);
    pinMode(22,OUTPUT);
    pinMode(24,OUTPUT);

    pinMode(17,INPUT);
    pinMode(19,INPUT);
    pinMode(23,INPUT);
    pinMode(25,INPUT);

    Serial.begin(9600);
}


void loop(){
    char A,B,C,D;
    int A_read=0, B_read=0, C_read=0, D_read=0;
    for(int i=0;i<20;i++){
        A_read += Ultra_A.read();
        B_read += Ultra_B.read();
        C_read += Ultra_C.read();
        D_read += Ultra_D.read();
    }
    
    // Serial.print("A:");
    // Serial.println(A_read/20);
    Serial.print("B:");
    Serial.println(B_read/20);
    // Serial.print("C:");
    // Serial.println(C_read/20);
    Serial.print("D:");
    Serial.println(D_read/20);
    
/* 
    if(A_read<a_b_boundary)
        A = 'a';
    else if(A_read<b_c_boundary)
        A = 'b';
    else if(A_read<c_d_boundary)
        A = 'c';
    else
        A = 'd';

    if(B_read<a_b_boundary)
        B = 'a';
    else if(B_read<b_c_boundary)
        B = 'b';
    else if(B_read<c_d_boundary)
        B = 'c';
    else
        B = 'd';

    if(C_read<a_b_boundary)
        C = 'a';
    else if(C_read<b_c_boundary)
        C = 'b';
    else if(C_read<c_d_boundary)
        C = 'c';
    else
        C = 'd';

    if(D_read<a_b_boundary)
        D = 'a';
    else if(D_read<b_c_boundary)
        D = 'b';
    else if(D_read<c_d_boundary)
        D = 'c';
    else
        D = 'd';

    String info = "P00001";
    info += A;
    info += B;
    info += C;
    info += D;
    info += 'e';
    Serial.println(info);  
 */
}

