#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2 // 告訴 OneWire library DQ 接在哪個pin
OneWire onewire(ONE_WIRE_BUS); // 建立 OneWire 物件
DallasTemperature DS18B20(&onewire); // 建立 DS18B20 物件
void setup() {
 DS18B20.begin();
}

void loop() {
 float temperature; // 因溫度讀值帶小數，故用 float
 DS18B20.requestTemperatures(); // 下指令開始轉換成溫度讀值
 temperature = DS18B20.getTempCByIndex(0);
 delay(500);
}
