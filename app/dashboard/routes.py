from . import dashboard_bp
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Formulir
from app.extensions import db

@dashboard_bp.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@dashboard_bp.route('/formulir', methods=['GET', 'POST'])
@login_required
def formulir():
    if request.method == 'POST':
        nama = request.form['nama']
        alamat = request.form['alamat']
        ttl = request.form['ttl']
        asal_sekolah = request.form['asal_sekolah']
        no_hp = request.form['no_hp']
        data = Formulir(
            nama=nama,
            alamat=alamat,
            ttl=ttl,
            asal_sekolah=asal_sekolah,
            no_hp=no_hp,
            user_id=current_user.id
        )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    return render_template('formulir.html')