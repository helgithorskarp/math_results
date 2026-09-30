"""Reproduce the small arbitrary-length sole-wire0 closure by bit transitions.

Author/executing agent: six-sorting-2, researcher. The separate scalar
checker imports none of this generator. All comparator pairs are allowed.
"""
import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PAIRS=tuple(itertools.combinations(range(9),2))
INITIAL=(5,7,1,288,40,0,0,0,0)


def move(x,a,b):
    return x^((1<<a)|(1<<b)) if x>>a&1 and not x>>b&1 else x


def step(s,pair):
    p5,p7,pmin,high,test,q5,q8,union,q0=s;a,b=pair
    q5+=p5 in pair;q8+=8 in pair
    union+=a==0 or bool(high&((1<<a)|(1<<b)))
    q0=min(2,q0+(a==0))
    if q5>2 or q8>1 or union>4:return None
    return(b if p5==a else p5,b if p7==a else p7,a if pmin==b else pmin,
           move(high,a,b),move(test,a,b),q5,q8,union,q0)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--path',type=Path,required=True)
    args=parser.parse_args();states={INITIAL};todo=deque([INITIAL])
    while todo:
        s=todo.popleft()
        for pair in PAIRS:
            nxt=step(s,pair)
            if nxt is not None and nxt not in states:states.add(nxt);todo.append(nxt)
    cert=dict(agent='six-sorting-2',role='researcher',wires=9,
              fields=['max5','max7','min1','high288','test40','q5','q8','union288_510','q0_capped2'],
              initial=list(INITIAL),bounds=dict(q5=2,q8=1,union288_510=4),
              excluded=dict(max5=8,max7=8,min1=0,high288=384,test40=384,q0_capped2=2),
              states=[list(s) for s in sorted(states)])
    raw=(json.dumps(cert,separators=(',', ':'),sort_keys=True)+'\n').encode()
    expected=json.loads((HERE/'fixture.json').read_text())['min0_certificate']
    assert len(states)==expected['states'] and hashlib.sha256(raw).hexdigest()==expected['sha256']
    args.path.write_bytes(raw)
    print(json.dumps(dict(states=len(states),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())))


if __name__=='__main__':main()
