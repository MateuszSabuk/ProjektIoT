import RPi.GPIO as gpio
import time
import threading


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
        self.stop_roll = True
        self.colors = LedColors()
        self.leds = {
            self.colors.RED: red_pin,
            self.colors.GREEN: green_pin,
            self.colors.BLUE: blue_pin,
        }
        # self.currently_on = {
        #     self.colors.RED: False,
        #     self.colors.GREEN: False,
        #     self.colors.BLUE: False,
        # }
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

    def off_all(self):
        """Wyłącza diodę"""
        for color, led in self.leds.items():
            self.off(color)

    def roll_leds(self, chosen_colors=None, roll_time=1):
        """
        chosen_colors domyślnie jest listą wszystkich kolorów
        Zmienia kolory leda, co << roll_time >>
        """

        def roll(colors_list):
            self.stop_roll = False
            if colors_list == None:
                colors_list = self.colors.get_list()
            while not self.stop_roll:
                for color in colors_list:
                    if self.stop_roll:
                        break
                    if color != None:
                        self.on_single(color)
                    else:
                        self.off_all()
                    time.sleep(roll_time)

        th = threading.Thread(daemon=True, target=roll, args=[chosen_colors])
        th.start()

    def blink(self, color, light_time: int = 1, dark_time: int = 1):
        """Mruga"""
        light = [color for x in range(light_time)]
        dark = [None for x in range(dark_time)]
        arr = light + dark
        self.roll_leds(arr)
