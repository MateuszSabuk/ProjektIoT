import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library


class Controller:
    def __init__(self, pin, bouncetime, reading_start_function, reading_end_function):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            pin,
            GPIO.RISING,
            callback=reading_start_function,
            bouncetime=bouncetime * 1000,
        )
        GPIO.add_event_detect(
            pin,
            GPIO.FALLING,
            callback=reading_end_function,
            bouncetime=bouncetime * 1000,
        )

    def get_reading(self):
        return GPIO.input(self.pin)
