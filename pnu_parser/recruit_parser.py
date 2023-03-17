from parser import Parser
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class RecruitParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.base_url = "https://cse.pusan.ac.kr"
        self.notice_page = f"{self.base_url}/cse/14667/subview.do"


    def getRecentIndex(self):
        print("Reading database...")

        con, cursor = self.getConnection()
        read_sql = "SELECT * from pnu where type='recruit';"
        cursor.execute(read_sql)
        rows = cursor.fetchall()

        if len(rows) == 0:
            self.recent_index = 0
        else:
            self.recent_index = rows[-1][2]

        print("Recent announcement index is", self.recent_index)
        con.commit()
        con.close()

        
    def parseData(self):
        browser = self.getParser()
        self.getRecentIndex()

        print("Parsing announcements...")
        end_point = False
        for i in range(1, 10):
            browser.switch_to.active_element.find_element(By.XPATH, f'//*[@id="menu14667_obj289"]/div[2]/form[3]/div[1]/div/ul/li[{i}]').click()
            sources = []
            soup_ = BeautifulSoup(browser.page_source, "html.parser")
            t_table = soup_.find('table', class_="artclTable artclHorNum1")
            notice_list = t_table.select('tbody tr')

            for notice in notice_list:
                index_info = notice.find('td', class_="_artclTdNum")
                title_info = notice.find('td', class_="_artclTdTitle").find('a')
                date_info = notice.find('td', class_="_artclTdRdate")
                
                index_ = index_info.string
                if index_ is None:
                    continue
                else:
                    index_ = int(index_)
                    if index_ <= self.recent_index:
                        end_point = True
                        break

                title_ = title_info.find('strong').string
                link_ = title_info['href']
                date_ = date_info.string

                sources.append({
                    'id': 0,
                    'type': 'recruit',
                    'index': index_,
                    'title': title_.replace(",", " "),
                    'link': f"{self.base_url}{link_}",
                    'date': date_.replace(".", "-")
                })

            sources = sources[::-1]
            self.page_sources.append(sources)

            if end_point is True:
                break
            

        self.page_sources = self.page_sources[::-1]
        browser.quit()

        print("Complete")
        print("New announcements is", self.page_sources)


    def saveData(self):
        if len(self.page_sources) != 0:
            print("Insert new announcements in database...")
            con, cursor = self.getConnection()
            insert_sql = "INSERT INTO pnu VALUES (%(id)s, %(type)s, %(index)s, %(title)s, %(link)s, %(date)s);"

            for page_source in self.page_sources:
                for notice in page_source:
                    cursor.execute(insert_sql, notice)

            print("Complete")
            con.commit()
            con.close()
        else:
            print("No updating")