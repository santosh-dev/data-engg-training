from flask import Flask, jsonify, request
import json

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Product API'
    }
)
app = Flask(__name__)

products = [
    { 'name': 'dell xps 13', 'description': 'Dell performance laptop', 'price': 50000 }
]


@app.route('/products')
def get_products():
    return jsonify(products)

def product_is_valid(product):
 for key in product.keys():
   if key != 'name':
     return False
 return True

@app.route('/products', methods=['POST'])
def add_product():
    products.append(request.get_json())
    return 'Product successfully added', 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id: int):
 product = get_products(id)
 if product is None:
   return jsonify({ 'error': 'product does not exist.' }), 404

 updated_product = json.loads(request.data)
 if not product_is_valid(updated_product):
   return jsonify({ 'error': 'Invalid product properties.' }), 400

 product.update(updated_product)

 return jsonify(product)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id: int):
 global products
 product = get_products(id)
 if product is None:
   return jsonify({ 'error': 'product does not exist.' }), 404

 products = [e for e in products if e['id'] != id]
 return jsonify(product), 200


if __name__ == '__main__':
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    app.run(debug=True,host="0.0.0.0",port=8080)
    #app.run(port=5000)