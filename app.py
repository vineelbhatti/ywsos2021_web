from flask import Flask, render_template
from flask_session import Session
from flask_pymongo import PyMongo
import pymongo
import os
from config import Config

app = Flask(__name__)


app.config.from_object(Config)


mongo = PyMongo(app)

Session(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
