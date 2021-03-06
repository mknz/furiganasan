# -*- coding: utf-8 -*-

import os
import uuid

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired

import furi
import rubi_html
import write2odt


class ConfigError(Exception):
    pass

SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    raise ConfigError

app = Flask(__name__)
app.config.from_object(__name__)


class InputForm(Form):
    text = TextAreaField('テキストを入力', validators=[DataRequired()])


def preprocess_input(istr):
    istr = istr.replace('\r', '')
    return istr


@app.route('/', methods=('GET', 'POST'))
def main():
    form = InputForm()
    resp = make_response(render_template('main.html', form=form))
    resp.set_cookie('filename', "dummy")

    if form.validate_on_submit():
        try:
            rstr = furi.add_yomi(preprocess_input(form.text.data))
            rhtml = rubi_html.convert(rstr)
            resp = make_response(render_template('main.html', form=form, rstr=rstr, rhtml=rhtml))

            temp_file_str = str(uuid.uuid4())
            filename = '{}.odt'.format(temp_file_str)
            resp.set_cookie('filename', filename)

            write2odt.convert_and_save(rstr, os.path.join('/tmp', filename))
            return resp
        except:
            return render_template('main.html', form=form, rstr='Error!')

    return resp


@app.route('/download', methods=('GET', 'POST'))
def download():
    filename = os.path.join('/tmp',  request.cookies.get('filename'))
    if not os.path.exists(filename):
        form = InputForm()
        return render_template('main.html', form=form)

    f = open(filename, 'rb')
    response = make_response()
    response.data = f.read()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=furigana.odt'
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
