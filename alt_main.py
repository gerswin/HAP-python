"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client querries, etc.
"""
import logging
import os
import pickle
import signal

import pyhap.util as util
from pyhap.accessories.mqtt.LightBulbDimmer import LightBulbDimmer
from pyhap.accessories.mqtt.LightBulb import LightBulb
from pyhap.accessories.mqtt.GarageDoor import GarageDoor

from pyhap.accessories.TemperatureMQTT import TemperatureMQTT
from pyhap.accessory import Bridge
from pyhap.accessory_driver import AccessoryDriver
import json
logging.basicConfig(level=logging.INFO)

server_auth = json.loads('{"host":"localhost","port":1883,"auth":{"username":"gerswin","password":"16745665"}}')


# def lightDimmer(server,device_id,name):
#     return LightBulbDimmer(name,server=server,device_id=device_id)


# def lightBulb(server,device_id,name):
#     return LightBulb("Luz",server=server_auth,device_id="F9-CB-E6-6D-F4-00")

# def GarageDoor(server,device_id,name):
#     return LightBulb("Luz",server=server_auth,device_id="F9-CB-E6-6D-F4-00")


def get_bridge():
    """Call this method to get a Bridge instead of a standalone accessory."""

    devices = json.loads(open("devices.json",'r').read())
    bridge = json.loads(open("bridge.json",'r').read())

    bridge = Bridge(display_name=bridge['name'],mac=util.generate_mac(), pincode=b"111-11-111")
    #bridge = Bridge(display_name="Bridge",  mac=util.generate_mac(),pincode=b"203-23-999")

    #bridge.add_accessory(LightBulb("Luz",server=server_auth,device_id="F9-CB-E6-6D-F4-00"))
    #bridge.add_accessory(LightBulbDimmer("Luz",server=server_auth,device_id="F9-CB-E6-6D-F4-02"))

    for device in devices:

        if (device['service'] == "LIGHTBULB"):
            if(device['dimmer']):
                bridge.add_accessory(LightBulbDimmer(device['name'],server=server_auth,device_id=device['device_id']))
            else:
                 bridge.add_accessory(LightBulb(device['name'],server=server_auth,device_id=device['device_id']))
        elif (device['service'] == "GARAGE_DOOR_OPENER"):
            bridge.add_accessory(GarageDoor(device['name'],server=server_auth,device_id=device['device_id']))
        else:
            pass


    return bridge

def get_accessory():
    """Call this method to get a standalone Accessory."""
    acc = 0 
    return acc


# The AccessoryDriver preserves the state of the accessory
# (by default, in the below file), so that you can restart it without pairing again.
if os.path.exists("accessory.pickle"):
    with open("accessory.pickle", "rb") as f:
        acc = pickle.load(f)
       # acc.config_version += 1
else:
    acc = get_bridge()  # Change to get_bridge() if you want to run a Bridge.

# Start the accessory on port 51826
driver = AccessoryDriver(acc, 51816)
# We want KeyboardInterrupts and SIGTERM (kill) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGINT, driver.signal_handler)
signal.signal(signal.SIGTERM, driver.signal_handler)
# Start it!

driver.start()
#driver.update_advertisment()
# Persist the new config_version (see issue #11)
#driver.persist()
