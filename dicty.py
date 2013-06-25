#!/usr/bin/python

import collections

def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


dictionary1={'level1':{'level2':{'levelA':0,'levelB':1}}}
update={'level1':{'level2':{'levelB':10}}}
dictionary1.update(update)
print dictionary1
{'level1': {'level2': {'levelB': 10}}}