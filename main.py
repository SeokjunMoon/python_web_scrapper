from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.jobkorea import extract_jobkorea_jobs


keyword = input("What do you want to search for? ")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
jobkorea = extract_jobkorea_jobs(keyword)
jobs = indeed + wwr + jobkorea

file_name = f"{keyword}.csv"

# 인코딩 지정 안하면 한글 깨짐
# utf-8 로 하면 한글 깨짐
# 해결을 위해 인코딩을 utf-8-sig 로 변경
file = open(file_name, "w", encoding='utf-8-sig')
file.write("Position,Company,Location,URL\n")

for job in jobs:
    file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")

file.close()