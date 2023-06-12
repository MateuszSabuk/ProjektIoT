import RPi.GPIO as gpio
import time


class LedColors:
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    
    def get_list(self):
        return [self.RED, self.GREEN, self.BLUE]


class LedController:
    """Przyjmuje tuplet numerów pinów: (red, green, blue)"""

    def __init__(self, rgb_pins) -> None:
        red_pin, green_pin, blue_pin = rgb_pins
        self.colors = LedColors()
        self.leds = {
            self.colors.RED: red_pin,
            self.colors.GREEN: green_pin,
            self.colors.BLUE: blue_pin,
        }
        for pin in self.leds.values():
            gpio.setup(pin, gpio.OUT)

    def on_single(self, led_color):
        """Włącza pojedynczy kolor, wyłącza pozostałe"""
        for color, led in self.leds.items():
            if color == led_color:
                self.on(color)
            else:
                self.off(color)

    def on(self, led_color):
        """Włącza podany kolor"""
        gpio.output(self.leds[led_color], gpio.HIGH)

    def off(self, led_color):
        """Wyłącza podany kolor"""
        gpio.output(self.leds[led_color], gpio.LOW)

    def roll_leds(self, break_pin, roll_time=1):
        """
        Zmienia kolory leda, co << roll_time >> \\
        Sygnał na pinie << break_pin >> przerywa pętlę
        """
        gpio.setup(break_pin, gpio.IN)
        breaked = False
        # TODO Opcjonalne breaked jako przerwanie
        while not breaked:
            for color in self.colors.get_list():
                self.on_single(color)
                breaked = gpio.input(break_pin)
                if breaked:
                    break
                time.sleep(roll_time)
