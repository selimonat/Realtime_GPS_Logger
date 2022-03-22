# Realtime Geographic Logger

Log the geographic position of your(self) mobile phone in real-time for visualization and analytics purposes.

![image info](./img/cover.jpg)

# Requirements

- [Owntracks](https://owntracks.org/) is an app for iOS that regularly sends geographic coordinates as events to an 
  MQTT broker.

- `Docker` stack installed in order to spin up different containers with `docker-compose`.

- The container running the MQTT broker (running on own premises behind the house router) needs to be accessed from the 
  phone's internet connection. With a free dynamic-dns service for domain resolution and traffic redirection it is 
  possible to find a solution. But it requires a computer that is always on. Unfortunately a Raspberry Pi 3 will 
  give a lot of pain to get the `docker-compose` running.

# How to run ?

MQTT broker, MySQL db and the connector can be spun off as services with `docker-compose`.

`docker-compose run` should spin of 3 different containers. To test it locally, enter the IP address of your host to 
Owntrack. Each time you trigger a new message, you should be able to see corresponding information on the logs of 
the 3 containers. 

![image info](./img/diagram/event_processing.png)
