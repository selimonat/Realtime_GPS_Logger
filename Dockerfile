FROM python:3.7.6

RUN apt-get update
RUN apt-get -y install python3-dev
RUN apt-get -y install default-libmysqlclient-dev
RUN apt-get -y install build-essential

WORKDIR /opt/mqtt

COPY ./connector ./
COPY ./.env ./

RUN pip install -U pip
RUN pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple
RUN pip install mysqlclient==1.4.6

CMD python ./mqtt_python.py
