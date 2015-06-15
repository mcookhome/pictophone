from flask import Flask, render_template, request, session,redirect,url_for
import csv, unicodedata, requests, sqlite3

def setup():
    conn = sqlite3.connect("databases/user.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'uinfo' (username text, password text)")
    conn = sqlite3.connect("databases/todo.db")
    c= conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'todraw' (id integer primary key, user text, name text, scenario text,completed text)")
    c.execute("CREATE TABLE IF NOT EXISTS 'todescribe' (id integer primary key, user text, name text, scenario text,completed text)")
    conn = sqlite3.connect("databases/pictures.db")
    c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS PICTURES (id integer primary key, user text, picture text)")
    
def wipegames():
    conn = sqlite3.connect("databases/todo.db")
    c= conn.cursor()
    c.execute("DROP TABLE IF EXISTS 'todraw'")
    c.execute("DROP TABLE IF EXISTS 'todescribe'")
    conn = sqlite3.connect("databases/pictures.db")
    c=conn.cursor()
    c.execute("DROP TABLE IF EXISTS PICTURES")
    conn = sqlite3.connect("databases/games.db")
    c= conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    names= c.fetchall()
    for i in names:
        c.execute("DROP TABLE IF EXISTS '"+i[0]+"'")
    setup()
def wipeusers():
    conn = sqlite3.connect("databases/user.db")
    c= conn.cursor()
    c.execute("DROP TABLE IF EXISTS 'uinfo'")
    setup()
def getIDs():
    ids=[]
    conn = sqlite3.connect("databases/users.db")
    c = conn.cursor()
    c.execute("select * from uinfo")
    tabledata = c.fetchall()
    for d in tabledata:
        ids.append(d[0]);
        conn.close()
    ids[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in ids]
    return ids

def getProfilePath():
    ids=getIDs()
    user=request.form["query"]
    path="profile/"+user
    #if user not in ids:
     #   return ""
    print path
    return path

def isComplete(name):
    conn=sqlite3.connect("databases/games.db")
    c=conn.cursor()
    c.execute("select turns from '"+name+"' where id=1")
    tabledata=c.fetchall()
    turns=tabledata[0][0]
    print turns
    c.execute("SELECT MAX(id) from '"+name+"'")
    maxid= c.fetchall()
    currentlength=maxid[0][0]
    conn.commit()
    conn.close()
    if currentlength==turns:
        print "complete"
        return True
    print "incomplete"
    return False

def getMembers(game):
    conn = sqlite3.connect('databases/games.db')
    
    with conn:
        
        cursor = conn.cursor()    
        cursor.execute("SELECT user FROM '"+ game+"'")
    
        rows = cursor.fetchall()
        rows = [x[0] for x in rows]
        rows[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in rows]
        return rows

def getUserGames(username):
	games = getGames()
	gameNames = []
	for x in games:
		if username in getMembers(x):
			gameNames.append(x)
	print gameNames
	return gameNames

def getGameFax(name):
    conn=sqlite3.connect("databases/games.db")
    c=conn.cursor()
    c.execute("select id,user,scenario from '"+name+"'")
    tabledata=c.fetchall()
    tabledata[:]=[[item[0],item[1],item[2]] for item in tabledata]
    for n in tabledata:
        n[1:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in n[1:]]
    return tabledata

def getDrawGameInfo():#returns tuple as follows (game id, username of recent contributor, game name, game scenario, completion status)
    conn=sqlite3.connect("databases/todo.db")
    c=conn.cursor()
    c.execute("select * from todraw where id=(SELECT MIN(id) FROM todraw WHERE completed='no')")
    tabledata=c.fetchall()
    if len(tabledata) == 0:
        return None
    #scenario=unicodedata.normalize('NFKD',tabledata[0][0]).encode('ascii','ignore')
    conn.commit()
    conn.close()
    return tabledata[0]
    
def getWriteGameInfo():#returns tuple as follows (game id, username of recent contributor, game name, picture daraurl, completion status)
    conn=sqlite3.connect("databases/todo.db")
    c=conn.cursor()
    c.execute("select * from todescribe where id=(SELECT MIN(id) FROM todescribe WHERE completed='no')")
    tabledata=c.fetchall()
    if len(tabledata) == 0:
        return None
    #scenario=unicodedata.normalize('NFKD',tabledata[0][0]).encode('ascii','ignore')
    conn.commit()
    conn.close()
    return tabledata[0]

def needsDrawing(name, username,scenario):
    conn=sqlite3.connect("databases/todo.db")
    c = conn.cursor()
    c.execute("INSERT INTO todraw(user,name,scenario,completed) VALUES ('"+username+"','"+name+"','"+scenario+"','no')")
    conn.commit()
    conn.close()

def completeDescription(name):
    conn=sqlite3.connect("databases/todo.db")
    c=conn.cursor()
    c.execute("update todescribe set completed='yes' where name='"+name+"'")
    conn.commit()
    conn.close()

def needsDescription(name, username,scenario):
    conn=sqlite3.connect("databases/todo.db")
    c=conn.cursor()
    c.execute("update todraw set completed='yes' where name='"+name+"'")
    conn.commit()
    conn.close()
    conn=sqlite3.connect("databases/todo.db")
    c = conn.cursor()
    c.execute("INSERT INTO todescribe(user,name,scenario,completed) VALUES ('"+username+"','"+name+"','"+scenario+"','no')")
    conn.commit()
    conn.close()
    
