# RPI_ESP32
Sensors control with Raspberry Pi 4 and ESP-32 with Micropython

**RAPBERRY PI:** (setting username and password)

sudo apt install -y mosquitto mosquitto-clients

sudo systemctl enable mosquitto.service

# To subscribe to an MQTT topic

mosquitto_sub -d -t testTopic

# To publish

mosquitto_pub -d -t testTopic -m "Hello world!"

**ESP32**

from umqtt.robust import MQTTClient

client = MQTTClient("esp32-01", "192.168.1.171")

client.connect()

client.publish(b"testTopic", "msg")

#
def sub_cb(topic, msg):

  print((topic, msg))
  
  if topic == b'testTopic' and msg == b'on':
  
	print('ESP received command ON')

client = MQTTClient("esp32-01", "192.168.1.171")

client.connect()
