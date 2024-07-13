from page_analyzer.config import Config
from page_analyzer import models
from .forms import URLForm
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    flash,
    request,
    abort
)

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def get_and_check_url():
    form = URLForm()
    if form.validate_on_submit():
        if models.check_exist_url(form.url.data):
            flash('Страница уже существует', category='info')
        else:
            models.add_new_url(form.url.data)
            flash('Страница успешно добавлена', category='success')

        url_id = models.get_url_id(form.url.data)
        return redirect(url_for('get_url', url_id=url_id)), 302

    if request.method == 'POST':
        flash('Некорректный URL', category='error')

    return render_template('index.html', form=form)


@app.route('/urls/<url_id>')
def get_url(url_id=None):
    url_items = models.get_url_items(url_id)
    if not url_items:
        abort(404)
    return render_template('url_check.html', url_items=url_items)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404
