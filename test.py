import api
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def index():
    sensor_data = list(api.grab_sensor_list())
    return render_template('index.html', sensor_data=list)


app.run(host='0.0.0.0', port='8000', debug=True)
