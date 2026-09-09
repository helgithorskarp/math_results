from itertools import combinations
import json
from pathlib import Path
import random
import time
import generate

def literal(a):
    return sum(all((a[u]>>v&1)==color for u,v in combinations(s,2))
               for s in combinations(range(len(a)),5) for color in (0,1))

def run():
    r=random.Random(427531)
    checked=0
    for n in (5,8,10):
        for word in (0,(1<<(n*(n-1)//2))-1,*[r.getrandbits(n*(n-1)//2) for _ in range(6)]):
            a,b=generate.decode(n,word);start=literal(a)
            if start!=generate.cliques(a,5)+generate.cliques(b,5):raise ValueError('initial census')
            if generate.encode(a)!=word:raise ValueError('edge encoding')
            for u,v in combinations(range(n),2):
                d=generate.delta(a,b,u,v)
                generate.flip(a,b,u,v)
                if literal(a)!=start+d:raise ValueError('literal delta')
                generate.flip(a,b,u,v);checked+=1
    a,b=generate.decode(43,r.getrandbits(903));pairs=list(combinations(range(43),2))
    start=time.monotonic()
    for i in range(10000):generate.delta(a,b,*pairs[i%903])
    elapsed=time.monotonic()-start
    return {'status':'REFERENCE_CONTROLS_PASS','literal_single_flip_checks':checked,
            'benchmark_proposals':10000,'seconds':elapsed,'estimated_full_delta_seconds':elapsed*(32*524288)/10000,
            'implementation_choice':'retain Python reference; no native rewrite'}

if __name__=='__main__':
    import sys
    result=run();Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
