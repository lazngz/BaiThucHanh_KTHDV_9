from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    IdUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Token = db.Column(db.String(255))

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