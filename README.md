# Realtime Geographic Logger

Log the geographic position of your mobile phone in real-time for visualization and analytic purposes.

![image info](./img/cover.jpg)

# Requirements

- [Owntracks](https://owntracks.org/) is an app that regularly sends geographic coordinates as events to an MQTT
  broker. You need to have it on your mobile device.

- The broker container needs to be accessed from the phone's internet connection. My solution is to run it on a
  Rasberry Pi 3 and use a free dynamic dns service for domain resolution and directing trafic.

- You need to have the `Docker` stack installed in order to spin up the app with `docker-compose`.

# How to run ?

MQTT broker, MYSQL DB and the connector can be spin off as services with docker-compose.

`docker-compose run` should spin of 3 different containers. To test it locally, enter the IP address of your host to 
Owntrack. Each time you trigger a new message from Owntracks, you should be able to see corresponding information on 
the logs of the 3 containers.

![image info](./img/diagram/event_processing.png)
