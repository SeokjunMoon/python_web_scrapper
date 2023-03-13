from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pymysql
# from os import path



class Parser:
    def __init__(self):
        self.browser = 0
        self.soup = 0
        self.page_sources = []
        self.base_url = ""
        self.notice_page = ""
        self.page_count = 0
        self.recent_index = 0


    def getParser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/61.0.3163.100 Safari/537.36")
        options.add_argument("lang=ko_KR")

        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        browser.get(self.notice_page)

        return browser


    def getConnection(self):
        print("Connecting to mysql database...")
        con = pymysql.connect(host='104.196.224.16', user='root', password='ms38559851!',
                                db='pnu_parser', charset='utf8')
        cursor = con.cursor()
        return con, cursor


    def getRecentIndex(self):
        pass

    def parseData(self):
        pass

    def saveData(self):
        pass