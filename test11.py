import json
import urllib.request
import base64
import os
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VoucherDetails')  # Your DynamoDB table name

    # Query DynamoDB to find vouchers that need to be generated
    vouchers_to_generate = []
    
    try:
        response = table.scan()  # Consider using query for more specific results
        items = response.get('Items', [])
        
        for item in items:
            # Check if voucher code or ID is not set
            if not item.get('VoucherID'):
                vouchers_to_generate.append(item)

    except ClientError as e:
        print(f"Error retrieving data from DynamoDB: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to retrieve data from DynamoDB'})
        }

    # Process vouchers that need to be generated
    for voucher in vouchers_to_generate:
        pnr = voucher.get('PNR')
        voucher_id = voucher.get('ID')  # Using the ID field here

        if not pnr:
            print(f"Skipping entry without a valid PNR: {voucher}")
            continue

        # Generate the voucher (mock API request for example purposes)
        try:
            voucher_code = generate_voucher_for_pnr(pnr)
            
            # Update DynamoDB with the generated voucher code
            update_response = table.update_item(
                Key={'PNR': pnr, 'ID': voucher_id},  # Ensure you're using the correct keys
                UpdateExpression="SET VoucherCode = :v_code",
                ExpressionAttributeValues={':v_code': voucher_code}
            )
            print(f"Voucher updated for PNR {pnr} with VoucherCode {voucher_code}")

        except Exception as e:
            print(f"Error generating or updating voucher for PNR {pnr}: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Vouchers processed and updated.'})
    }

def generate_voucher_for_pnr(pnr):
    # Simulated voucher generation function
    # In your case, this would be replaced with an API call to generate the voucher
    return f"VCHR-{base64.urlsafe_b64encode(pnr.encode()).decode()[:8]}"
