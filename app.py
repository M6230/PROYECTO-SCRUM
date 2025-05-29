from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import uuid

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'priprapri'
jwt = JWTManager(app)

app.config["MYSQL_HOST"]       = "localhost"
app.config["MYSQL_USER"]       = "root"
app.config["MYSQL_PASSWORD"]   = ""
app.config["MYSQL_DB"]       = "db_scrum"
app.config["MYSQL_PORT"]       = 3306 

mysql = MySQL(app)

@app.route('/login', methods=["POST"]) # ENDPOINT
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == "hola" and password == "hola":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'msg': 'Credenciales inválidas'}), 401

@app.route('/perfil', methods=["GET"]) # ENDPOINT
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/showUsuarios") # ENDPOINT
@jwt_required()
def ShowUsuarios():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM usuarios WHERE USU_estado = 1")
    usuarios = con.fetchall()
    listado = []
    for usuario in usuarios:
        listado.append({"USU_id":usuario[0],"USU_nombre":usuario[1] , "USU_apellido":usuario[2],
                        "USU_correo":usuario[3], "USU_rol":usuario[4], "USU_estado":usuario[5], "USU_uuid":usuario[6], "USU_contraseña":usuario[7]})
    return jsonify(listado)


@app.route("/createUsuario", methods=["POST"]) # ENDPOINT
@jwt_required()
def createUsuario():
    campos_requeridos = ["USU_nombre", "USU_apellido","USU_correo", "USU_rol", "USU_password"]
    peticion          = request.json 
    faltantes = [ x  for x in campos_requeridos if x not in peticion  ]

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    nombre              = peticion["USU_nombre"]
    apellido            = peticion["USU_apellido"]
    correo              = peticion["USU_correo"]
    rol                 = peticion["USU_rol"]
    estado              = 1
    uid                 = uuid.uuid4()
    password            = peticion["USU_password"]
    con = mysql.connection.cursor()
    con.execute("""
            INSERT INTO  usuarios (USU_nombre, USU_apellido, USU_correo, USU_rol, USU_estado, USU_uid, USU_password)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s)
                """,[nombre, apellido, correo, rol, estado, uid, password])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha registrado el usuario"})

@app.route("/updateUsuario/<id>", methods=["POST"]) # ENDPOINT
@jwt_required()
def updateUsuario(id):
    campos_requeridos = ["USU_nombre", "USU_apellido","USU_correo", "USU_rol","USU_password"]
    peticion          = request.json 
    faltantes = [ x  for x in campos_requeridos if x not in peticion  ]

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    nombre              = peticion["USU_nombre"]
    apellido            = peticion["USU_apellido"]
    correo              = peticion["USU_correo"]
    rol                 = peticion["USU_rol"]
    estado              = 1
    uid                 = uuid.uuid4()
    password            = peticion["USU_password"]
    con = mysql.connection.cursor()
    con.execute("""
            UPDATE usuarios SET USU_nombre= %s , USU_apellido= %s, USU_correo = %s, USU_rol= %s , USU_estado= %s, USU_uid=%s, USU_password=%s
                WHERE id = %s
                """,[nombre, apellido,correo, rol,estado, uid, password, id])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha actualizado el usuario"})

@app.route("/deleteUsuario/<id>", methods=["DELETE"]) # ENDPOINT
@jwt_required()
def deleteUsuario(id):

    con = mysql.connection.cursor()
    con.execute("""   UPDATE usuarios SET USU_estado = 0 WHERE USU_id = %s  """,[ id])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha eliminado el usuario"})

# Proyecto

@app.route("/showProyectos") # ENDPOINT
@jwt_required()
def showProyectos():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM proyecto WHERE estado = 1")
    proyectos = con.fetchall()
    listado = []
    for proyecto in proyectos:
        listado.append({"id":proyecto[0],"nombre":proyecto[1] , "descripcion":proyecto[2],
                         "estado":proyecto[3], "uuid":proyecto[4]})
    return jsonify(listado)

@app.route("/createProyecto", methods=["POST"]) # ENDPOINT
@jwt_required()
def createProyecto():
    campos_requeridos = ["PROY_nombre", "PROY_descripcion"]
    peticion          = request.json 
    faltantes = [ x  for x in campos_requeridos if x not in peticion  ]

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    nombre              = peticion["PROY_nombre"]
    descripcion         = peticion["PROY_descripcion"]
    estado              = 1
    uid                 = uuid.uuid4()
    con = mysql.connection.cursor()
    con.execute("""
            INSERT INTO proyecto (PROY_nombre, PROY_descripcion, PROY_estado, PROY_uid)
                VALUES
                (%s, %s, %s, %s)
                """,[nombre, descripcion, estado, uid])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha creado el proyecto"})

