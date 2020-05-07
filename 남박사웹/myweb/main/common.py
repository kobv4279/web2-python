# common.py
#conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if session.get("id") is None or session.get("id") == "":
            return redirect(url_for("member_login", next_url=request.url))
        return f(*args, **kwargs)
    return decorated_function
