from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


base_url = "https://www.jobkorea.co.kr/Search/?stext="


def parse_website(keyword):
    # 옵션 없이 진행하면 크롬 화면이 나타난다
    # 화면 없이 크롤링을 위해서 옵션을 추가해주었다.
    # browser = webdriver.Chrome(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # 화면 없이 크롤링을 하게되면, 이를 막는 사이트가 있다.
    # 이를 위해 user-agent 를 추가해주었다.
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    options.add_argument("lang=ko_KR")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(f"{base_url}{keyword}")
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    browser.quit()

    return soup

    
def get_page_count(soup):
    pagination = soup.find_all('div', class_="tplPagination newVer wide")[1]
    pages = pagination.select("ul li")
    
    return len(pages)


def extract_jobkorea_jobs(keyword):
    soup = parse_website(keyword)
    pages = get_page_count(soup)
    
    print("Found", pages, "pages in jobkorea.")
    
    results = []
    
    for page in range(pages):
        page_keyword = f"{keyword}&tabType=recruit&Page_No={page + 1}"
        print("Requesting:", f"{base_url}{page_keyword}")
        soup = parse_website(page_keyword)
        job_list = soup.find('div', class_="list-default")
        jobs = job_list.select("ul li")

        for job in jobs:
            company = job.find('a', class_="name dev_view")
            location = job.find('span', class_="loc long")
            title = job.find('a', class_="title dev_view")
            link = title['href']
            job_data = {
                'link': f"https://www.jobkorea.co.kr{link}",
                'company': company.string.replace(",", " "),
                'location': location.string.replace(",", " "),
                'position': title['title'].replace(",", " ")
            }
            results.append(job_data)

    print("Found", len(results), "jobs in jobkorea.\n")
    
    return results