from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.users import User

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nameUser = request.form['nameUser']
        passwordUser = request.form['passwordUser']
        
        user = User.query.filter_by(nameUser=nameUser).first()
        if user and user.check_password(passwordUser):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('user.index'))
        
        flash('Invalid credentials. Please try again.', 'danger')
    
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return render_template("login.html")

@bp.route('/dashboard')
@login_required
def dashboard():    
    return render_template('dashboard.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Limpiar completamente la sesión
    flash('You have been logged out.', 'info')
    response = make_response(redirect(url_for('auth.login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@bp.route('/pruebajs')
def pruebajs():
    example_data = {
        'title': 'Bienvenido a Flet',
        'message': 'Este es un mensaje desde Flask.'
    }
    import json
    return json.dumps(example_data)

@bp.route('/check_auth')
@login_required
def check_auth():
    return {'authenticated': True}