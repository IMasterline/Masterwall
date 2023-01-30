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
def insert(url):
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
        cur.execute("INSERT INTO blacklist VALUES (?, ?)", (random.randint(1, 999999), url))

    #save and close connection
    con.commit()
    con.close()
    
    return jsonify({"code": "200"})
    
app.run(host="localhost", debug=True, port=8080)
