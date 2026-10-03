"""Construct a small exact covering certificate; no floating selector."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as Q
import argparse,hashlib,json,signal
from polynomials import P,dot
from model import positive_factors
from algebra import LO,HI,require,primitive,row_planes,vertex,cramer,parameter_box
from signs import integer_bernstein
from schema import system,validate

def sample(p,t):return p.evaluate((t,Q(),Q()))
def positive(p,a,b):return min(integer_bernstein(p,a,b))>0

def record(planes,inds,t,known):
    D,W=vertex(planes,inds,t)
    if not D.c:return {'triple':list(inds),'type':'S'}
    norm=primitive(49*D*D-50*dot(W,W,t),known)
    H={i:primitive(sum((a*b for a,b in zip(row,W)),t*0)-rhs*D,known) for i,(row,rhs) in planes.items() if i not in inds}
    H={i:p for i,p in H.items() if p.c};leaves=[];stack=[()]
    while stack:
        path=stack.pop();a,b=parameter_box(path);mid=(a+b)/2
        if sample(norm,mid)>0 and positive(norm,a,b):leaves.append({'path':list(path),'type':'N'});continue
        values={i:sample(p,mid) for i,p in H.items()};ordered=sorted(H,key=lambda i:values[i])
        negative=[i for i in ordered if values[i]<0];pos=[i for i in reversed(ordered) if values[i]>0];done=False
        for j in pos[:3]:
            if not positive(H[j],a,b):continue
            for k in negative[:3]:
                if positive(-H[k],a,b):
                    leaves.append({'path':list(path),'type':'I2','positive_residual':j,'negative_residual':k});done=True;break
            if done:break
        if done:continue
        require(len(path)<9,'INCOMPLETE triple sign cover; no certificate emitted')
        stack.extend((path+(1,),path+(0,)))
    return {'triple':list(inds),'type':'COVER','leaves':leaves}

def generate():
    t=P.var(0);known=positive_factors(t);planes,Y,O=row_planes(t)
    labels=(0,4,9,11);M=[[Y[labels[j]][i] for j in range(3)] for i in range(3)]
    D,C=cramer(M,[-x for x in Y[11]],t);value=sample(D,(LO+HI)/2);require(value!=0,'boundedness determinant')
    sign=1 if value>0 else -1
    require(all(positive(primitive(sign*p,known),LO,HI) for p in [D]+C),'strict positive dependence throughout CLOSED band')
    records=[record(planes,inds,t,known) for inds in combinations(sorted(planes),3)]
    out={'system':system(),'boundedness_determinant_sign':sign,'records':records};validate(out);return out

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second generation guard')));signal.alarm(50)
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    c=generate();raw=json.dumps(c,sort_keys=True,separators=(',',':'))+'\n';args.output.write_text(raw)
    print(json.dumps({'status':'complete exact certificate','triple_count':len(c['records']),'bytes':len(raw.encode()),'sha256':hashlib.sha256(raw.encode()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
