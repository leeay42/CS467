from functools import wraps
from flask import session, redirect, url_for, flash


def admin_access(f):
    """Decorator that ensures the current session has admin privileges.

    This is intentionally simple: it checks `session.get('is_admin')` and
    redirects to the login page with a flash message if not present.
    Adapt/replace this with your project's real auth check as needed.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Admin access required. Please log in with an admin account.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function
