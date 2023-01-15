from python_web_scrapper.extractors.extractor import Extractor


class IndeedExtractor(Extractor):
    def __init__(self):
        Extractor.__init__(self)
        self.set_base_url("https://kr.indeed.com/jobs?q=")

    def get_page_count(self, soup):
        left_pane = soup.find('div', class_="jobsearch-LeftPane")
        buttons = left_pane.select("nav div")

        if buttons is None:
            return 1

        page_count = len(buttons)

        if page_count <= 5:
            return page_count
        else:
            return 5

    def extract_jobs(self, _keyword):
        soup = self.parse_website(_keyword)
        pages = self.get_page_count(soup)

        print("Found", pages, "pages in indeed.\n")

        results = []
        for page in range(pages):
            page_keyword = f"{_keyword}&start={page * 10}"
            print("Requesting:", f"{self.get_base_url()}{page_keyword}")

            soup = self.parse_website(page_keyword)
            job_list = soup.find('ul', class_="jobsearch-ResultsList")
            jobs = job_list.find_all('li', recursive=False)

            for job in jobs:
                zone = job.find('div', class_="mosaic-zone")

                if zone is None:
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
        self.set_jobs(results)
