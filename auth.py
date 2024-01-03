from flask import Blueprint, render_template
from flask import Blueprint, render_template, redirect, url_for, flash
from model import User, db
from flask_bcrypt import check_password_hash, generate_password_hash
from flask import request, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password).decode('utf-8')

        # Save user to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))

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
            print('session username logged in: ', session['username'])
            flash('Logged in successfully!', 'success')
            return redirect(url_for('chat'))
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')

    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    # Implement logout logic here
    return "Logged out successfully"

