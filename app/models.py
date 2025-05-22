from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    formulirs = db.relationship('Formulir', backref='user', lazy=True)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lists = db.relationship('List', backref='board', lazy=True)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    cards = db.relationship('Card', backref='list', lazy=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50))    # todo, in-progress, done
    priority = db.Column(db.String(50))  # low, medium, high
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)

class Formulir(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    ttl = db.Column(db.String(100), nullable=False)
    asal_sekolah = db.Column(db.String(150), nullable=False)
    no_hp = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    catatan = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment = db.relationship('Payment', backref='formulir', uselist=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_proof = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    catatan = db.Column(db.Text, nullable=True)
    formulir_id = db.Column(db.Integer, db.ForeignKey('formulir.id'), nullable=False)
