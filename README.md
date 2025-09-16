# wifi-scanner

Projekt dotyczy skanera wifi. Układ jest oparty o esp32. 

## Instrukcja obsługi

Układ należy podpiąć do komputera przez USB. Następnie urządzenie zacznie automatycznie pracę. Aby uruchomić program należy uruchomić za pomocą python3 plik esp32_wifi_test.py. Program automatycznie wykryje układ i wyświetli dane o pobliskich sieciach tzn. ssid, rssi, kanał, szyfrowanie, odległość od nadajnika i moc sygnału. Układ widzi tylko sieci 2.4 GHz.

## Dane techniczne 

* kontroler esp32
* wyświetlacz OLED 128x64 I2C SSD1306
* Python w wersji 3.13.7
