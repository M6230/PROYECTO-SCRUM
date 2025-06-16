from .usuarios import usuarios_bp
from .proyectos import proyectos_bp
from .sprints import sprints_bp
from .auth import auth_bp
from .documentacion import documentacion_bp

def registrar_rutas(app):
    app.register_blueprint(usuarios_bp, url_prefix  ='/usuarios')
    app.register_blueprint(proyectos_bp, url_prefix  ='/proyectos')
    app.register_blueprint(sprints_bp, url_prefix  ='/sprints')
    app.register_blueprint(auth_bp, url_prefix  ='/auth')
    app.register_blueprint(documentacion_bp, url_prefix  ='/documentacion')