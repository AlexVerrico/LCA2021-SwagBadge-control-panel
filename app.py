# LCA2021 SwagBadge Control Panel. More details at https://github.com/AlexVerrico/LCA2021-SwagBadge-control-panel
# Copyright (C) 2021  Alex Verrico (https://alexverrico.com/)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import Flask, request, render_template, json
import paho.mqtt.client as mqtt
import sqlite3
from dotenv import load_dotenv
import os

env_vars = ['MQTT_CLIENT_ID', 'MQTT_SERVER_IP', 'MQTT_BADGE_TOPIC', 'PORT']
load_dotenv()
for i in env_vars:
    if os.getenv(i) is None:
        raise Exception('Fatal Error: Environment Variable "%s" must contain a value' % i)

app = Flask(__name__)                       #
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Configure flask

api_base_url = '/api/v1/'
db_path = 'main.sqlite'

mqtt_client = mqtt.Client(os.getenv('MQTT_CLIENT_ID'))  # Configure mqtt


def auth(_id, _pass):
    _connection = sqlite3.connect(db_path)
    _cursor = _connection.cursor()
    _auth_cmd = "SELECT pass FROM %s WHERE id = ?"
    _temp = _cursor.execute(_auth_cmd % 'auth', (''.join(('id_', str(_id))),)).fetchone()
    _connection.close()
    if str(_pass) == str(_temp[0]):
        return True
    return False


@app.route('/')
def home():
    return render_template('index.jinja2')
    # return '', 200


@app.route(''.join((api_base_url, 'send/log_text')), methods=['POST'])
def api_send_log_text():
    if 'id' not in request.values or 'auth' not in request.values or 'data' not in request.values:
        return '', 400
    _id = request.values['id']
    _auth = request.values['auth']
    _text = str(request.values['data'])
    if auth(_id, _auth) is False:
        return '', 200
    mqtt_client.connect(os.getenv('MQTT_SERVER_IP'))
    mqtt_client.publish(os.getenv('MQTT_BADGE_TOPIC'), '(oled:log %s)' % _text)
    mqtt_client.disconnect()
    return '', 200


@app.route(''.join((api_base_url, 'send/clear')), methods=['POST'])
def api_send_clear():
    if 'id' not in request.values or 'auth' not in request.values:
        return '', 400
    _id = request.values['id']
    _auth = request.values['auth']
    if auth(_id, _auth) is False:
        print("Auth failed")
        return '', 200
    mqtt_client.connect(os.getenv('MQTT_SERVER_IP'))
    mqtt_client.publish(os.getenv('MQTT_BADGE_TOPIC'), '(oled:clear)')
    mqtt_client.disconnect()
    return '', 200


@app.route(''.join((api_base_url, 'send/light_pixels')), methods=['POST'])
def api_send_light_pixels():
    if 'id' not in request.values or 'auth' not in request.values or 'data' not in request.values:
        return '', 400
    _id = request.values['id']
    _auth = request.values['auth']
    _data = json.loads(request.values['data'])
    if auth(_id, _auth) is False:
        return '', 200
    mqtt_client.connect(os.getenv('MQTT_SERVER_IP'))
    for i in _data:
        mqtt_client.publish(os.getenv('MQTT_BADGE_TOPIC'), '(oled:pixel %s %s)' % (i[0], i[1]))
    mqtt_client.disconnect()
    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')))
