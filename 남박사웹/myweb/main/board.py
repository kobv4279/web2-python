# board.py
# conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)
 

from main import *
from flask import Blueprint
from flask import send_from_directory

                          #모듈이름
blueprint = Blueprint("board", __name__, url_prefix="/board")


def board_delete_attach_file(filename):
    abs_path = os.path.join(app.config["BOARD_ATTACH_FILE_PATH"], filename)
    if os.path.exists(abs_path):
        os.remove(abs_path)
        return True
    return False


@blueprint.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["image"]     # write.html에서ajax에서 image를 image라는 이름의 데이타러 받아오기떄문에 
        if file and allowed_file(file.filename):
            filename = "{}.jpg".format(rand_generator())
            savefilepath = os.path.join(app.config["BOARD_IMAGE_PATH"], filename)
            file.save(savefilepath)
            return url_for("board.board_images", filename=filename)



@blueprint.route("/images/<filename>")
def board_images(filename):
    return send_from_directory(app.config["BOARD_IMAGE_PATH"], filename)
# 실제프로젝트 바깥의 폴더에 접근하기 위해서 함수의 인자는 절대경로를 넘겨주고, 파일명을 같이 넘겨주면
# 그 데이터를 뽑아 리턴해줌

@blueprint.route("/files/<filename>")
def board_files(filename):
    return send_from_directory(app.config["BOARD_ATTACH_FILE_PATH"], filename, as_attachment=True)



@blueprint.route("/list")
def lists(): 
    # 페이지값 값이 없는 경우 기본값은 1
    page = request.args.get("page", default=1, type=int)
    # 한페이지당 몇개의 게시물을 룰력할지
    limit = request.args.get("limit", 7, type=int)


    search = request.args.get("search", -1, type=int)
    keyword = request.args.get("keyword", "", type=str)
    
    # 최종적 완성된 쿼리를 만들 변수 -딕셔너리형태변수
    query = {}
    # 검색어 상태를 추가할 리스트 변수
    search_list = []

    if search == 0:    #제목
        search_list.append({"title": {"$regex": keyword}})   #제목에"녕"이 있는지 안녕하세요를 검색하기위해 $regex연산자를 사용
    elif search == 1:
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 2:
        search_list.append({"title": {"$regex": keyword}})
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 3:
        search_list.append({"name": {"$regex": keyword}})

    # 검색 대상이 한개라도 존재할 경우 query 변수에 $or 리스트를 query합니다 
    if len(search_list) > 0 :
        query = {"$or": search_list}

    print(query)


    board = mongo.db.board
    datas = board.find(query).skip((page - 1) * limit).limit(limit).sort("pubdate", -1)
    # limit디폴트값이 10개니까 앞 10개 없애고 10개로 제한 
    
    # 게시물의 총 갯수
    tot_count = board.find(query).count()
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
        last_page_num=last_page_num,
        search=search,
        keyword=keyword,
        title="게시판 리스트")
        # 왼쪽은 변수명 = 오른쪽은 값


@blueprint.route("/view/<idx>")
@login_required
def board_view(idx):
    # idx = request.args.get("idx")
    # idx는 몽고디비의 id값이다 이것을 get방식으로 바다서
    if idx is not None:
        page = request.args.get("page")
        search = request.args.get("search")
        keyword = request.args.get("keyword")

        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})    #id값이 idx인것을 찾아서 data에 넣겠다

# view count를 올리는 코드
# $inc 증강연산자 :{"view":1}
        data = board.find_one_and_update({"_id": ObjectId(idx)},
         {"$inc": {"view": 1}},
         return_document=True)   # 업데이트 된 후 data에 저장

        if data is not None:
            result = {
                "id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "pubdate": data.get("pubdate"),
                "view": data.get("view"),
                "writer_id": data.get("writer_id", ""),
                "attachfile": data.get("attachfile","")
            }

            # 이 데이타를 html로 표기해주어야 한다 
            return render_template(
                "view.html",
                result=result,
                page=page,
                search=search,
                keyword=keyword,
                title = "글상세보기")

    return abort(404)

    #request method가 POST인경우 form에서 얻어옴 -url상 노출 안됨
    #request method가 GET 인경우 form에서 얻오울수없다 -url상 노출


