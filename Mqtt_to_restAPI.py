import paho.mqtt.client as mqtt
import requests
import json

# MQTT 브로커 설정
MQTT_BROKER = "172.18.0.3"  # 브로커 주소
MQTT_PORT = 1883           # 브로커 포트
MQTT_TOPIC = "topic/sensor1"  # 구독할 토픽

# 기본 REST API 엔드포인트 (JSON 메시지에 없을 경우)
DEFAULT_API_ENDPOINT = "http://172.18.0.2:5001/submodels/aHR0cC4vL2k0MC5jdXN0b21lci5jb20vdHlwZS8xLzEvN0E3MTA0QkRBQjU3RTE4NA/submodel/submodel-elements/MaxRotationSpeed/"

# 메시지 수신 핸들러
def on_message(client, userdata, msg):
    try:
        # 수신된 MQTT 메시지 디코딩
        payload = msg.payload.decode('utf-8')
        print(f"Received MQTT message on topic '{msg.topic}': {payload}")

        # JSON 메시지 파싱
        data = json.loads(payload)

        # REST API 호출
        headers = {
            "accept": "*/*",
            "Content-Type": "application/json-patch+json"
        }
        response = requests.put(DEFAULT_API_ENDPOINT, headers=headers, json=data)
        print(f"REST API Response: {response.status_code} - {response.text}")

    except json.JSONDecodeError:
        print("Error: Invalid JSON format in MQTT message payload.")
    except Exception as e:
        print(f"Error processing message: {e}")

# MQTT 연결 핸들러
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker.")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")

# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# MQTT 서버 시작
def start_mqtt_to_rest():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        print(f"MQTT to REST API bridge is running on port {MQTT_PORT}...")
        client.loop_forever()
    except Exception as e:
        print(f"Error starting MQTT to REST bridge: {e}")

if __name__ == "__main__":
    start_mqtt_to_rest()
