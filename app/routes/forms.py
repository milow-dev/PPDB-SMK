from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Judul Tugas', validators=[DataRequired()])
    submit = SubmitField('Tambah Tugas')
