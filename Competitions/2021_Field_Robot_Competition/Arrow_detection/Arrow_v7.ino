int LED = 13;
String str;
int R =3;
int G =5;
int B =6;

void setup() {
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  light(0,255,0);
  //Serial.println("LED is ON");
  if (Serial.available()) {
    // 讀取傳入的字串直到'e'結尾 不包括e
    str = Serial.readStringUntil('e');
    //Serial.println(str); // 回應訊息給電腦
    
    flash("white",100);
    flash("party",300);
    flash("white",100);
    
    if(str=="R"){
      delay(500);
      flash("pink",3000);
    }
    if(str=="L"){
      delay(500);
      flash("aquablue",3000);
    }
    
 
  }
}

void light(int r,int g,int b){
  analogWrite(R,255-r);
  analogWrite(G,255-g);
  analogWrite(B,255-b);
}

void flash(String color,int t){
  if(color=="white"){
    light(255,255,255);
    delay(t);
    light(0,0,0);
    delay(t);
  }
  if(color=="red"){
    light(2,0,0);
    delay(t);
    light(0,0,0);
    delay(t);
  }
  if(color=="green"){
    light(0,255,0);
    delay(t);
    light(0,0,0);
    delay(t);
  }
  if(color=="blue"){
    light(0,0,255);
    delay(t);
    light(0,0,0);
    delay(t);
  }
  if(color=="pink"){
    light(220,100,100);
    delay(t);
    light(0,0,0);
    delay(t);
  }
  if(color=="aquablue"){
    light(95,230,210);
    delay(t);
    light(0,0,0);
    delay(t);
  }
  if(color=="party"){
    light(255,69,0);
    delay(t);
    light(255,215,0);
    delay(t);
    light(127,255,0);
    delay(t);
    light(102,255,230);
    delay(t);
    light(13,51,255);
    delay(t);
    light(139,0,255);
    delay(t);
  }
 
 
}

