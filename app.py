from flask import Flask,request,url_for,redirect,render_template,session,flash
from utils import manager

app=Flask(__name__)

@app.route("/")
def index():
    print manager.getIDs()
    return render_template("index.html")

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/login", methods=['GET','POST'])
def login():
    print "login"
    return render_template("login.html", loggedin=False)

@app.route("/register",methods=['GET','POST'])
def register():
    ids= manager.getIDs()
    if 'username' in session:
        loggedin=True
        username=session['username']
    else:
        loggedin=False
        username=''
    if request.method=='POST':
        if 'username' not in session:
            username = request.form['username']
            password = request.form['password']
            reppassword = request.form['password2']
            reason = ""
            registered=False

            if password == reppassword:
                registered=True
            else:
                registered=False
                reason = "Passwords do not match"
                print "Passwords do not match"
            manager.finishRegistration(username,password,registered)
            if registered:
                return render_template("register.html", page=1, username=username,ids=ids)
        return render_template("register.html", page=2, reason=reason,ids=ids)
    else:
        return render_template("register.html", page=3, loggedin=loggedin, username=username, ids=ids) 

@app.route("/canvas")
def canvas():
    return render_template("canvas.html")

if __name__=="__main__":
    app.debug=True
    app.secret_key="Dankmemesbro"
    app.run()

#testbranch
