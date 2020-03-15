# Main application file
from machine import Pin, I2C
from time import sleep
import BME280
import ssd1306


print("MAIN START")

def main():
	print("START")
	i2c = I2C(scl=Pin(18), sda=Pin(23), freq=10000)
	i2c_oled = I2C(-1, scl=Pin(22), sda=Pin(21))

	oled_width = 128
	oled_height = 64
	oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

	while True:
		oled.fill(0)
		bme = BME280.BME280(i2c=i2c)
		temp = bme.temperature
		pres = bme.pressure
		print('Temp.: ', temp)
		print('Pres.: ', pres)
		oled.text('Temp.: %s' %temp, 0, 20)
		oled.text('Pres.: %s' %pres, 0, 30)
		oled.show()
		time.sleep(5)
		
try:
  #run main app here to reset on unhandled exceptions
  main()
except Exception as e:
  print("Unhandled exception:%s" % (str(e),))
  print("Runtime error encountered. Restarting in 10s")
  time.sleep(60.0)
  print("Restarting now!")
  machine.reset()
print("MAIN END")