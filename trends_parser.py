
from pytrends.request import TrendReq
import random, time

def run_parser():
    pytrends = TrendReq(hl='en-US', tz=330, backoff_factor=0.5,
                        requests_args={'headers': {'User-Agent': 'Mozilla/5.0'}})
    time.sleep(random.uniform(2, 5))  # Anti-ban delay

    keywords = ["online casino", "casino app india", "teen patti", "real money game", "slot games"]
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
