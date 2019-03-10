import datetime
import json
import urllib.request


def reverse_geocode(lat, lon):
    appid = "grab code from here.com"
    appcode = "grab code from here.com"
    url = "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?prox=" \
          + lat + "%2C" + lon + "%2C50&mode=retrieveAddresses&maxresults=1&gen=9&app_id=" \
          + appid + "&app_code=" + appcode
    data = urllib.request.urlopen(url)
    location_details = json.loads(data.read())
    return location_details


def grab_sensor_list():
    list_devices = "https://aq.connectedhumber.org/api.php?action=list-devices&only-with-location=true"
    response = urllib.request.urlopen(list_devices)
    sensors = json.loads(response.read())
    sensor_list = []
    for z in sensors:
        sensor_list.append(z['id'])
    return sensor_list


def grab_sensor_urls():
    # Generate an ISO formatted datestamp for 24 hours ago..
    # Go through the list of all known sensors (with a location)
    # Grab the data and add it to a dictionary where key = sensor id and value = the url to pull data
    # from it
    time_last_day = (datetime.datetime.now() - datetime.timedelta(minutes=1440)).isoformat()
    url_dict = {}
    for y in grab_sensor_list():
        # grab 24 hours of data, with the data averaged each hour by the API
        sensor_data_url = "https://aq.connectedhumber.org/api.php?action=device-data&device-id=" + str(
            y) + "&reading-type=PM25&start=" + time_last_day + "&end=now&average-seconds=3600"
        url_dict.update({y: sensor_data_url})
    return url_dict


def grab_sensor_data():
    # iterate through the items in our dictionary and retrieve data from each url
    # Create a new dict where the key is the sensor id and the value is the retrieved json data
    sensor_reading_dict = {}
    url_dict = grab_sensor_urls()
    for key, value in url_dict.items():
        try:
            data = urllib.request.urlopen(value)
            sensor_reading = json.loads(data.read())
            sensor_reading_dict.update({key: sensor_reading})
        # if it isn't a valid json obj because no readings exist it'll throw
        # an exception, pass it to ignore sensors without readings (dodgy and lazy I know...)
        except Exception:
            pass
    for key in sensor_reading_dict:
        # grab info about the sensors
        url = "https://aq.connectedhumber.org/api.php?action=device-info&device-id=" + str(key)
        data = urllib.request.urlopen(url)
        sensor_details = json.loads(data.read())
        # create a temporary list to hold the data about the sensor and the sensor readings for this pass
        sensor_list_details = []
        sensor_list_details.append(sensor_details)
        sensor_list_details.append(sensor_reading_dict.get(key))
        sensor_location = reverse_geocode(str(sensor_details["latitude"]), str(sensor_details["longitude"]))
        sensor_list_details.append(sensor_location)
        # update the sensor ID key with a list containing 2 values, sensor info and sensor data
        sensor_reading_dict.update({key: sensor_list_details})
    return sensor_reading_dict
