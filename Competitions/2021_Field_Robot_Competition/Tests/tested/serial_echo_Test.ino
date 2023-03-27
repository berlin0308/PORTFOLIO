String str;

void setup() {
  Serial.begin(9600);
}

void loop() {
 
  if (Serial.available()) {
    
    // 讀取傳入的字串直到'e'結尾 不包括e
    str = Serial.readStringUntil('e');
    Serial.println(str); // 回應訊息給電腦
    
 
  }
}

