from flask import Blueprint,jsonify,request
from app import db
# from app.models import User
from sqlalchemy import text
import cloudinary.uploader

main=Blueprint('main', __name__, url_prefix='/main')

@main.route('/')
def index():
    return "Hello from the main blueprint!"

# @main.route('/testdb')
# def test_db():
#     try:
#         result = db.session.execute(text("SELECT NOW();"))  # ✅ wrap in text()
#         server_time = list(result)[0][0]
#         return jsonify({
#             "message": "Connected to TiDB Cloud!",
#             "server_time": str(server_time)
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)})
    
# @main.route('/add_user')
# def get_users():
#     new_user = User(name="Kanchan", email="kanchan@example.com")
#     db.session.add(new_user)
#     db.session.commit()
#     print('ADDED USER:', new_user.name)
#     return jsonify({"message": "User added successfully!"})


# @main.route('/upload', methods=['POST'])
# def upload_image():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image provided"}), 400

#     image = request.files['image']
    
#     if image.filename == '':
#         return jsonify({"error": "No file selected"}), 400

#     try:
#         upload_result = cloudinary.uploader.upload(image)
#         return jsonify({
#             "message": "Upload successful!",
#             "url": upload_result['secure_url'],
#             "public_id": upload_result['public_id']
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

