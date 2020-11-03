
import pika

credentials = pika.PlainCredentials('testuser', 'testuser')
connection = pika.BlockingConnection( pika.ConnectionParameters('10.243.84.199',5672,'/',credentials))
#connection = pika.BlockingConnection(
 #   pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

print( "Enter SQL Statement: ")
bodStr = input()

channel.basic_publish(exchange='', routing_key='hello', body='%r' % bodStr)
print(" [x] Sent '%r'" % bodStr)
connection.close()
