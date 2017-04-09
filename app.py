import json
import os

from gpiozero import LED

from tinydb import TinyDB, Query

from flask import Flask
from flask import request
from flask import make_response

# Flask app starts in global layout
app = Flask(__name__)

# Initialize db
db = TinyDB('db.json')

# GPIO 17 for led
led = LED(17)

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

    return makeWebhookResult(action)

def makeWebhookResult(action):
    speech = handleLightAction(action)

    return {
    "speech": speech,
    "displayText": speech,
    "source": "home-bot"
    }

def handleLightAction(action):
    if action is None:
        return "Please try again"
    elif action == 'lightOn':
        if getSwitchState('light1'):
            return "Light is already on"
        else:
            led.on()
            db.insert()
            return "Light has been turned on"
    elif action == 'lightOff':
        if not getSwitchState('light1'):
            return "Light is already off"
        else:
            led.off()
            return "Light has been turned off"

def getSwitchState(light):
    result = db.search(query.type == light)[0]
    return result['state']

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    db.insert({'type':'light1', 'state':False})
    # Initialize db
    db = TinyDB('db.json')

    # GPIO 17 for led
    led = LED(17)

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='localhost')
