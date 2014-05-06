# coding: utf-8
import json
from collections import defaultdict
from hashlib import md5
from itertools import chain


def datename(datelike):
    return '{year}-{month}-{day}'.format(**datelike)


def file_md5sum(filename):
    try:
        with open(filename) as f:
            return md5(f.read()).hexdigest()
    except IOError:
        return False


with open('dates.json') as f:
    dates = json.load(f)

md5sums = {datename(d): file_md5sum('source/' + datename(d) + '.jpg')
           for d in dates}
grouped_results = defaultdict(set)

for filename, result in md5sums.iteritems():
    grouped_results[result].add(filename)

rerun = list(chain.from_iterable(
    [keys for value, keys in grouped_results.iteritems() if len(keys) > 1]))

rerun = [{'year': dt[0], 'month': dt[1], 'day': dt[2]} for dt in [d.split() for d in rerun]]

with open('rerun.json', 'w') as f:
    json.dump(rerun, f)
