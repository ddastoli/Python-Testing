import requests
from kafka import KafkaConsumer
import json
from config import *

def send_message_to_webex(api_token, room_id, message):
    """
    Sends a message to a Cisco Webex room.

    Parameters:
        api_token (str): Webex API access token.
        room_id (str): ID of the Webex room.
        message (str): The message to send.

    Returns:
        dict: Response from the Webex API.
    """
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "roomId": room_id,
        "text": message
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

    return response.json()

def consume_messages_and_send(api_token, room_id, kafka_server, kafka_topic):
    """
    Consumes messages from a Kafka topic and sends them to a Webex room.

    Parameters:
        api_token (str): Webex API access token.
        room_id (str): ID of the Webex room.
        kafka_server (str): Kafka server address.
        kafka_topic (str): Kafka topic to consume messages from.
    """
    consumer = KafkaConsumer(
        kafka_topic,
        bootstrap_servers=[kafka_server],
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    print(f"Listening for messages on topic '{kafka_topic}' from Kafka server '{kafka_server}'...")

    for message in consumer:
        formatted_message = json.dumps(message.value, indent=4)
        print(f"Received message: {formatted_message}")
        send_message_to_webex(api_token, room_id, formatted_message)

if __name__ == "__main__":
    api_token = WEBEX_API_TOKEN  # Retrieved from the config file
    room_id = ROOM_ID # Retrieved from the config file
    kafka_server = KAFKA_SERVER
    kafka_topic = TOPIC

    # Consume messages from Kafka and send to Webex
    consume_messages_and_send(api_token, room_id, kafka_server, kafka_topic)
