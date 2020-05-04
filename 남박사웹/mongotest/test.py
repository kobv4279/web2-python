import pymongo


#mongodb
#program: Robo 3t -1.3
#localhost:27017

m = {
    "이름": "깜수니",
    "나이": "4",
    "거주지":"광주",
    "몸무게":"3.8",
    "키":"40",
    "프로필사진":[
        "KKam.jpg"
    ]
}

#mongodb는 BSON binay형태의 json 형태를 가지고 있따


m2 = {
    "이름": "촐랭",
    "나이": "4",
    "거주지":"광주",
    "몸무게":"6.8",
    "키":"60",
    "프로필사진":[
        "KKam.jpg"
    ]
}

#몽고db에 접속해서 conn이라는 객체로 받음
conn = pymongo.MongoClient("localhost",27017)
db = conn.test
#table명을 collection명이라고 함
col = db.members
#col.insert(m)

#mongoclient 변수가 conn이고 db의 이름이 db= 연결클라이언트객체.데이터베이스이름test 
#그 db.member는 컬렉션 이름 
#컬렉션을 테이블명
#없으면 생성함 최종 컬렉션에다 데이터를 집어넣음 

#데이터 검색은 어떻게 하느냐 



#
# results = col.find({"나이":{"$gt":30}},{"_id":False,"이름":True}).sort(-1).skip(1).limit(3)
# for r in results:
#      print(r)   #gt: greater then  더큰
#
#
#
# results = col.find()
# print(results)
# cursor object가 왔다는 뜻이다 커서가 왔다는건 실제데이터가 왔다는건 아니다는 의미
# 그럼 cursor object를 뿌려주는 기능이 필요함
# idx primary key 생성 objectid가 유니크아이디가 자동으로 생성

#and 연산이다 이름이 깜수니고 몸무게가 3.8인
results = col.find({"이름":"깜수니","몸무게":"3.8"})
for r in results:
    print(r)

#or연산
# results=col.find({"$or":[{"이름":"깜순이"},{"몸무게":"3.8"}]})
# for r in results:
#    print(r)
#
# o = col.find_one({"이름":"깜수니"})
# print(o)



#이름만 바꾸는것
col.update({"이름":"촐랭"},{"$set":{"이름":"김촐랭"}})

#데이터셋 전체가 바귀는것
col.update({"이름":"촐랭"},{"이름":"김촐랭"})