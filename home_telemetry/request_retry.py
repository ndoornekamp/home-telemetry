import requests
from requests.adapters import HTTPAdapter, Retry


def requests_retry_get(url):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))

    return session.get(url)
