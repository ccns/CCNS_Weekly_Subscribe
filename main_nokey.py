import os
from flask import Flask, redirect, request, render_template, url_for
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from flask_wtf.csrf import CSRFProtect
import json
import requests


URL = "https://<DC>.api.mailchimp.com/3.0/lists/<List ID>/members"
SECRET_KEY = '<SECRET_KEY>'
RECAPTCHA_PUBLIC_KEY = "<RECAPTCHA_PUBLIC_KEY>"
RECAPTCHA_PRIVATE_KEY = "<RECAPTCHA_PRIVATE_KEY>"


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(__name__)


class EmailForm(FlaskForm):
    email = EmailField('email', [validators.DataRequired(), validators.Email()])
    recaptcha = RecaptchaField()


@app.route('/')
def index(form=None):
    if form is None:
        form = EmailForm()
    return render_template('form_submit.html', form=form)


@app.route('/failed')
def failed():
    return render_template('form_failed.html') 


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate_on_submit():
            email = form.email.data
        else:
            return failed()
        post_data = {'email_address': email, 'status': 'subscribed'}
        auth = ('user', '<API_KEY>')
        r = requests.post(URL, data=json.dumps(post_data), auth=auth)
        if r.status_code == 200:
            return render_template('form_success.html', email=email)
        else:
            return failed()
    else:
        return redirect(url_for('index'), code=302)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
