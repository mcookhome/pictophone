from flask import Flask,request,url_for,redirect,render_template,session,flash

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/canvas")
def canvas():
    return render_template("canvas.html")

if __name__=="__main__":
    app.debug=True
    app.secret_key="Dankmemesbro"
    app.run()

#testbranch
