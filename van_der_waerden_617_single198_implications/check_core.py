"""Exact actual-AP forcing-core checker, independent of QR or packing code."""
import argparse
import json
from pathlib import Path


def need(condition,message):
    if not condition:raise ValueError(message)


def ap(a,d,N):
    need(type(a) is int and type(d) is int and d>0 and 0<=a<a+6*d<N,
         'An actual nonconstant integer seven-term AP')
    return tuple(a+j*d for j in range(7))


def check(data):
    need(type(data) is dict and set(data)=={'format','N','color','seed','units','terminal_AP'},'Exact forcing-core schema')
    need(data['format']=='ACTUAL_AP_FORCING_CORE_1','Forcing-core format')
    N=data['N'];c=data['color']
    need(type(N) is int and N>=7 and type(c) is int and c in [0,1],'Integer geometry and binary colour')
    H=data['seed'];need(type(H) is list and H and all(type(x) is int and 0<=x<N for x in H),'Actual seed positions')
    need(H==sorted(set(H)),'Sorted distinct forcing seed')
    known={x:c for x in H};rows=data['units']
    need(type(rows) is list and len(rows)<=N,'Bounded fresh implication list')
    for row in rows:
        need(type(row) is list and len(row)==4 and all(type(x) is int for x in row),'Integer unit row')
        a,d,x,b=row;A=ap(a,d,N)
        need(x in A and x not in known and b in [0,1],'One fresh actual AP literal')
        need(all(y in known and known[y]==1-b for y in A if y!=x),'ALL six actual predecessors have the opposite colour')
        known[x]=b
    last=data['terminal_AP'];need(type(last) is list and len(last)==2,'Terminal AP schema')
    A=ap(*last,N)
    need(all(x in known for x in A) and len({known[x] for x in A})==1,'Actual terminal monochromatic AP')
    return {'N':N,'seed_color':c,'seed_size':len(H),'units_checked':len(rows),
            'terminal_AP':last,'unextendable':True,'QR_or_weight_assumptions':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('certificate',type=Path);args=parser.parse_args()
    print(json.dumps(check(json.loads(args.certificate.read_text())),sort_keys=True))
