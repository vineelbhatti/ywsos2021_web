from flask import Flask, render_template, jsonify, request, redirect, session
from flask_session import Session
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
import pymongo
import os
from config import Config, db
import datetime
import jwt
import bson

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)

Session(app)

################Token Decorator#########################

SECRET_KEY = app.config['SECRET_KEY']

def token_required(something):
    def wrap_token():
        try:
            token_passed = request.headers['TOKEN']
            if request.headers['TOKEN'] != '' and request.headers['TOKEN'] != None:
                try:
                    data = jwt.decode(token_passed,SECRET_KEY, algorithms=['HS256'])
                    return something(data['user_id'])
                except jwt.exceptions.ExpiredSignatureError:
                    return_data = {
                        "error": "1",
                        "message": "Token has expired"
                        }
                    return jsonify(return_data)
                except:
                    return_data = {
                        "error": "1",
                        "message": "Invalid Token"
                    }
                    return jsonify(return_data)
            else:
                return_data = {
                    "error" : "2",
                    "message" : "Token required",
                }
                return jsonify(return_data)
        except Exception as e:
            print(e)
            return_data = {
                "error" : "3",
                "message" : "An error occured",
                "d_message" : str(e)
                }
            return jsonify(return_data)
    return wrap_token

##############Login & Singup############################################
def handle_auth(login_form, signup_form, url):
    users = db['users']
    session['logged_in'] = False
    if login_form.validate_on_submit():
        result = users.find_one({
            'username': login_form.username.data,
            'password': login_form.password.data,
        })
        if result != None:
            session['logged_in'] = True
            session['logged_in_id'] = result['_id']
            return redirect('/main')
        return redirect(url)
    if signup_form.validate_on_submit():
        users.insert_one({
            "username": signup_form.username.data,
            "email": signup_form.email.data,
            "password": signup_form.password.data,
        })
        return redirect(url)
    return None
#########Require Login#################################################
def login_required(something):
    def wrap():
        if session['logged_in']:
            return something(session['logged_in_id'])
        else:
            return redirect('/')
    return wrap

########################################################################
#########################Forms##########################################
########################################################################
class LoginForm(FlaskForm):
    username = StringField("Username :", validators = [DataRequired()])
    password = PasswordField("Password :", validators = [DataRequired()])
    submit = SubmitField("Log In")

class SignupForm(FlaskForm):
    username = StringField("Username :", validators = [DataRequired()])
    email = StringField("Email :", validators = [DataRequired(), Email()])
    password = PasswordField("Password :", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password :", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")
########################################################################
#########################Routes#########################################
########################################################################
@app.route('/about', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def about():
    login_form = LoginForm()
    signup_form = SignupForm()
    res = handle_auth(login_form, signup_form, '/')
    if res != None:
        return res
    return render_template('index.html', login_form=login_form, signup_form=signup_form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    login_form = LoginForm()
    signup_form = SignupForm()
    res = handle_auth(login_form, signup_form, '/upload')
    if res != None:
        return res
    return render_template('upload.html', login_form=login_form, signup_form=signup_form)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    login_form = LoginForm()
    signup_form = SignupForm()
    res = handle_auth(login_form, signup_form, '/forum')
    if res != None:
        return res
    return render_template('forum.html', login_form=login_form, signup_form=signup_form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    login_form = LoginForm()
    signup_form = SignupForm()
    res = handle_auth(login_form, signup_form, '/contact')
    if res != None:
        return res
    return render_template('contact.html', login_form=login_form, signup_form=signup_form)

@app.route('/main')
@login_required
def main(user_id):
    user = users.find_one({'_id': bson.ObjectId(insert_result.inserted_id)})
    return "Hello, {}".format(user['username'])

########################################################################
#########################API############################################
########################################################################
@app.route('/api')
def api_index():
    # Very simple
    return_data = {
        'title' : 'API test'
    }
    return jsonify(return_data)

@app.route('/api/login', methods=['POST'])
def api_login():
    # Get details from post request
    username = request.form.get('username')
    password = request.form.get('password')
    if password == "abcdefg":
        # Generate exp time and token and return them
        timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        payload = {"user_id": username,"exp":timeLimit}
        token = jwt.encode(payload,SECRET_KEY)
        return_data = {
            "error": "0",
            "message": "Successful",
            "token": token,
            "Elapse_time": f"{timeLimit}"
        }
        return jsonify(return_data)
    # IF not correct credentials, give error reponse
    return_data = {
        "error": "1",
        "message": "Invalid password"
    }
    return jsonify(return_data)

@app.route('/api/wel',methods=['POST'])
@token_required
def api_welcome(userId):
    #Code explains itself (note the new paraameter from the decorator)
    return_data = {
        "error": "0",
        "welcome": "Hello {}".format(userId),
        "message": "You Are verified"
    }
    return jsonify(return_data)

if __name__ == "__main__":
    app.run()
