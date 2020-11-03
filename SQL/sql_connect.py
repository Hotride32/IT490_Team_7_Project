import mysql.connector, pika, sys, os
    


def main():

    credentials = pika.PlainCredentials('testuser','testuser')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.243.154.71',5672,'/',credentials))
    channel = connection.channel()

    channel.queue_declare(queue='user_key')
    channel.queue_declare(queue='pass_key')
    channel.queue_declare(queue='access')
    
    
    def callback1(ch, method, properties, body):
        print(" [x] Received %r" % body)
        b = body.decode('utf-8')
        info = b.split()
        sql_query(info[0], info[1], info[2], channel)
        
        
    def callback2(ch, method, properties, body):
        print(" [x] Received %r" % body)
        pass_word = body
     
    
    channel.basic_consume(queue='user_key', on_message_callback=callback1, auto_ack=True)
    channel.basic_consume(queue='pass_key', on_message_callback=callback2, auto_ack=True)
    #sql_query(user_name, pass_word)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    #sql_query(user_name, pass_word)

def sql_query(opt, uname, pword, channel):  
	cnx = mysql.connector.connect(
		host = "localhost",
		user = "backend",
		password = "password",
		database = "db_test"
	)
	mycursor = cnx.cursor()
	print("Cursor made")
	option = '%s' % opt
	email = uname
	password = pword
	print("if")
	print(option, email, password)
	if option == 'register':
		print("Register")
		query = ("INSERT INTO accounts (email, password) VALUES(%s, %s);")
		mycursor.execute(query, (uname, pword))
	elif option == 'login':
		query = ("SELECT * FROM accounts WHERE email='%s' AND password='%s';" % (uname, pword))
		mycursor.execute(query)
		myresult = mycursor.fetchall()
		print(len(myresult))
		if len(myresult) > 0:
			print("logged")
			channel.basic_publish(exchange='',routing_key='access',body='logged')
		else:
			channel.basic_publish(exchange='',routing_key='access',body='invalid')
	else:
		print("Didnt work")
	
	cnx.commit()
	cnx.close()
	
#print("Connection Established")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
            
print("Connection Closed")
