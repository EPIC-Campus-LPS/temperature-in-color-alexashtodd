import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
from datetime import datetime

sensor = adafruit_dht.DHT11(board.D27) # Change the pin number to the data pin of your DHT11

print("time,celsius,fahrenheit")


def to_fahrenheit(c):
    # TODO: Assign f where f represents the Farienheit equivalent to the input Celcius c
    f = (c * 9 / 5) + 32
    return f    

def lights(red = bool, blue = bool):
    try:
        GPIO.cleanup()

        GPIO.setmode(GPIO.BCM)

        PIN_BLUE = 22
        PIN_RED = 6

        GPIO.setup(PIN_BLUE, GPIO.OUT)
        GPIO.setup(PIN_RED, GPIO.OUT)

        if(red == 1):
            GPIO.output(PIN_RED, GPIO.HIGH)
        else:
            GPIO.output(PIN_RED, GPIO.LOW)

        if(blue == 1):
            GPIO.output(PIN_BLUE, GPIO.HIGH)
        else:
            GPIO.output(PIN_BLUE, GPIO.LOW)
    except:
        GPIO.cleanup()
    # finally:
        # GPIO.cleanup()

def printToCSV(celsius, fahrenheit, current_time):
    with open("temperature.csv", "a") as file:
        file.write("{0},{1:0.1f},{2:0.1f}\n".format(current_time.strftime("%H:%M:%S"), celsius, fahrenheit))
    # TODO

while True:
    try:
        celsius = sensor.temperature # Get the temperature in Celcius from the sensor
        fahrenheit = to_fahrenheit(celsius)
        current_time = datetime.now()

        printToCSV(celsius, fahrenheit, current_time)
        print("{0},{1:0.1f},{2:0.1f}".format(current_time.strftime("%H:%M:%S"), celsius, fahrenheit))
        
        if(fahrenheit > 72):
            lights(1,0)
        else:
            lights(0,1)

        time.sleep(3.0)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except KeyboardInterrupt:
        GPIO.cleanup()
    except Exception as error:
        sensor.exit()
        raise error   

GPIO.cleanup()
