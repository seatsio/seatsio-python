import os

DEFAULT_URL = "https://httpbingo.org"


def httpbin_url(path=""):
    base = os.environ.get("HTTPBIN_URL", DEFAULT_URL)
    return base + path
