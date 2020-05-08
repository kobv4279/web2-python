from main import session, redirect, url_for, request, ALLOWED_EXTENSIONS
from functools import wraps
import random
from string import digits, ascii_uppercase, ascii_lowercase
import re
import os

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





# 공백기준으로 잘라서 하나의 문자열로 만드는데 그사이를 _로 만들겠다
# reg.sub 는 여기서 나온 문자열이 패턴이 일치하다면 공문자를 업애버려라
# ^ 은 아니라는 뜻
# 전체를 문자열로 다시 캐스팅한다음
# 이걸 다시 파일 네임에 다시 담음
def check_filename(filename):
    reg = re.compile(r'[^A-Za-z0-9_.가-힝-]')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
            print(filename)
            filename = str(reg.sub('', '_'.join(filename.split()))).strip('._')
    return filename