from python_web_scrapper.extractors.indeed import IndeedExtractor
from python_web_scrapper.extractors.jobkorea import JobKoreaExtractor
from python_web_scrapper.extractors.wwr import WWRExtractor

keyword = input("What do you want to search for? ")

indeed = IndeedExtractor()
jobkorea = JobKoreaExtractor()
wwr = WWRExtractor()

indeed.extract_jobs(keyword)
jobkorea.extract_jobs(keyword)
wwr.extract_jobs(keyword)

jobs = indeed.get_jobs() + jobkorea.get_jobs() + wwr.get_jobs()
file_name = f"{keyword}.csv"

# 인코딩 지정 안하면 한글 깨짐
# utf-8 로 하면 한글 깨짐
# 해결을 위해 인코딩을 utf-8-sig 로 변경
file = open(file_name, "w", encoding='utf-8-sig')
file.write("Position,Company,Location,URL\n")

for job in jobs:
    file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")

file.close()