import i2clcd
import time
import random
import Adafruit_DHT
from threading import Thread
from datetime import datetime
import RPi.GPIO as gpio
import keyboard


pin = "21"
sensor = Adafruit_DHT.DHT11

done_flag = False
def get_weather():
	humid, temp = Adafruit_DHT.read_retry(sensor, pin)
	temp_data = {
		"temp": temp,
		"humid": humid
	}
	temp = temp_data["temp"]
	humid = temp_data["humid"]
	done_flag = True
	print(done_flag)

	return temp, humid

weather_log = []

def on_press(key):
	if key.read == "f1":
		weather_log.append(get_weather())

def loading_anim():
	dots = "."
	while done_flag == False:
		for i in range(16):
			lcd.print_line(dots, line=1)
			dots += "."
			time.sleep(1)

lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
lcd.init()

start_dialogs = ["Searching meteo", "Finding the sun", "TrueWeather"]

# Default text
lcd.print_line("Tey community", line=0)

weather = get_weather()

gpio.setmode(gpio.BCM)
gpio.setup(12, gpio.IN)

while True:
	try:
			now = datetime.now()
			dt = now.strftime("%d.%m %H:%M")
			keyboard.on_press(on_press)
			if gpio.input(12):
				# is NOT pressed
				lcd.print_line(f"{weather[0]}C | {weather[1]}%", line=0)
				lcd.print_line(dt, line=1)

			else:
				# is pressed
				dn = now.strftime("%d %b %Y %a")
				dt = now.strftime("%H:%M:%S")
				lcd.print_line(dn + "", line=0)
				lcd.print_line(f"{dt} | LBT", line=1)
			
				
			time.sleep(1)
	except KeyboardInterrupt:
		lcd.print_line("Keyboard", line=0)
		lcd.print_line("Interrupt", line=1)
		break
