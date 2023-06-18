import time
import threading
import RPi.GPIO as GPIO
from LedController import LedController, LedColors as colors
from TemperatureController import TemperatureController
from TiltController import TiltController
from Controller import Controller
from BuzzerController import BuzzerController
from flask import Flask, jsonify, render_template

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
buzz = BuzzerController(26)


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
            led_controller.on_single(colors.GREEN)
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


def stop_alarm():  # TODO Fuction calling this function
    # TODO stop alarm
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

    # th = threading.Thread(target=test)
    # th.daemon = True
    # th.start()

    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
# example json
# {"flame":[1686578313.5134768,1686578314.5145347,1686578315.515693,1686578316.516824,1686578317.5178974,1686578318.5189867,1686578319.5200775,1686578320.5211418,1686578321.5222034,1686578322.5232773,1686578323.5243468,1686578324.5254297,1686578325.5265098,1686578326.5276196,1686578327.5287714,1686578328.5290003,1686578329.5300684,1686578330.5311506,1686578331.5322301,1686578332.5333078,1686578333.533935,1686578334.5350168,1686578335.5357056,1686578336.5368001,1686578337.5378733,1686578338.5383952,1686578339.539469,1686578340.5405416,1686578341.5415967,1686578342.542665,1686578343.5437596,1686578344.5448596,1686578345.5459383,1686578346.54703,1686578347.5480797,1686578348.5492647,1686578349.5503502,1686578350.5514286,1686578351.552551,1686578352.5536392,1686578353.5547087,1686578354.5557477,1686578355.5568225,1686578356.5579062,1686578357.5589676,1686578358.560031,1686578359.5611227,1686578360.5621717,1686578361.563236,1686578362.5643082,1686578363.565379,1686578364.5664415,1686578365.5675037,1686578366.5685658,1686578367.569629,1686578368.5706828,1686578369.571737,1686578370.5728009,1686578371.5738626,1686578372.5749211,1686578373.5757036,1686578374.5768502,1686578375.5782468,1686578376.5793343,1686578377.5803864,1686578378.5814707,1686578379.5825503,1686578380.5836647,1686578381.5848982,1686578382.585776,1686578383.5868855,1686578384.587962,1686578385.5890346,1686578386.5901072,1686578387.5911767,1686578388.5922492,1686578389.5933135,1686578390.5943773,1686578391.595432,1686578392.5964868,1686578393.5992734,1686578394.6003346,1686578395.6014113,1686578396.6024535,1686578397.6035085],"mic":[1686578331.244646,1686578331.645355,1686578331.7455375,1686578331.8457022,1686578331.945879,1686578332.0460706,1686578332.1462572,1686578332.3466113,1686578332.4467936,1686578332.546974,1686578332.64715,1686578332.8475046,1686578332.947671,1686578333.047827,1686578333.148009,1686578333.2481954,1686578340.6606588,1686578340.7608345,1686578340.8610063,1686578340.9611833,1686578341.061358,1686578341.1615345,1686578341.2617273,1686578341.9631977,1686578343.7664423],"pir":[1686578331.5257013,1686578391.579631],"temperature":[[24.812,1686578314.407371],[27.375,1686578335.2872138],[27.562,1686578356.167047],[27.625,1686578377.0475214],[27.625,1686578397.9271762]],"tilt":[1686578334.704918,1686578334.8152244,1686578335.5873706,1686578335.807975,1686578337.2423525,1686578340.9915617,1686578389.08215,1686578390.2949982]}
