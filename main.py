import argparse
import pandas as pd

from database import (
    create_database,
    job_exists,
    save_job
)
from fetcher import fetch_jobs
from scorer import score_job
from filters import is_allowed_job


# ----------------------------
# COMMAND LINE ARGUMENTS
# ----------------------------
parser = argparse.ArgumentParser(
    description="Opportunity Scraper Pro"
)

parser.add_argument(
    "--top",
    type=int,
    default=5,
    help="Number of top jobs to display"
)

parser.add_argument(
    "--save",
    action="store_true",
    help="Save results to CSV"
)

parser.add_argument(
    "--all",
    action="store_true",
    help="Show all matching jobs"
)

args = parser.parse_args()

create_database()

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
data = fetch_jobs()

if data is None:
    exit()


# ----------------------------
# FILTERING
# ----------------------------


jobs = []

for job in data:

    if "position" not in job:
        continue

    

    title = str(job.get("position", ""))
    job_id = str(job.get("id", ""))

    matched = is_allowed_job(title)

    if not matched:
        continue

    if job_exists(job_id) and not args.all:
        continue


    score = score_job(
        title,
        job.get("description", "")
    )

    save_job(
        job_id,
        title,
        job.get("company"),
        job.get("location"),
        score
    )

    jobs.append(
        {
            "title": title,
            "company": job.get("company"),
            "location": job.get("location"),
            "fit_score": score,
        }
    )

# ----------------------------
# HANDLE EMPTY RESULTS SAFELY
# ----------------------------
if not jobs:
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

top_jobs = df.head(args.top)

for i, (_, row) in enumerate(top_jobs.iterrows(), start=1):
    print(
        f"{i}. {row['title']} | "
        f"{row['company']} | "
        f"Score: {row['fit_score']}"
    )

# ----------------------------
# SAVE CSV
# ----------------------------
if args.save:
    df.to_csv("filtered_jobs.csv", index=False)
    print("\nResults saved to filtered_jobs.csv")

# ----------------------------
# SAVE MEMORY
# ----------------------------
with open("seen_jobs.txt", "w") as file:
    for job_id in seen_jobs:
        file.write(job_id + "\n")