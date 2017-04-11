from tinydb import TinyDB, Query
from gpiozero import LED

LED_PIN = 17
FAN_PIN = 18

class Device:
    def __init__(self, name):
        if deviceType == FAN:
            self.type = FAN
            self.component = LED(FAN_PIN)
        else:
            self.type = LIGHT
            self.component = LED(LED_PIN)

    def on(self):
        if getSwitchState():
            return "{} is already on".format(self.type)
        else:
            self.component.on()
            updateSwitchState(True)
            return "{} has been turned on".format(self.type)

    def off(self):
        if getSwitchState():
            return "{} is already off".format(self.type)
        else:
            self.component.off()
            updateSwitchState(False)
            return "{} has been turned off".format(self.type)

# device methods
def getSwitchState():
    result = db.search(Query().device_type == self.type)[0]
    return result['state']

def updateSwitchState(state):
    db.update({'state':state}, Query().device_type == self.type)
# end region
