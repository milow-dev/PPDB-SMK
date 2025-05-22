from . import dashboard_bp
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import Formulir, Payment
from app.extensions import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

@dashboard_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.home'))
        
    if current_user.role == 'admin':
        return redirect(url_for('dashboard.admin_dashboard'))
    
    formulir = Formulir.query.filter_by(user_id=current_user.id).first()
    if not formulir:
        return redirect(url_for('dashboard.formulir'))
    
    payment = Payment.query.filter_by(formulir_id=formulir.id).first()
    return render_template('dashboard.html', formulir=formulir, payment=payment)

@dashboard_bp.route('/formulir', methods=['GET', 'POST'])
@login_required
def formulir():
    # Check if user already has a form
    if Formulir.query.filter_by(user_id=current_user.id).first():
        return redirect(url_for('dashboard.dashboard'))
        
    if request.method == 'POST':
        data = Formulir(
            nama=request.form['nama'],
            alamat=request.form['alamat'],
            ttl=request.form['ttl'],
            asal_sekolah=request.form['asal_sekolah'],
            no_hp=request.form['no_hp'],
            user_id=current_user.id,
            status='pending'
        )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('dashboard.payment', formulir_id=data.id))
    return render_template('formulir.html')

@dashboard_bp.route('/payment/<int:formulir_id>', methods=['GET', 'POST'])
@login_required
def payment(formulir_id):
    formulir = Formulir.query.get_or_404(formulir_id)
    
    # Verify ownership
    if formulir.user_id != current_user.id:
        flash('Akses ditolak')
        return redirect(url_for('dashboard.dashboard'))
    
    # Check if payment already exists
    if Payment.query.filter_by(formulir_id=formulir_id).first():
        return redirect(url_for('dashboard.dashboard'))
        
    if request.method == 'POST':
        if 'payment_proof' not in request.files:
            flash('Tidak ada file yang dipilih')
            return redirect(request.url)
            
        file = request.files['payment_proof']
        if file.filename == '':
            flash('Tidak ada file yang dipilih')
            return redirect(request.url)
            
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
            payment = Payment(
                amount=float(request.form['amount']),
                payment_date=datetime.now(),
                payment_proof=filename,
                formulir_id=formulir_id,
                status='pending'
            )
            db.session.add(payment)
            db.session.commit()
            flash('Pembayaran berhasil diupload')
            return redirect(url_for('dashboard.dashboard'))
            
    return render_template('payment.html', formulir=formulir)

@dashboard_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Akses ditolak')
        return redirect(url_for('auth.login'))
        
    formulirs = Formulir.query.all()
    payments = Payment.query.all()
    pending_count = Formulir.query.filter_by(status='pending').count()
    payment_pending_count = Payment.query.filter_by(status='pending').count()
    
    return render_template('admin_dashboard.html', 
                         formulirs=formulirs, 
                         payments=payments,
                         pending_count=pending_count,
                         payment_pending_count=payment_pending_count)

@dashboard_bp.route('/admin/formulir/<int:formulir_id>/approve')
@login_required
def approve_formulir(formulir_id):
    if current_user.role != 'admin':
        flash('Akses ditolak')
        return redirect(url_for('auth.login'))
        
    formulir = Formulir.query.get_or_404(formulir_id)
    formulir.status = 'approved'
    db.session.commit()
    flash('Pendaftaran berhasil disetujui')
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard_bp.route('/admin/formulir/<int:formulir_id>/reject', methods=['POST'])
@login_required
def reject_formulir(formulir_id):
    if current_user.role != 'admin':
        flash('Akses ditolak')
        return redirect(url_for('auth.login'))
        
    formulir = Formulir.query.get_or_404(formulir_id)
    formulir.status = 'rejected'
    formulir.catatan = request.form.get('catatan')
    db.session.commit()
    flash('Pendaftaran ditolak')
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard_bp.route('/admin/payment/<int:payment_id>/verify')
@login_required
def verify_payment(payment_id):
    if current_user.role != 'admin':
        flash('Akses ditolak')
        return redirect(url_for('auth.login'))
        
    payment = Payment.query.get_or_404(payment_id)
    payment.status = 'verified'
    db.session.commit()
    flash('Pembayaran berhasil diverifikasi')
    return redirect(url_for('dashboard.admin_dashboard'))

@dashboard_bp.route('/admin/payment/<int:payment_id>/reject', methods=['POST'])
@login_required
def reject_payment(payment_id):
    if current_user.role != 'admin':
        flash('Akses ditolak')
        return redirect(url_for('auth.login'))
        
    payment = Payment.query.get_or_404(payment_id)
    payment.status = 'rejected'
    payment.catatan = request.form.get('catatan')
    db.session.commit()
    flash('Pembayaran ditolak')
    return redirect(url_for('dashboard.admin_dashboard'))