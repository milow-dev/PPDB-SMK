from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class FormulirPPDB(FlaskForm):
    nama_siswa = StringField('Nama Siswa', validators=[DataRequired()])
    tanggal_lahir = DateField('Tanggal Lahir', format='%Y-%m-%d', validators=[DataRequired()])
    asal_sekolah = StringField('Asal Sekolah', validators=[DataRequired()])
    no_hp_siswa = StringField('Nomor HP Siswa', validators=[DataRequired()])
    no_hp_ortu = StringField('Nomor HP Orang Tua', validators=[DataRequired()])
    submit = SubmitField('Kirim Formulir')
    