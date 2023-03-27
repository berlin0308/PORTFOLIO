#include <dht.h>
#define DHT11_PIN 2
dht DHT;
void setup() {
 Serial.begin(9600);
 Serial.println("Type,\tHumidity (%),\tTemperature (C)");
}

void loop() {
  Serial.print("DHT11, \t");
  int chk = DHT.read11(DHT11_PIN); // 讀取資料
  // 顯示資料
  Serial.print(DHT.humidity,1);
  Serial.print(",\t\t");
  Serial.println(DHT.temperature,1);
  delay(250);
}
