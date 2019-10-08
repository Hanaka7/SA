import boto3


def delete(QueueName):
    sqs = boto3.resource('sqs')
    try:
        queue = sqs.get_queue_by_name(QueueName=QueueName)
        queue.delete()
    except Exception as e:
        print(e)


delete('test1.fifo')
