from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from . import auth_bp
from app.extensions import db

@auth_bp.route('/home')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('dashboard.admin_dashboard'))
        return redirect(url_for('dashboard.dashboard'))
    return render_template('home.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar')
            return redirect(url_for('auth.register'))
            
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('dashboard.admin_dashboard'))
            if not user.formulirs:
                return redirect(url_for('dashboard.formulir'))
            return redirect(url_for('dashboard.dashboard'))
        flash('Username atau password salah')
    return render_template('login.html')

@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, role='admin').first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard.admin_dashboard'))
        flash('Username atau password admin salah')
    return render_template('admin_login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))