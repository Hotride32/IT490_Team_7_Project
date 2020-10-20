import mysql.connector, pika, sys, os
    


def main():

    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='user_key')
    channel.queue_declare(queue='pass_key')
    
    
    def callback1(ch, method, properties, body):
        print(" [x] Received %r" % body)
        info = body.split()
        sql_query(info[0], info[1])
        
        
    def callback2(ch, method, properties, body):
        print(" [x] Received %r" % body)
        pass_word = body
     
    
    channel.basic_consume(queue='user_key', on_message_callback=callback1, auto_ack=True)
    channel.basic_consume(queue='pass_key', on_message_callback=callback2, auto_ack=True)
    #sql_query(user_name, pass_word)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    #sql_query(user_name, pass_word)

def sql_query(uname, pword):  
	cnx = mysql.connector.connect(
		host = "localhost",
		user = "test_user",
		password = "password",
		database = "db_test"
	)
	email = uname;
	password = pword;
	query = ("INSERT INTO accounts (email, password) VALUES(%s, %s);")
	mycursor = cnx.cursor()
	print("Cursor made")
	mycursor.execute(query, (uname, pword))
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
