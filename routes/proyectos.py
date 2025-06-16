from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
import uuid

proyectos_bp = Blueprint('proyectos', __name__)

# Mostrar proyectos (requiere token)
@proyectos_bp.route('/mostrar', methods=['GET'])
@jwt_required()
def showProyectos():
    con = current_app.mysql.connection.cursor()
    con.execute("SELECT * FROM T_PROYECTOS WHERE PROY_ESTADO = 1")
    proyectos = con.fetchall()
    listado = []
    for proyecto in proyectos:
        listado.append({
            "PROY_ID": proyecto[0],
            "PROY_NOMBRE": proyecto[1],
            "PROY_DESCRIPCION": proyecto[2],
            "PROY_ESTADO": proyecto[3],
            "PROY_UID": proyecto[4]
        })
    return jsonify(listado)

# Crear proyecto (requiere token)
@proyectos_bp.route('/crear', methods=['POST'])
@jwt_required()
def createProyecto():
    campos_requeridos = ["PROY_NOMBRE", "PROY_DESCRIPCION"]
    peticion = request.json
    faltantes = [x for x in campos_requeridos if x not in peticion]

    if faltantes:
        return jsonify({"mensaje": f"Faltan campos en la petición: {faltantes}"}), 400

    nombre = peticion["PROY_NOMBRE"]
    descripcion = peticion["PROY_DESCRIPCION"]

    con = current_app.mysql.connection.cursor()
    con.execute("SELECT * FROM T_PROYECTOS WHERE PROY_NOMBRE = %s AND PROY_ESTADO = 1", [nombre])
    duplicado = con.fetchone()

    if duplicado:
        con.close()
        return jsonify({"mensaje": "Ya existe un proyecto activo con ese nombre"}), 409

    estado = 1
    uid = uuid.uuid4()
    con.execute("""
        INSERT INTO T_PROYECTOS (PROY_NOMBRE, PROY_DESCRIPCION, PROY_ESTADO, PROY_UID)
        VALUES (%s, %s, %s, %s)
    """, [nombre, descripcion, estado, uid])
    con.connection.commit()
    con.close()

    return jsonify({"mensaje": "Se ha registrado el proyecto"}), 201


# Actualizar proyecto (requiere token)
@proyectos_bp.route('/editar/<id>', methods=['PUT'])
@jwt_required()
def updateProyecto(id):
    campos_requeridos = ["PROY_NOMBRE", "PROY_DESCRIPCION"]
    peticion = request.json
    faltantes = [x for x in campos_requeridos if x not in peticion]

    if faltantes:
        return jsonify({"mensaje": f"Faltan campos en la petición: {faltantes}"}), 400

    nombre = peticion["PROY_NOMBRE"]
    descripcion = peticion["PROY_DESCRIPCION"]

    con = current_app.mysql.connection.cursor()
    con.execute("""
        SELECT * FROM T_PROYECTOS 
        WHERE PROY_NOMBRE = %s AND PROY_ID != %s AND PROY_ESTADO = 1
    """, [nombre, id])
    duplicado = con.fetchone()

    if duplicado:
        con.close()
        return jsonify({"mensaje": "Ya existe otro proyecto activo con ese nombre"}), 409

    estado = 1
    uid = uuid.uuid4()
    con.execute("""
        UPDATE T_PROYECTOS
        SET PROY_NOMBRE = %s, PROY_DESCRIPCION = %s, PROY_ESTADO = %s, PROY_UID = %s
        WHERE PROY_ID = %s
    """, [nombre, descripcion, estado, uid, id])
    con.connection.commit()
    con.close()

    return jsonify({"mensaje": "Se ha actualizado el proyecto"})


# Eliminar proyecto (requiere token)
@proyectos_bp.route('/eliminar/<id>', methods=['DELETE'])
@jwt_required()
def deleteProyecto(id):
    con = current_app.mysql.connection.cursor()
    con.execute("UPDATE T_PROYECTOS SET PROY_ESTADO = 0 WHERE PROY_ID = %s", [id])
    con.connection.commit()

    return jsonify({"mensaje": "Se ha eliminado el proyecto"})
