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