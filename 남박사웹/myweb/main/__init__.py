#conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)

from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
from datetime import datetime
from datetime import timedelta
from bson.objectid import ObjectId
from flask import abort
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from functools import wraps
import time 
import math
import os


#flask_pymongo는 접속될 주소를 app.config로 선언해준다
#몽고디비에 접속될주소 db이름까지 반드시 설정할것
#mongo라는 인스턴스에 PyMongo에 app을 넘겨줌

app = Flask(__name__)
app.config["MONGO_URI"]= "mongodb://localhost:27017/myweb"
app.config["SECRET_KEY"] = "abcd"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
mongo = PyMongo(app)


#플라스크에서 이미지 업로드 구현

BOARD_IMAGE_PATH = "G:\\images"
ALLOWED_EXTENSIONS = set(["txt", "pdf","png","jpg","jpeg","gif"])

app.config["BOARD_IMAGE_PATH"] = BOARD_IMAGE_PATH    #쉽게접근하기위해 환경변수 설정
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024   #15메가


#이미지패스폴더가 없을경우 만들어주는 코드-------도커에서
if not os.path.exists(app.config["BOARD_IMAGE_PATH"]):
    os.mkdir(app.config["BOARD_IMAGE_PATH"])




#이 패키지에 귀속이 되게 함 board와 memeber를 가져오는 방법 
from .common import login_required, allowed_file, rand_generator
from .filter import format_datetime
from . import board
from . import member

#.common의.은 현재 경로라는 뜻임 

app.register_blueprint(board.blueprint)
app.register_blueprint(member.blueprint)