"""Generate untrusted event/factor proposals for the independent verifier."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from math import lcm
from pathlib import Path
import json
import time
import sympy as s
import model

K=s.QQ.algebraic_field(s.sqrt(33))
T=s.Symbol('t')


def encode(poly):
    rows=[]
    for c in reversed(poly.rep.to_list()):
        q=list(c.to_list())
        q=[s.QQ(0)]*(2-len(q))+q
        rows.append((Fraction(str(q[1])),Fraction(str(q[0]))))
    d=lcm(*(v.denominator for c in rows for v in c))
    return model.canonical([(int(a*d),int(b*d)) for a,b in rows])


def factor_task(row):
    kind,index,p=row
    f=s.Poly.from_list([K([b,a]) for a,b in p[::-1]],gens=T,domain=K)
    if kind=='collision':
        f=f.gcd(f.diff())
    _,factors=f.factor_list()
    return {'kind':kind,'index':index,
            'factors':[[encode(g),e] for g,e in factors]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if not 1<=args.workers<=16:
        raise ValueError('workers must be between1 and16')
    args.out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    data=model.generate()
    (args.out/'contacts.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    tasks=[(kind,i,r['poly'])
           for kind,name in [('unit','contacts'),('collision','collision_norms')]
           for i,r in enumerate(data[name])]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows=list(pool.map(factor_task,tasks,chunksize=10))
    (args.out/'factorizations.json').write_text(json.dumps(rows,separators=(',',':'))+'\n')
    print(json.dumps({'proposed':True,'unit_polynomials':len(data['contacts']),
                      'collision_norms':len(data['collision_norms']),
                      'seconds':time.monotonic()-start}))


if __name__=='__main__':
    main()
