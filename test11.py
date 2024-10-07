import json
import urllib.request
import os

# Function to send payload to Klaviyo using urllib
def send_to_klaviyo(payload):
    klaviyo_url = "https://a.klaviyo.com/api/track"
    
    headers = {
        "Authorization": f"Klaviyo-API-Key {payload['token']}",
        "Content-Type": "application/json"
    }
    
    request_headers = {key: value for key, value in headers.items()}
    
    data = json.dumps(payload).encode("utf-8")
    
    request = urllib.request.Request(klaviyo_url, data=data, headers=request_headers)
    
    try:
        with urllib.request.urlopen(request) as response:
            response_data = response.read().decode("utf-8")
            return response_data
    except urllib.error.HTTPError as e:
        return f"HTTPError: {e.code}, {e.reason}"
    except urllib.error.URLError as e:
        return f"URLError: {e.reason}"

# Lambda Handler
def lambda_handler(event, context):
    try:
        # Build the payload dynamically from the event
        payload = {
            "token": "your_actual_klaviyo_api_token",  # Replace with actual token or pass it via environment variable
            "event": "OTPG voucher email",
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
            'body': json.dumps(f'Event pushed to Klaviyo successfully: {response}')
        }
    
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': f"Missing key in event: {str(e)}"
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Internal server error: {str(e)}"
        }
