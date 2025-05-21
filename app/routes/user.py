from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, login_manager
from app.models import User, Formulir  # Add Formulir import

user = Blueprint('user', __name__)

def create_admin():
    # Cek apakah sudah ada admin dengan username 'admin'
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            is_admin=True,
            email='admin@ppdb.com'  # Add required email field
        )
        admin.set_password('adminpassword')
        db.session.add(admin)
        db.session.commit()

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@user.route('/')
def index():
    return redirect(url_for('user.login'))

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = User.query.filter_by(username=username).first()

        if user_data and user_data.check_password(password):
            login_user(user_data)
            flash('Login berhasil!', 'success')

            if user_data.is_admin:
                return redirect(url_for('dashboard.dashboard'))
            else:
                return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Username atau password salah.', 'danger')
            return redirect(url_for('user.login'))

    return render_template('login.html')

@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar.', 'danger')
            return redirect(url_for('user.register'))

        new_user = User(username=username, is_admin=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Akun berhasil dibuat. Silakan login.', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html')

@user.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('user.admin_dashboard'))
    formulir = Formulir.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', formulir=formulir)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Kamu berhasil logout.', 'info')
    return redirect(url_for('user.login'))
