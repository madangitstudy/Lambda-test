import json
import os
import urllib.request

# Function to send payload to Klaviyo
def send_to_klaviyo(payload):
    klaviyo_url = "https://a.klaviyo.com/api/track"
    headers = {
        "Authorization": f"Klaviyo-API-Key {os.getenv('KLAVIYO_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(klaviyo_url, data=data, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        return e.read()

# Lambda Handler
def lambda_handler(event, context):
    try:
        # Build the payload dynamically from the event
        payload = {
            "token": os.getenv("KLAVIYO_API_TOKEN"),  # Ensure you set this environment variable
            "event": "Flight Voucher Event",
            "Customer_properties": {
                "$email": event['primary_email']
            },
            "properties": {
                "flight_details": event['flight_details'],
                "passengers": event['passengers'],
                "flight_status": event['flight_status']
            }
        }

        # Send the payload to Klaviyo
        response = send_to_klaviyo(payload)

        return {
            'statusCode': 200,
            'body': json.dumps('Event pushed to Klaviyo successfully')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Internal server error: {str(e)}"
        }
