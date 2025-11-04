from flask import render_template, redirect, url_for, flash, request, session
from app import db
from flask import session, redirect, flash, render_template
from app.forms import LoginForm, RegisterForm
#from app.forms import TestForm

users_collection = db['users']

def init_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
    # Get login information from user
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            entered_login = {'email': email, 'password': password}
            user = users_collection.find_one(entered_login)
            # Check database for login credentials
            if user:
                print("success")
                # Save admin access T/F value for session
                session['admin_access'] = user.get('admin_access')
                flash("Log in successful.")
                return render_template('index.html')
            else:
                print("unsuccessful")
                flash("User not found. Please try again or create an account.")
                return redirect('/login')
        return render_template('auth/login.html', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        # Get account information from user
        form = RegisterForm()
        if form.validate_on_submit():
            print('here')
            admin_access = form.admin_access.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            user = {"admin_access": admin_access, "first_name": first_name, "last_name": last_name, "email": email, "password": password}
            # Check that user info doesn't already exist in DB
            if users_collection.find_one(user):
                print("unsuccessful")
                flash("User already exists. Please try again.")
                return render_template('register.html')
            # Create user account in DB
            else:
                print("success")
                users_collection.insert_one(user)
                flash("User created successfully. Please log in.")
                return redirect('/login')
        return render_template('auth/register.html', form=form)

    # Not in app architecture, clears session
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/login')