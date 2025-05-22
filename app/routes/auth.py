from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username sudah terdaftar')
        return redirect(url_for('auth.register'))
    
    new_user = User(username=username, is_admin=False)  # Set as student by default
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('Pendaftaran berhasil')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
        
    if request.method == 'GET':
        role = request.args.get('role', 'siswa')
        return render_template('login.html', role=role)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'siswa')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Verify role matches
            if (role == 'admin' and user.is_admin) or (role == 'siswa' and not user.is_admin):
                login_user(user)
                flash('Login berhasil!')
                if user.is_admin:
                    return redirect(url_for('dashboard.admin'))
                return redirect(url_for('dashboard.student'))
            
        flash('Username atau password salah')
        return redirect(url_for('auth.login', role=role))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
