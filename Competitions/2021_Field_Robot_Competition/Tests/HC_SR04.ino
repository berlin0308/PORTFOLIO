#include <Ultrasonic.h>
#include <LiquidCrystal_PCF8574.h> // 這是 LCD 顯示螢幕的H檔
LiquidCrystal_PCF8574 lcd(0x27); // 設定 LCD 螢幕的位址
Ultrasonic ultrasonic(2, 3); // 設定超聲波的 pin 角 (Trig 12, Echo 13)
int distance; // 宣告來存放讀取到的訊息
void setup() {
  Serial.begin(9600);
  // 以下都是關於 LCD 的設定
  lcd.begin(16, 2); // 初始化LCD
  lcd.setBacklight(255);
  lcd.clear();
  lcd.setCursor(0, 0);  //設定游標位置 (字,行)
  lcd.print("This is depth sensor");
  delay(2000);
}

void loop() {
  // 定義 distance 用來讀取超聲波的數值，函數裡面不放參數數值單位就是公分
  distance = ultrasonic.read(); // 不加參數就是 CM, INC 英吋
  Serial.print("Distance in CM: ");
  Serial.println(distance);
  // 以下都是 LCD 顯示時的設定
  lcd.clear();
  lcd.setCursor(0, 0);  //設定游標位置 (字,行)
  lcd.print("Depth:");
  lcd.setCursor(7, 0);  
  lcd.print(distance);
  lcd.setCursor(9,0);
  lcd.print(" CM");
  delay(500);
}
