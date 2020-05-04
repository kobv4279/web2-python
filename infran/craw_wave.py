from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import datetime
import selenium
from selenium import webdriver
#import image
# https://www.weather.go.kr/mini/marine/wavemodel_c.jsp?prefix=kim_cww3_%5BAREA%5D_wdpr_&area=jeju&tm=2020.04.28.09
# &ftm=s000&newTm=2020.04.28.09&x=4&y=10


a = input("날짜")

url = "https://www.weather.go.kr/mini/marine/wavemodel_c.jsp?prefix=kim_cww3_%5BAREA%5D_wdpr_&area=jeju&tm="+a

driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)


soup = BeautifulSoup(driver.page_source,"html.parser")

for i in soup.select("#chart_image"):
    src=i.find("img")['src']





#
# image = image.open(src)
# image.show()