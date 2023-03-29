#include "pitches.h"

int melody[] = {
NOTE_C4, NOTE_D4,NOTE_E4, NOTE_F4, NOTE_G4, NOTE_A4, NOTE_B4};

void setup() {
   pinMode(3,OUTPUT);
   for(int i=14;i<=19;i++)
     pinMode(i,INPUT);
   pinMode(2,INPUT);
}

void loop() {
  
  for(int t=14;t<=19;t++)
  {
  if(digitalRead(t)==HIGH)
  {
    tone(3, melody[t-14], 4);
  }
  if(digitalRead(2)==HIGH)
  {
    tone(3, melody[6], 4);
  }
  }
}