def newGame(name, username, scenario,turns):
    conn =sqlite3.connect("databases/games.db")
    c=conn.cursor()
    command="CREATE TABLE IF NOT EXISTS '" + name + "' (id integer primary key, user text, scenario text, turns int)"
    print command
    c.execute(command)
    c.execute("INSERT INTO '"+name+"'(user,scenario,turns) VALUES ('"+username+"','"+scenario+"','"+turns+"')")
    conn.commit()
    conn.close()

def updateGame(name, username, scenario):
    conn=sqlite3.connect("databases/games.db")
    c=conn.cursor()
    c.execute("select turns from '"+name+"' where id=1")
    tabledata=c.fetchall()
    turns=tabledata[0][0]
    print turns
    c.execute("INSERT INTO '"+name+"'(user,scenario,turns) VALUES ('"+ username+"','"+scenario+"',"+str(turns)+")")
    c.execute("SELECT MAX(id) from '"+name+"'")
    maxid= c.fetchall()
    currentlength=maxid[0][0]
    print str(currentlength)+"BLAH"
    conn.commit()
    conn.close()
    if currentlength==turns:
        print True
        return True
    print False
    return False

def exists(name):
    conn=sqlite3.connect("databases/games.db")
    c=conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+name+"'")
    tabledata=c.fetchall()
    games=[]
    for d in tabledata:
        games.append(d[0]);
    conn.close()
    games[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in games]
    if len(games)==1:
        return True
    return False
    

def getGames():
    conn = sqlite3.connect('databases/games.db')
    with conn:
        cursor = conn.cursor()    
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
        rows = cursor.fetchall()
        rows = [x[0] for x in rows]
        rows[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in rows]
        return rows

def getCompleteGames():
    games=getGames()
    completegames=[]
    for n in games:
        if isComplete(n) is True:
            completegames.append(n)
    return completegames

def getAllUsers():
    conn = sqlite3.connect('databases/users.db')
    with conn:
        cursor = conn.cursor()    
        cursor.execute("SELECT username FROM uinfo")
        rows = cursor.fetchall()
        rows = [x[0] for x in rows]
        rows[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in rows]
        return rows

def storePicture(username, dataUrl):
    conn = sqlite3.connect("databases/pictures.db")
    c = conn.cursor()
    putPic = "INSERT INTO PICTURES(user,picture) VALUES ('"+username+"','"+dataUrl+"')"
    c.execute(putPic)
    conn.commit()
    conn.close()

def getPicture(number):
    conn = sqlite3.connect("databases/pictures.db")
    cursor = conn.cursor()
    command = "SELECT picture FROM PICTURES"
    cursor.execute(command)
    pic=cursor.fetchall()
    conn.close()
    pic=[x[0] for x in pic]
    pic[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in pic]
    if (len(pic)>number):
        return pic[number]
    else:
        return -1
        
    
    
    

def finishLogin(username):
      
    conn = sqlite3.connect("databases/users.db")
    c = conn.cursor()
    c.execute("select * from uinfo")
    tabledata = c.fetchall()
    conn.close()
    for d in tabledata:
        if username == d[0]:
            return d[1]
    return ""

     

def finishRegistration(username,password,registered):
    conn = sqlite3.connect("databases/users.db")
    c = conn.cursor()
    reason=''
    c.execute("select * from uinfo")
    tabledata = c.fetchall()
    for d in tabledata:
        if username == d[0]:
            registered=False
            reason="The username "+username+" already exists!"
            print "Username %s is already in use" %username
            
    pvalidate = validateEntry(password)
    if pvalidate != "":
        registered=False
        reason = "Password: " + pvalidate
                
    uvalidate = validateEntry(username)
    if uvalidate != "":
        registered=False
        reason = "Username: " + uvalidate
            
    if registered:
        insinfo="insert into uinfo values ('"+username+"','"+password+"')"
        c.execute(insinfo)
        conn.commit()
        print 'Username and Password have been recorded as variables'
    else:
        print "Failure to register"
    conn.close()
    return [registered,reason]
    
def validateEntry(entry):
    allowChars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    specialChars="!#$%&*+,-./:;<=>?@\^_`|~"
    if len(entry)<4 or len(entry)>16:
        return "Invalid Length (4-16 characters)"
    for x in entry:
        if x not in allowChars and x not in specialChars:
            return "You can't use this character. Special characters allowed: " + specialChars
    return ""

def revert(x):
    x=unicodedata.normalize('NFKD',x).encode('ascii','ignore')    
    return x

def newPrivateGame(name, username, scenario,turns,password):
    conn =sqlite3.connect("databases/games.db")
    c=conn.cursor()
    command="CREATE TABLE IF NOT EXISTS '" + name + "' (id integer primary key, user text, scenario text, turns int)"
    print command
    c.execute(command)
    c.execute("INSERT INTO '"+name+"'(user,scenario,turns,password) VALUES ('"+username+"','"+scenario+"','"+turns+"','"+password+"')")
    conn.commit()
    conn.close()

def hasPassword(name):
    conn = sqlite3.connect("databases/game.db")
    c = conn.cursor()
    c.execute("select password from '"+name+"'")
    p = c.fetchall()
    print p
    if p!="":
        return False
    return True

def getPrivateGames(username):
	games = getGames()
	gameNames = []
	for x in games:
		if username in getMembers(x):
                    if x.hasPassword(x)
			gameNames.append(x)
	print gameNames
	return gameNames
