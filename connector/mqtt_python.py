#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import MySQLdb
import json
import utils

logger = utils.get_logger("Connector")
# read the credential json with user_mqtt, user_mysql, pw_mqtt and pw_mysql
# fields.
file = open('credentials.json')
s = file.read()
d = json.loads(s)

# assign credential variables.
USERNAME_MQTT = d["user_mqtt"]
USERNAME_MYSQL = d["user_mysql"]
PW_MQTT = d["pw_mqtt"]
PW_MYSQL = d["pw_mysql"]

# the name of the table that we will write data
TABLE_NAME = "db"
MQTT_HOSTNAME = "mosquitto"
MYSQL_HOSTNAME = "db"


def on_connect(client, userdata, flags, rc):
    """
    The callback to be executed when the client receives a CONNACK response from the broker, that is on connect.
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    logger.info(f"Connected with result code {rc}.")
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe("owntracks/+/+")


def on_message(client, userdata, msg):
    """
        Each time MQTT server receives a message this is executed. The received JSON payload contains many fields, only
        a subset is used and enriched with two new fields. (1) a binary telling whether we are at home or not,
        and (2) Euclidean distance to home. The resulting list is then inserted to the mysql table.
    """
    logger.info(f"Received a message.")
    keys = ['lat', 'lon', 'tid', 'tst', 'acc']
    my_json = msg.payload.decode('utf8').replace("'", '"')
    # print(my_json)
    data = json.loads(my_json)
    data = tuple(data[your_key] for your_key in keys)
    # print(data)
    data = [(*data, utils.is_at_home(data[0], data[1]), utils.latlon_to_distance((data[0], data[1])))]
    logger.info(f"Payload is {data}")
    logger.info('Connecting to mysql server.')
    db = MySQLdb.connect(MYSQL_HOSTNAME, USERNAME_MYSQL, PW_MYSQL, TABLE_NAME)
    curs = db.cursor()
    logger.info(f'Inserting data to sql table {TABLE_NAME}')
    query = \
        """INSERT INTO gps_log(lat, lon, tid, time, accuracy, at_home, distance_home) values (%s,%s,%s,%s,%s,%s,%s)"""
    curs.executemany(query, data)
    db.commit()


logger.info("Connecting to broker.")
client = mqtt.Client("connector")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(USERNAME_MQTT, PW_MQTT)

try:
    client.connect(MQTT_HOSTNAME, 1883, 60)
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.publish("topic/test", "Hello world!")
    client.loop_forever()
    client.loop_stop()

except:
    logger.info("Cannot connect")
    raise ConnectionError
