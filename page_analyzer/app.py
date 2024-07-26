from page_analyzer.forms import URLForm
from page_analyzer.config import Config
from page_analyzer import parse_url
from page_analyzer import db
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
        connection = db.make_connection()
        url = parse_url.get_netloc_url(form.url.data)
        if db.check_exist_url(connection, url):
            flash('Страница уже существует', category='info')
        else:
            db.add_new_url(connection, url)
            flash('Страница успешно добавлена', category='success')

        url_id = db.get_url_id(connection, url)

        connection.close()
        return redirect(url_for('get_url', url_id=url_id)), 302

    flash('Некорректный URL', category='error')
    return render_template('index.html', form=form), 422


@app.route('/urls/<int:url_id>')
def get_url(url_id):
    connection = db.make_connection()
    url_items = db.get_url_items(connection, url_id)
    if not url_items:
        abort(404)
    items_check_url = db.get_checks_url(connection, url_id)

    connection.close()
    return render_template('url_check.html',
                           url_items=url_items,
                           items_check_url=items_check_url)


@app.post('/urls/<int:url_id>/checks')
def url_checks(url_id):
    connection = db.make_connection()
    url = db.get_url_items(connection, url_id)['name']
    if db.add_new_check(connection, url, url_id):
        flash('Страница успешно проверена', category='success')
    else:
        flash('Произошла ошибка при проверке', category='error')
    connection.close()
    return redirect(url_for('get_url', url_id=url_id))


@app.route('/urls')
def get_urls():
    connection = db.make_connection()
    urls_checks = db.get_checks_urls(connection)
    connection.close()
    return render_template('urls.html', urls_checks=urls_checks)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404
