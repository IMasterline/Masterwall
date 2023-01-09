from flask import Flask, request
import sqlite3

#connect to db
con = sqlite3.connect("db.db")
#create cursor
cur = con.cursor()
#commands section
cur.execute("CREATE TABLE reported(url TEXT PRIMARY KEY, count INTEGER)")

#save and close connection
con.commit()
con.close()



#server website creator
app = Flask(__name__)

@app.route("/")
def index():
    print(request.args.get("name"))
    return (request.args.get("name"))
    
app.run(host="localhost", debug=True, port=8080)
