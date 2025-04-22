from pytrends.request import TrendReq
import random
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def run_parser():
    # Настраиваем HTTP-сессию с ретраями
    requests_session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.3,
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    requests_session.mount("https://", adapter)
    requests_session.mount("http://", adapter)

    try:
        pytrends = TrendReq(
            hl="en-US",
            tz=330,
            requests_args={"headers": {"User-Agent": "Mozilla/5.0"}},
            requests_session=requests_session
        )

        # Анти‑бан-задержка
        time.sleep(random.uniform(2, 5))

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

        # Уникальные и максимум 10
        results = list(dict.fromkeys(results))[:10]
        return results

    except Exception as e:
        # тут можно залогировать e, например print(e) или в файл
        return []
