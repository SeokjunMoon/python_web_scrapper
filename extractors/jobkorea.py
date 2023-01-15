from python_web_scrapper.extractors.extractor import Extractor


class JobKoreaExtractor(Extractor):
    def __init__(self):
        Extractor.__init__(self)
        self.set_base_url("https://www.jobkorea.co.kr/Search/?stext=")

    def get_page_count(self, soup):
        pagination = soup.find_all('div', class_="tplPagination newVer wide")[1]
        pages = pagination.select("ul li")

        return len(pages)

    def extract_jobs(self, _keyword):
        soup = self.parse_website(_keyword)
        pages = self.get_page_count(soup)

        print("Found", pages, "pages in jobkorea.")

        results = []
        for page in range(pages):
            page_keyword = f"{_keyword}&tabType=recruit&Page_No={page + 1}"
            print("Requesting:", f"{self.get_base_url()}{page_keyword}")

            soup = self.parse_website(page_keyword)
            job_list = soup.find('div', class_="list-default")
            jobs = job_list.select("ul li")

            for job in jobs:
                company = job.find('a', class_="name dev_view")
                location = job.find('span', class_="loc long")
                title = job.find('a', class_="title dev_view")
                link = title['href']

                company_str = ""

                if company.string is None:
                    company_str = "None Company"
                else:
                    company_str = company.string.replace(",", " ")

                job_data = {
                    'link': f"https://www.jobkorea.co.kr{link}",
                    'company': company_str,
                    'location': location.string.replace(",", " "),
                    'position': title['title'].replace(",", " ")
                }
                results.append(job_data)

        print("Found", len(results), "jobs in jobkorea.\n")
        self.set_jobs(results)