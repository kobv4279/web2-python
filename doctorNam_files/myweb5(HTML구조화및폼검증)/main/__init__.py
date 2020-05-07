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
import time
import math

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb" 
app.config['SECRET_KEY'] = 'password1'

mongo = PyMongo(app)

from .common import login_required
from .filter import format_datetime
from . import board
from . import member

app.register_blueprint(board.blueprint)
app.register_blueprint(member.blueprint)
