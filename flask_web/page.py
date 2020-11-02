from flask import Flask, redirect, url_for, render_template, request
import pika

app = Flask(__name__)

#@app.route("/")
#def home():
#    return render_template("index.html")
#app.run(host='0.0.0.0')

@app.route("/register", methods=["POST", "GET"])
def register():
    credentials = pika.PlainCredentials('testuser', 'testuser')
    connection = pika.BlockingConnection( pika.ConnectionParameters('10.243.84.199',5672,'/',credentials))
    channel = connection.channel()
    channel.queue_declare(queue='user_key')
    channel.queue_declare(queue='pass_key')
    if request.method == "POST":
       if request.form.get("login"):
          return redirect(url_for("login")) 
       else:
          user = request.form["username"]
          password = request.form["password"]
          info = user + ' ' + password
          channel.basic_publish(exchange='', routing_key='user_key', body=info)
          print(user)
          channel.basic_publish(exchange='', routing_key='pass_key', body=password)
          connection.close()
          return redirect(url_for("user", usr=user))
    elif request.method == "GET":
          return render_template("index.html")
    

@app.route("/login")
def login():
    return render_template("login.html") 
    
@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
    
