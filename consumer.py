import pika

def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

parameters = pika.URLParameters('amqp://guest:guest@localhost:5672')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='face_recog')

channel.basic_consume('face_recog', on_message)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()