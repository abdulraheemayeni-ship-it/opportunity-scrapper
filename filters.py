from config import ALLOWED_ROLES


def is_allowed_job(title):
    title = title.lower()

    return any(
        role in title
        for role in ALLOWED_ROLES
    )