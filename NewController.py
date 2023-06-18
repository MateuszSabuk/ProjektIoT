import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library


class Controller:
    def __init__(self, pin, function):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=function)

    def get_reading(self):
        return GPIO.input(self.pin)
