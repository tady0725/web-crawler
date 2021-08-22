import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import quote
s = time.time()
SCROLL_PAUSE_TIME = 0.001
SPIDER_NUM = 100
URL = 'https://tw.news.yahoo.com/'
req = requests.get(URL)
print(req.status_code)

# 將整個網站的程式碼爬下來
soup = BeautifulSoup(req.content, "html.parser")

nav = soup.findAll('li', {'class': '_yb_sryu3 _yb_126vh'})
# for li in range(1, len(nav)-1):
#     keyword = nav[li].find("div", {'class': "_yb_ocf8p"}).text.strip()
keyword = "東京奧運"
# if keyword == "東京戰報":
#     keyword = "東京奧運"
url = "https://tw.news.yahoo.com/search?p=" + keyword + "&fr=news"

options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome(chrome_options=options)
chrome.get(url)

# Get scroll height
scrollHeight = chrome.execute_script("return document.body.scrollHeight")
while(len(BeautifulSoup(chrome.page_source, "html.parser").select(".StreamMegaItem h3")) < SPIDER_NUM):
    # Scroll down to bottom
    chrome.execute_script(
        "window.scrollTo(0, " + str(scrollHeight) + ");")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = chrome.execute_script("return document.body.scrollHeight")
    scrollHeight += new_height

soup = BeautifulSoup(chrome.page_source, "html.parser")
outFile = open("./" + str(keyword) + "新聞_" +
               str(SPIDER_NUM) + "則.txt", 'w', encoding="utf-8")
for li in soup.select(".StreamMegaItem"):
    print(li.h3.text)
    print(li.p.text)
    print('https://tw.news.yahoo.com/' + li.h3.a["href"])
    outFile.write("標題： " + li.h3.text + '\n')
    outFile.write("內容： " + li.p.text + '\n')
    outFile.write("網址： " + 'https://tw.news.yahoo.com/' +
                  li.h3.a["href"] + '\n')
    outFile.write("====================================\n")
chrome.close()
outFile.close()
print("====================================")
e = time.time()
print("耗時:", round(e-s, 6), "秒")
