from .config import Config
from .forms import URLForm
from flask import (
    Flask,
    render_template,
    url_for,
    redirect
)

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def get_main_page():
    form = URLForm()
    return render_template("index.html", title="Анализатор страниц", form=form)


@app.post('/urls')
def check_url():
    return redirect(url_for('get_url'))


@app.route('/urls/')
def get_url():
    return 'hello'
