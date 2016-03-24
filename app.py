# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import furi
import write2odt
from flask import Flask, render_template, make_response, session, request
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
import glob
import os
import time

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
    if form.validate_on_submit():
        rstr = furi.add_yomi(preprocess_input(form.text.data))
        resp = make_response(render_template('main.html', form=form, rstr=rstr))
        filename = str(time.clock()) + '.odt'
        resp.set_cookie('filename', filename)

        write2odt.convert_and_save(rstr, filename)
        return resp

    return make_response(render_template('main.html', form=form))


@app.route('/download', methods=('GET', 'POST'))
def download():
    filename = request.cookies.get('filename')
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

