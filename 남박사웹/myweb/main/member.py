# memeber.py
# conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)


from main import *
from flask import Blueprint


blueprint = Blueprint("member", __name__, url_prefix="/member")


@blueprint.route("/join", methods=["GET","POST"])
def member_join():
    if request.method == "POST":
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        pass1 = request.form.get("pass", type=str)
        pass2 = request.form.get("pass2", type=str)

        if name == "" or email == "" or pass1 == "" or pass2 == "":
            flash("입력되지 않은값이 있습니다")
            return render_template("join.html", title="회원가입")

        if pass1 != pass2:
            flash("비밀번호가 일치하지 않습니다. ")
            return render_template("join.html", title="회원가입")

        members = mongo.db.members    
        cnt = members.find({"email":email}).count() 
        if cnt > 0:
            flash("중복된 이메일 주소입니다")
            return render_template("join.html", title="회원가입")

        current_utc_time = round(datetime.utcnow().timestamp()*1000)
        post = {
            "name": name,
            "email": email,
            "pass": pass1,
            "joindate": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }
        members.insert_one(post)

        return ""
    else:
        return render_template("join.html",title="회원가입")


@blueprint.route("/login", methods=["GET","POST"])
def member_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        next_url = request.form.get("next_url")


        members = mongo.db.members
        data = members.find_one({"email": email})

        if data is None:
            flash("회원정보가 없습니다")
            return redirect(url_for("member.member_join"))

# 다시 member_login함수호출하고 get으로 넘어가니까 다시login.html창이 열림
        else:
            if data.get("pass") == password:
                session["email"] = email
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True
                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect(url_for("board.lists"))
                

            else:
                flash("비밀번호가 일치하지 않습니다")
                return redirect(url_for("member.member_login"))

        return ""
    else:   # GET 방식인 경우
        next_url = request.args.get("next_url", type=str)
        if next_url is not None:
            return render_template("login.html", next_url=next_url, title="회원로그인")
        else:
            return render_template("login.html",title="회원로그인")

# 로그인이 필요한페이지에서 redirect(url_for("member.member_login"), next_url 변수에 request.url (현재페이지의url주소)을 넘겨준다)
# 그럼 member_login함수는 get으로 넘겨받으니까 next_url=request.args.get("next_url", type=str)
# 이 next_url을 login.html로 넘겨줌, 그러면 
# login.html에서
# {% if next_url %} <input type="hidden" name="next_url" value="{{next_url}}"> {% endif %}
# input type hidden값으로 
# member_login()함수에서
# next_url값이 있으면 next_url값으로 redirect 시키고 그렇지 않으면 url_for("board.lists")


@blueprint.route("/logout")
def member_logout():
    try:
        del session["name"]
        del session["id"]
        del session["email"]
       
    except:
        pass
    return redirect(url_for('member.member_login'))