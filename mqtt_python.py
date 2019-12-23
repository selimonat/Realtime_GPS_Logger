#!/usr/bin/env python3

#Assumes appropriately set mysql db and a mqtt broker

import paho.mqtt.client as mqtt
import MySQLdb
import subprocess
import json
from geo_utils import *

#read the credential json with user_mqtt, user_mysql, pw_mqtt and pw_mysql
#fields.
file = open('credentials.json');
s=file.read();
d=json.loads(s)

#assign crediential variables.
USERNAME_MQTT  =  d["user_mqtt"]
USERNAME_MYSQL =  d["user_mysql"]
PW_MQTT        =  d["pw_mqtt"]
PW_MYSQL       =  d["pw_mysql"]
                
#the name of the table that we will write data
TABLE_NAME     = "devices"

#creation command for database
#CREATE TABLE log_owntracks_test2 (time BIGINT UNSIGNED, tid VARCHAR(2), lat
#DECIMAL(10, 8) NOT NULL, lon DECIMAL(11, 8) NOT NULL, accuracy SMALLINT
#UNSIGNED, at_home BOOLEAN, distance_home DOUBLE, PRIMARY KEY (time, tid));

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #Code to be executed on connect
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("owntracks/+/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    """
        Each time MQTT server receives a message this is executed.
        The original json contains many fields we extract only the KEYS
        from it. We add two new contentn, namely whether a binary telling
        whether we are at home or not, and Euclidean distance to home.
        The resulting list is then inserted to the devices.log_owntracks_test2
    """
    keys = ['lat', 'lon','tid', 'tst', 'acc']
    my_json = msg.payload.decode('utf8').replace("'", '"')
    #print(my_json)
    data = json.loads(my_json)
    data = tuple(data[your_key] for your_key in keys)
    #print(data)
    data = [( *data , is_at_home(data[0],data[1]) , latlon_to_distance( (data[0],data[1]) ) ) ]
    #print(len(data))
    print(data)
    db   = MySQLdb.connect("127.0.0.1", USERNAME_MYSQL, PW_MYSQL, TABLE_NAME)
    curs=db.cursor()
    
    query = """INSERT INTO log_owntracks_test2(lat, lon, tid, time, accuracy, at_home, distance_home) values (%s,%s,%s,%s,%s,%s,%s)"""
    curs.executemany(query,data)
    db.commit()

client = mqtt.Client("lalalala")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(USERNAME_MQTT,PW_MQTT)
client.connect("localhost", 1883, 60)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

client.loop_stop()
