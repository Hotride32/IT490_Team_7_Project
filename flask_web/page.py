from flask import Flask, redirect, url_for, render_template, request, json, flash
import pika

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def home():
   return render_template("index.html")
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
	  #user = request.form["username"]
          #password = request.form["password"]
          #info = 'login' + ' ' + user + ' ' + password
          #channel.basic_publish(exchange='', routing_key='user_key', body=info)
          #print(user)
          #channel.basic_publish(exchange='', routing_key='pass_key', body=password)
          #connection.close()
          #     return redirect(url_for("user", usr=user))
          #elif request.method == "GET":
          #     return render_template("index.html")
          return redirect(url_for("login")) 
       else:
          user = request.form["username"]
          password = request.form["password"]
          info = 'register' + ' ' + user + ' ' + password
          channel.basic_publish(exchange='', routing_key='user_key', body=info)
          print(user)
          channel.basic_publish(exchange='', routing_key='pass_key', body=password)
          connection.close()
          return redirect(url_for("user", usr=user))
    elif request.method == "GET":
          return render_template("register.html")
    

@app.route("/login", methods=["POST", "GET"])
def login():
    credentials = pika.PlainCredentials('testuser', 'testuser')
    connection = pika.BlockingConnection( pika.ConnectionParameters('10.243.84.199',5672,'/',credentials))
    #cconnection = pika.BlockingConnection( pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue='user_key')
    channel.queue_declare(queue='pass_key')
    if request.method == "POST":
       if request.form.get("register"):
          return redirect(url_for("register"))
       else:
          user = request.form["username"]
          password = request.form["password"]
          info = 'login' + ' ' +  user + ' ' + password
          channel.basic_publish(exchange='', routing_key='user_key', body=info)

          

          channel.queue_declare(queue='access')

          def check(work):
             if(work == 'logged'):
                  print("successful log in")
                  flash('You were successfully logged in')
                  #connection.close()
                  #return redirect(url_for("logged")
                  return render_template("logged.html")
                  #return redirect(url_for("user", usr=work))
             else:
                  print('failed log in')
                  flash('Incorrect log in')
                  #connection.close()
                  #return redirect(url_for("logged")
                  return render_template("logged.html")
                  #return redirect(url_for("user", usr="failed"))



          def callback2(ch, method, properties, body):
              print(" [x] Received %r" % body)
              l = body.decode('utf-8')
              return check(l)


          channel.basic_consume(queue='access', on_message_callback=callback2, auto_ack=True)
          channel.start_consuming()


          connection.close()
          #return redirect(url_for("logged")
          return render_template("logged.html")
          #return redirect(url_for("user", usr=user))
    elif request.method == "GET":
          return render_template("login.html")
    
@app.route("/leaderboard", methods =["GET"])
def leaderboard():
    scores = [1.0,2.0,3.0]
    #names = ["name" : "12-31-18", " name" : "01-01-19", "name" : "01-02-19"] 
    names = [{ "Name": "zbc", "Rank": 50 , "Score": 5000 },{ "Rank": "25", "Name": "swimming", "Score": 2043 },  { "Name": "xyz", "Rank": "2", "Score": 500 }];

    data = json.dumps( scores )
    labels = json.dumps( names )
    #print(labels)
    return render_template("Leaderboard.html", data=data, labels=labels)

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/logged")
def logged():
    #flash('You were successfully logged in')
    return render_template("logged.html")

if __name__ == "__main__":
    app.run(debug=True)
    
