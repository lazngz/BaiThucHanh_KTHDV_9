from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, User, OrderReport,ProductReport
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

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

@app.route('/reports/products', methods=['GET'])
@jwt_required()
def get_product_reports():
    reports = ProductReport.query.all()
    result = []
    for report in reports:
        result.append({
            'id': report.id,
            'order_report_id': report.order_report_id,
            'product_id': report.product_id,
            'total_sold': report.total_sold,
            'revenue': report.revenue,
            'cost': report.cost,
            'profit': report.profit
        })
    return jsonify(result), 200

@app.route('/reports/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product_report_by_id(id):
    report = ProductReport.query.get_or_404(id)
    return jsonify({
        'id': report.id,
        'order_report_id': report.order_report_id,
        'product_id': report.product_id,
        'total_sold': report.total_sold,
        'revenue': report.revenue,
        'cost': report.cost,
        'profit': report.profit
    }), 200

@app.route('/reports/products', methods=['POST'])
@jwt_required()
def create_product_report():
    data = request.get_json()
    new_report = ProductReport(
        order_report_id=data['order_report_id'],
        product_id=data['product_id'],
        total_sold=data['total_sold'],
        revenue=data['revenue'],
        cost=data['cost'],
        profit=data['profit']
    )
    db.session.add(new_report)
    db.session.commit()
    return jsonify(message="Product report created successfully"), 201

@app.route('/reports/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product_report(id):
    report = ProductReport.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    return jsonify(message="Product report deleted successfully"), 200

@app.route('/reports/orders', methods=['GET'])
@jwt_required()
def get_order_reports():
    reports = OrderReport.query.all()
    result = []
    for report in reports:
        result.append({
            'id': report.id,
            'order_id': report.order_id,
            'total_revenue': report.total_revenue,
            'total_cost': report.total_cost,
            'total_profit': report.total_profit
        })
    return jsonify(result), 200

@app.route('/reports/orders/<int:id>', methods=['GET'])
@jwt_required()
def get_order_report_by_id(id):
    report = OrderReport.query.get_or_404(id)
    return jsonify({
        'id': report.id,
        'order_id': report.order_id,
        'total_revenue': report.total_revenue,
        'total_cost': report.total_cost,
        'total_profit': report.total_profit
    }), 200

@app.route('/reports/orders', methods=['POST'])
@jwt_required()
def create_order_report():
    data = request.get_json()
    new_report = OrderReport(
        order_id=data['order_id'],
        total_revenue=data['total_revenue'],
        total_cost=data['total_cost'],
        total_profit=data['total_revenue'] - data['total_cost']
    )
    db.session.add(new_report)
    db.session.commit()
    return jsonify(message="Order report created successfully"), 201

@app.route('/reports/orders/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order_report(id):
    report = OrderReport.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    return jsonify(message="Order report deleted successfully"), 200

if __name__ == '__main__':
    app.run(debug=True, port=5004)
