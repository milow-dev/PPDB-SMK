from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Formulir, db

admin_bp = Blueprint('admin', __name__, template_folder='../templates')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Akses hanya untuk admin.', 'danger')
        return redirect(url_for('user.login'))
    
    formulirs = Formulir.query.all()
    return render_template('admin/dashboard.html', formulirs=formulirs)

@admin_bp.route('/konfirmasi/<int:id>/<string:status>')
@login_required
def konfirmasi(id, status):
    if current_user.role != 'admin':
        flash('Akses hanya untuk admin.', 'danger')
        return redirect(url_for('user.login'))
    
    formulir = Formulir.query.get_or_404(id)
    formulir.status = status
    db.session.commit()
    flash(f'Formulir {formulir.nama} berhasil di-{status}', 'success')
    return redirect(url_for('admin.dashboard'))
