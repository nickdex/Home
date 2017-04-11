class Device:
    def __init__(self, name):
        if deviceType == FAN:
            self.type = FAN
        else:
            self.type = LIGHT

# device methods
def getLocalDeviceType(deviceFromRequest):
    if deviceType == FAN:
        return FAN
    else:
        return LIGHT

def handleOnAction(device):
    if getSwitchState(device):
        return "{} is already on".format(device)
    else:
        turnDeviceOn(device)
        updateSwitchState(device, True)
        return "{} has been turned on".format(device)

def handleOffAction(device):
    if not getSwitchState(device):
        return "{} is already off".format(device)
    else:
        turnDeviceOff(device)
        updateSwitchState(device, False)
        return "{} has been turned off".format(device)

def turnDeviceOn(device):
    device.on()

def turnDeviceOff(device):
    device.off()

def getSwitchState(device):
    result = db.search(Query().device_type == device)[0]
    return result['state']

def updateSwitchState(device, state):
    db.update({'state':state}, Query().device_type == device)
# end region
