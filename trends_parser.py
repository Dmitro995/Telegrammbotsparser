from pytrends.request import TrendReq
import random
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def run_parser():
    # Configure session with retries
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.3,
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        pytrends = TrendReq(
            hl="en-US",
            tz=330,
            requests_args={"headers": {"User-Agent": "Mozilla/5.0"}},
            requests_session=session
        )

        time.sleep(random.uniform(2, 5))  # Anti-ban delay

        keywords = [
            "online casino", "casino app india", "teen patti",
            "real money game", "slot games"
        ]
        pytrends.build_payload(keywords, geo="IN", timeframe="now 7-d")
        data = pytrends.related_queries()

        results = []
        for kw, queries in data.items():
            if isinstance(queries, dict) and queries.get("rising") is not None:
                trends = queries["rising"]["query"].tolist()
                results.extend(trends)

        # Preserve first occurrence order and limit to 10
        unique = list(dict.fromkeys(results))
        return unique[:10]
    except Exception:
        return []
