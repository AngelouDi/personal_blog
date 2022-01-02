import sys
from datetime import datetime
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
import re

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
DEV_POSTS_DIR = 'dev_posts'
PERSONAL_POSTS_DIR = 'personal_posts'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}


@app.route("/dev_posts/")
def dev_posts():
    posts = [p for p in flatpages if p.path.startswith(DEV_POSTS_DIR)]
    posts.sort(key=lambda item: datetime.strptime(item['date'], "%d/%m/%Y"), reverse=True)
    return render_template('posts.html', posts=posts)


@app.route("/personal_posts/")
def personal_posts():
    posts = [p for p in flatpages if p.path.startswith(PERSONAL_POSTS_DIR)]
    posts.sort(key=lambda item: datetime.strptime(item['date'], "%d/%m/%Y"), reverse=True)
    return render_template('posts.html', posts=posts)


@app.route('/dev_posts/<name>/')
def dev_post(name):
    path = '{}/{}'.format(DEV_POSTS_DIR, name)
    post = flatpages.get_or_404(path)
    return (render_template('post.html', post=post))


@app.route('/personal_posts/<name>/')
def personal_post(name):
    path = '{}/{}'.format(PERSONAL_POSTS_DIR, name)
    post = flatpages.get_or_404(path)
    return (render_template('post.html', post=post))


@app.route('/')
def index():
    posts = [p for p in flatpages]
    posts.sort(key=lambda item: datetime.strptime(item['date'], "%d/%m/%Y"), reverse=True)
    return render_template('index.html', posts=posts)

@app.route("/contact/")
def contact():
    return render_template('contact.html')


@app.template_filter()
def regex_replace(s, find, replace):
    return re.sub(find, replace, s)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)
