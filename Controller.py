import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library


class Controller:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)  # Set pin as GPIO in

    def get_reading(self):
        return GPIO.input(self.pin)
