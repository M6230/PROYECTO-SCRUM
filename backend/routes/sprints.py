from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

sprints_bp = Blueprint('sprints', __name__)

# Mostrar sprints (requiere token)
@sprints_bp.route('/mostrar', methods=['GET'])
@jwt_required()
def showSprint():
    con = current_app.mysql.connection.cursor()
    con.execute("SELECT * FROM sprint WHERE SPR_ESTADO = 1")
    sprints = con.fetchall()
    listado = []
    for sprint in sprints:
        listado.append({
            "SPR_ID": sprint[0],
            "SPR_FCH_INICIO": sprint[1],
            "SPR_FCH_FIN": sprint[2],
            "SPR_OBJETIVO": sprint[3],
            "SPR_ESTADO": sprint[4],
            "SPR_UID": sprint[5]
        })
    return jsonify(listado)

# Crear sprint (requiere token)
@sprints_bp.route('/crear', methods=['POST'])
@jwt_required()
def createSprint():
    campos_requeridos = ["SPR_FCH_INICIO", "SPR_FCH_FIN", "SPR_OBJETIVO"]
    peticion = request.json
    faltantes = [x for x in campos_requeridos if x not in peticion]

    if faltantes:
        return jsonify({"mensaje": f"Faltan campos en la petición: {faltantes}"}), 400

    fch_inicio = peticion["SPR_FCH_INICIO"]
    fch_fin = peticion["SPR_FCH_FIN"]
    objetivo = peticion["SPR_OBJETIVO"]

    con = current_app.mysql.connection.cursor()
    con.execute("""
        SELECT * FROM sprint 
        WHERE SPR_FCH_INICIO = %s AND SPR_FCH_FIN = %s AND SPR_ESTADO = 1
    """, [fch_inicio, fch_fin])
    duplicado = con.fetchone()

    if duplicado:
        con.close()
        return jsonify({"mensaje": "Ya existe un sprint activo con esas fechas"}), 409

    con.execute("""
        SELECT * FROM sprint 
        WHERE SPR_OBJETIVO = %s AND SPR_ESTADO = 1
    """, [objetivo])
    duplicado_obj = con.fetchone()

    if duplicado_obj:
        con.close()
        return jsonify({"mensaje": "Ya existe un sprint activo con ese objetivo"}), 409

    estado = 1
    uid = uuid.uuid4()
    con.execute("""
        INSERT INTO sprint (SPR_FCH_INICIO, SPR_FCH_FIN, SPR_OBJETIVO, SPR_ESTADO, SPR_UID)
        VALUES (%s, %s, %s, %s, %s)
    """, [fch_inicio, fch_fin, objetivo, estado, uid])
    con.connection.commit()
    con.close()

    return jsonify({"mensaje": "Se ha registrado el sprint"}), 201


# Actualizar sprint (requiere token)
@sprints_bp.route('/editar/<id>', methods=['PUT'])
@jwt_required()
def updateSprint(id):
    campos_requeridos = ["SPR_FCH_INICIO", "SPR_FCH_FIN", "SPR_OBJETIVO"]
    peticion = request.json
    faltantes = [x for x in campos_requeridos if x not in peticion]

    if faltantes:
        return jsonify({"mensaje": f"Faltan campos en la petición: {faltantes}"}), 400

    fch_inicio = peticion["SPR_FCH_INICIO"]
    fch_fin = peticion["SPR_FCH_FIN"]
    objetivo = peticion["SPR_OBJETIVO"]

    con = current_app.mysql.connection.cursor()
    con.execute("""
        SELECT * FROM sprint 
        WHERE SPR_FCH_INICIO = %s AND SPR_FCH_FIN = %s AND SPR_ID != %s AND SPR_ESTADO = 1
    """, [fch_inicio, fch_fin, id])
    duplicado = con.fetchone()

    if duplicado:
        con.close()
        return jsonify({"mensaje": "Ya existe otro sprint activo con esas fechas"}), 409

    con.execute("""
        SELECT * FROM sprint 
        WHERE SPR_OBJETIVO = %s AND SPR_ID != %s AND SPR_ESTADO = 1
    """, [objetivo, id])
    duplicado_obj = con.fetchone()

    if duplicado_obj:
        con.close()
        return jsonify({"mensaje": "Ya existe otro sprint activo con ese objetivo"}), 409

    estado = 1
    uid = uuid.uuid4()
    con.execute("""
        UPDATE sprint
        SET SPR_FCH_INICIO = %s, SPR_FCH_FIN = %s, SPR_OBJETIVO = %s, SPR_ESTADO = %s, SPR_UID = %s
        WHERE SPR_ID = %s
    """, [fch_inicio, fch_fin, objetivo, estado, uid, id])
    con.connection.commit()
    con.close()

    return jsonify({"mensaje": "Se ha actualizado el sprint"})


# Eliminar sprint (requiere token)
@sprints_bp.route('/eliminar/<id>', methods=['DELETE'])
@jwt_required()
def deleteSprint(id):
    con = current_app.mysql.connection.cursor()
    con.execute("UPDATE sprint SET SPR_ESTADO = 0 WHERE SPR_ID = %s", [id])
    con.connection.commit()

    return jsonify({"mensaje": "Se ha eliminado el sprint"})
