import json
import os

from tinydb import TinyDB, Query

from flask import Flask
from flask import request
from flask import make_response

from device import Device

# Flask app starts in global layout
app = Flask(__name__)

# Global Variables
ON_ACTION = 'deviceOn'
OFF_ACTION = 'deviceOff'
LIGHT = 'light'
FAN = 'fan'

# Initialize db
db = TinyDB('db.json')

@app.route('/')
def home_page():
    return "Welcome to Home bot"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print("Response:")
    print(res)
    r= make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(request):
    result = request.get('result')
    if result is None:
        return {}

    data = None
    action = result.get('action')

    deviceType = result.get('parameters').get('device')
    print('processRequest: ' + deviceType)

    return makeWebhookResult(action, deviceType)

def makeWebhookResult(action, deviceType):
    speech = handleAction(action, deviceType)

    return {
    "speech": speech,
    "displayText": speech,
    "source": "home-bot"
    }

def handleAction(action, deviceType):
    device = Device(deviceType)

    if action is None:
        return "Action not found"
    elif action == ON_ACTION:
        return device.on()
    elif action == OFF_ACTION:
        return device.off()
    return "Action not recognized"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    db.purge()
    db.insert({'device_type':FAN, 'state':False})
    db.insert({'device_type':LIGHT, 'state':False})

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='localhost')
