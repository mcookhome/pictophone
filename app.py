from flask import Flask,request,url_for,redirect,render_template,session,flash
from auth import auth
app=Flask(__name__)

@app.route("/")
def index:
    return render_template("index.html")

@app.route("/base")
def base:
    return render_template("base.html")

@app.route("/login")
def login:
    return render_template("login.html")


if __name__=="main":
    app.debug=True
    app.secret_key="Dankmemesbro"
    app.run()

#testbranch
