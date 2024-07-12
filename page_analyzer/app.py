from page_analyzer.config import Config
from page_analyzer import models
from .forms import URLForm
from flask import (
    Flask,
    render_template,
    url_for,
    redirect
)

app = Flask(__name__)
app.config.from_object(Config)


# @app.route('/')
# def get_main_page(form=None):
#     form = URLForm() if not form else form
#     return render_template("index.html", form=form)


@app.route('/', methods=['GET', 'POST'])
def get_and_check_url():
    form = URLForm()
    if form.validate_on_submit():
        models.add_new_url(form.url.data)
        new_url_id = models.get_url_id(form.url.data)
        print(new_url_id)
        return redirect(url_for('get_url', url_id=new_url_id))
    return render_template('index.html', form=form)


@app.route('/urls/<url_id>')
def get_url(url_id=None, form=None):
    url_items = models.get_url_items(url_id)
    return render_template('url_check.html', url_id=url_id, url_items=url_items)
