from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.api
import cloudinary.uploader
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate


db = SQLAlchemy()
jwt = JWTManager()
mail=Mail()
migrate=Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)
    CORS(app)

    from app.routes.main import main
    app.register_blueprint(main)

    from app.routes.userLogin import login
    app.register_blueprint(login)
    
    from app.routes.home import home
    app.register_blueprint(home)

    from app.routes.product import product
    app.register_blueprint(product)

    from app.routes.Email_message import email_send
    app.register_blueprint(email_send)

    from app.routes.otp_verify import otp_ver
    app.register_blueprint(otp_ver)
    
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