@blueprint.route("/write", methods=["GET","POST"])
@login_required
def board_write():
    if request.method == "POST":
        filename = None
        if "attachfile" in request.files:   # 첨부파일이 첨부가 됐냐 안됬냐 물어보는것
            file = request.files["attachfile"]   # 파일을 받아서
            if file and allowed_file(file.filename): # 원본파일이름이 허용하는 확장자이면
                filename = check_filename(file.filename)    #원본파일 이름을 넘겨주고 새로운 파일네임 받음
                file.save(os.path.join(app.config['BOARD_ATTACH_FILE_PATH'], filename))
        
        name =  request.form.get("name")
        title = request.form.get("title")
        contents = request.form.get("contents")
        



# 파일을 접근, 저장하는 코드
# secure_filename()함수를 이용하게 flask는 추천함
# 그러므로 secure_filename() 함수를 흉내내서 따로 만듬 common.py

        request.files


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
            "writer_id":session.get("id"),  #mongodb회원의id값unique값
            "view":0,
        }


        if filename is not None:
            post["attachfile"] = filename



        x = board.insert_one(post)
        print(x.inserted_id)
        return redirect(url_for("board.board_view", idx= x.inserted_id))
    else: 
        return render_template("write.html", title="글작성")


@blueprint.route("/edit", methods=["POST"])
@blueprint.route("/edit/<idx>", methods=["GET"])
def board_edit(idx=None):
    if request.method == "GET":
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})  # objectId형태로 캐스팅해야함
        if data is None:
            flash("해당 게시물이 존재하지 않습니다")
            return redirect(url_for("board.lists"))
        else:  # 데이터가 있는경우
            if session.get("id") == data.get("write_id"):    
                # session.get("id")= 로그인한 아이디 | write_id=게시물의 작성자 id
                return render_template("edit.html", data=data, title="글수정")
            else:
                flash("글 수정 권한이 없습니다")
                return redirect(url_for("board.lists"))
    else:    # 글작성에서 넘어가는경우 post형태로 받을경우
        idx = request.form.get("idx")
        title = request.form.get("title")
        contents = request.form.get("contents")
        deleteoldfile = request.form.get("deleteoldfile", "")
 


# 권한이 있는지 확인 
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})

        if session.get("id") == data.get("writer_id"):     # 세션 권한이 확인이 되면 
            # attach_file = data.get("attachfile")
            filename = None
            if "attachfile" in request.files:             # 첨부파일이 새로 등록되었고
                file = request.files["attachfile"]
                if file and allowed_file(file.filename):    #파일이 존재하고, 확장자 체크하고
                    filename = check_filename(file.filename)              #문제없는 파일이름 받고
                    file.save(os.path.join(app.config["BOARD_ATTACH_FILE_PATH"], filename))
                    

                    if data.get("attachfile"):    # 첨부파일이 예전에 있다면 
                        board_delete_attach_file(data.get("attachfile"))    # 기존의 파일을  삭제



            else:                       # 첨부파일이 새로 등록되지 않았고
                if deleteoldfile == "on":                   
                    filename = None
                    if data.get("attachfile"):
                        board_delete_attach_file(data.get("attachfile"))
                else:
                    filename = data.get("attach_file")

            
            board.update_one({"_id": ObjectId(idx)}, {    # 업데이트될 내용을 명시
                "$set":{
                    "title": title,
                    "contents": contents,
                    "attachfile": filename
                }
            })
            flash("수정되었습니다")
            return redirect(url_for("board.board_view", idx=idx))  #상세페이지로
        else:
            flash("글 수정 권한이 없습니다")
            return redirect(url_for("board.lists"))


@blueprint.route("/delete/<idx>", methods=["GET","POST"])
def board_delete(idx):
    board = mongo.db.board
    data = board.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        board.delete_one({"_id": ObjectId(idx)})
        flash("삭제 되었습니다")
    else:
        flash("삭제 권한이 없습니다")
    return redirect(url_for("board.lists"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9000)
    