import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='54.226.145.124'))
channel = connection.channel()

queue = 'device_1'
# channel.queue_declare(queue=queue)
# https://qclibs.s3.amazonaws.com/testsamples/node1.zip
body = '{ "command": "deploy_source", "node": "node2", "key": "downloadsource-node2-1", "data": { "url": "https://qclibs.s3.amazonaws.com/testsamples/node2.zip" } }'
body2 = '{ "command": "deploy_model", "node": "node2", "key": "downloadmodel-node2-1", "data": { "url": "https://qclibs.s3.amazonaws.com/testsamples/node2.zip" } }'

# for i in range(10):
#     channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')

# print(" [x] Sent 'DOWNLOAD_SOURCE'")
# for i in range(2):
#     channel.basic_publish(exchange='', routing_key='device', body=body % (i))
# channel.basic_publish(exchange='message', routing_key=queue, body='{ "command": "run" }')
# time.sleep(5)
# channel.basic_publish(exchange='message', routing_key=queue, body=body)
# time.sleep(2)
# channel.basic_publish(exchange='', routing_key=queue, body='{ "command": "DEPLOY", "node": "node2", "data": { "source_url": "https://qclibs.s3.amazonaws.com/testsamples/node2.zip", "model_url": "https://qclibs.s3.amazonaws.com/testsamples/node2.zip" } }')

# channel.basic_publish(exchange='', routing_key=queue, body='{ "command": "STOP_DEPLOY", "node": "node2" }')

# channel.basic_publish(exchange='', routing_key=queue, body=body)
# time.sleep(5)
# channel.basic_publish(exchange='', routing_key=queue, body=body)
channel.basic_publish(exchange='', routing_key=queue, body=body)
# channel.basic_publish(exchange='', routing_key=queue, body='{ "command": "stop_run_code" }')

# channel.basic_publish(exchange='', routing_key=queue, body='{ "command": "run_code", "node": "node3", "key": "node3node3", "data": null }')

# channel.basic_publish(exchange='', routing_key=queue, body='{ "command": "DEPLOY", "node": "node1" }')
# time.sleep(35);
# channel.basic_publish(exchange='', routing_key=queue, body=body)
# time.sleep(2)
# print(" [x] Sent 'DOWNLOAD_MODEL'")
# for i in range(5):
#     channel.basic_publish(exchange='', routing_key='device4', body=body2 % (i))

# channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')
# time.sleep(0.02)
# channel.basic_publish(exchange='', routing_key='device10', body='{ "command": "run" }')
# time.sleep(0.02)
# channel.basic_publish(exchange='', routing_key=queue, body='{ "command": "stop", "node": "node3" }')
# channel.basic_publish(exchange='', routing_key=queue, body='{ "command": "DOWNLOAD_MODEL" }')
# time.sleep(0.01)
# channel.basic_publish(exchange='', routing_key='device10', body=body2)
connection.close()