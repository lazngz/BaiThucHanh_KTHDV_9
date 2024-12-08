from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import datetime
from model import db, User, Order, OrderItem  

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'your_secret_key' 

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('userName', None)
    password = request.json.get('password', None)
    
    user = User.query.filter_by(UserName=username).first()
    if user and user.Password == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@app.route('/orders', methods=['POST'])
@jwt_required() 
def create_order():
    data = request.get_json()
    
    customer_name = data['customer_name']
    customer_email = data['customer_email']
    total_amount = data['total_amount']
    status = data['status']
    order_items = data['order_items']
    
    new_order = Order(
        customer_name=customer_name,
        customer_email=customer_email,
        total_amount=total_amount,
        status=status
    )
    db.session.add(new_order)
    db.session.commit()

    for item in order_items:
        new_order_item = OrderItem(
            order_id=new_order.id,
            product_id=item['product_id'],
            product_name=item['product_name'],
            quantity=item['quantity'],
            unit_price=item['unit_price'],
            total_price=item['quantity'] * item['unit_price']
        )
        db.session.add(new_order_item)
    db.session.commit()

    return jsonify({"message": "Order created", "order_id": new_order.id}), 201

@app.route('/orders', methods=['GET'])
@jwt_required() 
def get_orders():
    orders = Order.query.all()
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'total_amount': str(order.total_amount),
            'status': order.status,
            'created_at': order.created_at,
            'updated_at': order.updated_at
        })
    return jsonify({"orders": result}), 200

@app.route('/orders/<int:id>', methods=['GET'])
@jwt_required() 
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    order_items = OrderItem.query.filter_by(order_id=id).all()
    items = []
    for item in order_items:
        items.append({
            'product_id': item.product_id,
            'product_name': item.product_name,
            'quantity': item.quantity,
            'unit_price': str(item.unit_price),
            'total_price': str(item.total_price)
        })
    return jsonify({
        'order': {
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'total_amount': str(order.total_amount),
            'status': order.status,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
            'items': items
        }
    }), 200

@app.route('/orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    data = request.get_json()
    order.status = data.get('status', order.status)
    order.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Order updated", "order_id": order.id}), 200

@app.route('/orders/<int:id>', methods=['DELETE'])
@jwt_required() 
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({"message": "Order deleted", "order_id": id}), 200

@app.route('/order_items', methods=['POST'])
@jwt_required() 
def create_order_item():
    data = request.get_json()
    
    order_id = data['order_id']
    product_id = data['product_id']
    product_name = data['product_name']
    quantity = data['quantity']
    unit_price = data['unit_price']
    
    new_order_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
        total_price=quantity * unit_price
    )
    db.session.add(new_order_item)
    db.session.commit()

    return jsonify({"message": "Order item created", "order_item_id": new_order_item.id}), 201

@app.route('/order_items', methods=['GET'])
@jwt_required() 
def get_order_items():
    order_items = OrderItem.query.all()
    result = []
    for item in order_items:
        result.append({
            'order_id': item.order_id,
            'product_id': item.product_id,
            'product_name': item.product_name,
            'quantity': item.quantity,
            'unit_price': str(item.unit_price),
            'total_price': str(item.total_price)
        })
    return jsonify({"order_items": result}), 200

@app.route('/order_items/<int:id>', methods=['GET'])
@jwt_required() 
def get_order_item(id):
    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({"message": "Order item not found"}), 404
    
    return jsonify({
        'order_item': {
            'id': order_item.id,
            'order_id': order_item.order_id,
            'product_id': order_item.product_id,
            'product_name': order_item.product_name,
            'quantity': order_item.quantity,
            'unit_price': str(order_item.unit_price),
            'total_price': str(order_item.total_price)
        }
    }), 200

@app.route('/order_items/<int:id>', methods=['PUT'])
@jwt_required()
def update_order_item(id):
    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({"message": "Order item not found"}), 404
    
    data = request.get_json()
    order_item.quantity = data.get('quantity', order_item.quantity)
    order_item.unit_price = data.get('unit_price', order_item.unit_price)
    order_item.total_price = order_item.quantity * order_item.unit_price
    db.session.commit()
    
    return jsonify({"message": "Order item updated", "order_item_id": order_item.id}), 200

@app.route('/order_items/<int:id>', methods=['DELETE'])
@jwt_required() 
def delete_order_item(id):
    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({"message": "Order item not found"}), 404
    
    db.session.delete(order_item)
    db.session.commit()
    
    return jsonify({"message": "Order item deleted", "order_item_id": id}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)
