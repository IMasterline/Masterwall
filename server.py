import hashlib
import json
import sqlite3
import requests
from flask import Flask, request, jsonify
from werkzeug.local import Local

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = Local()

    def __del__(self):
        if hasattr(self.db, 'connection'):
            self.db.connection.close()

    def get_db(self):
        if not hasattr(self.db, 'connection'):
            self.db.connection = sqlite3.connect("db.db")
        return self.db.connection

    def index(self):
        print(request.args.get("name"))
        return request.args.get("name")

    def insertToBlacklist(self, url):
        ip = requests.get('https://api.ipify.org').text
        hashed_ip = hashlib.sha256(ip.encode()).hexdigest()

        con = self.get_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM blacklist WHERE URL=? AND IP=?", (url, hashed_ip))
        if len(cur.fetchall()) > 0:
            print("website removed from blacklist")
            cur.execute("DELETE FROM blacklist WHERE URL=? AND IP=?", (url, hashed_ip))
        else:
            cur.execute("INSERT INTO blacklist (URL, IP) VALUES (?,?)", (url, hashed_ip))
            print("website blacklisted")

        con.commit()
        return jsonify({"code": "200"})

    def insertToReported(self, url):
        ip = requests.get('https://api.ipify.org').text
        hashed_ip = hashlib.sha256(ip.encode()).hexdigest()

        con = self.get_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM reported WHERE URL=? AND IP=?", (url, hashed_ip))
        if len(cur.fetchall()) > 0:
            con.close()
            print("This IP range has already reported this URL.")
            return jsonify({"error": "You have already reported this URL."})
        else:
            cur.execute("INSERT INTO reported (URL, IP) VALUES (?,?)", (url, hashed_ip))
            print("URL has been reported")

        con.commit()
        return jsonify({"code": "200"})

    def checkBlacklistDB(self):
        hostname = request.json.get('hostname', '')
        if hostname:
            print(f'Received hostname: {hostname}')

            ip = requests.get('https://api.ipify.org').text
            hashed_ip = hashlib.sha256(ip.encode()).hexdigest()

            con = self.get_db()
            cur = con.cursor()

            cur.execute("SELECT COUNT(*) FROM blacklist WHERE URL=? AND IP=?", (hostname, hashed_ip))
            result = cur.fetchone()[0]

            if result > 0:
                print("website is in blacklist")
                isblacklisted = 1
                return jsonify({"isblacklisted": isblacklisted})
            else:
                print("website is not in blacklist")
                isblacklisted = 0
                return jsonify({"isblacklisted": isblacklisted})

    def checkReportedDB(self):
        hostname = request.json.get('hostname', '')
        if hostname:
            print(f'Received hostname: {hostname}')

            con = self.get_db()
            cur = con.cursor()

            cur.execute("SELECT COUNT(*) FROM reported WHERE URL=?", (hostname,))
            result = cur.fetchone()[0]
            con.close()

            if result > 0:
                reportscount = result
                print("Reports count is " + str(reportscount))
                return jsonify({"reportscount": reportscount})
            else:
                reportscount = 0
                print("Reports count is 0")
                return jsonify({"reportscount": reportscount})

    def run(self):
        self.app.route("/")(self.index)
        self.app.route("/addToBlacklist/<url>", methods=["POST"])(self.insertToBlacklist)
        self.app.route("/addToReported/<url>", methods=["POST"])(self.insertToReported)
        self.app.route("/checkBlacklist", methods=["POST"])(self.checkBlacklistDB)
        self.app.route("/checkReported", methods=["POST"])(self.checkReportedDB)
        self.app.run(host="localhost", debug=True, port=8080)

server = Server()
server.run()
