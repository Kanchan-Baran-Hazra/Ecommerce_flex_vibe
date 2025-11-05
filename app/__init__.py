from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.api
import cloudinary.uploader
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.main import main
    app.register_blueprint(main)

    from app.routes.userLogin import login
    app.register_blueprint(login)
    
    from app.routes.home import home
    app.register_blueprint(home)

    from app.routes.product import product
    app.register_blueprint(product)
    
    # ✅ Cloudinary Config
    cloudinary.config(
        cloud_name = app.config['CLOUDINARY_CLOUD_NAME'],
        api_key = app.config['CLOUDINARY_API_KEY'],
        api_secret = app.config['CLOUDINARY_API_SECRET']
    )

    # ✅ Create tables within app context
    with app.app_context():
        db.create_all()

    return app
