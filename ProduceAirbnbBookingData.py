import random
import string
import json
import datetime
import os
import boto3

# make sure to create env variable NUM_RECORDS and SQS_QUEUE_UR 
# this scritp generates the airbnd data in realtime
# Initialize SQS client
sqs = boto3.client('sqs')

def generate_booking_data(num_records):
    booking_data = []
    for _ in range(num_records):
        booking_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        property_id = random.randint(1000, 9999)
        location = random.choice(["New York, USA", "London, UK", "Paris, France", "Tokyo, Japan", "Sydney, Australia"])
        start_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))
        end_date = start_date + datetime.timedelta(days=random.randint(1, 14))
        price = round(random.uniform(50, 500), 2)
        
        booking_record = {
            'bookingId': booking_id,
            'userId': user_id,
            'propertyId': property_id,
            'location': location,
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'price': price
        }
        booking_data.append(booking_record)
    
    return booking_data

def lambda_handler(event, context):
    num_records = int(os.environ['NUM_RECORDS']) if 'NUM_RECORDS' in os.environ else 10
    booking_data = generate_booking_data(num_records)
    
    # Send booking data to SQS
    queue_url = os.environ['SQS_QUEUE_URL']  # Retrieve SQS queue URL from environment variable
    print ("Queue URL: ",queue_url)
    for booking_record in booking_data:
        # Send each booking record as a message to SQS
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(booking_record)
        )
        print(f"Sent message to SQS: {response['MessageId']}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Booking data sent to SQS successfully')
    }
