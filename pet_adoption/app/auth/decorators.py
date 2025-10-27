from functools import wraps
from flask import redirect, url_for, session, flash

def admin_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check session for admin_access T/F value
        if not session.get('admin_access'):
            flash("This page requires admin access.")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function