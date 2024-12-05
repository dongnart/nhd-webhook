from flask import request, session, redirect, url_for
from app.models import Admin

def authenticate(username, password):
    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        session['admin'] = True
        return True
    return False

def login_required(f):
    def wrapper(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return wrapper