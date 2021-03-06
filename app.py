from flask import Flask,request,url_for,redirect,render_template,session,flash
from utils import manager, match

app=Flask(__name__)
app.secret_key="Dankmemesbro"

@app.route("/",methods=['GET','POST'])
def index():
    print manager.getGames()
    ids= manager.getIDs()
    if 'username' in session:
        loggedin=True
        username=session['username']
        print username
        myGames=manager.getUserGames(username)
        if request.method=='POST':
            if request.form["submit"] == "Go":
                if manager.getProfilePath() != "profile/":
                    return redirect(manager.getProfilePath())

        print ids
        return render_template("base.html", loggedin=loggedin, username=username,ids=ids,myGames=myGames)
    else:
        loggedin=False
        username = '-'
        print loggedin
        return render_template("base.html", loggedin=loggedin, username=username,ids=ids)

@app.route("/game",methods=['GET','POST'])
@app.route("/game/<name>",methods=['GET','POST'])
def game(name=None):
    ids= manager.getIDs()
    if 'username' in session:
        loggedin=True
        username=session['username']
        myGames=manager.getUserGames(username)
        if request.method=='POST':
            if request.form["submit"] == "Go":
                if manager.getProfilePath() != "profile/":
                    return redirect(manager.getProfilePath())
        if name is None:
            gamelist=manager.getCompleteGames()
            #print gamelist
            return render_template("game.html",loggedin=loggedin,username=username,ids=ids,gamelist=gamelist,myGames=myGames)
        print name
        gameFax=manager.getGameFax(name)
        starts=gameFax[0][2]
        ends=gameFax[-1][2]
        percent=match.match(starts,ends)
        percent=int(round(abs(percent)*100))
        
        finished=manager.isComplete(name)
        if finished is False:
            return render_template("game.html",loggedin=loggedin,username=username,ids=ids,reason="This game is still in progress!",myGames=myGames)
        else:
            return render_template("game.html", loggedin=loggedin, username=username,ids=ids,gameFax=gameFax,name=name,myGames=myGames,percent=percent)
    else:
        loggedin=False
        username = '-'
        return render_template("game.html", loggedin=loggedin, username=username,ids=ids)

@app.route("/profile",methods=['GET','POST'])
@app.route("/profile/<name>",methods=['GET','POST'])
def profile(name=None):
    ids= manager.getIDs()
    if 'username' in session:
        loggedin=True
        username=session['username']
        myGames=manager.getUserGames(username)
        theirgames=manager.getUserGames(name)
        users=manager.getAllUsers()
        if name is None:
            #print users
            return render_template("profile.html",loggedin=loggedin,username=username,ids=ids,users=users)
        if request.method=='POST':
            if request.form["submit"] == "Go":
                if manager.getProfilePath() != "profile/":
                    return redirect(manager.getProfilePath())
        print name
        if name not in users:
            return render_template("game.html",loggedin=loggedin,username=username,ids=ids,reason="There is no user with this name!", myGames=myGames)
        return render_template("profile.html", loggedin=loggedin, username=username,ids=ids,name=name,myGames=myGames,theirgames=theirgames)
    else:
        loggedin=False
        username = '-'
        return render_template("profile.html", loggedin=loggedin, username=username,ids=ids)

@app.route("/creategame",methods=['GET','POST'])
def creategame():
    ids= manager.getIDs()
    if 'username' in session:
        loggedin=True
        username=session['username']
        myGames=manager.getUserGames(username)
        if request.method=='POST':
            if request.form["submit"] == "Go":
                if manager.getProfilePath() != "profile/":
                    return redirect(manager.getProfilePath())
            if request.form["submit"] == "Start":
                gamename= request.form["name"]
                gamescenario=request.form["styled-textarea"]
                gamelength=request.form["turns"]
                if (gamename==""):
                    reason="Please enter a game name."
                    return render_template("creategame.html",loggedin=loggedin,username=username,ids=ids,reason=reason,myGames=myGames)
                if (gamescenario==""):
                    reason="Please enter a scenario."
                    return render_template("creategame.html",loggedin=loggedin,username=username,ids=ids,reason=reason,myGames=myGames)
                if (manager.exists(gamename)):
                    reason="This name is not unique. Please try another."
                    return render_template("creategame.html",loggedin=loggedin,username=username,ids=ids,reason=reason,myGames=myGames)
                else:
                    manager.newGame(gamename,username,gamescenario,gamelength)
                    manager.needsDrawing(gamename,username,gamescenario)
                    flash("Success!")
                    return redirect("/")
        print ids
        return render_template("creategame.html", loggedin=loggedin, username=username,ids=ids,myGames=myGames)
    else:
        loggedin=False
        username = '-'
        return render_template("creategame.html", loggedin=loggedin, username=username,ids=ids)

@app.route("/joingame",methods=['GET','POST'])
def joingame():
    ids= manager.getIDs()
    if 'username' in session:
        loggedin=True
        username=session['username']
        myGames=manager.getUserGames(username)
        if request.method=='POST':
            if request.form["submit"] == "Go":
                if manager.getProfilePath() != "profile/":
                    return redirect(manager.getProfilePath())

        print ids
        return render_template("jumpin.html", loggedin=loggedin, username=username,ids=ids,myGames=myGames)
    else:
        loggedin=False
        username = '-'
        return render_template("jumpin.html", loggedin=loggedin, username=username,ids=ids)

