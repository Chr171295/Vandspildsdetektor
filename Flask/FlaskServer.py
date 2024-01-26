from flask import Flask, request
import json
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/postdata",methods=["post"])
def postData():
        data = request.json
        sendToDb(data)
        return "detvirker"
@app.route("/getalldata",methods=["get"])
def getAllData():
        return json.dumps(allDataFromDb())
@app.route("/getdata",methods=["post"])
def getdata():
       data = request.json
       return json.dumps(dataFromDb(data))
def connectToDb():
        server = "localhost"
        database = "Tempsensdb"
        username = "redrock5"
        password = "Redrock123"

        conn = mysql.connector.connect(host=server,database=database,user=username,password=password)
        return conn
def sendToDb(data):
        conn = connectToDb()
        cursor = conn.cursor()
        unpacked = json.loads(data)
        query = f"INSERT INTO Tempsensdb(templuft,temproer,tempdiff) VALUES({unpacked['templuft']},{unpacked['temproer']},{unpacked['templuft']}-{unpacked['temproer']})"
        cursor.execute(query)
        conn.commit()
        cursor.close()
def allDataFromDb():
        conn = connectToDb()
        cursor = conn.cursor()
        query = "SELECT * FROM Tempsensdb"
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        return toJson(data)
def dataFromDb(querystring):
        conn = connectToDb()
        cursor = conn.cursor()
        query = querystring
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        return toJson(data)
def toJson(data):
    listToDict = []
    for row in data:
          print(row[0].strftime("%m/%d/%Y, %H:%M:%S"))
          listToDict.append({'tid': row[0].strftime("%m/%d/%Y, %H:%M:%S") ,'templuft': row[1],'temproer': row[2],'tempdiff': row[3]})
    return json.dumps(listToDict)
if __name__ == "__main__":
    app.run(host="0.0.0.0")
