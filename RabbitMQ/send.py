import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

print( "Enter SQL Statement: ")
bodStr = input()

channel.basic_publish(exchange='', routing_key='hello', body='%r' % bodStr)
print(" [x] Sent '%r'" % bodStr)
connection.close()
