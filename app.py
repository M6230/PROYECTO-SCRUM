from flask import Flask
from flask_mysqldb import MySQL 
from routes import registrar_rutas
from config import config

app = Flask(__name__)
app.config.from_object(config)
mysql = MySQL(app)

app.mysql = mysql

registrar_rutas(app)

if __name__ == '__main__':
    app.run(debug=True) 
