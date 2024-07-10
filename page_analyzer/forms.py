from flask_wtf import FlaskForm
from wtforms.validators import URL, InputRequired, Length
from wtforms import URLField, SubmitField


class URLForm(FlaskForm):
    url = URLField('', validators=[InputRequired(), URL(), Length(max=255)])
    check = SubmitField('Проверить')
