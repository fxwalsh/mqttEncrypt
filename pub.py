#!/usr/bin/python3

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

def on_publish(client, obj, mid, properties=None):
    print("Message ID: " + str(mid))

def encrypt_payload(payload):
    #HAVING A HARD CODED KEY IS INSECURE  - SHOULD BE ENV/EXTERNAL VARIABLE
    cypher_key=b'xqi9zRusHkcv3Om050HwX82eMTO-LbeW4YlqVVEzpw8=' 
    cypher=Fernet(cypher_key)
    encrypted_payload=cypher.encrypt(payload.encode('utf-8'))
    return(encrypted_payload.decode())

mqttc = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

url = urlparse("mqtt://806efec501e14bae9dde3d6b97243d9c.s1.eu.hivemq.cloud:8883/home")
base_topic = url.path[1:]

# Connect
username="fxwalsh"
password="xxx"

# enable TLS for secure connection
mqttc.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

mqttc.username_pw_set(username, password)
mqttc.connect(url.hostname, url.port)

mqttc.loop_start()

# Publish a message to temp every 15 seconds
while True:
    temp=30
    temp_json=json.dumps({"temperature":temp, "timestamp":time.time()})
    #mqttc.publish(base_topic+"/temperature", temp_json)
    mqttc.publish(base_topic+"/temperature", encrypt_payload(temp_json))
    time.sleep(15)
