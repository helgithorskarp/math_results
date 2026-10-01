from paths import INPUTS, WORK
"""Actual full fixture groups using the independently reviewed root fibers."""
import hashlib
import importlib.util
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
SOURCE_SHA='7546be335318c027e45ece973b40528f5cae6def83fc1c29ff565f73620b27e8'
REVIEW_ORDERS=(5760,72,36,12,6,6,8,2,2,6,6,2,6,18,18,6,6,8,6,2,24,18,72)


def normalizer():
    f=INPUTS/'audit.py'
    if hashlib.sha256(f.read_bytes()).hexdigest()!=SOURCE_SHA:
        raise ValueError('changed reviewed normalization source')
    spec=importlib.util.spec_from_file_location('reviewed_star_normalizer',f)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main():
    started=time.monotonic()
    audit=normalizer()
    data=json.loads((INPUTS/'fixtures.json').read_text())
    expected=json.loads((INPUTS/'REVIEW_EXPECTED.json').read_text())['classes']
    groups=[]
    for fi,raw in enumerate(data['stars']):
        q=audit.blocks(raw); key=audit.key(q)
        g=tuple(sorted(p for k,p in audit.normalized(q) if k==key))
        audit.require(len(g)==len(set(g))==REVIEW_ORDERS[fi],'reviewed full group order')
        audit.require(all(tuple(sorted(tuple(sorted(p[v] for v in b)) for b in q))==q for p in g),
                      'false group map')
        audit.require(audit.digest(g)==expected[fi]['automorphisms_sha256'], 'reviewed full group entrywise digest')
        groups.append(g)
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_ACTUAL_FULL_FIXTURE_GROUPS',
            'groups':groups,'orders':list(map(len,groups)),'seconds':time.monotonic()-started,
            'normalizer_sha256':SOURCE_SHA,'source_commit':'0509c3808f44b45fd3c333a10cf36bd329003450',
            'review_ref':'bafkreic2wb2z6reycvrsrywbgjxdtjl5f7eqkbe2yk2xtco2su6tgn43aq',
            'claim':'replay of reviewed generic groups; validation only'}
    (WORK/'swapped-full-groups.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='groups'},sort_keys=True))


if __name__=='__main__':main()
