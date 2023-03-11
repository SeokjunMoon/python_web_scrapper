# def plus(a = 0, b = 0):
#     print(a + b)
    
# def minus(a = 0, b = 0):
#     print(a - b)
    
# def multiple(a = 0, b = 0):
#     print(a * b)
    
# def divide(a = 0, b = 1):
#     if b == 0:
#         print("cannot divide")
#         return
#     print(a / b)
    
# def power(a = 0, b = 0):
#     print(a ** b)



from requests import get

websites = (
    "google.com",
    "naver.com",
    "https://twitter.com",
    "facebook.com",
    "https://tiktok.com"
)

results = {}

def get_website_status(status_code):
    if status_code >= 500:
        return "5xx / server error"
    elif status_code >= 400:
        return "4xx / client error"
    elif status_code >= 300:
        return "3xx / redirection"
    elif status_code >= 200:
        return "2xx / successful"
    elif status_code >= 100:
        return "1xx / informational response"


for website in websites:
    if not website.startswith("https://"):
        website = f"https://{website}"
    
    response = get(website)
    status_code = response.status_code
    results[website] = get_website_status(status_code)
        
print(results)



from requests import get
from bs4 import BeautifulSoup


def check_website_status(status_code):
    return 100 <= status_code < 400


base_url = "https://weworkremotely.com/remote-jobs/search?term="
search_term = "python"

response = get(f"{base_url}{search_term}")
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
            company, kind, region = anchor.find_all('span', class_ = "company")
            title = anchor.find('span', class_ = "title")
            
            job_data = {
                'link': f"https://weworkremotely.com{link}",
                'company': company.string,
                'region': region.string,
                'position': title.string,
                'kind': kind.string
            }
            results.append(job_data)
            
    print(results)