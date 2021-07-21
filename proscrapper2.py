from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import csv
import requests
starturl="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome(executable_path=r"chromedriver.exe")
browser.get(starturl)
time.sleep(10)
headers=["NAME","LIGHT-YEARS FROM EARTH","PLANET MASS","STELLAR MAGNITUDE","DISCOVERY DATE","hyperlink","planet_type","planet_radius","orbical_radius","orbical_period","eccentricity"]
planetdata=[]
newplanetdata=[]
def scrape():
    for i in range(0,443):
        while True:
            time.sleep(2)

            soup=BeautifulSoup(browser.page_source,"html.parser")
            currentpagenumber=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if currentpagenumber<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentpagenumber>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ultag in soup.find_all("ul",attrs={"class","exoplanet"}):
            litags=ultag.find_all("li")
            templist=[]
            for index,litag in enumerate(litags):
                if index==0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else :
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            hyperlink_li_tag=[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planetdata.append(templist)     
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i}pagedone 1")
def scrapemoreedata(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        temp_list=[]
        for trtag in soup.find_all("tr",attrs={"class","fact_row"}):
            tdtags=trtag.find_all("td")
            for tdtag in tdtags:
                try:
                    temp_list.append(tdtag.find_all("div",attrs={"class","value"})[0].contents[0])
                except:
                    temp_list.append("")
        newplanetdata.append(temp_list)
    except:
        time.sleep(1)
        scrapemoreedata(hyperlink)
scrape()
for index,data in enumerate(planetdata):
    scrapemoreedata(data[5])
    print(f"{index+1}pagedone 2")
finalplanetdata=[]
for index,data in enumerate(planetdata):
    newplanetdataelement=newplanetdata[index]
    newplanetdataelement=[elem.replace("\n","")for elem in newplanetdataelement]
    newplanetdataelement=newplanetdataelement[:7]
    finalplanetdata.append(data+newplanetdataelement)
with open("scrapper2.csv","w")as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planetdata)
    

