from pytrends.request import TrendReq
import random, time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

def run_parser():
    # Настраиваем сессию с ретраями
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.3, allowed_methods=["GET", "POST"])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    pytrends = TrendReq(
        hl='en-US',
        tz=330,
        requests_args={
            'headers': {'User-Agent': 'Mozilla/5.0'}
        },
        requests_session=session
    )

    time.sleep(random.uniform(2, 5))  # Anti-ban delay

    keywords = [
        "online casino", "casino app india", "teen patti",
        "real money game", "slot games"
    ]
    pytrends.build_payload(keywords, geo='IN', timeframe='now 7-d')

    data = pytrends.related_queries()
    results = []

    for kw, queries in data.items():
        if queries['rising'] is not None:
            trends = queries['rising']['query'].tolist()
            results.extend(trends)

    results = list(set(results))
    if len(results) > 10:
        results = results[:10]

    return results
