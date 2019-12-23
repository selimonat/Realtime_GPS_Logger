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
