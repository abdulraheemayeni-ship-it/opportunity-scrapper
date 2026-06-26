# Opportunity Scraper

A Python application that fetches remote jobs from the RemoteOK API, filters software and AI-related roles, ranks them using a custom scoring system, removes duplicates using persistent memory, and exports the best opportunities to CSV.

## Features

- Fetches live jobs from RemoteOK
- Scores jobs based on relevance
- Filters software-related jobs
- Avoids duplicate jobs
- Saves results to CSV

## Tech Stack

- Python
- Requests
- Pandas

## Run

```bash
python main.py
```