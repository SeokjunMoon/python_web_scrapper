from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pymysql
# from os import path




page_sources = []
notices = []
base_url = "https://cse.pusan.ac.kr"
cse_notice_page = f"{base_url}/cse/14651/subview.do"
page_count = 0


# 옵션 없이 진행하면 크롬 화면이 나타난다
# 화면 없이 크롤링을 위해서 옵션을 추가해주었다.
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

# 화면 없이 크롤링을 하게되면, 이를 막는 사이트가 있다.
# 이를 위해 user-agent 를 추가해주었다.
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR")

browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
browser.get(cse_notice_page)

soup = BeautifulSoup(browser.page_source, "html.parser")

print("Check page counts...")

page_inner = soup.find('div', class_="_inner")
page_ul = page_inner.find('ul')
page_list = page_ul.find_all('li')
page_count = len(page_list)

print("Complete")
print("Parsing announcements...")

for i in range(1, page_count + 1):
    browser.switch_to.active_element.find_element(By.XPATH, f'//*[@id="menu14651_obj251"]/div[2]/form[3]/div[1]/div/ul/li[{i}]').click()
    sources = []
    soup_ = BeautifulSoup(browser.page_source, "html.parser")
    t_table = soup_.find('table', class_="artclTable artclHorNum1")
    notice_list = t_table.select('tbody tr')

    for notice in notice_list:
        index_info = notice.find('td', class_="_artclTdNum")
        title_info = notice.find('td', class_="_artclTdTitle").find('a')
        date_info = notice.find('td', class_="_artclTdRdate")
        
        index_ = index_info.string
        if (index_ is None):
            continue

        title_ = title_info.find('strong').string
        link_ = title_info['href']
        date_ = date_info.string

        sources.append({
            'index': index_,
            'title': title_.replace(",", " "),
            'link': f"{base_url}{link_}",
            'date': date_
        })
    sources = sources[::-1]
    page_sources.append(sources)

page_sources = page_sources[::-1]
browser.quit()

print("Complete")

print("Connecting to mysql database...")
con = pymysql.connect(host='104.196.224.16', user='root', password='ms38559851!',
                        db='pnu_parser', charset='utf8')

cursor = con.cursor()
insert_sql = "INSERT INTO cse VALUES (%(index)s, %(title)s, %(link)s, %(date)s);"
read_sql = "SELECT * from cse;"

print("Reading database...")
cursor.execute(read_sql)
rows = cursor.fetchall()
recent_index = 0

for row in rows:
    if row[0] > recent_index:
        recent_index = row[0]

print("Insert announcements in database...")
for page_source in page_sources:
    for notice in page_source:
        if int(notice['index']) > recent_index:
            cursor.execute(insert_sql, notice)

con.commit()
con.close()

print("Complete all tasks.")

# file_name = "./github/python_web_scrapper/pnu_parser/PNU_CSE_공지사항.csv"

# if not path.exists(file_name):
#     create_file = open(file_name, 'w', encoding='utf-8-sig')
#     create_file.write("Title,Link,Date\n")
#     for page_source in page_sources:
#         for notice in page_source:
#             create_file.write(f"{notice['index']},{notice['title']},{notice['link']},{notice['date']}\n")

# else:
#     with open(file_name, 'r') as f:
#         last_line = f.readlines()[-1]
    
#     last_index = int(last_line.split(',')[0])
#     modify_file = open(file_name, 'a', encoding='utf-8-sig')

#     for page_source in page_sources:
#         for notice in page_source:
#             current_index = int(notice['index'])
#             if current_index <= last_index:
#                 continue
#             modify_file.write(f"{notice['index']},{notice['title']},{notice['link']},{notice['date']}\n")
