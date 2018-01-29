# An Accessory for a LED attached to pin 11.
import logging
from pyhap.accessory import Accessory, Category
import pyhap.loader as loader

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

from pyhap.accessories.mqtt.utils import Utils


class LightBulbDimmer(Accessory):

    category = Category.LIGHTBULB

    def __init__(self, *args, server=False, device_id=False, **kwargs):
        super(LightBulbDimmer, self).__init__(*args, **kwargs)
        self.deviceid = device_id
        self.servers = server
        #self.get_service("Lightbulb").get_characteristic("Name").set_value("Luz Interior")

    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_bulb(self, value):
        value = Utils.standardizeResponse(value)
        Utils.deviceSet(value, "onoff", self.servers, self.deviceid)

    def set_dimm(self, value):
        Utils.deviceSet(value, "brightness", self.servers, self.deviceid)

    def _set_services(self):
        """Add the fan service. Also add optional characteristics to it."""
        super(LightBulbDimmer, self)._set_services()
        service_loader = loader.get_serv_loader()
        fan_service = service_loader.get("Lightbulb")
        # NOTE: Don't forget that all characteristics must be added to the service before
        # adding the service to the accessory, so that it can assign IIDs to
        # all.

        # Add the optional RotationSpeed characteristic to the Fan
        # if (self.dimmer):
        rotation_speed_char = loader.get_char_loader().get("Brightness")
        fan_service.add_opt_characteristic(rotation_speed_char)
        rotation_speed_char.setter_callback = self.set_dimm

        # Add the optional RotationSpeed characteristic to the Fan
        # rotation_dir_char = loader.get_char_loader().get("RotationDirection")
        # fan_service.add_opt_characteristic(rotation_dir_char)
        # rotation_dir_char.setter_callback = self.set_rotation_direction

        self.add_service(fan_service)
        fan_service.get_characteristic("On").setter_callback = self.set_bulb

    def stop(self):
        super(LightBulbDimmer, self).stop()

    def run(self):
        while not self.run_sentinel.wait(10):

            self.get_service("Lightbulb").get_characteristic("On").set_value(Utils.deviceStatus("onoff", self.servers, self.deviceid,True))
            self.get_service("Lightbulb").get_characteristic("Brightness").set_value(Utils.deviceStatus("brightness", self.servers, self.deviceid))
