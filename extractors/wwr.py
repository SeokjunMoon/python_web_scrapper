from requests import get
from bs4 import BeautifulSoup


def check_website_status(status_code):
    return 200 <= status_code < 400


def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="

    # wwr의 경우 get으로도 크롤링이 가능했다.
    # 따라서 셀레니움을 사용하지 않았다.
    response = get(f"{base_url}{keyword}")
    status_code = response.status_code
    website_status = check_website_status(status_code)
    results = []

    if website_status is False:
        print("Cannot request website")
    else:

        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all('section', class_ = "jobs")
        
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                
                link = anchor['href']
                company, kind, location = anchor.find_all('span', class_ = "company")
                title = anchor.find('span', class_ = "title")
                
                job_data = {
                    'link': f"https://weworkremotely.com{link}",
                    'company': company.string.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'position': title.string.replace(",", " "),
                }
                results.append(job_data)

    print("Found", len(results), "jobs in wwr.\n")

    return results