import json
import os

from gpiozero import LED

from flask import Flask
from flask import request
from flask import make_response

# Flask app starts in global layout
app = Flask(__name__)

# GPIO 17 for led
led = LED(17)

lightSwitch = False

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
    speech = light(action, lightSwitch)

    return {
    "speech": speech,
    "displayText": speech,
    "source": "home-bot"
    }

def handleLightAction(action, lightSwitch):
    if action is None:
        return "Please try again"
    elif action == 'lightOn':
        if lightSwitch:
            return "Light is already on"
        else:
            lightSwitch = True
            led.on()
            return "Light has been turned on"
    elif action == 'lightOff':
        if not lightSwitch:
            return "Light is already off"
        else:
            lightSwitch = False
            led.off()
            return "Light has been turned off"


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='localhost')
