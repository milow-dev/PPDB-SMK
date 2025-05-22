from app.extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    formulirs = db.relationship('Formulir', backref='user', lazy=True)
=======
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
>>>>>>> dbd657281f5a6ccc42ee16120d6febdfb2c7ee73

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Formulir(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    umur = db.Column(db.Integer, nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    ttl = db.Column(db.String(100), nullable=False)
    asal_sekolah = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.String(20), nullable=False)
<<<<<<< HEAD
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    catatan = db.Column(db.Text, nullable=True)
=======
    no_hp_ortu = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Menunggu Verifikasi')
>>>>>>> dbd657281f5a6ccc42ee16120d6febdfb2c7ee73
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
