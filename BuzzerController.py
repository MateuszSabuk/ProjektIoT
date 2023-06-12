import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library
import math


class BuzzerController:
    def __init__(self, buzzer_pin):
        self.buzzer_pin = buzzer_pin
        GPIO.setup(buzzer_pin, GPIO.OUT)  # Set pin as GPIO in
        self.p = GPIO.PWM(buzzer_pin, 1)
        self.p.start(0)

    def check_volume(self):
        return GPIO.input(self.mic_pin)

    def tone1(self):
        self.p.start(50)
        for x in range(0, 361):  # Frequency of the tone along the sine wave
            sinVal = math.sin(x * (math.pi / 180.0))  # Calculate the sine value
            toneVal = (
                2000 + sinVal * 500
            )  # Add to the resonant frequency with a Weighted
            self.p.ChangeFrequency(toneVal)  # Output PWM
            time.sleep(0.001)

    def tone2(self):
        self.p.start(50)
        for x in range(0, 361):
            sinVal = math.sin(x * (math.pi / 180.0))
            toneVal = 1000 + sinVal * 500
            self.p.ChangeFrequency(toneVal)
            time.sleep(0.001)

    def tone3(self):
        self.p.start(50)
        for x in range(0, 361):
            sinVal = math.sin(x * (math.pi / 180.0))
            toneVal = 3000 + sinVal * 800
            self.p.ChangeFrequency(toneVal)
            time.sleep(0.001)

    def stopTone(self):
        self.p.stop()
