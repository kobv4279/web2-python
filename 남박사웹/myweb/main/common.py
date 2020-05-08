# common.py
#conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)


from functools import wraps
from main import session, redirect, request, url_for, ALLOWED_EXTENSIONS
from string import digits, ascii_lowercase, ascii_uppercase
import random
import re
import os


# 파일네임을 secure로 변환해주는 함수 구현
def check_filename(filename):
    reg = re.compile(r'[^A-Za-z0-9_.가-힝-]')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
            print(filename)
            filename = str(reg.sub('', '_'.join(filename.split()))).strip('._')
    return filename


#확장자를 체크하는 함수
def allowed_file(filename):
    return "." in filename  and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS
#.이 파일이름에 있으면 확장자가 있으면 그리고 rsplit은 오른쪽을 기준으로 .을 기준으로 잘라내서 리스트로 


# 임의로 파일명 생성해줌
def rand_generator(length=8):
    char = ascii_lowercase + ascii_uppercase + digits   
    return "".join(random.sample(char, length))
 



def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if session.get("id") is None or session.get("id") == "":
            return redirect(url_for("member.member_login", next_url=request.url))
        return f(*args, **kwargs)
    return decorated_function

