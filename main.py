import time
import threading
import RPi.GPIO as GPIO
from LedController import LedController, LedColors as colors
from TemperatureController import TemperatureController
from TiltController import TiltController
from Controller import Controller
from BuzzerController import BuzzerController
from flask import Flask, jsonify, render_template
from keypad import keypad_start

# Pins setup
rgb_pins = (2, 3, 14)
pir_pin = 22
tilt_pin = 17
mic_pin = 5
flame_pin = 27
# timeouts for each sensor
times = {"temperature": 20, "pir": 2, "tilt": 0.1, "mic": 0.1, "flame": 1}


# Output setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_controller = LedController(rgb_pins)
buzz = BuzzerController(
    26,
)


# values and timestamps
values = {"temperature": [], "pir": [], "tilt": [], "mic": [], "flame": []}

pir_rising_time = None
mic_rising_time = None
flame_rising_time = None


alarm_armed = False
alarm_muted = True


def reset_leds():
    led_controller.stop_roll = True
    if alarm_armed:
        if alarm_muted:
            led_controller.blink(color=colors.BLUE, light_time=1, dark_time=4)
        else:
            led_controller.blink(color=colors.GREEN, light_time=1, dark_time=4)
    else:
        led_controller.off_all()


def check_alarm():
    if alarm_armed:
        # TODO add a short buzz
        led_controller.roll_leds([colors.BLUE, colors.GREEN], roll_time=0.2)
        # wait for 20 seconds with a buzz every 2 seconds
        for i in range(10):
            # TODO buzz
            time.sleep(2)
        led_controller.stop_roll = True
        if alarm_armed:
            start_alarm()


def start_alarm():
    led_controller.blink(color=colors.RED, light_time=1, dark_time=1, roll_time=0.3)
    # start the buzzer


def stop_alarm():
    print("Alarm stopped")
    alarm_armed = False
    # TODO stop buzz
    reset_leds()


def arm_alarm():
    print(" Alarm armed!")
    alarm_armed = True
    reset_leds()


def reading_start_function(pin):
    if pin == pir_pin:
        pir_rising_time = time.time()
        check_alarm()

    elif pin == mic_pin:
        mic_rising_time = time.time()
        check_alarm()

    elif pin == flame_pin:
        flame_rising_time = time.time()
        if alarm_muted:
            return
        led_controller.on_single(colors.BLUE)
        led_controller.on(colors.RED)
        # Check the flames 10 times in 10 seconds
        flames = True
        for i in range(10):
            if GPIO.input(flame_pin):
                pass  # TODO buzz
            else:
                flames = False
                break
            time.sleep(1)
        if flames:
            start_alarm()


def reading_end_function(pin):
    if pin == pir_pin:
        if pir_rising_time is not None:
            values["pir"].append([pir_rising_time, time.time()])
            pir_rising_time = None

    elif pin == mic_pin:
        if mic_rising_time is not None:
            values["mic"].append([mic_rising_time, time.time()])
            mic_rising_time = None

    elif pin == flame_pin:
        if flame_rising_time is not None:
            values["flame"].append([flame_rising_time, time.time()])
            flame_rising_time = None


controllers = {
    "temperature": TemperatureController(),  # pin 4 in /boot/config.txt
    "pir": Controller(
        pir_pin, times["pir"], reading_start_function, reading_end_function
    ),
    "tilt": TiltController(tilt_pin),
    "mic": Controller(
        mic_pin, times["mic"], reading_start_function, reading_end_function
    ),
    "flame": Controller(
        flame_pin, times["flame"], reading_start_function, reading_end_function
    ),
}


def update_tilt():
    global values
    global controllers
    global times
    while True:
        if controllers["tilt"].get_reading():
            values["tilt"].append(time.time())
            check_alarm()
        time.sleep(times["tilt"])


def update_temperature():
    global values
    global controllers
    global times
    while True:
        values["temperature"].append(
            (controllers["temperature"].get_reading(), time.time())
        )
        time.sleep(times["temperature"])


# SERVER
app = Flask(__name__)


@app.route("/")
def get_values():
    return render_template("graph.html")


@app.route("/data")
def get_data():
    return jsonify(values)


def test():
    while True:
        print(values)
        time.sleep(5)


def main():
    # Dodanie threadów czujników
    th_temp = threading.Thread(target=update_temperature)
    th_temp.daemon = True
    th_temp.start()
    th_tilt = threading.Thread(target=update_tilt)
    th_tilt.daemon = True
    th_tilt.start()

    keypad_start(stop_alarm=stop_alarm, arm_alarm=arm_alarm)
    # th = threading.Thread(target=test)
    # th.daemon = True
    # th.start()

    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
