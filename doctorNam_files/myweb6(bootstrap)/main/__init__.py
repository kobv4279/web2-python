from flask import Flask
from flask import request
from flask import render_template
from flask import url_for, redirect, flash
from flask import abort
from flask import session
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from datetime import datetime
from datetime import timedelta
from werkzeug import secure_filename
import time
import math

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb" 
app.config['SECRET_KEY'] = 'password1'

import os

BOARD_IMAGE_PATH = "z:\\images\\"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['BOARD_IMAGE_PATH'] = BOARD_IMAGE_PATH
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

if not os.path.exists(app.config["BOARD_IMAGE_PATH"]):
    os.mkdir(app.config["BOARD_IMAGE_PATH"])

mongo = PyMongo(app)

from .common import login_required, rand_generator, allowed_file
from .filter import format_datetime
from . import board
from . import member

app.register_blueprint(board.blueprint)
app.register_blueprint(member.blueprint)
