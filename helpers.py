import os

from flask import redirect, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*arg, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*arg, **kwargs)
    return decorated_function