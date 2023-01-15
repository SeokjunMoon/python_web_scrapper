from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


base_url = "https://kr.indeed.com/jobs?q="


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
    left_pane = soup.find('div', class_="jobsearch-LeftPane")
    buttons = left_pane.select("nav div")
    
    if buttons == None:
        return 1
    
    page_count = len(buttons)
    
    if page_count <= 5:
        return page_count
    else:
        return 5



def extract_indeed_jobs(keyword):
    soup = parse_website(keyword)
    pages = get_page_count(soup)
    
    print("Found", pages, "pages in indeed.\n")
    
    results = []
    
    for page in range(pages):
        page_keyword = f"{keyword}&start={page * 10}"
        print("Requesting:", f"{base_url}{page_keyword}")
        soup = parse_website(page_keyword)
        job_list = soup.find('ul', class_="jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False)

        for job in jobs:
            zone = job.find('div', class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                location = job.find('div', class_="companyLocation")
                company = job.find('span', class_="companyName")
                
                job_data = {
                    'link': f"https://kr.indeed.com{link}",
                    'company': company.string.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'position': title.replace(",", " ")
                }
                results.append(job_data)

    print("Found", len(results), "jobs in indeed.\n")
    return results