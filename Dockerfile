FROM python:3.5

WORKDIR /opt/mqtt

COPY requirements.txt /opt/mqtt/requirements.txt
COPY mqtt_python.py /opt/mqtt/mqtt_python.py
COPY geo_utils.py /opt/mqtt/geo_utils.py

RUN apt-get update
RUN apt-get -y install python3-dev 
RUN apt-get -y install default-libmysqlclient-dev
RUN apt-get -y install build-essential

RUN pip install -U pip
RUN pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple
RUN pip install mysqlclient==1.4.6

CMD python ./mqtt_python.py
