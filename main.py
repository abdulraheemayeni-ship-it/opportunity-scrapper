import requests
import pandas as pd

# ----------------------------
# LOAD MEMORY
# ----------------------------
try:
    with open("seen_jobs.txt", "r") as file:
        seen_jobs = set(file.read().splitlines())
except FileNotFoundError:
    seen_jobs = set()

# ----------------------------
# FETCH DATA
# ----------------------------
url = "https://remoteok.com/api"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

except Exception as e:
    print(f"Connection error: {e}")
    exit()

# ----------------------------
# SCORING SYSTEM
# ----------------------------
def score_job(title):
    title_lower = title.lower()

    tech_roles = {
        "data scientist": 10,
        "machine learning engineer": 10,
        "software engineer": 8,
        "backend developer": 7,
        "python developer": 7,
        "data analyst": 6,
        "frontend developer": 7,
        "full stack developer": 8,
        "ai engineer": 10,
        "automation engineer": 8,
        "ml engineer": 10
    }

    score = 0

    for role, points in tech_roles.items():
        if role in title_lower:
            score += points

    return score



# ----------------------------
# FILTERING
# ----------------------------
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
    job_id = str(job.get("id", ""))

    title_lower = title.lower()

    matched = score_job(title) > 0

    if not matched:
        continue

    if job_id in seen_jobs:
        continue

    seen_jobs.add(job_id)

    jobs.append({
        "title": title,
        "company": job.get("company"),
        "location": job.get("location"),
        "fit_score": score_job(title)
    })

# ----------------------------
# HANDLE EMPTY RESULTS SAFELY
# ----------------------------
if len(jobs) == 0:
    print("No new matching jobs found.")
    exit()

# ----------------------------
# DATAFRAME + SORT
# ----------------------------
df = pd.DataFrame(jobs)
df = df.sort_values(by="fit_score", ascending=False)

# ----------------------------
# OUTPUT
# ----------------------------
print(f"\nFound {len(jobs)} matching jobs\n")

print("Matching Jobs:\n")
for job in jobs:
    print(f"{job['title']} | {job['company']}")

print("\nTOP OPPORTUNITIES TODAY\n")

top_jobs = df.head(5)

for i, (_, row) in enumerate(top_jobs.iterrows(), start=1):
    print(
        f"{i}. {row['title']} | "
        f"{row['company']} | "
        f"Score: {row['fit_score']}"
    )

# ----------------------------
# SAVE CSV
# ----------------------------
df.to_csv("filtered_jobs.csv", index=False)

# ----------------------------
# SAVE MEMORY
# ----------------------------
with open("seen_jobs.txt", "w") as file:
    for job_id in seen_jobs:
        file.write(job_id + "\n")