from datetime import datetime
from model import db, Watch
from scrape import scrape


def fetch_all_watches() -> list[Watch]:
    result = db.fetch()
    items = [Watch(**item) for item in result.items]
    while result.last:
        result = db.fetch()
        items = [Watch(**item) for item in result.items]
    items.sort(key=lambda w: w.updated_time)
    return items

def execute_watch(watch: Watch, notify=False):
    info = scrape(watch.url, watch.xpath)
    watch.values.append((datetime.now().timestamp(), info))
    db.update({
        "values": watch.values,
        "updated_time": datetime.utcnow().timestamp()
    }, watch.key)

    if notify and len(watch.values) >= 2 and watch.values[-1][1] != watch.values[-2][1]:
        # TODO implement notification
        pass