from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

#@app.route("/")
#def home():
#    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
       if request.form.get("register"):
          return redirect(url_for("register")) 
       else:
          user = request.form["username"]
          password = request.form["password"]
          return redirect(url_for("user", usr=user))
    elif request.method == "GET":
          return render_template("index.html")
    

@app.route("/register")
def register():
    return render_template("register.html") 
    
@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
    

