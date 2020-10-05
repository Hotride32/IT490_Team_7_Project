import pika

connection = pika.BlockingConnection()
channel = connection.channel()
channel.basic_publish(exchange='test', routing_key='test',
                      body=b'Test message.')
connection.close()
