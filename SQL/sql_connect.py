import mysql.connector
print("SQL Connector imported")

cnx = mysql.connector.connect(
	host = "localhost",
	user = "test_user",
	password = "password",
	database = "db_test"
)
	
print("Connection Established")



query = ("INSERT INTO accounts (email, password) VALUES(%s, %s);")
mycursor = cnx.cursor()
print("Cursor made")

mycursor.execute(query, (email, data_password))

cnx.commit()
cnx.close()
print("Connection Closed")
