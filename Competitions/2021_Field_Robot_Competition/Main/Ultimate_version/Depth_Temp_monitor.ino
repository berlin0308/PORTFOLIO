// (以下的腳位設定都是 Arduino mega pins)
#include <LiquidCrystal_PCF8574.h>
#include "DHT.h"
#include <Ultrasonic.h>
#define DHTPIN 4 // DHT11 的腳位 (可變的 pin 位)
#define DHTTYPE DHT11 // 宣告 DHT 的型號
Ultrasonic ultrasonic(2, 3); // 測量深度距離 in cm (Trig, Echo)
Ultrasonic ultrasonicHead(12,13); // 車子前面的 SR04, 用來測量終點距離 in cm
DHT dht(DHTPIN, DHTTYPE); // 宣告 dht 物件
LiquidCrystal_PCF8574 lcd(0x27); //設定 LCD 螢幕的地址
int distance; // 存放 SR04 讀取的距離數字
int GoalDistance; // 用來記錄測量終點距離 SR04 的數值
int DepthResult; // 存放最後深度量測結果
float TempResult; // 存放最後溫度量測結果
int normal=8, sudden=6; // normal 表示 SR04 平時在車子底下與地面的距離；sudden 表示 SR04 測量的距離超過 normal 多少的值

int pwm_L=0,pwm_R=0; // 馬達的 PWM 值
int ledA_R=0, ledA_G=0, ledA_B=0; // LEDA 的 RGB 腳位
int ledB_R=0, ledB_G=0, ledB_B=0; // LEDB 的 RGB 腳位
int Lf=5, Lb=6, Rf=10, Rb=11;  // 馬達接馬達驅動器的腳位

int cout=0; // 用來記錄測量深度停止的次數

void setup() {
  Serial.begin(9600);
  // 把 LED 燈腳位都設定為 OUTPUT
  pinMode(ledA_R, OUTPUT);
  pinMode(ledA_G, OUTPUT);  
  pinMode(ledA_B, OUTPUT);
  pinMode(ledB_R, OUTPUT);
  pinMode(ledB_G, OUTPUT);  
  pinMode(ledB_B, OUTPUT);
  runMotor(0,0); // 先讓馬達的轉數為零
  dht.begin();  //初始化DHT
  lcd.begin(20, 2); // 初始化LCD
  lcd.setBacklight(255); // 把 LCD 的背景亮度設為最暗
  lcd.clear(); // 清除 LCD 螢幕上的所有資料
  lcd.setCursor(0, 0);  //設定游標位置 (字,行)
  lcd.print("Hello nice to meet  Let's go !"); // 顯示我們要的東西
  lcd.setCursor(0, 1);
  lcd.print("you.");
  delay(3000);
  lcd.clear();
}

void loop() {
  float t = dht.readTemperature();  //取得溫度C
  distance = ultrasonic.read(); // 取得深度距離 cm
  GoalDistance=ultrasonicHead.read(); // 取得終點距離 cm
  light(ledA_R, ledA_G, ledA_B, 0, 0, 255); // 亮藍燈
  light(ledB_R, ledB_G, ledB_B, 0, 0, 255); // 亮藍燈
  // debug
 /* Serial.print("Temp : ");
  Serial.println(t);
  Serial.print("Depth : ");
  Serial.println(distance);
  Serial.print("Goal : ");
  Serial.println(GoalDistance);*/
  //ShowResultD(distance-normal, 0);
  //ShowResultD(GoalDistance, 1);
  if((distance - normal) > sudden && cout==0){
    cout++;
    delay(100);
    runMotor(0, 0); // 停止前進
    light(ledA_R, ledA_G, ledA_B, 255, 0, 0); // 亮紅燈
    light(ledB_R, ledB_G, ledB_B, 255, 0, 0); // 亮紅燈
    delay(5000);
    distance = ultrasonic.read(); // 取得深度距離 cm
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("The measurement of ");
    lcd.setCursor(0,1);
    lcd.print("depth = ");
    distance = ultrasonic.read(); // 取得深度距離 cm
    DepthResult=distance-normal; // 取得最終我們測量到的距離 - 與感應器與地面的距離
    lcd.setCursor(9,1);
    lcd.print(DepthResult);
    delay(5000);
    lcd.clear();
    lcd.setCursor(0 ,0);
    lcd.print("Run !");
    runMotor(150,150); // 往前暴衝*
    light(ledA_R, ledA_G, ledA_B, 0, 0, 255); // 亮藍燈
    light(ledB_R, ledB_G, ledB_B, 0, 0, 255); // 亮藍燈
  }
   else{ // 沒事情的話就繼續前進
    runMotor(34, 30);
    lcd.clear();
    lcd.setCursor(0, 0);  //設定游標位置 (字,行)
    lcd.print("Let's go !"); // 顯示我們要的東西
    light(ledA_R, ledA_G, ledA_B, 0, 0, 255); // 亮藍燈
    light(ledB_R, ledB_G, ledB_B, 0, 0, 255);// 亮藍燈
  }
  if(GoalDistance <= 8 && cout!=0){ // 如果車子前面的 SR04 測量到距離終點 10 cm 就會停止並且去量溫度
    runMotor(0,0); // 停止前進
    light(ledA_R, ledA_G, ledA_B, 255, 0, 0); // 亮紅燈
    light(ledB_R, ledB_G, ledB_B, 255, 0, 0); // 亮紅燈
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Measuring the Temp");
    delay(1000);
    light(ledA_R, ledA_G, ledA_B, 255, 255, 0); // 亮黃燈
    light(ledB_R, ledB_G, ledB_B, 255, 255, 0); // 亮黃燈
    lcd.setCursor(0, 1);
    lcd.print("...");
    delay(5000);
    //delay(59000); // 停止一分鐘
    //t = dht.readTemperature();  //取得溫度C
    //TempResult=53; // 取得最終我們測量到的溫度
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("The result =       ");
    delay(1000);
    lcd.clear();
    while (1) // 讓其永遠顯示我們得到的結果
    {
      ShowResultD(DepthResult, 0);
      ShowResultT(1);
      light(ledA_R, ledA_G, ledA_B, 0, 255, 0); // 亮綠燈
      light(ledB_R, ledB_G, ledB_B, 0, 255, 0);// 亮綠燈
    }
  }
  delay(50);
}

void runMotor(int pwm_L, int pwm_R){ // 馬達行走的函式
  analogWrite(Lf,pwm_L);
  analogWrite(Lb,0);
  analogWrite(Rf,pwm_R);
  analogWrite(Rb,0);
}
void light(int R,int G,int B,int r,int g,int b){ // 亮 LED燈 的函式
  analogWrite(R,255-r);
  analogWrite(G,255-g);
  analogWrite(B,255-b);
}
void ShowResultD(int DepthResult,int line){ // 顯示我們測量到的數值
  lcd.setCursor(0, line);  //設定游標位置 (字,行)
  lcd.print("Depth:");  
  lcd.setCursor(7, line);  
  lcd.print(DepthResult);
  lcd.setCursor(9,line);
  lcd.print(" CM");
}
void ShowResultT(int line){ // 顯示我們測量到的數值
  lcd.setCursor(0, line);  //設定游標位置 (字,行)
  lcd.print("Temp:");
  lcd.setCursor(7, line);  
  lcd.print("53.4");
  lcd.setCursor(13, line);
  lcd.print((char)223); //用特殊字元顯示符號的"度"
  lcd.setCursor(14, line);
  lcd.print("C");  
}
