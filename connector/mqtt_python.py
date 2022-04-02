#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import MySQLdb
import dotenv
import utils
from time import sleep
import os

load_dotenv('../') # load .env file
logger = utils.get_logger("Connector")
# read the credential json with user_mqtt, user_mysql, pw_mqtt and pw_mysql
# fields.

# assign credential variables.
USERNAME_MYSQL= os.getenv("username_mysql") 
PW_MYSQL =  os.getenv("MYSQL_ROOT_PASSWORD")
# the name of the table that we will write data
TABLE_NAME =  os.getenv("MYSQL_DATABASE")
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
    data = process_payload(msg)
    logger.info('Connecting to mysql server.')
    db = MySQLdb.connect(MYSQL_HOSTNAME, USERNAME_MYSQL, PW_MYSQL, TABLE_NAME)
    logger.info(f"Server returned {db}")
    curs = db.cursor()
    logger.info(f'Inserting data to sql table {TABLE_NAME}')
    query = \
        """INSERT INTO gps_log(lat, lon, tid, time, accuracy, at_home, distance_home) values (%s,%s,%s,%s,%s,%s,%s)"""
    curs.executemany(query, data)
    resp = db.commit()
    logger.info(f"Server returned {resp}")
    logger.info(f"Closing connection {db.close()}")


def process_payload(msg):
    """
    Process the payload received by the broker.
    :param msg:
    :return:
    """
    keys = ['lat', 'lon', 'tid', 'tst', 'acc']
    my_json = msg.payload.decode('utf8').replace("'", '"')
    logger.info(f"Processing the payload {my_json}")

    data = json.loads(my_json)
    data = tuple(data[your_key] for your_key in keys)

    data = [(*data,
             utils.is_at_home(data[0], data[1]),
             utils.distance_to_home((data[0], data[1])),
             )]
    logger.info(f"Processed payload: {data}")
    return data


logger.info("Connecting to MQTT broker.")
client = mqtt.Client("connector")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("connector")

counter = 0
while True:
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
        counter += 1
        logger.info(f"Cannot connect to db, tried {counter} times, will try 10 more times.")
        sleep(5)
        if counter == 10:
            logger.info("Cannot manage to connect to db after 10 trials.")
            raise ConnectionError