@app.route("/updateProyecto/<id>", methods=["POST"]) # ENDPOINT
@jwt_required()
def updateProyecto(id):
    campos_requeridos = ["PROY_nombre", "PROY_descripcion"]
    peticion          = request.json 
    faltantes = [ x  for x in campos_requeridos if x not in peticion  ]

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    nombre              = peticion["PROY_nombre"]
    descripcion         = peticion["PROY_descripcion"]
    estado              = 1
    uid                 = uuid.uuid4()
    con = mysql.connection.cursor()
    con.execute("""
            UPDATE proyecto SET PROY_nombre= %s, PROY_descripcion= %s, PROY_estado= %s, PROY_uid=%s
                WHERE PROY_id = %s
                """,[nombre, descripcion, estado, uid, id])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha actualizado el proyecto"})

@app.route("/deleteProyecto/<id>", methods=["DELETE"]) # ENDPOINT
@jwt_required()
def deleteProyecto(id):

    con = mysql.connection.cursor()
    con.execute("""   UPDATE proyecto SET PROY_estado = 0 WHERE PROY_id = %s  """,[ id])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha eliminado el proyecto"})

# Sprint

@app.route("/showSprint") # ENDPOINT
@jwt_required()
def showSprint():
    con = mysql.connection.cursor()
    con.execute("SELECT * FROM sprint WHERE SPR_estado = 1")
    sprints = con.fetchall()
    listado = []
    for sprint in sprints:
        listado.append({"SPR_id":sprint[0],"SPR_fch_inicio":sprint[1] , "SPR_fch_fin":sprint[2],
                        "SPR_objetivo":sprint[3], "SPR_estado":sprint[4], "SPR_uid":sprint[5]})
    return jsonify(listado)


@app.route("/createSprint", methods=["POST"]) # ENDPOINT
@jwt_required()
def createSprint():
    campos_requeridos = ["SPR_fch_inicio","SPR_fch_fin","SPR_objetivo"]
    peticion          = request.json 
    faltantes = [ x  for x in campos_requeridos if x not in peticion  ]

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    fch_inicio         = peticion["SPR_fch_inicio"]
    fch_fin            = peticion["SPR_fch_fin"]
    objetivo           = peticion["SPR_objetivo"]
    estado             = 1
    uid                = uuid.uuid4()
    con = mysql.connection.cursor()
    con.execute("""
            INSERT INTO  sprint (SPR_fch_inicio,SPR_fch_fin,SPR_objetivo,SPR_estado,SPR_uid)
                VALUES
                (%s, %s, %s, %s, %s)
                """,[fch_inicio,fch_fin,objetivo,estado, uid])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha registrado el sprint"})

@app.route("/updateSprint/<id>", methods=["POST"]) # ENDPOINT
@jwt_required()
def updateSprint(id):
    campos_requeridos = ["SPR_fch_inicio","SPR_fch_fin","SPR_objetivo"]
    peticion          = request.json 
    faltantes = [ x  for x in campos_requeridos if x not in peticion  ]

    if len(faltantes)>0:
        return jsonify({"mensaje":f"faltan campos en la peticion {faltantes}"})
    
    fch_inicio         = peticion["SPR_fch_inicio"]
    fch_fin            = peticion["SPR_fch_fin"]
    objetivo           = peticion["SPR_objetivo"]
    estado              = 1
    uid                 = uuid.uuid4()
    con = mysql.connection.cursor()
    con.execute("""
            UPDATE sprint SET SPR_fch_inicio= %s, SPR_fch_fin= %s, SPR_objetivo = %s, SPR_estado= %s, SPR_uid=%s
                WHERE SPR_id = %s
                """,[fch_inicio, fch_fin, objetivo, estado, uid, id])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha actualizado el sprint"})

@app.route("/deleteSprint/<id>", methods=["DELETE"]) # ENDPOINT
@jwt_required()
def deleteSprint(id):

    con = mysql.connection.cursor()
    con.execute("""   UPDATE sprint SET SPR_estado = 0 WHERE SPR_id = %s  """,[ id])
    con.connection.commit()
    
    return jsonify({"mensaje":"Se ha eliminado el sprint"})

app.run(debug=True, port=3333, host="0.0.0.0")