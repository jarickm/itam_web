from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default="Admin")

class Asset(db.Model):
    __tablename__ = 'asset_labels'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    qr_asset_code = db.Column(db.String(50), unique=True)
    date_encoded = db.Column(db.Date, default=datetime.utcnow)
    control_number = db.Column(db.String(50))
    item_description = db.Column(db.Text)
    issued_to = db.Column(db.String(100))
    date_purchase = db.Column(db.Date)
    status = db.Column(db.String(20), default="Available")

class AssetHistory(db.Model):
    __tablename__ = 'asset_history'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer)
    change_date = db.Column(db.DateTime, default=datetime.utcnow)
    changed_by = db.Column(db.String(50))
    action = db.Column(db.String(50))
    status = db.Column(db.String(20))
    issued_to = db.Column(db.String(100))
    notes = db.Column(db.Text)