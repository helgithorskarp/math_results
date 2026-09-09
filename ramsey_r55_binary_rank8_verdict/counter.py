"""Exact prefix-threshold encoding, checked at the local Boolean identity."""
import json
from pathlib import Path
from itertools import product

def require(ok,msg):
    if not ok:raise ValueError(msg)

def encode(n,k):
    ids={};next_id=n;clauses=[]
    def state(i,j):
        if j==0:return True
        if j>i:return False
        return ids[i,j]
    def emit(*values):
        if any(v is True for v in values):return
        clauses.append([v for v in values if v is not False])
    def neg(v):return not v if isinstance(v,bool) else -v
    for i in range(1,n+1):
        for j in range(1,min(i,k)+1):
            next_id+=1;ids[i,j]=s=next_id
            a,b,x=state(i-1,j),state(i-1,j-1),i
            emit(neg(a),s);emit(-x,neg(b),s)
            emit(-s,a,x);emit(-s,a,b)
    emit(state(n,k))
    return next_id,clauses,ids

def controls():
    for a,b,x,s in product([False,True],repeat=4):
        cnf=((not a)or s)and((not x)or(not b)or s)and((not s)or a or x)and((not s)or a or b)
        require(cnf==(s==(a or(x and b))),'local threshold identity')
    cases=0
    for n in range(1,9):
        for k in range(1,n+1):
            nv,clauses,ids=encode(n,k)
            for bits in product([0,1],repeat=n):
                values={i+1:bool(b) for i,b in enumerate(bits)}
                values.update({v:sum(bits[:i])>=j for (i,j),v in ids.items()})
                sat=all(any(values[abs(v)]==(v>0) for v in c) for c in clauses)
                require(sat==(sum(bits)>=k),'threshold cardinality boundary');cases+=1
    return {'local_boolean_states':16,'prefix_assignments':cases}

if __name__=='__main__':
    import sys
    out=Path(sys.argv[1]);nv,clauses,_=encode(255,43)
    out.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    print(json.dumps({'variables':nv,'clauses':len(clauses),'controls':controls()}))
