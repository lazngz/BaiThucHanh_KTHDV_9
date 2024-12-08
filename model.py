from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    IdUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Token = db.Column(db.String(255))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    db.ForeignKeyConstraint([order_id], ['order.id'], ondelete='CASCADE')

class OrderReport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False)
    total_revenue = db.Column(db.DECIMAL(10, 2), nullable=False)
    total_cost = db.Column(db.DECIMAL(10, 2), nullable=False)
    total_profit = db.Column(db.DECIMAL(10, 2), nullable=False)

class ProductReport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_report_id = db.Column(db.Integer, db.ForeignKey('order_report.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    total_sold = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.DECIMAL(10, 2), nullable=False)
    cost = db.Column(db.DECIMAL(10, 2), nullable=False)
    profit = db.Column(db.DECIMAL(10, 2), nullable=False)