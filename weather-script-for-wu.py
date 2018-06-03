from sense_hat import SenseHat
import time
import sys
import serial
import datetime
import os
from urllib import urlencode
import urllib2
sense = SenseHat()
MEASURMENT_INTERVAL = 2

WEATHER_UPLOAD = True

WU_URL = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

SINGLE_HASH = '#'

HASHES = '####################################'
SLASH_N = '\n'


def main():

        global last_temp

        last_minute = datetime.datetime.now().minute

        last_minute -= 1
        if last_minute == 0: 
                last_minute = 59
        while 1:

                current_second = datetime.datetime.now().second
                if (current_second == 0) or ((current_second % 5) == 0):
                        serialMsg = serial.Serial("/dev/ttyACM0", 9600, timeout = 1)
                        rawMsg = serialMsg.readline()
                        message = (rawMsg.decode().strip())
                        calc_temp = message
                        print(calc_temp)
                        temp_f = calc_temp 
                        humidity = round(sense.get_humidity(), 0)
                        pressure = round(sense.get_pressure() * 0.0295300, 1)
                        print("Temp: %sF, Pressure: %s inHg, Humidity: %s%%" % (temp_f, pressure, humidity))
                        current_minute = datetime.datetime.now().minute
                        if current_minute:
                                last_minute = current_minute
                                if (current_minute == 0) or ((current_minute % MEASURMENT_INTERVAL) == 0):
                                        now = datetime.datetime.now()
                                        print("\n%d minute mark (%d @ %s)" % (MEASURMENT_INTERVAL, current_minute, str(now)))

                                        if WEATHER_UPLOAD:
                                                print("Uploading data to Weather Underground")

                                                weather_data = {
                                                        "action": "updateraw",
                                                        "ID": wu_station_id,
                                                        "PASSWORD": wu_station_key,
                                                        "dateutc": "now",
                                                        "tempf": str(temp_f),
                                                        "humidity": str(humidity),
                                                        "baromin": str(pressure),
                                                }
                                                try:
                                                        upload_url = WU_URL + "?" + urlencode(weather_data)
                                                        response = urllib2.urlopen(upload_url)
                                                        html = response.read()
                                                        print("Server response:", html)
                                                        response.close()
                                                except:
                                                        print("Exception:", sys.exc_info()[0], SLASH_N)
                                        else:
                                                print("Skipping Weather Underground upload")
                time.sleep(1)
        print("Leaving main()")

print(SLASH_N + HASHES)
print(SINGLE_HASH, "Pi Weather Station                  ", SINGLE_HASH)
print(HASHES)

if (MEASURMENT_INTERVAL is None) or (MEASURMENT_INTERVAL > 60):
        print("The application's 'MEASURMENT_INTERVAL' cannot be empty or greater than 60")
        sys.exit(1)

print("\nIntalising Weather Underground configuration")
wu_station_id = "IDROITWI14"
wu_station_key = "tbrmknbc"
if (wu_station_id is None) or (wu_station_key is None):
        print("Missingvalues from the Weather Underground config")
        sys.exit(1)

print("Sucsessfully read Weather Underground config")
print("Station ID:", wu_station_id)



try:
        main()
except KeyboardInterrupt:
        print("\nExiting application\n")
        sys.exit(0)
                
                        

