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

    if action is None:
        return {}
    else:
        status = light(action)

    return makeWebhookResult(status)

def light(action):
    if action == 'lightOn':
        led.on()
        return 'LIGHT_ON'
    elif action == 'lightOff':
        led.off()
        return 'LIGHT_OFF'


def makeWebhookResult(status):
    speech = None
    if (status is None) or status == 'FAIL':
        speech = "Please try again"
    if status == 'LIGHT_ON':
        speech = "Light has been turned on"
    elif status == "LIGHT_OFF":
        speech = "Light has been turned off"

    return {
        "speech": speech,
        "displayText": speech,
        "source": "home-bot"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='localhost')
