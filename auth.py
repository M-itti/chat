from flask import Blueprint, render_template
from flask import Blueprint, render_template, redirect, url_for, flash
from models import User, db
from flask_bcrypt import check_password_hash, generate_password_hash
from flask import request, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("reg in") # TODO
        username = request.form.get('username')
        session['username'] = username
        password = request.form.get('password')
        hashed_password = generate_password_hash(password).decode('utf-8')

        # Save user to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))

    print("didn't reg up") # TODO
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("login started **************")
    if request.method == 'POST':
        username = request.form.get('username')
        print("login inside post **************")
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Log the user in
            flash('Logged in successfully!', 'success')
            print("logged in") # TODO
            return redirect(url_for('chat'))
        else:
            print(" didn't logged in") # TODO
            flash('Login unsuccessful. Please check your credentials.', 'danger')

    print("login failed **************")
    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    # Implement logout logic here
    return "Logged out successfully"

