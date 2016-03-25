# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import furi
import write2odt
import rubi_html
from flask import Flask, render_template, make_response, request
from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired
import os
import random

SECRET_KEY = 'fdfsasfdee3@re'

app = Flask(__name__)
app.config.from_object(__name__)

class MyForm(Form):
    text = TextAreaField('テキストを入力', validators=[DataRequired()])

def preprocess_input(istr):
    istr = istr.replace('\r', '')
    return istr

@app.route('/', methods=('GET', 'POST'))
def main():
    form = MyForm()
    resp = make_response(render_template('main.html', form=form))
    resp.set_cookie('filename', "dummy")

    if form.validate_on_submit():
        rstr = furi.add_yomi(preprocess_input(form.text.data))
        rhtml = rubi_html.convert(rstr)
        print(rhtml)
        resp = make_response(render_template('main.html', form=form, rstr=rstr, rhtml=rhtml))
        filename = str(int(random.random()*1e8)) + '.odt'
        resp.set_cookie('filename', filename)

        write2odt.convert_and_save(rstr, '/tmp/' + filename)
        return resp

    return resp


@app.route('/download', methods=('GET', 'POST'))
def download():
    filename = '/tmp/' + request.cookies.get('filename')
    if not os.path.exists(filename):
        form = MyForm()
        return render_template('main.html', form=form)

    f = open(filename, 'rb')
    response = make_response()
    response.data = f.read()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=furigana.odt'
    return response
    

if __name__ == "__main__":
    app.run(host="0.0.0.0")

