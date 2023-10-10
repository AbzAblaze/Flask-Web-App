from . import db 
from .models import User
import requests
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

#Blueprint for Auth Routes
auth = Blueprint("auth", __name__)

#Require User NOT logged in
def not_logged_in_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash('You are already logged in.', 'info')
            return redirect(url_for('dashboard'))  # Redirect to a different view, e.g., the dashboard
        return view_func(*args, **kwargs)
    return decorated_function

#Login Route
@auth.route('/login', methods=['GET','POST']) #(GET=Retrieve, POST=Send)
@not_logged_in_required
def login():
    #POST output retreived from request.form
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #Check Credentials
        user = User.query.filter_by(email=email).first()
        #If User Exists
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    #Render Login Page (When /login route is accessed.)
    return render_template("login.html")

#Logout Route (Must be logged in to see).
@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#Signup Route
@auth.route('/sign-up', methods=['GET','POST'])
@not_logged_in_required
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('FirstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #Check if Email Exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        #Other Checks
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords dont match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        #Create User
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created.', category='success')
            return redirect(url_for('views.home'))
    #Render Signup Page
    return render_template("sign-up.html")