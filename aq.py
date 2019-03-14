import api
from flask import Flask
from flask import render_template
from flask import make_response
from flask_caching import Cache
import datetime
from wsgiref.handlers import format_date_time
from time import mktime


#cache = Cache(config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': './cache'})
cache = Cache(config={'CACHE_TYPE': 'memcached', 'CACHE_KEY_PREFIX': 'AQgraph283'})
app = Flask(__name__)
cache.init_app(app)


@app.route('/')
# Cache view for 10 minutes
@cache.cached(timeout=600)
def index():
    now = datetime.datetime.now()
    nowstamp = mktime(now.timetuple())
    then = (datetime.datetime.now() - datetime.timedelta(minutes=15))
    thenstamp = mktime(then.timetuple())
    sensor_data = api.grab_sensor_data()
    resp = make_response(render_template('graph.html', sensor_data=sensor_data))
    resp.headers['Last-Modified'] = format_date_time(nowstamp)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)

