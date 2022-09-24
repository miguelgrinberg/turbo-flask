import random
import re
import sys
import threading
import time
from flask import Flask, render_template, request, flash
from turbo_flask import Turbo

app = Flask(__name__)
app.secret_key = 'top-secret!'
turbo = Turbo(app)


@app.after_request
def after_request(response):
    # if the response has the turbo-stream content type, then append one more
    # stream with the contents of the alert section of the page
    if response.headers['Content-Type'].startswith(
            'text/vnd.turbo-stream.html'):
        response.response.append(turbo.update(
            render_template('alert.html'), 'alert').encode())
        if response.content_length:
            response.content_length += len(response.response[-1])
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    name_error = ''
    if request.method == 'POST':
        name = request.form['name']
        if name:
            flash(f'Hello, {name}!')
            name_error = ''
        else:
            flash('Invalid name')
            name_error = 'The username cannot be empty.'
        if turbo.can_stream():
            return turbo.stream(turbo.update(name_error, 'name_error'))
    return render_template('index.html', name_error=name_error)
