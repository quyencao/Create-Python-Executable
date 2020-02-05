import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue = 'device_y'
# channel.queue_declare(queue=queue)

body = '{ "command": "source", "data": { "url": "https://qclibs.s3.amazonaws.com/samples/sources.zip" } }'
body2 = '{ "command": "model", "data": { "url": "https://qclibs.s3.amazonaws.com/samples/models.zip" } }'

# for i in range(10):
#     channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')

# print(" [x] Sent 'DOWNLOAD_SOURCE'")
# for i in range(2):
#     channel.basic_publish(exchange='', routing_key='device', body=body % (i))
# channel.basic_publish(exchange='message', routing_key=queue, body='{ "command": "run" }')
# time.sleep(5)
# channel.basic_publish(exchange='message', routing_key=queue, body=body2)
# time.sleep(2)
# channel.basic_publish(exchange='', routing_key=queue, body=body)
# time.sleep(2)
# print(" [x] Sent 'DOWNLOAD_MODEL'")
# for i in range(5):
#     channel.basic_publish(exchange='', routing_key='device4', body=body2 % (i))

# channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')
# time.sleep(0.02)
# channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')
# time.sleep(0.02)
channel.basic_publish(exchange='', routing_key=queue, body='{ "command": "run" }')
# time.sleep(0.01)
# channel.basic_publish(exchange='', routing_key='device10', body=body2)
connection.close()