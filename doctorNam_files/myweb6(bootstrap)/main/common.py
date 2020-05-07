from main import session, redirect, url_for, request, ALLOWED_EXTENSIONS
from functools import wraps
import random
from string import digits, ascii_uppercase, ascii_lowercase

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS

def rand_generator(length=8):
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(random.sample(chars, length))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None or session.get("id") == "":
            return redirect(url_for("member.member_login", next_url=request.url))
        return f(*args, **kwargs)
    return decorated_function
