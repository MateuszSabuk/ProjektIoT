## Używane moduły

- Input

  - Czujnik dźwięku
  - Czujnik ruchu (PIR)
    CzujkaPIR.py
  - Czujnik temperatury
    DS18B20 TEMPERATURE SENSOR
    https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
    Ustawienie config.txt
    temperatureControl.py
  - Czujnik wibracji
  - Czujnik płomieni

- Output
  - Dioda RGB LED
  - Buzzer

## Używane piny

rgb_pins = (2, 3, 14)
pir_pin = 22
tilt_pin = 17
mic_pin = 5
flame_pin = 27
buzzer_pin = 26

temperatura = 4

## Pomocne linki

- [Multithreading post](https://forums.raspberrypi.com/viewtopic.php?t=338134)
- [Botland strona](https://botland.com.pl/zestawy-czujnikow/12795-zestaw-czujnikow-i-modulow-box-65-elementow-5904422377205.html)
