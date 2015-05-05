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
    
    c.execute("select * from uinfo")
    tabledata = c.fetchall()
    for d in tabledata:
        if username == d[0]:
            registered=False
            reason="The username "+username+" already exists!"
            print "Username % is already in use" %username
            
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

    
def validateEntry(entry):
    allowChars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    specialChars="!#$%&*+,-./:;<=>?@\^_`|~"
    if len(entry)<4 or len(entry)>16:
        return "Invalid Length (4-16 characters)"
    for x in entry:
        if x not in allowChars and x not in specialChars:
            return "You can't use this character. Special characters allowed: " + specialChars
    return ""
