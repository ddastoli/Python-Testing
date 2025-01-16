import requests

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

if __name__ == "__main__":
    # User inputs the API token
    api_token = input("Enter your Webex API token: ")
    room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vZDc4NmY5NTAtNzY5MC0xMWVmLWJkYzAtMDdhODkzNDViNDYz"
    message = "helloworld"

    # Send the message
    send_message_to_webex(api_token, room_id, message)
