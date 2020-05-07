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


#flask_pymongo는 접속될 주소를 app.config로 선언해준다
#몽고디비에 접속될주소 db이름까지 반드시 설정할것
#mongo라는 인스턴스에 PyMongo에 app을 넘겨줌

app = Flask(__name__)
app.config["MONGO_URI"]= "mongodb://localhost:27017/myweb"
app.config["SECRET_KEY"] = "abcd"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
mongo = PyMongo(app)



#이 패키지에 귀속이 되게 함 board와 memeber를 가져오는 방법 
from .common import login_required
from .filter import format_datetime
from . import board
from . import member

#.common의.은 현재 경로라는 뜻임 

app.register_blueprint(board.blueprint)
app.register_blueprint(member.blueprint)