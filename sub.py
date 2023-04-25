import paho.mqtt.client as paho
from paho import mqtt
from urllib.parse import urlparse
import sys
import time
import json
from cryptography.fernet import Fernet

# Define event callbacks
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connection Result: " + str(rc))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + decrypt_payload(msg.payload))

def decrypt_payload(payload):
    cypher_key=b'xqi9zRusHkcv3Om050HwX82eMTO-LbeW4YlqVVEzpw8=' #THIS IS VERY INSECURE - SHOULD BE ENV/EXTERNAL VARIABLE
    cypher=Fernet(cypher_key)
    decrypted_payload=cypher.decrypt(payload)
    return(decrypted_payload.decode())

mqttc = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Assign event cal  lbacks
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
url = urlparse("mqtt://806efec501e14bae9dde3d6b97243d9c.s1.eu.hivemq.cloud:8883/home")
base_topic = url.path[1:]

# Connect
username="fxwalsh"
password="xxx"

# enable TLS for secure connection
mqttc.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

mqttc.username_pw_set(username, password)
mqttc.connect(url.hostname, url.port)
mqttc.subscribe(base_topic+"/#")
mqttc.loop_start()

# Publish a message to temp every 15 seconds
while True:
    
    time.sleep(15)
