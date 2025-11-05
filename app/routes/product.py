from flask import Blueprint,jsonify,request
from app import db
from app.models import Brand, Category,Product,ProductImage
import cloudinary
import cloudinary.api
import cloudinary.uploader

product = Blueprint('product', __name__, url_prefix='/product')

# 🆕 ADD PRODUCT
@product.route('/add_category', methods=['POST'])
def add_category():
    try:
        data = request.get_json()
        name = data.get('name')
        parent_id = data.get('parent_id')

        new_category = Category(name=name, parent_id=parent_id)
        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            "message": "Category added successfully",
            "category_id": new_category.category_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@product.route('/add_brand', methods=['POST'])
def add_brand():
    try:
        data = request.get_json()
        name = data.get('name')

        # Assuming Brand model exists
        new_brand = Brand(name=name)
        db.session.add(new_brand)
        db.session.commit()

        return jsonify({
            "message": "Brand added successfully",
            "brand_id": new_brand.brand_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@product.route('/add_product', methods=['POST'])
def add_product():
    try:
        # Get non-file fields from request.form
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        sku = request.form.get('stock_quantity')
        category_id = request.form.get('category_id')
        brand_id = request.form.get('brand_id')
        discount = request.form.get('discount')
        is_active = request.form.get('is_active')

        # Get the image file
        image = request.files.get('image')

        # Upload image to Cloudinary if provided
        image_url = None
        if not image:
            return jsonify({"message": "Image file is required"}), 400
        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result.get('secure_url')
        public_id = upload_result.get('public_id')

        # Create new product
        new_product = Product(
            name=name,
            description=description,
            price=price,
            sku=sku,
            category_id=category_id,
            brand_id=brand_id,
            discount=discount,
            is_active=is_active,
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "message": "Product added successfully",
            "product_id": new_product.product_id,
            "image_url": image_url
        }), 201
    
    except Exception as e:
        # ❌ If anything fails → delete uploaded Cloudinary image
        if 'public_id' in locals():
            cloudinary.uploader.destroy(public_id)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@product.route('/add_image', methods=['POST'])
def add_image():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        image_url= data.get('image_url')

        if not product_id or not image_url:
            return jsonify({"message": "product_id and image_url are required"}), 400

        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        new_image = ProductImage(product_id=product_id, image_url=image_url)
        db.session.add(new_image)
        db.session.commit()

        return jsonify({
            "message": "Image added successfully",
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@product.route('/get_products', methods=['GET'])
def get_products():
    try:
        page = int(request.args.get('page', 1))
        per_page = 10

        if page < 1:
            return jsonify({"message": "Page number must be at least 1"}), 400

        products = Product.query.all()
        total = len(products)

        start = (page - 1) * per_page
        end = start + per_page
        paginated = products[start:end]
        
        product_list = []
        for product in paginated:
            images = ProductImage.query.filter_by(product_id=product.product_id).all()
            product_data = {
                "product_id": product.product_id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "sku": product.sku,
                "category_id": product.category_id,
                "brand_id": product.brand_id,
                "discount": str(product.discount),
                "is_active": product.is_active,
                'images': [image.image_url for image in images]
            }
            product_list.append(product_data)
        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500