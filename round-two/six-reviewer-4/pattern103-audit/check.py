"""Literal original-coordinate Euler/square checker; imports no proposal kernel."""
import argparse, csv, hashlib, json
from pathlib import Path
Q=103
SQUARES={x*x%Q for x in range(1,Q)}
def require(test, reason):
    if not test: raise ValueError(reason)
def char(x):
    x %= Q; require(x != 0, 'undefined root character')
    square = int(x not in SQUARES)
    euler = pow(x, 51, Q)
    require(euler in (1,102) and int(euler==102)==square, 'Euler/squares disagreement')
    return square
def label(x, p, u):
    require(x not in {p,(p+u)%Q,(p+2*u)%Q,(p+4*u)%Q}, 'free column in witness')
    return sum(weight*char(x-p-u*r) for weight,r in ((4,1),(2,2),(1,4)))
def check_row(row, max_step=50):
    require(len(row)==12, 'row width')
    u, word = row[:2]; require(1<=u<Q and word in range(0,256,2), 'case domain')
    supports=[]; integer_lifts=[]; cyclic_lifts=[]
    for i in range(2,12,2):
        a,d = row[i:i+2]; require(0<=a<Q and 1<=d<=max_step, 'start/step')
        points=[(a+j*d)%Q for j in range(7)]; points_set=set(points)
        require(len(points_set)==7, 'repeated witness point')
        require(not any(points_set.intersection(old) for old in supports), 'overlapping supports')
        require(len({(word>>label(x,0,u))&1 for x in points})==1, 'nonmonochromatic witness')
        supports.append(points_set)
        # Physical phase6 inputs use U=6u. This is a new bijective enumeration of all102 scales.
        actual_word=sum(((word>>(k^(7*char(6))))&1)<<k for k in range(8))
        for t in range(1,7):
            start=next(n for n in range(t,t+6*Q,6) if n%Q==(6*a)%Q)
            ints=[start+6*d*j for j in range(7)]
            require(ints[-1] <= t+402*6, 'improved endpoint')
            require(len({(actual_word>>label(n%Q,0,6*u%Q))&1 for n in ints})==1,'actual integer colors')
            require(all(n%6==t%6 for n in ints), 'actual phase')
            cyc=[n%(6*Q) for n in ints]
            require(len(set(cyc))==7, 'cyclic distinctness')
            integer_lifts.append((t,ints)); cyclic_lifts.append((t,cyc))
    for t in range(1,7):
        require(len({n for phase,seq in integer_lifts if phase==t for n in seq})==35, 'integer overlap')
        require(len({n for phase,seq in cyclic_lifts if phase==t for n in seq})==35, 'cyclic overlap')
    return {'aps':5,'points':35,'integer_aps':30,'integer_points':210,'cyclic_aps':30}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--lo',type=int,required=True);ap.add_argument('--hi',type=int,required=True);args=ap.parse_args()
    raw=Path(args.input).read_bytes();rows=[list(map(int,r)) for r in csv.reader(raw.decode().splitlines())]
    require([(r[0],r[1]) for r in rows]==[(u,w) for u in range(args.lo,args.hi) for w in range(0,256,2)], 'whole case coverage/order')
    total={k:0 for k in ('aps','points','integer_aps','integer_points','cyclic_aps')}
    for row in rows:
        for k,v in check_row(row).items():total[k]+=v
    print(json.dumps({'lo':args.lo,'hi':args.hi,'cases':len(rows),'sha256':hashlib.sha256(raw).hexdigest(),**total},sort_keys=True))
if __name__=='__main__':main()
