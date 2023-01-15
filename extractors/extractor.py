from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Extractor:
    def __init__(self):
        self.jobs = []
        self.base_url = ""
        self.keyword = ""

    def set_jobs(self, _jobs):
        self.jobs = _jobs

    def set_base_url(self, url):
        self.base_url = url

    def get_jobs(self):
        return self.jobs

    def get_base_url(self):
        return self.base_url

    def get_page_count(self, soup):
        pass

    def parse_website(self, _keyword):
        # 옵션 없이 진행하면 크롬 화면이 나타난다
        # 화면 없이 크롤링을 위해서 옵션을 추가해주었다.
        # browser = webdriver.Chrome(ChromeDriverManager().install())

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
        browser.get(f"{self.base_url}{_keyword}")
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        browser.quit()

        return soup

    def extract_jobs(self, _keyword):
        pass