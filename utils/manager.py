from flask import Flask, render_template, request, session,redirect,url_for
import csv, unicodedata, requests, sqlite3


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


def getDrawGameInfo():#returns tuple as follows (game id, username of recent contributor, game name, game scenario, completion status)
    conn=sqlite3.connect("databases/todraw.db")
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
    conn=sqlite3.connect("databases/todescribe.db")
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
    conn=sqlite3.connect("databases/todraw.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'todraw' (id integer primary key, user text, name text, scenario text,completed text)")
    c.execute("INSERT INTO todraw(user,name,scenario,completed) VALUES ('"+username+"','"+name+"','"+scenario+"','no')")
    conn.commit()
    conn.close()

def completeDescription(name):
    conn=sqlite3.connect("databases/todescribe.db")
    c=conn.cursor()
    c.execute("update todescribe set completed='yes' where name='"+name+"'")
    conn.commit()
    conn.close()

def needsDescription(name, username,scenario):
    conn=sqlite3.connect("databases/todraw.db")
    c=conn.cursor()
    c.execute("update todraw set completed='yes' where name='"+name+"'")
    conn.commit()
    conn.close()
    conn=sqlite3.connect("databases/todescribe.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS 'todescribe' (id integer primary key, user text, name text, scenario text,completed text)")
    c.execute("INSERT INTO todescribe(user,name,scenario,completed) VALUES ('"+username+"','"+name+"','"+scenario+"','no')")
    conn.commit()
    conn.close()
    
def newGame(name, username, scenario):
    conn =sqlite3.connect("databases/games.db")
    c=conn.cursor()
    command="CREATE TABLE IF NOT EXISTS '" + name + "' (id integer primary key, user text, scenario text)"
    print command
    c.execute(command)
    c.execute("INSERT INTO '"+name+"'(user,scenario) VALUES ('"+username+"','"+scenario+"')")
    conn.commit()
    conn.close()

def updateGame(name, username, scenario):
    conn=sqlite3.connect("databases/games.db")
    c=conn.cursor()
    c.execute("INSERT INTO '"+name+"'(user,scenario) VALUES ('"+ username+"','"+scenario+"')")
    conn.commit()
    conn.close()

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
    
def getTables():
    conn = sqlite3.connect('databases/games.db')
    with conn:
        cursor = conn.cursor()    
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
        rows = cursor.fetchall()
        rows = [x[0] for x in rows]
        rows[:]=[unicodedata.normalize('NFKD',o).encode('ascii','ignore') for o in rows]
        return rows

def storePicture(username, dataUrl):
    conn = sqlite3.connect("databases/pictures.db")
    cursor = conn.cursor()
    command = "CREATE TABLE IF NOT EXISTS PICTURES (id integer primary key, user text, picture text)"
    cursor.execute(command)
    putPic = "INSERT INTO PICTURES(user,picture) VALUES ('"+username+"','"+dataUrl+"')"
    cursor.execute(putPic)
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
