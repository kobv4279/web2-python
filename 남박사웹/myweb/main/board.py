# board.py
# conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)

@app.route("/list")
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
        keyword=keyword)
        # 왼쪽은 변수명 = 오른쪽은 값

@app.route("/view/<idx>")
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
                "writer_id": data.get("writer_id", "")
            }

            # 이 데이타를 html로 표기해주어야 한다 
            return render_template(
                "view.html",
                result=result,
                page=page,
                search=search,
                keyword=keyword)

    return abort(404)

    #request method가 POST인경우 form에서 얻어옴 -url상 노출 안됨
    #request method가 GET 인경우 form에서 얻오울수없다 -url상 노출


@app.route("/write", methods=["GET","POST"])
@login_required
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
            "writer_id":session.get("id"),  #mongodb회원의id값unique값
            "view":0,
        }

        x = board.insert_one(post)
        print(x.inserted_id)
        return redirect(url_for("board_view", idx= x.inserted_id))
    else: 
        return render_template("write.html")



@app.route("/edit/<idx>", methods=["GET","POST"])
def board_edit(idx):
    if request.method == "GET":
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})  # objectId형태로 캐스팅해야함
        if data is None:
            flash("해당 게시물이 존재하지 않습니다")
            return redirect(url_for("lists"))
        else:  # 데이터가 있는경우
            if session.get("id") == data.get("write_id"):    
                # session.get("id")= 로그인한 아이디 | write_id=게시물의 작성자 id
                return render_template("edit.html", data=data)
            else:
############# # flash("글 수정 권한이 없습니다")
                return redirect(url_for("lists"))
    else:    # 글작성에서 넘어가는경우 post형태로 받을경우
        title = request.form.get("title")
        contents = request.form.get("contents")

# 권한이 있는지 확인 
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})
        if session.get("id") == data.get("writer_id"):
            board.update_one({"_id": ObjectId(idx)}, {    # 업데이트될 내용을 명시
                "$set":{
                    "title": title,
                    "contents": contents,
                }
            })
            flash("수정되었습니다")
            return redirect(url_for("board_view", idx=idx))  #상세페이지로
        else:
            flash("글 수정 권한이 없습니다")
            return redirect(url_for("lists"))


@app.route("/delete/<idx>", methods=["GET","POST"])
def board_delete(idx):
    board = mongo.db.board
    data = board.find_one({"_id": ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        board.delete_one({"_id": ObjectId(idx)})
        flash("삭제 되었습니다")
    else:
        flash("삭제 권한이 없습니다")
    return redirect(url_for("lists"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9000)
    