@app.route("/write",methods=['GET','POST'])
def write():
    ids= manager.getIDs()
    if 'username' in session:
        loggedin=True
        username=session['username']
        myGames=manager.getUserGames(username)
        gameInfo=manager.getWriteGameInfo()
        games=True
        if gameInfo==None:
            games=False
            reason= "There are currently no pictures to describe. Sorry!"
            return render_template("write.html",loggedin=loggedin,username=username,ids=ids,reason=reason,games=games,myGames=myGames)
        gamename=manager.revert(gameInfo[2])
        pictureURL=manager.revert(gameInfo[3])
        if request.method=='POST':
            if request.form["submit"] == "Go":
                if manager.getProfilePath() != "profile/":
                    return redirect(manager.getProfilePath())
            if request.form["submit"] == "Submit":
                gamescenario=request.form["styled-textarea"]
                if (gamescenario=="" or gamescenario=="Describe here!"):
                    error="Please enter a scenario"
                    print error
                    return render_template("write.html",loggedin=loggedin,username=username,ids=ids,error=error,games=games,pictureURL=pictureURL,gamename=gamename,myGames=myGames)
                done=manager.updateGame(gamename,username,gamescenario)
                manager.completeDescription(gamename)
                if (done is False):
                    print "are we here- write"
                    manager.needsDrawing(gamename,username,gamescenario)
                flash("Success!")
                return redirect("/")
        return render_template("write.html", loggedin=loggedin, username=username,ids=ids,pictureURL=pictureURL,games=games,gamename=gamename,myGames=myGames)
    else:
        loggedin=False
        username = '-'
        return render_template("write.html", loggedin=loggedin, username=username,ids=ids)


@app.route("/picture",methods=['GET','POST'])
@app.route("/picture/<num>",methods=['GET','POST'])
def picture(num=-1):
    num=int(num)
    ids= manager.getIDs()
    if 'username' in session:
        loggedin=True
        username=session['username']
        myGames=manager.getUserGames(username)
        if request.method=='POST':
            if request.form["submit"] == "Go":
                if manager.getProfilePath() != "profile/":
                    return redirect(manager.getProfilePath())
        
        print ids
        print num
        dataUrl=manager.getPicture(num)
        if dataUrl == -1:
            return render_template("picture.html",loggedin=loggedin,username=username,ids=ids,reason="There is no picture with that ID!",myGames=myGames)
        else:
            return render_template("picture.html", loggedin=loggedin, username=username,ids=ids,dataUrl=dataUrl,myGames=myGames)
    else:
        loggedin=False
        username = '-'
        return render_template("picture.html", loggedin=loggedin, username=username,ids=ids)



@app.route("/login", methods=['GET','POST'])
def login():
    ids= manager.getIDs()
    if 'username' in session:
        luser = session['username']
        myGames=manager.getUserGames(username)
        return render_template("login.html", loggedin=True, username=luser,ids=ids,myGames=myGames)
    
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
            matchpass = True
            if password == reppassword:
                registered=True
            else:
                registered=False
                reason = "Passwords do not match"
                if len(password)>4 and len(password)<16 and len(reppassword)>4 and len(reppassword)<16:
                    matchpass = False
                print "Passwords do not match"
            info= manager.finishRegistration(username,password,registered)
            registered=info[0]
            reason=info[1]
            if not matchpass:
                reason = "Passwords do not match"
            if registered:
                session['username']=username
                return render_template("register.html", page=1, username=username,ids=ids)
        return render_template("register.html", page=2, reason=reason,ids=ids)
    else:
        return render_template("register.html", page=3, loggedin=loggedin, username=username, ids=ids) 

@app.route("/canvas", methods=['GET','POST'])
def canvas():
    ids=manager.getIDs();
    sentence=None
    if 'username' in session:
        username=session['username']
        loggedin=True
        myGames=manager.getUserGames(username)
        gameInfo=manager.getDrawGameInfo()
        print gameInfo
        games=True
        if gameInfo==None:
            games=False
            reason= "There are currently no sentences to depict. Sorry!"
            return render_template("canvas.html",loggedin=loggedin,username=username,ids=ids,reason=reason,games=games,myGames=myGames)
        gameName=manager.revert(gameInfo[2])
        sentence=manager.revert(gameInfo[3])
        if request.method=='POST':
            print "wemadeit"
            if request.form["submit"] == "publish":
                dataUrl= request.form["dataurl"]
                manager.storePicture(username,dataUrl)
                done=manager.updateGame(gameName,username,dataUrl)
                if (done is False):
                    manager.needsDescription(gameName,username,dataUrl)
                flash('success')
                return redirect("/")
    else:
        loggedin=False
        username=""
    return render_template("canvas.html",ids=ids,loggedin=loggedin,sentence=sentence,games=games)

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
   #logout

@app.route("/wipe")
def wipe():
    manager.wipegames()
    return redirect("/")
@app.route("/base")
def base():
    return render_template("base.html")


if __name__=="__main__":
    app.debug=True
    app.secret_key="Dankmemesbro"
    manager.setup()
    app.run()
    
#testbranch
