from flask import Blueprint, app,jsonify,request
from app import db
from app.models import Role, User
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token,create_refresh_token,jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


login=Blueprint('userLogin', __name__, url_prefix='/userLogin')


@login.route('/add_role', methods=['POST'])
def add_role():
    data = request.get_json()

    # 1️⃣ Validate input
    if not data or 'role_name' not in data:
        return jsonify({"error": "role_name is required"}), 400

    try:
        # 2️⃣ Create and add new role
        new_role = Role(role_name=data['role_name'])
        db.session.add(new_role)
        db.session.commit()
        return jsonify({"message": "Role added successfully"}), 201

    except IntegrityError:
        # 3️⃣ Handle unique constraint violation
        db.session.rollback()
        return jsonify({"error": "Role already exists"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    


# 📝 SIGNUP
@login.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data.get("email") or not data.get("password") or not data.get("full_name"):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = generate_password_hash(data['password'])
    new_user = User(full_name=data['full_name'], email=data['email'], password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
    

# 🔐 SIGNIN
@login.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token (valid for 1 hour)
    token = create_access_token(identity=str(user.email))
    ref_token = create_refresh_token(identity=str(user.email))
    return jsonify({"message": "Login successful", "token": token, "refresh_token": ref_token})


# 🔄 REFRESH TOKEN
@login.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({"token": new_token}), 200