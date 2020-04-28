from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
#https://www.weather.go.kr/mini/marine/wavemodel_c.jsp?prefix=kim_cww3_%5BAREA%5D_wdpr_&area=jeju&tm=2020.04.28.09&ftm=s000&newTm=2020.04.28.09&x=4&y=10
url = "https://www.weather.go.kr/mini/marine/wavemodel_c.jsp?prefix=kim_cww3_%5BAREA%5D_wdpr_&area=jeju&tm="+2020.04.28.09&ftm=s018&newTm=2020.04.29.03&x=30&y=5
        for i in range(1, int(page)+1):
            req = requests.get(url+"&p="+page)
            soup = BeautifulSoup(req.text, 'html.parser')
            for i in soup.find_all("a", class_="f_link_b"):
                print(i.text)
                daum_list.append(i.text)

        for i in range(1, len(daum_list)+1):
            write_ws.cell(i,1,daum_list[i-1])