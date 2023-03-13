from parser import Parser
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class PnuParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.base_url = "https://www.pusan.ac.kr/kor/CMS/Board/Board.do?"
        self.notice_page = f"{self.base_url}mgr_seq=3&page="


    def getRecentIndex(self):
        print("Reading database...")

        con, cursor = self.getConnection()
        read_sql = "SELECT * from pnu;"
        cursor.execute(read_sql)
        rows = cursor.fetchall()

        if len(rows) == 0:
            self.recent_index = 0
        else:
            self.recent_index = rows[-1][1]

        print("Recent announcement index is", self.recent_index)
        con.commit()
        con.close()


    def parseData(self):
        self.notice_page = f"{self.notice_page}1"
        browser = self.getParser()
        self.getRecentIndex()

        print("Parsing announcements...")
        end_point = False
        for i in range(1, 4):
            sources = []
            soup_ = BeautifulSoup(browser.page_source, "html.parser")
            t_table = soup_.find('table', class_="board-list-table")
            notice_list = t_table.select('tbody tr')

            for notice in notice_list:
                index_info = notice.find('td', class_="num")
                title_info = notice.find('td', class_="subject").find('a')
                date_info = notice.find('td', class_="date")
                
                index_ = index_info.string
                if index_ is None:
                    continue
                else:
                    index_ = int(index_)
                    if index_ <= self.recent_index:
                        end_point = True
                        break

                title_ = title_info.string.replace("\n", "").replace("\t", "")
                link_ = title_info['href']
                date_ = date_info.string

                sources.append({
                    'id': 0,
                    'index': index_,
                    'title': title_.replace(",", " "),
                    'link': f"{self.base_url}{link_}",
                    'date': date_
                })

            sources = sources[::-1]
            self.page_sources.append(sources)

            if end_point is True:
                break

            browser.switch_to.active_element.find_element(By.XPATH, f'//*[@id="board-wrap"]/div[3]/div/a[{i + 1}]').click()
            

        self.page_sources = self.page_sources[::-1]
        browser.quit()

        print("Complete")
        print("New announcements is", self.page_sources)


    def saveData(self):
        print("Insert new announcements in database...")
        con, cursor = self.getConnection()
        insert_sql = "INSERT INTO pnu VALUES (%(id)s, %(index)s, %(title)s, %(link)s, %(date)s);"

        for page_source in self.page_sources:
            for notice in page_source:
                cursor.execute(insert_sql, notice)

        print("Complete")
        con.commit()
        con.close()