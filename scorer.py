from config import TECH_ROLES


def score_job(title, description):
    text = (title + " " + description).lower()

    score = 0

    for role, points in TECH_ROLES.items():
        if role in text:
            score += points

    return score