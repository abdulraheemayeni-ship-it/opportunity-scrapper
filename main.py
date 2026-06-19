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

# import requests
# import pandas as pd

# url = "https://remoteok.com/api"

# headers = {
#     "User-Agent": "Mozilla/5.0"
# }

# response = requests.get(url, headers=headers)
# data = response.json()

# jobs = []

# for job in data:
#     # first item is metadata, skip it
#     if "position" in job:
#         jobs.append({
#             "title": job.get("position"),
#             "company": job.get("company"),
#             "location": job.get("location")
#         })

# df = pd.DataFrame(jobs)
# df.to_csv("jobs.csv", index=False)

# print(f"Extracted {len(jobs)} jobs → jobs.csv")

import requests
import pandas as pd
import re

url = "https://remoteok.com/api"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
data = response.json()

# def score_job(title):
#     score = 0

#     keywords = {
#         "python": 3,
#         "ai": 5,
#         "machine learning": 5,
#         "backend": 2,
#         "data": 2
#     }

#     title = title.lower()

#     for keyword, points in keywords.items():
#         if keyword in title:
#             score += points

#     return score

def score_job(title):
    score = 0

    keywords = {
        "python": 5,
        "ai": 8,
        "machine learning": 8,
        "data scientist": 6,
        "data analyst": 4,
        "backend": 4,
        "software engineer": 5,
        "developer": 4,
        "automation": 5,
        "data": 1
    }

    title = title.lower()

    for keyword, points in keywords.items():

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, title):
            score += points

    return score

keywords = [
    "python",
    "ai",
    "machine learning",
    "data",
    "backend",
    "developer",
    "engineer",
    "software",
    "automation"
]


jobs = []

for job in data:

    if "position" not in job:
        continue

    title = str(job.get("position", ""))

    # if any(keyword.lower() in title.lower() for keyword in keywords):

    title_lower = title.lower()

    matched = False

    for keyword in keywords:
        pattern = r"\b" + re.escape(keyword.lower()) + r"\b"

        if re.search(pattern, title_lower):
            matched = True
            break

    # print("Checking:", title)

    if matched:

        # jobs.append({
        #     "title": title,
        #     "company": job.get("company"),
        #     "location": job.get("location"),
        #     "salary_min": job.get("salary_min"),
        #     "salary_max": job.get("salary_max")
        # })
        jobs.append({
            "title": title,
            "company": job.get("company"),
            "location": job.get("location"),
            "fit_score": score_job(title)
        })

df = pd.DataFrame(jobs)

df.to_csv("filtered_jobs.csv", index=False)

print(f"Found {len(jobs)} matching jobs")


print("\nMatching Jobs:\n")

for job in jobs:
    print(f"{job['title']} | {job['company']}")


df = pd.DataFrame(jobs)

df = df.sort_values(
    by="fit_score",
    ascending=False
)

print("\nTOP OPPORTUNITIES TODAY\n")

top_jobs = df.head(5)

for i, (_, row) in enumerate(top_jobs.iterrows(), start=1):
    print(
        f"{i}. {row['title']} | "
        f"{row['company']} | "
        f"Score: {row['fit_score']}"
    )