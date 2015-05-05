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
    ids= manager.getIDs()
    if 'username' in session:
        luser = session['username']
        return render_template("login.html", loggedin=True, username=luser,ids=ids)
    
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        print 'Username and Password have been recorded as variables'
        savedpass="not"
        loggedin = False
        reason = ""
        savedpass = manager.finishLogin(username)
        print savedpass == ""
       
        if (savedpass == password):
            loggedin = True
        if (savedpass != password):
            reason = "Your username and password do not match"
        if savedpass == "":
            reason = "The username "+ username + " does not exist."
        if loggedin:
            session['username']=username
        
      
        return render_template("login.html", loggedin=loggedin, username=username, reason=reason, ids=ids)
    else:
        print session
        return render_template("login.html", loggedin=False, ids=ids)

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

@app.route("/logout",methods=['GET','POST'])
def logout():
   ids=manager.getIDs()
   if 'username' in session:
      session.pop('username', None)
      print "login status: logged in"
      return render_template("logout.html", loggedin=False, previous=True, ids=ids)
   else:
      print "login status: not logged in"
      return render_template("logout.html",loggedin=False, previous=False, ids=ids)
    
@app.route("/canvas")
def canvas():
    return render_template("canvas.html")

if __name__=="__main__":
    app.debug=True
    app.secret_key="Dankmemesbro"
    app.run()

#testbranch
