import paho.mqtt.client as mqtt_client
import json


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code {}".format(rc))

    client = mqtt_client.Client(client_id="berlin")
    client.username_pw_set("chen", "0000")
    client.on_connect = on_connect
    client.connect("140.112.94.129", 20010, 60)
    return client


def on_message(client, userdata, msg):
    rx = msg.payload.decode()
    json_rx = json.loads(rx)
    print(json_rx)


if __name__ == '__main__':

    client = connect_mqtt()
    client.subscribe("mqtt_class/test")

    client.on_message = on_message
    client.loop_forever()


