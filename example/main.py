# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for, flash

from wtforms import Form

from pyuploadcare_wtforms import ImageField
from pyuploadcare import conf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
conf.pub_key = 'demopublickey'
conf.secret = 'demoprivatekey'


class PhotoForm(Form):
    image = ImageField()
    image_cropped = ImageField(manual_crop='200x200')


@app.route('/', methods=['POST', 'GET'])
def index():
    form = PhotoForm(request.form)
    form.validate()
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
