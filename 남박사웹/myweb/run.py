#conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)

from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
from flask import abort
from flask import redirect
from flask import url_for
import time 
import math


#flask_pymongo는 접속될 주소를 app.config로 선언해준다
#몽고디비에 접속될주소 db이름까지 반드시 설정할것
#mongo라는 인스턴스에 PyMongo에 app을 넘겨줌

app = Flask(__name__)
app.config["MONGO_URI"]= "mongodb://localhost:27017/myweb"
mongo = PyMongo(app)

#utc 시간을 현재 시간에 맞게 구현하기
@app.template_filter("formatdatetime")
def format_datetime(value):
    if value is None:
        return ""

    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    #시간차이 = datetime형 현재시간 - datetime형 utc 시간
    #현재 타임기준으로 datetime 객체 만듬
    value = datetime.fromtimestamp((int(value) / 1000)) + offset
    return value.strftime('%Y-%m-%d %H:%M:%S')


@app.route("/list")
def lists():
    # 페이지값 값이 없는 경우 기본값은 1
    page = request.args.get("page", default=1, type=int)
    # 한페이지당 몇개의 게시물을 룰력할지
    limit = request.args.get("limit", 10, type=int)

    board = mongo.db.board
    datas = board.find({}).skip((page - 1) * limit).limit(limit)
    #limit디폴트값이 10개니까 앞 10개 없애고 10개로 제한 
    
    # 게시물의 총 갯수
    tot_count = board.find({}).count()
    # 마지막페이지수를 구함
    last_page_num = math.ceil(tot_count / limit)
    # 게시물이 한개라도 있으면 페이지가 존재하므로 계산후 나머지가 있으면 무조건 올림해야함 math.ceil
 
    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 
    block_num = int((page - 1) / block_size)
    # 블럭의 시작 위치
    block_start = (int(block_size * block_num) + 1)
    # 블럭의 끝 위치
    block_last = math.ceil(block_start + (block_size - 1))
 
    return render_template(
        "list.html", 
        datas=datas,
        limit=limit,
        page=page,
        block_start=block_start,
        block_last=block_last,
        last_page_num=last_page_num)
        # 왼쪽은 변수명 = 오른쪽은 값

@app.route("/view/<idx>")
def board_view(idx):
    #idx = request.args.get("idx")
    #idx는 몽고디비의 id값이다 이것을 get방식으로 바다서
    if idx is not None:
        board = mongo.db.board
        data = board.find_one({"_id":ObjectId(idx)})    #id값이 idx인것을 찾아서 data에 넣겠다

        if data is not None:
            result = {
                "id":data.get("_id"),
                "name":data.get("name"),
                "title":data.get("title"),
                "contents":data.get("contents"),
                "pubdate":data.get("pubdate"),
                "view":data.get("view")
            }
            #이 데이타를 html로 표기해주어야 한다 
            return render_template("view.html",result=result)

    return abort(404)

    #request method가 POST인경우 form에서 얻어옴 -url상 노출 안됨
    #request method가 GET 인경우 form에서 얻오울수없다 -url상 노출


@app.route("/write", methods=["GET","POST"])
def board_write():
    if request.method == "POST":
        name =  request.form.get("name")
        title = request.form.get("title")
        contents = request.form.get("contents")
        print(name, title, contents)

        current_utc_time = round(datetime.utcnow().timestamp()*1000)
        #utc는 ms로 반환하므로 1000을 곱한후 소수점을 없애기위해 반올림 round함수로
        #utc는 협정세계표준시 
        #mongo라는 db에 board라는 컬렉션(db이름)을 board라는 객체에 집어넣음 
        board = mongo.db.board
        post = {
            "name":name,
            "title":title,
            "contents":contents,
            "pubdate":current_utc_time,
            "view":0,
        }

        x = board.insert_one(post)
        print(x.inserted_id)
        return redirect(url_for("board_view", idx= x.inserted_id))
    else: 
        return render_template("write.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9000)
    