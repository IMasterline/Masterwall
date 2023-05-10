from flask import Flask, request, jsonify, render_template
import json
import sqlite3
import random
import requests

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
        print("website blacklisted")

    #save and close connection
    con.commit()
    con.close()
    
    return jsonify({"code": "200"})
    
    

@app.route("/addToReported/<url>", methods=["post"])
def insertToReported(url):
    # get the public IP address of the client
    ip = requests.get('https://api.ipify.org').text
    # connect to db
    con = sqlite3.connect("db.db")
    # create cursor
    cur = con.cursor()
    # commands section
    cur.execute("SELECT * FROM reported WHERE URL=? AND IP=?", (url, ip))
    if len(cur.fetchall()) > 0:
        # user has already reported this URL
        con.close()
        print("This IP range has already reported this URL.")
        return jsonify({"error": "You have already reported this URL."})
    else:
        cur.execute("INSERT INTO reported (URL, IP) VALUES (?,?)", (url, ip))
        print("URL has been reported")
        # save and close connection
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
    
    
    
@app.route("/checkReported", methods=["POST"])
def checkReportedDB():
    hostname = request.json.get('hostname', '')
    if hostname:
        print(f'Received hostname: {hostname}')

        # Connect to db
        con = sqlite3.connect("db.db")
        # Create cursor
        cur = con.cursor()
        # Execute SQL command
        cur.execute("SELECT COUNT(*) FROM reported WHERE URL=?", (hostname,))
        result = cur.fetchone()[0]
        # Close connection
        con.close()

        if result > 0:
            # The website has been reported
            reportscount = result
            print("Website has been reported")
            return jsonify({"reportscount": reportscount})
        else:
            # Handle the case where the website has not been reported
            reportscount = 0
            print("Website has not been reported")
            return jsonify({"reportscount": reportscount})

    
    


    
    
app.run(host="localhost", debug=True, port=8080)
