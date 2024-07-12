from flask_wtf import FlaskForm
from wtforms.validators import url, InputRequired, Length
from wtforms import SubmitField, StringField


class URLForm(FlaskForm):
    url = StringField('', validators=[InputRequired(), url(), Length(max=255)])
    check = SubmitField('Проверить')
