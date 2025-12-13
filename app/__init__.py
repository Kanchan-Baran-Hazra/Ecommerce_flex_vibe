from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.api
import cloudinary.uploader
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate 
from flask_apscheduler import APScheduler
from datetime import datetime,timedelta

db = SQLAlchemy()
jwt = JWTManager()
mail=Mail()
migrate=Migrate()
Schudule=APScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)
    Schudule.init_app(app)
    Schudule.start()
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
    
    from app.routes.Oauth import auth_bp
    app.register_blueprint(auth_bp)
    
    # ✅ Cloudinary Config
    cloudinary.config(
        cloud_name = app.config['CLOUDINARY_CLOUD_NAME'],
        api_key = app.config['CLOUDINARY_API_KEY'],
        api_secret = app.config['CLOUDINARY_API_SECRET']
    )
    
    from app.btask import delete_unverified_users
    # Run the job every 24 hours
    Schudule.add_job(
        id='cleanup_task',
        func=lambda: delete_unverified_users(app),
        trigger='interval',
        hours=24
    )

    # ✅ Create tables within app context
    with app.app_context():
        db.create_all()

    return app
