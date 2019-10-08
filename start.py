import boto3


def create(QueueName):
    sqs = boto3.resource('sqs')
    try:
        sqs.create_queue(QueueName=QueueName, Attributes={'FifoQueue':'true', 'ContentBasedDeduplication':'true'})
    except Exception as e:
        print(e)


create('test1.fifo')
