from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)    
    app.config.from_object('config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(idUser):
        from .models.users import User
        return User.query.get(int(idUser))

    # Import all models so they are registered with SQLAlchemy
    from .models.users import User
    from .models.perfil import Perfil
    from .models.publicacion import Publicacion
    from .models.etiqueta import Etiqueta

    # Register blueprints
    from app.routes import (
        auth, users_route, 
        users_route_async, perfil_route, publicacion_route
    )
    from app.routes.etiqueta_routes import etiqueta_bp
    app.register_blueprint(auth.bp)
    app.register_blueprint(users_route.bp)
    app.register_blueprint(users_route_async.bp)
    app.register_blueprint(perfil_route.bp)
    app.register_blueprint(publicacion_route.bp)
    app.register_blueprint(etiqueta_bp)

    @app.after_request
    def add_no_cache_headers(response):
        if current_user.is_authenticated:
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response

    @app.errorhandler(Exception)
    def handle_error(e):
        print(f"An error occurred: {str(e)}")
        return {"error": str(e)}, 500

    return app