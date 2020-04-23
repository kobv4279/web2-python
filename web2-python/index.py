#!python3
print("Content-type: text/html")
print()
import cgi, os

files = os.listdir('data')
listStr = ''
for item in files:
    listStr = listStr + '<li><a href="index.py?id={name}">{name}</a></li>'.format(name=item)

form = cgi.FieldStorage()
if 'id' in form:
    pageId = form["id"].value
    description = open('data/' + pageId, 'r').read()
else:
    pageId = 'Welcome'
    description = 'hello, web'
print('''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>교사임용공고</title>


</head>
<body>
<h1>
    교사임용공고알림페이지
</h1>
<p>
    this page is for {{title}}
    모든 수험생 파이팅!!
</p>

<div class="kj_content">
    <h1><a href="index.py">광주광역시 교사임용공고 크롤링 페이지입니다
    </h1>
    <ol>
      <li><a href="index.py?id=kwangu">광주</a></li>
      <li><a href="index.py?id=chonnam.html">전남</a></li>
    </ol>

</body>
</html>'''.format(title=pageId, desc=description, listStr=listStr))
