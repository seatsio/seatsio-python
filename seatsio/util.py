from datetime import datetime


def parse_date(date_as_str):
    if date_as_str is None:
        return None
    else:
        try:
            return datetime.strptime(date_as_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return datetime.strptime(date_as_str, "%Y-%m-%dT%H:%M:%SZ")