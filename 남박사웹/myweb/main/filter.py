#filter.py
# conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)


from main import app, datetime, time


# utc 시간을 현재 시간에 맞게 구현하기 
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

