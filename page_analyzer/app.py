from page_analyzer.forms import URLForm
from page_analyzer.config import Config
from page_analyzer import parse_url
from page_analyzer import models
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    flash,
    abort
)

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    form = URLForm()
    return render_template('index.html', form=form)


@app.post('/urls')
def add_url():
    form = URLForm()
    if form.validate_on_submit():
        url = parse_url.get_netloc_url(form.url.data)
        if models.check_exist_url(url):
            flash('Страница уже существует', category='info')
        else:
            models.add_new_url(url)
            flash('Страница успешно добавлена', category='success')

        url_id = models.get_url_id(url)
        return redirect(url_for('get_url', url_id=url_id)), 302

    flash('Некорректный URL', category='error')
    return render_template('index.html', form=form), 422


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    url_items = models.get_url_items(url_id)
    if not url_items:
        abort(404)
    items_check_url = models.get_checks_url(url_id)
    return render_template('url_check.html',
                           url_items=url_items,
                           items_check_url=items_check_url,)


@app.post('/urls/<int:url_id>/checks')
def url_checks(url_id):
    url = models.get_url_items(url_id)['name']
    if models.add_new_check(url, url_id):
        flash('Страница успешно проверена', category='success')
    else:
        flash('Произошла ошибка при проверке', category='error')
    return redirect(url_for('get_url', url_id=url_id))


@app.route('/urls')
def get_urls():
    urls_checks = models.get_checks_urls()
    return render_template('urls.html', urls_checks=urls_checks)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404
