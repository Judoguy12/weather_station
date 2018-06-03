from sense_hat import SenseHat
import time
import sys
from ISStreamer.Streamer import Streamer
import serial

serialMsg = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)
sense = SenseHat()
logger = Streamer(bucket_name = "Weather Station Data v2", access_key = "DZ8aQ2EQncdq7DznX7qIySt0BJGWrZNO")
term = "*C"

sense.clear()
try:
        while True:
                rawMsg = serialMsg.readline()
                message = (rawMsg.decode().strip())
                if term in message:
                        logger.log("Temperature:", message)
                else:
                        logger.log("Light Sensor (Higher = more light, Max 1023) :", message)
                humidity = sense.get_humidity()
                humidity = round(humidity, 1)
                logger.log("Humidity %:",humidity)
                
                pressure = sense.get_pressure()
                pressure = round(pressure, 2)
                logger.log("Pressure (millibars):",pressure)
                time.sleep(1)
except KeyboardInterrupt:
        pass
sense.clear()
