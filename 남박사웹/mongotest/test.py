import pymongo

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

#몽고db에 접속해서 conn이라는 객체로 받음
conn = pymongo.MongoClient("localhost",27017)
db = conn.test
#table명을 collection명이라고 함
col = db.members
col.insert(m)

#mongodb는 BSON binay형태의 json 형태를 가지고 있따
