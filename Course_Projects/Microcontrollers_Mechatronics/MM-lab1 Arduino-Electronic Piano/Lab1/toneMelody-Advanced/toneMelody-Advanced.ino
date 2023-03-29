#include "pitches.h"
int melody[] = {
NOTE_C4, NOTE_C4,NOTE_G4, NOTE_G4, NOTE_A4, NOTE_A4, NOTE_G4, 0, NOTE_F4, NOTE_F4,NOTE_E4,NOTE_E4,NOTE_D4,NOTE_D4, NOTE_C4,0};
// note durations: 4 = quarter note, 8 = eighth note, etc.
const int noteDuration=250;
void setup() {
for (int thisNote = 0; thisNote < 16; thisNote++) {

tone(8, melody[thisNote],noteDuration);
int pauseBetweenNotes = noteDuration * 1.30;
delay(pauseBetweenNotes);
noTone(8); 
}
}
void loop() { }
