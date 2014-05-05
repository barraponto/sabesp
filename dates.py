#coding: utf-8
import json
from datetime import date, timedelta

start = date(2004, 1, 1)
today = date.today()
delta = today - start

dates = [{'day': d.day, 'month': d.month, 'year': d.year}
         for d in (start + timedelta(n) for n in xrange(delta.days))]

with open('dates.json', 'w') as f:
    json.dump(dates, f)
