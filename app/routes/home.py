from flask import Blueprint,jsonify,request
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User

home = Blueprint('home', __name__, url_prefix='/home')


# 🛡️ PROTECTED ROUTE
@home.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()  # email from token
    user = User.query.filter_by(email=current_user).first()
    return jsonify({
        "full_name": user.full_name,
        "email": user.email
    })