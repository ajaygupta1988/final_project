import boto3
from config import settings


class MessagingQueue:
    def __init__(self, client=None) -> None:
        # queue instace class
        self.client = client or boto3.client(
            "sqs", endpoint_url=settings.aws_sqs_endpoint
        )
        self.queue_url = settings.queue_url

    def send_message(self, message_body):
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message_body,
        )
        return response

    def recieve_message(self):
        response_from_queue = self.client.receive_message(QueueUrl=self.queue_url)
        return response_from_queue["Messages"]

    def delete_message(self, receipt_handle):
        response = self.client.delete_message(
            QueueUrl=self.queue_url, ReceiptHandle=receipt_handle
        )
        return response
