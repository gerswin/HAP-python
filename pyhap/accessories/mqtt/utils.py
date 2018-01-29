
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish


class Utils(object):

    @staticmethod
    def standardizeResponse(value):
        if (type(value) == bytes):
            value = value.decode()

        if value == True:
            return True
        elif (value == 1):
            return True
        elif (value == 0):
            return False
        elif (value == False):
            return False
        if value == "True":
            return True
        elif (value == "1"):
            return True
        elif (value == "0"):
            return False
        elif (value == "False"):
            return False
        elif (value == "0"):
            return False
        elif (value == "1"):
            return True
        elif (type(value) == bool):
            return value
        elif (type(value) == int):
            return value
        elif (int(value) > 1):
            return value
        else:
            try:
                data = value.decode()
                print(data)
            except AttributeError:
                pass
            print("else")
            print(value, type(value))
        return value

    @staticmethod
    def deviceSet(value, topic, server, device):
        value = Utils.standardizeResponse(value)
        setTopic = "/" + device + "/" + topic.lower() + "/set"
        statusTopic = "/" + device + "/" + topic.lower() + "/status"
        try:
            msgs = [{'topic': setTopic, 'payload': value, 'retain': False},
                    {'topic': statusTopic, 'payload': value, 'retain': True}]

            publish.multiple(msgs, hostname=server[
                             'host'], port=server['port'])

        except Exception as e:

            raise

    @staticmethod
    def deviceStatus(topic, server, device, stan=False):
        statusTopic = "/" + device + "/" + topic + "/status"

        m = subscribe.simple(statusTopic,
                             hostname=server['host'], port=server['port'], retained=True, msg_count=1)

        if stan:
            return Utils.standardizeResponse(m.payload)

        return Utils.standardizeResponse(m.payload)
