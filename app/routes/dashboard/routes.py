from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import FormulirPPDB
from app.models import Formulir
from app.extensions import db
from . import dashboard_bp

@dashboard_bp.route('/formulir', methods=['GET', 'POST'])
@login_required
def formulir():
    if current_user.is_admin:
        flash('Admin tidak dapat mengisi formulir.')
        return redirect(url_for('dashboard.dashboard'))

    existing_formulir = Formulir.query.filter_by(user_id=current_user.id).first()
    if existing_formulir:
        flash('Anda sudah mengisi formulir sebelumnya.')
        return redirect(url_for('dashboard.dashboard'))

    form = FormulirPPDB()
    if form.validate_on_submit():
        new_formulir = Formulir(
            nama=form.nama.data,
            ttl=form.ttl.data,
            asal_sekolah=form.asal_sekolah.data,
            no_hp_siswa=form.no_hp_siswa.data,
            no_hp_ortu=form.no_hp_ortu.data,
            user_id=current_user.id,
            status='Menunggu Verifikasi'
        )
        db.session.add(new_formulir)
        db.session.commit()
        flash('Formulir berhasil disubmit. Silakan tunggu verifikasi admin.')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('dashboard/formulir.html', form=form)
