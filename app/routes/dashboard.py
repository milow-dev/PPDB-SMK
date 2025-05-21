from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Formulir
from app.extensions import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('dashboard.admin_dashboard'))
    else:
        formulir = Formulir.query.filter_by(user_id=current_user.id).first()
        return render_template('dashboard/dashboard.html', formulir=formulir)

@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Akses ditolak. Hanya admin yang bisa masuk.', 'danger')
        return redirect(url_for('dashboard.dashboard'))
    
    formulirs = Formulir.query.all()
    return render_template('dashboard/admin_dashboard.html', formulirs=formulirs)

@dashboard_bp.route('/verify/<int:formulir_id>', methods=['POST'])
@login_required
def verify_formulir(formulir_id):
    if not current_user.is_admin:
        flash('Akses ditolak.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    formulir = Formulir.query.get_or_404(formulir_id)
    action = request.form['action']

    if action == 'terima':
        formulir.status = 'Diterima'
        flash(f'Formulir {formulir.nama} diterima.', 'success')
    elif action == 'tolak':
        formulir.status = 'Ditolak'
        flash(f'Formulir {formulir.nama} ditolak.', 'warning')

    db.session.commit()
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard_bp.route('/formulir', methods=['GET', 'POST'])
@login_required
def formulir():
    if current_user.is_admin:
        flash('Admin tidak boleh isi formulir.', 'warning')
        return redirect(url_for('dashboard.dashboard'))

    existing_formulir = Formulir.query.filter_by(user_id=current_user.id).first()
    if existing_formulir:
        flash('Kamu sudah pernah isi formulir.', 'info')
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        formulir = Formulir(
            nama=request.form['nama'],
            ttl=request.form['ttl'],
            asal_sekolah=request.form['asal_sekolah'],
            no_hp=request.form['no_hp'],
            no_hp_ortu=request.form['no_hp_ortu'],
            user_id=current_user.id
        )
        db.session.add(formulir)
        db.session.commit()
        flash('Formulir berhasil dikirim, tunggu verifikasi.', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('dashboard/formulir.html')
