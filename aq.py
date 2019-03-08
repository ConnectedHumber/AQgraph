import api
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def index():
    sensor_data = api.grab_sensor_data()
    return render_template('graph.html', sensor_data=sensor_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)


#Accessing data..
#sensor_data = api.grab_sensor_data()
#for key in sensor_data:
#    data = sensor_data.get(key)
#    # data[0] is the list containing the sensor info dict
#    print("***************")
#    # data[1] is the list containing sensor readings dicts
#    print("name:" + data[0]["name"] + " lat:" + str(data[0]["latitude"]) + " lon:" + str(data[0]["longitude"]))
#    for x in data[1]:
#        print(x["datetime"] + " " + str(x["value"]))


