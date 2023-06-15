from flask import Flask, url_for, render_template, make_response
from flask import send_from_directory, flash, request, redirect
from werkzeug.utils import secure_filename
from utils import *
from db import *
import os
from pathlib import Path

UPLOAD_FOLDER = Path("tables")
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def cookie():
    if request.method == 'POST':
        res = make_response(redirect(url_for('posts')))
        username = request.form['data']
        res.set_cookie('username', username, max_age=60 * 60 * 24 * 365 * 2)
        return res
    else:
        return render_template('cookie.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_file1 = Posts(post_name = filename, cookie = request.cookies.get('username'))
            st_name = str(session.query(Posts).count() + 1)
            filename = st_name + filename
            try:
                session.add(upload_file1)
                session.commit()
            finally:
                session.close()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('posts'))
    return render_template('upload.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/graphs', methods=['GET', 'POST'])
def posts():
    if request.method == "POST":
        id = str(request.form['data'])
        return redirect(url_for('get', id = id))

    query = session.query(Posts).filter(Posts.cookie == request.cookies.get('username')).all()
    return render_template('graph.html', rows=query)

@app.route('/result/<id>')
def get(id):
    query1 = session.query(Posts.post_name).filter(Posts.id == id).first()
    path = str(id)+query1.post_name
    path = Path("tables", path)
    file = create_file(path)
    plot = plotting_graph(file)
    return render_template('test.html', plot_url=url_for('static', filename='myplot.png'))


if __name__ == "__main__":
    app.run(debug=True)
