# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import furi
import write2odt
from flask import Flask, render_template, make_response, session
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
import random
import glob
import os

SECRET_KEY = 'fdfsasfdee3@re'

app = Flask(__name__)
app.config.from_object(__name__)

for f in glob.glob("*.odt"):
    os.remove(f)

FILENAME = str(int(random.random()*1e6)) + '.odt'

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
        write2odt.convert_and_save(rstr, FILENAME)
        return render_template('main.html', form=form, rstr=rstr)
    return render_template('main.html', form=form)


@app.route('/download', methods=('GET', 'POST'))
def download():
    if not os.path.exists(FILENAME):
        form = MyForm()
        return render_template('main.html', form=form)

    f = open(FILENAME, 'rb')
    response = make_response()
    response.data = f.read()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename=furigana.odt'
    return response
    

if __name__ == "__main__":
    app.run(host="0.0.0.0")

