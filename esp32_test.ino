#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define LED_PIN 2

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

//inicjalizacja OLED i diody
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 allocation failed");
    for(;;);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("ESP32 WiFi Scanner");
  display.display();

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
}
//sprawdzanie typu zabezpieczen

String encryptionType(wifi_auth_mode_t encryptionType) {
  switch (encryptionType) {
    case WIFI_AUTH_OPEN: return "OPEN";
    case WIFI_AUTH_WEP: return "WEP";
    case WIFI_AUTH_WPA_PSK: return "WPA-PSK";
    case WIFI_AUTH_WPA2_PSK: return "WPA2-PSK";
    case WIFI_AUTH_WPA_WPA2_PSK: return "WPA/WPA2";
    case WIFI_AUTH_WPA2_ENTERPRISE: return "WPA2-ENT";
    case WIFI_AUTH_WPA3_PSK: return "WPA3-PSK";
    case WIFI_AUTH_WPA2_WPA3_PSK: return "WPA2/WPA3";
    default: return "UNKNOWN";
  }
}

//glowna funkcja
void loop() {
  int n = WiFi.scanNetworks();
  display.clearDisplay();

  digitalWrite(LED_PIN, HIGH);
  unsigned long start = millis();

  //wyswietlanie danych
  if(n == 0) {
    display.setCursor(0,0);
    display.println("No networks found");
    Serial.println("No networks found");
  } else {
    for(int i = 0; i < n && i < 8; i++) {
      String line = WiFi.SSID(i) + " : " + String(WiFi.RSSI(i)) + "dBm";

      display.setCursor(0, i*8);
      display.println(line);

      Serial.print(WiFi.SSID(i));
      Serial.print(" : ");
      Serial.print(WiFi.RSSI(i));
      Serial.print(" : ");
      Serial.print(WiFi.channel(i));
      Serial.print(" : ");
      Serial.println(encryptionType(WiFi.encryptionType(i)));
    }
  }

  display.display();

  //miganie diody
  while (millis() - start < 3000) {
    delay(50);
  }
  digitalWrite(LED_PIN, LOW);  

  delay(3000);
}
