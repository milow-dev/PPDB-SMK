from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.extensions import db
from app.models import User

test_bp = Blueprint('test', __name__)

# Login route
@test_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # Cek password
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))  # Ganti ke halaman dashboard kamu
        else:
            flash('Username atau password salah.', 'danger')
            return redirect(url_for('test.login'))
    return render_template('login.html')

# Register route
@test_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar.', 'danger')
            return redirect(url_for('test.register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Akun berhasil dibuat. Silakan login.', 'success')
        return redirect(url_for('test.login'))

    return render_template('register.html')

# Logout route
@test_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Kamu berhasil logout.', 'info')
    return redirect(url_for('test.login'))
