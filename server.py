from flask import Flask, request, jsonify, render_template
import json
import sqlite3
import random

"""
#connect to db
con = sqlite3.connect("db.db")
#create cursor
cur = con.cursor()
#commands section
cur.execute("CREATE TABLE reported(url TEXT PRIMARY KEY, count INTEGER)")

#save and close connection
con.commit()
con.close()
"""


#server website creator
app = Flask(__name__)

isblacklisted = 0
reportscount = 0
spamcooldown = 0

async def reducecooldown():
    global spamcooldown
    while (spamcooldown > 0):
        spamcooldown = spamcooldown - 1



@app.route("/")
def index():
    print(request.args.get("name"))
    return (request.args.get("name"))
    
@app.route("/addToBlacklist/<url>", methods=["post"])
def insertToBlacklist(url):
    #connect to db
    con = sqlite3.connect("db.db")
    #create cursor
    cur = con.cursor()
    #commands section
    print(url)
    cur.execute("SELECT * FROM blacklist WHERE URL='" + url + "'")
    if len(cur.fetchall()) > 0:
        print(cur.fetchall())
        print("already in table")
    else:
        cur.execute("INSERT INTO blacklist (URL) VALUES (?)", (url, ))

    #save and close connection
    con.commit()
    con.close()
    
    return jsonify({"code": "200"})
    
    

@app.route("/addToReported/<url>", methods=["post"])
def insertToReported(url):
    global spamcooldown
    if (spamcooldown == 0):
        #connect to db
        con = sqlite3.connect("db.db")
        #create cursor
        cur = con.cursor()
        #commands section
        print(url)
        cur.execute("SELECT * FROM reported WHERE URL='" + url + "'")
        if len(cur.fetchall()) > 0:
            print(cur.fetchall())
            cur.execute("UPDATE reported SET reports = reports + 1 WHERE URL='" + url + "'")
            print("reports += 1")
            spamcooldown = 60
        else:
            cur.execute("INSERT INTO reported (URL,reports) VALUES (?,?)", (url,1))
    else:
        print("on cooldown")

    #save and close connection
    con.commit()
    con.close()
    
    return jsonify({"code": "200"})
    
    
@app.route("/checkBlacklist/<url>", methods=["post"])
def checkBlacklistDB(url):
    #connect to db
    con = sqlite3.connect("db.db")
    #create cursor
    cur = con.cursor()
    #commands section
    print(url)
    cur.execute("SELECT * FROM blacklist WHERE URL='" + url + "'")
    if len(cur.fetchall()) > 0:
        print("website is in blacklist")
        isblacklisted = 1
        return jsonify({"code": "200"})
    else:
        print("website is not in blacklist")
        isblacklisted = 0
        return jsonify({"code": "200"})
    
    
    #pass variables to js
    data = {
        "isblacklisted": isblacklisted
    }
    with open("data.json", "w") as f:
        json.dump(data, f)

    #save and close connection
    con.commit()
    con.close()
    
    
    
@app.route("/checkReported/<url>", methods=["post"])
def checkReportedDB(url):
    #connect to db
    con = sqlite3.connect("db.db")
    #create cursor
    cur = con.cursor()
    #commands section
    print(url)
    cur.execute("SELECT value FROM reported WHERE URL='" + url + "'")
    result = cursor.fetchone()
    
    if result is not None:
        print("website has been reported")
        reportscount = result[0]
        return jsonify({"code": "200"})
        
    else:
        # Handle the case where id does not exist in the table
        reportscount = 0  # or set a default value
        print("website has not been reported")
        return jsonify({"code": "200"})
    
    
    #pass variables to js
    data = {
        "reportscount": reportscount
    }
    with open("data.json", "w") as f:
        json.dump(data, f)

    #save and close connection
    con.commit()
    con.close()
    
    


    
    
app.run(host="localhost", debug=True, port=8080)
