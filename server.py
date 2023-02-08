from flask import Flask, request, jsonify
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
    else:
        cur.execute("INSERT INTO reported (URL,reports) VALUES (?,?)", (url,0))

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
        return jsonify({"code": "200"})
    else:
        print("website is not in blacklist")
        return jsonify({"code": "200"})

    #save and close connection
    con.commit()
    con.close()

    
app.run(host="localhost", debug=True, port=8080)
