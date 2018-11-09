from __future__ import print_function
import boto3
import json
import os

bucket = os.environ['BUCKET']
s3 = boto3.client('s3')

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    notification_type = message['notificationType']
    timestamp, report = handlers.get(notification_type, handle_unknown_type)(message)
    save_nortification(notification_type, timestamp, report)


def save_nortification(notification_type, timestamp, report):
    keyname = notification_type + '/' + timestamp
    print('Saving s3://' + bucket + '/' + keyname + ':' + report)
    s3.put_object(Bucket=bucket, Key=keyname , Body=report)


def handle_bounce(message):
    message_id = message['mail']['messageId']
    bounced_recipients = message['bounce']['bouncedRecipients']
    addresses = list(
        recipient['emailAddress'] for recipient in bounced_recipients
    )
    bounce_type = message['bounce']['bounceType']
    timestamp = message['bounce']['timestamp']
    report = "Message %s bounced when sending to %s. Bounce type: %s" % \
        (message_id, ", ".join(addresses), bounce_type)
    return (timestamp, report)


def handle_complaint(message):
    message_id = message['mail']['messageId']
    complained_recipients = message['complaint']['complainedRecipients']
    addresses = list(
        recipient['emailAddress'] for recipient in complained_recipients
    )
    timestamp = message['complaint']['timestamp']
    report = "A complaint was reported by %s for message %s." % \
          (", ".join(addresses), message_id)
    return (timestamp, report)


def handle_delivery(message):
    message_id = message['mail']['messageId']
    delivery_timestamp = message['delivery']['timestamp']
    timestamp = message['delivery']['timestamp']
    report = "Message %s was delivered successfully at %s" % \
          (message_id, delivery_timestamp)
    return (timestamp, report)


def handle_unknown_type(message):
    print("Unknown message type:\n%s" % json.dumps(message))
    raise Exception("Invalid message type received: %s" % \
                    message['notificationType'])


handlers = {"Bounce": handle_bounce,
            "Complaint": handle_complaint,
            "Delivery": handle_delivery}
