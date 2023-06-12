import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library


class TiltController:
    def __init__(self, tilt_pin):
        self.tilt_pin = tilt_pin
        GPIO.setup(tilt_pin, GPIO.IN)  # Set pin as GPIO in
        self.temp = 0

    def get_reading(self):
        self.temp = GPIO.input(self.tilt_pin)
        time.sleep(0.01)
        return GPIO.input(self.tilt_pin) != self.temp
