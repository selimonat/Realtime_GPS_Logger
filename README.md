# Realtime Geographic Position Logger

Log the geographic position of your(self) mobile phone in real-time for visualization and analytics purposes.

![image info](./img/cover.jpg)

# Tech stack

![image info](./img/diagram/event_processing.png)

# Requirements

- [Owntracks](https://owntracks.org/) is an app for iOS that regularly sends geographic coordinates as events to an 
  MQTT broker.

- `Docker` stack installed in order to spin up different containers with `docker-compose`. `docker-compose` is 
installed by Poetry during environment setup.

- The container running the MQTT broker (running on own Raspberry Pi 3 behind the house router) needs to be accessed 
  from outside using the phone's internet connection. I am using a free dynamic-dns service for domain resolution and 
  traffic redirection to the Raspberry.
  
- Python 3.7

# How to run ?

To install the Python environment you need to run `make setup.env`. This will install `docker-compose`.

`docker-compose up` should spin of 3 different containers after building them: 
- MQTT Broker, 
- database 
- the connector.

To test it locally, enter the IP address of your host to Owntrack. Each time you trigger a new message from it, you 
should be able to see the corresponding information on the logs of the MQTT and connector containers. 

# Current Issues:

Database container is not able to run the init script, so currently the tables must be ran manually from inside the 
container using a mysql shell. 

