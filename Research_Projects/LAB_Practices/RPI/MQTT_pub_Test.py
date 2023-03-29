import datetime
import time

import paho.mqtt.client as mqtt
import json

while True:
    try:

        t_format = '%m-%d %H:%M'
        t = datetime.datetime.now().strftime(t_format)
        payload = {"Tiem": t, "Name": "Berlin"}

        client = mqtt.Client(client_id="berlin")
        client.username_pw_set('chen', '0000')
        client.connect('140.112.94.129', 20010, 60)

        client.publish("mqtt_class/test", json.dumps(payload))
        print(payload)
        time.sleep(30)

    except Exception as exc:
        print(exc)




