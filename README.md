# Realtime Geographic Position Logger

Log the geographic position of your(self) mobile phone in real-time for visualization and analytics purposes.

![image info](./img/cover.jpg)

# Tech stack

![image info](./img/diagram/event_processing.png)

# Requirements

- Raspberry Pi. I tested the code using an RPI3. Because RPI3 uses an `armv7l` architecture, the database container 
  will not run on other machines. However, you may simply use another respository for `mysql` image.

- [Owntracks](https://owntracks.org/) is an app for iOS that regularly sends geographic coordinates as events to an 
  MQTT broker.

- `Docker` stack installed in order to spin up different containers with `docker-compose`. `docker-compose` is 
installed by Poetry during environment setup.

- The container running the MQTT broker (running on own Raspberry Pi 3 behind the house router) needs to be accessed 
  from outside using the phone's internet connection. I am using a free dynamic-dns service for domain resolution and 
  traffic redirection to the Raspberry. This is not required for testing within the same local network.
  
- A .env file located at at the project folder. This will be used both by the mysql container to set up a password and 
the connector to authenticate against it. The .env file must contain the following keys.

```
MYSQL_DATABASE=db
MYSQL_ROOT_PASSWORD=
username_mysql=root
home_lat=0.0 # use your home lat/lon
home_lon=0.0
``` 

# How to run ?

To install the Python environment you need to run `make setup.env`. In order to use `docker-compose` activate the 
`venv` environment with `. .venv/bin/activate`. 

`docker-compose up` should spin of 3 different containers after building them: 
- MQTT Broker, 
- database 
- the connector.

To test it locally, enter the IP address of your host to Owntrack. Each time you trigger a new message from it, you 
should be able to see the corresponding information on the logs of the MQTT and connector containers. 

