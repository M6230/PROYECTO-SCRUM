from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import uuid

app = Flask(__name__)

app.config["MYSQL_HOST"]       = "localhost"
app.config["MYSQL_USER"]       = "root"
app.config["MYSQL_PASSWORD"]   = "1234"
app.config["MYSQL_DB"]       = "db_scrum"
app.config["MYSQL_PORT"]       = 3306 

mysql = MySQL(app)


@app.route("/showUsuarios") # ENDPOINT
def ShowUsuarios():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM usuarios WHERE estado = 1")
    usuarios = con.fetchall()
    listado = []
    for usuario in usuarios:
        listado.append({"id":usuario[0],"nombre":usuario[1] , "apellido":usuario[2],
                        "correo":usuario[3], "rol":usuario[4], "estado":usuario[5], "uuid":usuario[6], "contraseña":usuario[7]})
    return jsonify(listado)


@app.route("/createUsuario", methods=["POST"]) # ENDPOINT
def createUsuario():
    campos_requeridos = ["nombre", "apellido","correo", "rol", "password"]
    peticion          = request.json 
    faltantes = [ x  for x in campos_requeridos if x not in peticion  ]

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    nombre              = peticion["nombre"]
    apellido            = peticion["apellido"]
    correo              = peticion["correo"]
    rol                 = peticion["rol"]
    estado              = 1
    uid                 = uuid.uuid4()
    password            = peticion["password"]
    con = mysql.connection.cursor()
    con.execute("""
            INSERT INTO  usuarios (nombre, apellido, correo, rol, estado, uid, password)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s)
                """,[nombre, apellido, correo, rol, estado, uid, password])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha registrado el usuario"})

@app.route("/updateUsuario/<id>", methods=["POST"]) # ENDPOINT
def updateUsuario(id):
    campos_requeridos = ["nombre", "apellido","correo", "rol","password"]
    peticion          = request.json 
    faltantes = [ x  for x in campos_requeridos if x not in peticion  ]

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    nombre              = peticion["nombre"]
    apellido            = peticion["apellido"]
    correo              = peticion["correo"]
    rol                 = peticion["rol"]
    estado              = 1
    uid                 = uuid.uuid4()
    password            = peticion["password"]
    con = mysql.connection.cursor()
    con.execute("""
            UPDATE usuarios SET nombre= %s , apellido= %s, correo = %s, rol= %s , estado= %s, uid=%s, password=%s
                WHERE id = %s
                """,[nombre, apellido,correo, rol,estado, uid, password, id])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha actualizado el usuario"})

@app.route("/deleteUsuario/<id>", methods=["DELETE"]) # ENDPOINT
def deleteUsuario(id):

    con = mysql.connection.cursor()
    con.execute("""   UPDATE usuarios SET estado = 0 WHERE id = %s  """,[ id])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha eliminado el usuario"})


app.run(debug=True, port=3333, host="0.0.0.0")
