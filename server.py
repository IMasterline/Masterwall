from flask import Flask, request
import sqlite3


con = sqlite3.connect("db.db")

cur = con.cursor()

res = cur.execute("SELECT * FROM blacklist")
print(res.fetchone())

app = Flask(__name__)

@app.route("/")
def index():
    print(request.args.get("name"))
    return (request.args.get("name"))
    
app.run(host="localhost", debug=True, port=8080)
