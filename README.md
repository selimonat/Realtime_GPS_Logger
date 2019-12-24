# Realtime_GPS_Logger
This repo allows you to log the GPS coordinates of your mobile phone running the app Owntracks to a database running on a remotely accessible Raspberry Pi using a MQTT server. 

# Requirements

MQTT server and mySQL database set up and running.

For installation of MQTT broker, the great source of information is here `https://owntracks.org/booklet/guide/broker/`.

# Check installation
`python mqtt_python.py` should return

```
pi@homebrain ~/code/python/mqtt: python mqtt_python.py        

Connected with result code 0
[(49.282318115234375, 8.399269868366922, 'se', 1577143402, 65, False, 489.1970030175267)]
[(53.57465554760496, 9.96199707861318, 'so', 1567090651, 65, False, 0.22306862648310322)]
```

# Create Docker Image

```
sudo docker build -t mqtt2sql . #create an image called mqtt2sql
sudo docker run -d --name=docker_mqtt2sql --network="host" e51acd19dc5d #run it as a container
```

# Start the docker container at system start up as daemon

based on:
https://stackoverflow.com/questions/30449313/how-do-i-make-a-docker-container-start-automatically-on-system-boot/39493500#39493500

create file `docker_mqtt2sql.service` in `/etc/systemd/system` with the following content 

```
[Unit]
Description=mqtt_2_sql container
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker start -a docker_mqtt2sql
ExecStop=/usr/bin/docker stop -t 2 docker_mqtt2sql

[Install]
WantedBy=default.target
```

and run `sudo systemctl enable docker_mqtt2sql.service` to enable it a service.
