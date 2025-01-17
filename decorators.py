from functools import wraps
from flask import abort
from flask_login import current_user
from flask_wtf import CSRFProtect

csrf = CSRFProtect()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.tipoUser != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

