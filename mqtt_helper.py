import paho.mqtt.client as mqtt
import logging
import time
import json

# MQTT Configuration
# MQTT_BROKER = "mqtt.talemate.co"
# MQTT_PORT = 1884
# MQTT_USERNAME = "c-dc78de52-a2e9-4eec-a19f-1812294d78f2"
# MQTT_PASSWORD = "c68c51e8-8048-46bb-aee3-e2b193a74f10"
# MQTT_TOPIC = "zbos/CA019UBT20000010/dialog/set"

MQTT_BROKER = "platform.qltyss.com"
MQTT_PORT = 1884
MQTT_USERNAME = "c-07d78f4e-3307-4f70-87fb-582bb7292406"
MQTT_PASSWORD = "8810e03b-77ba-4d6c-aad6-e71644f9a9f3"
MQTT_TOPIC = "zbos/CA019UBT20000010/dialog/set"




logger = logging.getLogger(__name__)



# Connect function (includes reconnect logic)
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            logger.info("Connected to MQTT Broker!")
        else:
            print("failed!")
            logger.error("Failed to connect, return code %d", rc)

    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set()
    client.on_connect = on_connect
    backoff_time = 1
    while True:  # Attempt connection indefinitely
        try:
            logger.info("Connecting to MQTT Broker...")
            client.connect(MQTT_BROKER, MQTT_PORT)
            return client
        except Exception as e:
            logger.warning(f"Connection failed: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            backoff_time *= 2  # Increase backoff time

# Publish function
def publish_message(client, topic, message,lang):
    if not client.is_connected():
        client = connect_mqtt()  # Attempt to reconnect if necessary
    try:
        if lang == "ar-SA":
            data = {
            "requestId": "1",
            "message": message,
            "speed": 100,
            "language": lang,
            "gesticulation": "true",
            "pitch": 100,
            "voice":"Maged"
        }
        else:
            data = {
            "requestId": "1",
            "message": message,
            "speed": 100,
            "language": lang,
            "gesticulation": "true",
            "pitch": 100
        }

        response_payload = json.dumps(data)
        result = client.publish(topic, response_payload)
        status = result[0]
        if status == 0:
            logger.info(f"Sent message to topic '{topic}'")
        else:
            logger.error(f"Failed to send message to topic '{topic}'")
    except Exception as e:
        logger.error(f"Error publishing message: {e}")
        
        
    client.disconnect()  # Disconnect after publishing