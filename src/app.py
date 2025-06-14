from flask import Flask,request,jsonify,Response
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from flask_pymongo import PyMongo
from bson import ObjectId,json_util
from traceback import format_exc

app = Flask(__name__)
load_dotenv()


app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")


db = MySQL(app) 
mongo = PyMongo(app)

@app.route("/add_sql", methods=["POST"])
def add_sql():

    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if name and email and password :

        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,password))
        db.connection.commit()
        return "Añadido correctamente"
    
@app.route("/get_sql",methods=["GET"])
def get_sql():


    cursor = db.connection.cursor()
    cursor.execute("SELECT * from users")
    users = cursor.fetchall()

    return jsonify(users)



@app.route("/get_sql/<int:id>",methods=["GET"])
def get_sql_id(id):


    cursor = db.connection.cursor()
    cursor.execute("SELECT * from users where id=%s",(id,))
    users = cursor.fetchone()

    return jsonify(users)

@app.route("/put_sql/<int:id>",methods=["PUT"])
def put_sql(id):

    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if name and email and password:

        cursor = db.connection.cursor()
        cursor.execute("UPDATE users SET name = %s,email=%s,password=%s WHERE id=%s",(name,email,password,id))
        db.connection.commit()

        return "Actualizado correctamente..."

@app.route("/delete_sql/<int:id>",methods=["DELETE"])
def delete_sql(id):

    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s",(id,))
    db.connection.commit()

    return "Usuario eliminado correctamente..."

@app.route("/add_mongo",methods=["POST"])
def add_mongo():
    try:
        name = request.json["name"]
        email = request.json["email"]
        password = request.json["password"]

        if name and email and password:

            result = mongo.db.users.insert_one({
                "name": name,
                "email": email,
                "password": password
            })

            response = {

                "id": str(result.inserted_id),
                "name": name,
                "email": email,
                "password": password
            }

            return jsonify(response)
    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": format_exc()
        }), 500

@app.route("/get_mongo",methods=["GET"])
def get_mongo():

    usuarios = mongo.db.users.find()

    response = json_util.dumps(usuarios)

    return Response(response, mimetype="application/json")


@app.route("/get_mongo/<id>",methods=["GET"])
def get_mongo_id(id):

    usuario = mongo.db.users.find_one({"_id": ObjectId(id)})

    usuario["_id"] = str(usuario["_id"])
    return jsonify(usuario)


@app.route("/put_mongo/<id>",methods=["PUT"])
def put_mongo_id(id):

    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if name and email and password:

        mongo.db.users.update_one({"_id":ObjectId(id)},
            {"$set":{

                "name":name,
                "email":email,
                "password":password 
            }}
        )

        return "Actualizado con exito..."



@app.route("/delete_mongo/<id>",methods=["DELETE"])
def delete_mongo_id(id):

    mongo.db.users.delete_one({"_id": ObjectId(id)})

    
    return "eliminado correctamente..."

if __name__ == "__main__":
    app.run(debug=True)