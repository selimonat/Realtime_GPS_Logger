def is_at_home(lat,lon,delta=(0.001,0.002)):
    '''
        Returns a binary state depending on whether lat lon is within a square
        plus minus the home_latidute and longitude.
    '''
    home_latitude, home_longitude =  53.573118, 9.959827

    #load geo-history data
    return (lat > home_latitude-delta[0]) & (lat < home_latitude+delta[0]) & (lon > home_longitude-delta[0]) & (lon < home_longitude+delta[0])

def latlon_to_distance(current):
    from haversine import haversine
    home =  53.573118, 9.959827
    return haversine(home, current)

import MySQLdb
import json

def last_observed_location():
    #read the credential json with user_mqtt, user_mysql, pw_mqtt and pw_mysql
    #fields.
    file = open('/home/pi/code/python/Realtime_GPS_Logger/credentials.json');
    s=file.read();
    d=json.loads(s)

    #assign crediential variables.
    USERNAME_MQTT  =  d["user_mqtt"]
    USERNAME_MYSQL =  d["user_mysql"]
    PW_MQTT        =  d["pw_mqtt"]
    PW_MYSQL       =  d["pw_mysql"]
                
    #the name of the table that we will write data
    TABLE_NAME     = "devices"

    db   = MySQLdb.connect("127.0.0.1", USERNAME_MYSQL, PW_MYSQL, TABLE_NAME)
    curs = db.cursor()
    
    query = """select *,FROM_UNIXTIME(time) from log_owntracks_test2 order by time desc limit 1;"""
    curs.execute(query)
    record = curs.fetchall()[0]
    lat = record[2]
    lon = record[3]
    return lat, lon
