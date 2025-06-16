import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv ()
class config :
  MYSQL_HOST      = os.getenv("MYSQL_HOST")
  MYSQL_USER      = os.getenv("MYSQL_USER")
  MYSQL_PASSWORD  = os.getenv("MYSQL_PASSWORD")
  MYSQL_DB        = os.getenv("MYSQL_DB")

# try:
#     # Conexión inicial
#     conn = mysql.connector.connect(
#         host=config.MYSQL_HOST,
#         user=config.MYSQL_USER,
#         password=config.MYSQL_PASSWORD
#     )
#     cursor = conn.cursor()

#     # Crear la base de datos si no existe
#     cursor.execute("CREATE DATABASE IF NOT EXISTS db_scrum")
#     cursor.execute("USE db_scrum")

#     # Crear tabla proyecto
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS proyecto (
#         PROY_ID INT AUTO_INCREMENT PRIMARY KEY,
#         PROY_NOMBRE VARCHAR(255) NOT NULL,
#         PROY_DESCRIPCION TEXT,
#         PROY_ESTADO VARCHAR(50),
#         PROY_UID VARCHAR(100) UNIQUE NOT NULL
#     )
#     ''')

#     # Crear tabla sprint
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS sprint (
#         SPR_ID INT AUTO_INCREMENT PRIMARY KEY,
#         SPR_FCH_INICIO DATE NOT NULL,
#         SPR_FCH_FIN DATE NOT NULL,
#         SPR_OBJETIVO TEXT,
#         SPR_ESTADO VARCHAR(50),
#         SPR_UID VARCHAR(100) UNIQUE NOT NULL
#     )
#     ''')

#     # Crear tabla usuarios
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS usuarios (
#         USU_ID INT AUTO_INCREMENT PRIMARY KEY,
#         USU_NOMBRE VARCHAR(100) NOT NULL,
#         USU_APELLIDO VARCHAR(100) NOT NULL,
#         USU_CORREO VARCHAR(150) NOT NULL UNIQUE,
#         USU_ROL VARCHAR(50),
#         USU_ESTADO VARCHAR(50),
#         USU_UID VARCHAR(100) UNIQUE NOT NULL,
#         USU_CONTRASEÑA VARCHAR(255) NOT NULL
#     )
#     ''')


#     conn.commit()
#     print("Base de datos 'db_scrum' y tablas creadas correctamente.")

# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#         print("Error: Usuario o contraseña incorrectos.")
#     elif err.errno == errorcode.ER_BAD_DB_ERROR:
#         print("Error: La base de datos no existe.")
#     else:
#         print(f"Error: {err}")
# finally:
#     if conn.is_connected():
#         cursor.close()
#         conn.close()
  
