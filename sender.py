import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue = 'device_y'
channel.queue_declare(queue=queue)

body = '{ "command": "source", "data": { "id": "123", "path": "/home/quyencm/Desktop/device-mqtt-python/download", "url": "https://qclibs.s3.amazonaws.com/graphqlServer.zip" } }'
body2 = '{ "command": "model", "data": { "id": "123", "path": "/home/quyencm/Desktop/device-mqtt-python/download", "url": "https://5e1e9b844789c1ef9065c0f2.s3.amazonaws.com/groups/5e1e9ba74789c1ef9065c0f3-5e1e9bb74789c1ef9065c0f4/models/model_1579071240.zip?AWSAccessKeyId=AKIAJIFD6CBNQF5GVGFA&Signature=M2Zewh6m3M8vFvjDikU3923SA8s%3D&Expires=1579074851" } }'

# for i in range(10):
#     channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')

# print(" [x] Sent 'DOWNLOAD_SOURCE'")
# for i in range(2):
#     channel.basic_publish(exchange='', routing_key='device', body=body % (i))
# channel.basic_publish(exchange='', routing_key='device_10', body=body)
# print(" [x] Sent 'DOWNLOAD_MODEL'")
# for i in range(5):
#     channel.basic_publish(exchange='', routing_key='device4', body=body2 % (i))

# channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')
# time.sleep(0.02)
# channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')
# time.sleep(0.02)
channel.basic_publish(exchange='message', routing_key=queue, body='{ "command": "run" }')
# time.sleep(0.01)
# channel.basic_publish(exchange='', routing_key='device10', body=body2)
connection.close()