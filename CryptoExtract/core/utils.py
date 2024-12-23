import os

LAST_UPDATED_FILE = "last_updated.txt"


def get_last_updated():
    if os.path.exists(LAST_UPDATED_FILE):
        with open(LAST_UPDATED_FILE, "r") as f:
            return f.read().strip()
    return "No data loaded yet."
