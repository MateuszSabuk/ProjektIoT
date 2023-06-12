import time
import threading
import RPi.GPIO as gpio
from LedController import LedController, LedColors as colors
from TemperatureController import TemperatureController
from TiltController import TiltController
from Controller import Controller
from BuzzerController import BuzzerController
from flask import Flask, jsonify


rgb_pins = (2, 3, 14)
pir_pin = 22
tilt_pin = 17
mic_pin = 5
flame_pin = 27


gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
led_controller = LedController(rgb_pins)
buzz = BuzzerController(26)

controllers = {}
controllers["temperature"] = TemperatureController()  # pin 4 in /boot/config.txt
controllers["pir"] = Controller(pir_pin)
controllers["tilt"] = TiltController(tilt_pin)
controllers["mic"] = Controller(mic_pin)
controllers["flame"] = Controller(flame_pin)

times = {}
times["temperature"] = 20
times["pir"] = 2
times["tilt"] = 0.1
times["mic"] = 0.1
times["flame"] = 1

values = {"temperature": [], "pir": [], "tilt": [], "mic": [], "flame": []}


def update_value(sensor: str):
    global values
    global controllers
    global times
    if controllers[sensor].get_reading():
        values[sensor].append(time.time())
    time.sleep(times[sensor])


def raiseAlarm():
    print("Wykryto alarm!")
    led_controller.on_single(colors.RED)
    time.sleep(5)
    pass


def dropAlarm():
    led_controller.on_single(colors.BLUE)
    pass


def configureAlarm():
    pass


# SERVER
app = Flask(__name__)


@app.route("/")
def get_values():
    return jsonify(values)


def main():
    # Dodanie threadów czujników
    global values
    for key in values.keys():
        th = threading.Thread(
            target=update_value,
            args=[key],
        )
        th.daemon = True
        th.start()

    app.run(host="0.0.0.0", port=8080)

    # while True:
    #     if tilt.get_reading():
    #         buzz.tone2()
    #     else:
    #         buzz.stopTone()
    #     print(temperature.get_reading())
    #     if (temperature.get_reading() > 30) and (flame.get_reading() == True):
    #         print("Wykryto pozar!")
    #         raiseAlarm()

    #     if pir.get_reading():
    #         print("Wykryto ruch w strefie chronionej!")
    #         raiseAlarm()

    #     if mic.get_reading():
    #         print("Wykryto glosny dzwiek w strefie chrononej!")
    #         raiseAlarm()

    #     if tilt.get_reading():
    #         print("Wykryto wstrzas w strefie ochronnej")
    #         raiseAlarm()

    #     else:
    #         print("System w stanie gotowosci")
    #         dropAlarm()


if __name__ == "__main__":
    main()
