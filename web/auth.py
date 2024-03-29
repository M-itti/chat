from flask import Blueprint, render_template, redirect, url_for, flash
from flask_bcrypt import check_password_hash, generate_password_hash
from flask import request, session
from sqlalchemy import exc

from .model import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password).decode('utf-8')
        
        try:
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))

        except exc.IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose different one', 'danger')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Log the user in
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.chat', username=username))
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')

    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    session.pop('username', None) 
    flash('Logged out in successfully!', 'success')
    return redirect(url_for('home_page'))

@auth_bp.route("/guest")
def anonymous():
    import random
    import string

    random_suffix = ''.join(random.choices(string.digits, k=6))  
    username = f"guest_{random_suffix}"
    session['username'] = username
    return redirect(url_for('main.chat', username=username))

