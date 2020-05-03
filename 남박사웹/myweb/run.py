from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo


#flask_pymongo는 접속될 주소를 app.config로 선언해준다
#몽고디비에 접속될주소 db이름까지 반드시 설정할것
#mongo라는 인스턴스에 PyMongo에 app을 넘겨줌

app = Flask(__name__)
app.config["MONGO_URI"]= "mongodb://localhost:27017/myweb"
mongo = PyMongo(app)


@app.route("/write", methods=["GET","POST"])
def board_write():
    if request.method == "POST":
        name =  request.form.get("name")
        title = request.form.get("title")
        contents = request.form.get("contents")


        #mongo라는 db에 board라는 컬렉션(db이름)을 board라는 객체에 집어넣음 
        board = mongo.db.board
        post = {
            "name":name,
            "title":title,
            "contents":contents
        }

        board.insert_one(post)

        return ""
    else: 
        return render_template("write.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9000)
    