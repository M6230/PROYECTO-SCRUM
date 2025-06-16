from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['POST'])
def login():
    campos_requeridos = ["USU_CORREO", "USU_CONTRASEÑA"]
    peticion = request.json
    faltantes = [x for x in campos_requeridos if x not in peticion]

    if len(faltantes) > 0:
        return jsonify({"mensaje": f"Faltan campos en la petición: {faltantes}"}), 400

    correo = peticion["USU_CORREO"]
    contraseña = peticion["USU_CONTRASEÑA"]

    con = current_app.mysql.connection.cursor()
    con.execute("SELECT * FROM usuarios WHERE USU_CORREO = %s", (correo,))
    row = con.fetchone()

    if row is None:
        return jsonify({"mensaje": "Correo o contraseña incorrectos"}), 401

    columns = [col[0] for col in con.description]
    usuario = dict(zip(columns, row))

    if usuario['USU_CONTRASEÑA'] != contraseña:
        return jsonify({"mensaje": "Correo o contraseña incorrectos"}), 401

    from flask_jwt_extended import create_access_token
    access_token = create_access_token(identity=usuario['USU_UID'])

    return jsonify(access_token=access_token)
