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


app = Flask(__name__, template_folder="templates")
app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb" 
app.config['SECRET_KEY'] = 'password'

mongo = PyMongo(app)


@app.template_filter('formatdatetime')
def format_datetime(value):
    if value is None:
        return ""

    # 현재 시간 타임스탬프를 구합니다.
    now_timestamp = time.time()
    
    # 현재 시간 타임스탬프를 현재 시간객체, UTC 시간 기준 시간객체로 변환하여
    # 현재 시간에서 UTC 시간을 빼 시간차를 구합니다.
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    
    # 구해진 시간차만큼 저장된 시간정보에 더해줍니다.
    value = datetime.fromtimestamp((int(value) / 1000)) + offset
    
    # 원하는 형태의 시간 포맷으로 변경합니다.
    return value.strftime('%Y-%m-%d %H:%M:%S')


@app.route("/view")
def board_view():
    idx = request.args.get("idx")
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", -1, type=int)
    keyword = request.args.get("keyword", "", type=str)

    if idx is not None:
        board = mongo.db.board
        #data = board.find_one({"_id": ObjectId(idx)})
        data = board.find_one_and_update({"_id": ObjectId(idx)}, {"$inc": {"view": 1}}, return_document=True)
        if data is not None:
            result = {
                "id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "pubdate": data.get("pubdate")
            }

            return render_template("view.html", result=result, page=page, search=search, keyword=keyword)
    return abort(404)


@app.route("/write", methods=["GET", "POST"])
def board_write():
    if request.method == "POST":
        name = request.form.get("name")
        title = request.form.get("title")
        contents = request.form.get("contents")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        board = mongo.db.board

        post = {
            "name": name,
            "title": title,
            "contents": contents,
            "view": 0,
            "pubdate": current_utc_time,
        }
        x = board.insert_one(post)

        flash("정상적으로 작성 되었습니다.")
        return redirect(url_for("board_view", idx=x.inserted_id))
    else:
        return render_template("write.html")

@app.route("/list")
def lists():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    search = request.args.get("search", -1, type=int)
    keyword = request.args.get("keyword", "", type=str)

    query = {}
    search_list = []

    if search == 0:
        search_list.append({"title": {"$regex": keyword}})
    elif search == 1:
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 2:
        search_list.append({"title": {"$regex": keyword}})
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 3:
        search_list.append({"name": {"$regex": keyword}})

    if len(search_list) > 0:
        query = {"$or": search_list}

    board = mongo.db.board
    datas = board.find(query).skip((page-1) * limit).limit(limit)

    tot_count = board.find(query).count()
    last_page_num = math.ceil(tot_count / limit)

    block_size = 5
    block_num = int((page-1) / block_size)
    block_start = int((block_size * block_num) + 1)
    block_last = math.ceil(block_start + (block_size-1))

    return render_template("list.html", 
                            datas=datas, 
                            limit=limit, 
                            page=page,
                            block_start=block_start,
                            block_last=block_last,
                            last_page=last_page_num,
                            search=search,
                            keyword=keyword,
                            )

@app.route("/join", methods=["GET", "POST"])
def member_join():
    if request.method == "GET":
        return render_template("join.html")
    else:
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        pass1 = request.form.get("pass", type=str)
        pass2 = request.form.get("pass2", type=str)

        if name is None or email is None or pass1 is None or pass2 is None:
            flash("입력되지 않은 값이 있습니다.")
            return render_template("join.html")
        
        if pass1 != pass2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("join.html")
        
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)
        members = mongo.db.members
        post = {
            "name": name,
            "email": email,
            "pass": pass1,
            "joindate": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }
        
        x = members.insert_one(post)
        return redirect(url_for("member_login"))

@app.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("pass")

        members = mongo.db.members
        data = members.find_one({"email": email})

        if data is None:
            flash("회원정보가 없습니다.")
            return redirect(url_for("member_join"))
        else:
            if data.get("pass") == password:
                session["email"] = email
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True
                return redirect(url_for("lists"))
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("member_login"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=9090)