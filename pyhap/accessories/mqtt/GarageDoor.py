# An Accessory for a LED attached to pin 11.
import logging
from pyhap.accessory import Accessory, Category
import pyhap.loader as loader
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
from pyhap.accessories.mqtt.utils import Utils



class GarageDoor(Accessory):
    category = Category.GARAGE_DOOR_OPENER

    def __init__(self, *args, server=False, device_id=False, **kwargs):
        super(GarageDoor, self).__init__(*args, **kwargs)
        self.deviceid = device_id
        self.servers = server
        self.CurrentDoorState = self.get_service(
            "GarageDoorOpener").get_characteristic("CurrentDoorState")
        self.ObstructionDetected = self.get_service(
            "GarageDoorOpener").get_characteristic("ObstructionDetected")

    def _pulse_door(self, value):
        value = Utils.standardizeResponse(value)
        
        self.CurrentDoorState.set_value(value)

        try:
            publish.single("/" + self.deviceid + "/set",
                           payload=value,
                           hostname=self.servers['host'],
                           client_id="screen",
                           # auth=self.servers['auth'],
                           retain=False,
                           port=1883)
        except Exception as e:
            raise
            print("error",e)
            pass
        

    def _set_services(self):
        super(GarageDoor, self)._set_services()

        garage_door_opener_service = loader.get_serv_loader().get("GarageDoorOpener")
        self.add_service(garage_door_opener_service)
        garage_door_opener_service.get_characteristic(
            "TargetDoorState").setter_callback = self._pulse_door

    def stop(self):
        super(GarageDoor, self).stop()

