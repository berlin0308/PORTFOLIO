String str;
int R =2;
int G =3;
int B =4;

void turnRight(int t);
void turnLeft(int t);
void forward();
void stopp(int t);
void flash(String color,int t);

void setup() 
{
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT); //5,6 for motor A, left wheel
  pinMode(10, OUTPUT);
  pinMode(11 ,OUTPUT); //7,8 for motor B, right wheel
  
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  Serial.begin(9600);

  delay(10000);
}

void loop() 
{
  forward();
  if (Serial.available()) {
    // 讀取傳入的字串直到'e'結尾 不包括e
    str = Serial.readStringUntil('e');
    Serial.println(str);
    flash("white",100);
    flash("party",300);
    flash("white",100);
    
    if(str=="R"){
      stopp(2000);
      flash("green",500);
      turnRight(5000);
      stopp(2000);
    }
    if(str=="L"){
      stopp(2000);
      flash("blue",500);
      turnLeft(5000);
      stopp(2000);
    }
    
    delay(50);
  }
  delay(1000);
}

void turnRight(int t)
{
  analogWrite(5, 60);
  analogWrite(6, 0);
  analogWrite(10, 0);
  analogWrite(11, 60);
  delay(t);
}


void turnLeft(int t)
{
  analogWrite(5, 0);
  analogWrite(6, 60);
  analogWrite(10, 60);
  analogWrite(11, 0);
  delay(t);
}

void forward()
{
  analogWrite(5, 60);
  analogWrite(6, 0);
  analogWrite(10, 60);
  analogWrite(11, 0 );
}

void stopp(int t)
{
  analogWrite(5, 0);
  analogWrite(6, 0);
  analogWrite(10, 0);
  analogWrite(11, 0);
  delay(t);
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
    light(255,0,0);
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
 
 

