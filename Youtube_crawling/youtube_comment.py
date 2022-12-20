from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pathlib

# print(pathlib.Path(__file__).parent.resolve())

# 최신 크롬 드라이버 사용하도록 세팅: 현재 OS에 설치된 크롬 브라우저 버전에 맞게 cache에 드라이버 설치
from selenium.webdriver.chrome.service import Service
# service = Service(ChromeDriverManager().install())
service = Service(str(pathlib.Path(__file__).parent.resolve())+"/chromedriver")

import time
import random
import pandas as pd

def scroll():
    try:        
        # 페이지 내 스크롤 높이 받아오기
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # 임의의 페이지 로딩 시간 설정
            # PC환경에 따라 로딩시간 최적화를 통해 scraping 시간 단축 가능
            pause_time = random.uniform(1, 2)
            pause_time = 2
            # 페이지 최하단까지 스크롤
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # 페이지 로딩 대기
            time.sleep(pause_time)
            # 무한 스크롤 동작을 위해 살짝 위로 스크롤(i.e., 페이지를 위로 올렸다가 내리는 제스쳐)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
            time.sleep(pause_time)
            # 페이지 내 스크롤 높이 새롭게 받아오기
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            # 스크롤을 완료한 경우(더이상 페이지 높이 변화가 없는 경우)
            if new_page_height == last_page_height:
                print("스크롤 완료")
                break
                
            # 스크롤 완료하지 않은 경우, 최하단까지 스크롤
            else:
                last_page_height = new_page_height
            
    except Exception as e:
        print("에러 발생: ", e)
        
        
url = input()


# 검색 키워드 설정: 키워드 내 띄어쓰기는 URL에서 '+'로 표시되기 때문에 이에 맞게 변환
SEARCH_KEYWORD = '잭 니콜라스 GC'.replace(' ', '+')


driver = webdriver.Chrome(service=service)
# 스크래핑 할 URL 세팅
# URL = "https://www.youtube.com/results?search_query=" + SEARCH_KEYWORD
# URL = "https://www.youtube.com/watch?v=dJXZRZvqbYg"
URL = str(url)
# 크롬 드라이버를 통해 지정한 URL의 웹 페이지 오픈
driver.get(URL)
# 웹 페이지 로딩 대기
time.sleep(3)
# 무한 스크롤 함수 실행
scroll()

input()

try:
    driver.find_element(By.CSS_SELECTOR, "#dismiss-button > button").click()
except:
    pass

# # 대댓글 버튼 누르기
# buttons = driver.find_elements(By.CSS_SELECTOR,"#more-replies > yt-button-shape > button")
# # buttons = driver.find_elements(By.CSS_SELECTOR,"#more-replies > a")

# time.sleep(1.5)
# print(type(buttons))

# for button in buttons:
#     button.send_keys(Keys.ENTER)
#     time.sleep(1.5)
#     try:
#         button.click()
#     except:
#         continue

# 다 열렸는지 확인
time.sleep(5.0)



# 페이지 소스 추출
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

id_list = soup.select("div#header-author > h3 > #author-text > span")
comment_list = soup.select("yt-formatted-string#content-text")
date_list = soup.select("div#header-author > yt-formatted-string > a")

id_final = []
comment_final = []
comment_date = []

for i in range(len(comment_list)):
    temp_id = id_list[i].text
    temp_id = temp_id.replace('\n', '')
    temp_id = temp_id.replace('\t', '')
    temp_id = temp_id.replace('    ', '')
    id_final.append(temp_id) # 댓글 작성자

    temp_comment = comment_list[i].text
    temp_comment = temp_comment.replace('\n', '')
    temp_comment = temp_comment.replace('\t', '')
    temp_comment = temp_comment.replace('    ', '')
    comment_final.append(temp_comment) # 댓글 내용
    
    temp_date = date_list[i].text
    temp_date = temp_date.replace('\n', '')
    temp_date = temp_date.replace('\t','')
    comment_date.append(temp_date)
    
    
pd_data = {"아이디" : id_final , "댓글 내용" : comment_final, "댓글 시간": comment_date}
youtube_pd = pd.DataFrame(pd_data)

youtube_pd.to_csv('./data_comment/라운드숄더/result_comment3.csv', encoding='utf-8-sig')
