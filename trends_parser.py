from pytrends.request import TrendReq
import json
from send_to_telegram import send_to_telegram
from datetime import datetime

with open("config.json") as f:
    config = json.load(f)

pytrends = TrendReq(hl='en-IN', tz=330)
keywords = config["keywords"]
geo = config.get("geo", "IN")
chat_id = config["telegram_chat_id"]

def load_history():
    try:
        with open("brands.json") as f:
            return set(json.load(f))
    except:
        return set()

def save_history(data):
    with open("brands.json", "w") as f:
        json.dump(sorted(list(data)), f)

history = load_history()
new_items = set()

for kw in keywords:
    pytrends.build_payload([kw], geo=geo, timeframe='now 7-d')
    related = pytrends.related_queries().get(kw, {}).get('rising', None)
    if related is not None:
        for query in related['query']:
            q_lower = query.lower()
            if any(x in q_lower for x in ['casino', 'bet', 'slot', 'rummy', 'teen']):
                if query not in history:
                    new_items.add(query)
                    history.add(query)

if new_items:
    message = "🎰 New Casino Trends:
" + "
".join(f"- {item}" for item in new_items)
    send_to_telegram(message, config["telegram_bot_token"], chat_id)

save_history(history)