# An Accessory for a LED attached to pin 11.
import logging
from pyhap.accessory import Accessory, Category
import pyhap.loader as loader
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from pyhap.accessories.mqtt.utils import Utils



class LightBulb(Accessory):

    category = Category.LIGHTBULB

    def __init__(self, *args, server=False, device_id=False, **kwargs):
        super(LightBulb, self).__init__(*args, **kwargs)
        self.deviceid = device_id
        self.servers = server
        #self.get_service("Lightbulb").get_characteristic("Name").set_value("Luz Interior")

    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_bulb(self, value):
        value = Utils.standardizeResponse(value)
        try:
            publish.single("/" + self.deviceid + "/set",
                           payload=value,
                           hostname=self.servers['host'],
                           client_id="screen",
                           # auth=self.servers['auth'],
                           retain=False,
                           port=1883)
        except Exception as e:
            print(e)
            pass

    def _set_services(self):
        """Add the fan service. Also add optional characteristics to it."""
        super(LightBulb, self)._set_services()
        service_loader = loader.get_serv_loader()
        fan_service = service_loader.get("Lightbulb")
        # NOTE: Don't forget that all characteristics must be added to the service before
        # adding the service to the accessory, so that it can assign IIDs to
        # all.

        # Add the optional RotationSpeed characteristic to the Fan
        # if (self.dimmer):

        # Add the optional RotationSpeed characteristic to the Fan
        # rotation_dir_char = loader.get_char_loader().get("RotationDirection")
        # fan_service.add_opt_characteristic(rotation_dir_char)
        # rotation_dir_char.setter_callback = self.set_rotation_direction

        self.add_service(fan_service)
        fan_service.get_characteristic("On").setter_callback = self.set_bulb

    def stop(self):
        super(LightBulb, self).stop()

    def run(self):
        while not self.run_sentinel.wait(10):
            m = subscribe.simple("/" + self.deviceid + '/status',
                                 hostname="localhost", retained=True, msg_count=1)
            self.get_service("Lightbulb").get_characteristic(
                "On").set_value(True if int(m.payload) == 1 else False)
