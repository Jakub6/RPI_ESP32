from machine import Pin, I2C
import time 
import BME280
import ssd1306
import json

from umqtt.robust import MQTTClient
import ubinascii
import micropython
import esp

mqtt_server = '192.168.1.171'
message_interval = 5
last_message = 0

topic_sub1 = b"led"
topic_pub1 = b"led"

topic_sub = b"temp"
topic_pub = b"temp"
client_id = "esp-32"

i2c_oled = I2C(-1, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

i2c = I2C(scl=Pin(18), sda=Pin(23), freq=10000)
bme = BME280.BME280(i2c=i2c)
led = machine.Pin(5, machine.Pin.OUT)

#button = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

def extIntHandler(pin):
	global button, client
	button_state = not button.value()
	led_state = 1 if button_state == True else 0
	client.publish(topic_pub1,b"%s" %led_state)

def sub_cb(topic, msg):
	global oled
	print((topic, msg))
	if topic == b'temp':
		oled.fill(0)
		j_msg = msg.decode()
		data = json.loads(j_msg)
		oled.text('Temp:%s' %data["temp"], 0, 20)
		oled.text('Press:%s' %data["pres"], 0, 40)
		oled.show()
		print('ESP received temperature')
	if topic == b'led':
		if msg==b'1':
			led.value(1)			
		else:
			led.value(0)
def connect_and_subscribe():
	global client_id, mqtt_server, topic_sub
	client = MQTTClient(client_id, mqtt_server)
	client.set_callback(sub_cb)
	client.connect()
	client.subscribe(topic_sub)
	client.subscribe(topic_sub1)
	
	print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
	return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
  
button = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=extIntHandler)

while True:
	try:
		client.check_msg()
		if (time.time() - last_message) > message_interval:
			  payload = {}
			  payload["temp"] = bme.temperature
			  payload["pres"] = bme.pressure
			  client.publish(topic_pub, json.dumps(payload))
			  state = led.value()
			  client.publish(topic_pub1,b"%s" %state) 
			  last_message = time.time()
	except OSError as e:
		restart_and_reconnect()
