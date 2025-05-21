from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from . import auth_bp
from app.extensions import db


@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash('Password tidak cocok.', 'danger')
        return redirect(url_for('auth.login'))

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username sudah terdaftar.', 'danger')
        return redirect(url_for('auth.login'))

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role='siswa')
    db.session.add(new_user)
    db.session.commit()

    flash('Pendaftaran berhasil, silakan login.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, role=role).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Berhasil login.', 'success')

            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))
        else:
            flash('Username atau password salah.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
