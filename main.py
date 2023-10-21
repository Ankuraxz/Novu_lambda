import boto3
import json
import os
import urllib3
import logging
import time
import uuid

# Initialize AWS clients using environment variables
aws_access_key_id = os.environ['AWS_ACCESS']
aws_secret_access_key = os.environ['AWS_SECRET']
aws_region = "us-east-1"
novu_key = os.environ['NOVU_KEY']

# Initialize AWS clients
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

Sender_email = "ankurvermaaxz@gmail.com"
recipient_email = "ankuraxz2000@gmail.com"

def send_mail(payload):
    """
    Send EMAIL with NOVU API
    :param payload:
    :return:
    """
    url = 'https://api.novu.co/v1/events/trigger'
    headers = {
        'Authorization': 'ApiKey ' + novu_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data = {
        "name": "emailerworkflow",
        "to":{
            "subscriberId": str(uuid.uuid4()),
            "email": recipient_email
        },
        "payload": ({'Message': "Hi User !",'Results': json.dumps(payload)})
    }

    # Send the POST request
    http = urllib3.PoolManager()
    encoded_data = json.dumps(data).encode('utf-8')
    response = http.request('POST', url, headers=headers, body=encoded_data)

    return response

def lambda_handler(event, context):
    """
    Lambda handler
    :param event:
    :param context:
    :return:
    """
    try:
        bucket_name = 'helpernovubucket'
        print(event)
        send_mail(event)
        return {
            'statusCode': 200,
            'body': json.dumps('Email Sent')
        }
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }
