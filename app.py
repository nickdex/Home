import json
import os

from gpiozero import LED

from tinydb import TinyDB, Query

from flask import Flask
from flask import request
from flask import make_response

# Flask app starts in global layout
app = Flask(__name__)

# Global Variables
ON_ACTION = 'deviceOn'
OFF_ACTION = 'deviceOff'
LIGHT = 'light'
FAN = 'fan'

# Initialize db
db = TinyDB('db.json')

# GPIO 17 for led
led = LED(17)
fan = LED(18)

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
    speech = handleLightAction(action, deviceType)

    return {
    "speech": speech,
    "displayText": speech,
    "source": "home-bot"
    }

def handleLightAction(action, deviceType):
    msg = ''
    device = ''
    if deviceType == FAN:
        device = FAN
    else:
        device = LIGHT
    if action is None:
        return "Please try again"
    elif action == ON_ACTION:
        if getSwitchState(device):
            return "{} is already on".format(deviceType)
        else:
            if deviceType == FAN:
                fan.on()
            else:
                led.on()
            updateSwitchState(device, True)
            return "{} has been turned on".format(deviceType)
    elif action == OFF_ACTION:
        if not getSwitchState(device):
            return "{} is already off".format(deviceType)
        else:
            if deviceType == FAN:
                fan.off()
            else:
                led.off()
            updateSwitchState(device, False)
            return "{} has been turned off".format(deviceType)
    return "Action not recognized"

def getSwitchState(light):
    result = db.search(Query().type == light)[0]
    return result['state']

def updateSwitchState(light, state):
    db.update({'state':state}, Query().type == light)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    db.purge()
    db.insert({'type':'fan', 'state':False})
    db.insert({'type':'light', 'state':False})

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='localhost')
