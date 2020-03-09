import pika

def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

parameters = pika.URLParameters('amqp://guest:guest@54.226.145.124:5672')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='publish_queue')

channel.basic_consume('publish_queue', on_message)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()