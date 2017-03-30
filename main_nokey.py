import os
from flask import Flask, redirect, request, render_template, url_for
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from flask_wtf.csrf import CSRFProtect
from mailchimp3 import MailChimp

weekly_client = MailChimp('MailChimp_USERNAME', 'MailChimp_API_Key')
SECRET_KEY = 'enter your key here'
RECAPTCHA_PUBLIC_KEY = "enter your key here"
RECAPTCHA_PRIVATE_KEY = "enter your key here"

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


@app.route('/success')
def success():
    return 'Congratulations, you\'ve successfully subscribed CCNS Weekly'


@app.route('/failed')
def failed():
    return 'Sorry, but the action failed, please try again'


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate_on_submit():
            email = form.email.data
        else:
            return failed()
        weekly_client.lists.members.create('8f670626ea', {'email_address': email, 'status': 'subscribed',})
        return render_template('form_success.html', email=email)
        # do_subscribe(request.form['user_email'])
    else:
        return redirect(url_for('index'), code=302)


def do_subscribe(email):
    return render_template('form_success.html', email=email)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
