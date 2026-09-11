"""Generate a necessary reconstruction CNF for one of five exhaustive flags."""
from pathlib import Path
import argparse, hashlib, json
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from model import arcs, lift23_cover, slots, reconstruction_rows, PLANES

def generate(case, out):
    K=arcs()['L23'];_,cover=lift23_cover(K)
    q,f=cover[case]['representative']
    ss=slots(K,q,f);eligible=sorted({i for s in ss for i in s})
    var={v:i+1 for i,v in enumerate(eligible)}
    pool=IDPool(start_from=len(var)+1);cnf=CNF()
    def card(vs,n,gate=()):
        if n<0 or n>len(vs):cnf.append(list(gate));return
        encoded=CardEnc.equals(lits=vs,bound=n,vpool=pool,encoding=EncType.totalizer)
        for c in encoded.clauses:cnf.append(list(gate)+c)
    for s in ss:card([var[i] for i in s],1)
    for r,allowed in reconstruction_rows(K,q,f):
        vs=[var[i] for i in PLANES[r] if i in var]
        if len(allowed)==1:card(vs,allowed[0])
        else:
            v=pool.id()
            card(vs,allowed[0],(v,))
            card(vs,allowed[1],(-v,))
    out.parent.mkdir(parents=True,exist_ok=True);cnf.to_file(str(out))
    return {'case':case,'q':q,'f':f,'covered_flags':len(cover[case]['flags']),
            'D_variables':len(eligible),'variables':cnf.nv,'clauses':len(cnf.clauses),
            'cnf_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,choices=range(5),required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    print(json.dumps(generate(a.case,a.out),indent=2))
