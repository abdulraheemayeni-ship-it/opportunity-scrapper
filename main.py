# # import requests
# # from bs4 import BeautifulSoup
# # import pandas as pd

# # url = "https://weworkremotely.com/remote-jobs/search?term=python"

# # response = requests.get(url)
# # soup = BeautifulSoup(response.text, "html.parser")

# # jobs = []

# # for job in soup.find_all("section"):
# #     titles = job.find_all("span", class_="title")
# #     companies = job.find_all("span", class_="company")

# #     for t, c in zip(titles, companies):
# #         jobs.append({
# #             "title": t.text.strip(),
# #             "company": c.text.strip()
# #         })

# # df = pd.DataFrame(jobs)
# # df.to_csv("jobs.csv", index=False)

# # print(f"Saved {len(jobs)} jobs to jobs.csv")


# # import requests

# # url = "https://httpbin.org/get"
# # response = requests.get(url)

# # print(response.status_code)
# # print(response.text[:200])

# # import requests
# # from bs4 import BeautifulSoup
# # import pandas as pd

# # url = "https://weworkremotely.com/remote-jobs"

# # headers = {
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
# # }

# # response = requests.get(url, headers=headers, timeout=15)

# # print("Status:", response.status_code)

# # soup = BeautifulSoup(response.text, "html.parser")

# # print("Page length:", len(response.text))

# # import requests
# # from bs4 import BeautifulSoup
# # import pandas as pd

# # url = "https://weworkremotely.com/remote-jobs"

# # headers = {
# #     "User-Agent": "Mozilla/5.0"
# # }

# # response = requests.get(url, headers=headers)
# # soup = BeautifulSoup(response.text, "html.parser")

# # jobs = []

# # sections = soup.find_all("section", class_="jobs")

# # for section in sections:
# #     listings = section.find_all("li")

# #     for job in listings:
# #         title = job.find("span", class_="title")
# #         company = job.find("span", class_="company")

# #         if title and company:
# #             jobs.append({
# #                 "title": title.text.strip(),
# #                 "company": company.text.strip()
# #             })

# # df = pd.DataFrame(jobs)
# # df.to_csv("jobs.csv", index=False)

# # print(f"Extracted {len(jobs)} jobs → saved to jobs.csv")


# import requests

# url = "https://weworkremotely.com/remote-jobs"

# headers = {"User-Agent": "Mozilla/5.0"}

# response = requests.get(url, headers=headers)

# print(response.text[:1000])

# url = "https://remoteok.com/remote-python-jobs"

# print(response.text[:1000])

# url = "https://remoteok.com/remote-python-jobs"


# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# url = "https://remoteok.com/remote-python-jobs"

# headers = {
#     "User-Agent": "Mozilla/5.0"
# }

# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "html.parser")

# jobs = []

# # RemoteOK stores jobs in table rows with class "job"
# rows = soup.find_all("tr", class_="job")

# for job in rows:
#     title_tag = job.find("h2")
#     company_tag = job.find("h3")

#     if title_tag and company_tag:
#         jobs.append({
#             "title": title_tag.text.strip(),
#             "company": company_tag.text.strip()
#         })

# df = pd.DataFrame(jobs)
# df.to_csv("jobs.csv", index=False)

# print(f"Extracted {len(jobs)} jobs → jobs.csv")

import requests
import pandas as pd

url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
data = response.json()

jobs = []

for job in data:
    # first item is metadata, skip it
    if "position" in job:
        jobs.append({
            "title": job.get("position"),
            "company": job.get("company"),
            "location": job.get("location")
        })

df = pd.DataFrame(jobs)
df.to_csv("jobs.csv", index=False)

print(f"Extracted {len(jobs)} jobs → jobs.csv")