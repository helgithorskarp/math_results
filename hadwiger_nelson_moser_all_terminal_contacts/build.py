"""Exact finite geometry behind the all-contact Moser terminal theorem."""
import argparse,hashlib,importlib.util,json,time
from itertools import combinations
from pathlib import Path
HERE=Path(__file__).resolve().parent
FIELD=HERE.parent/'hadwiger_nelson_long_terminal_gluing/verify.py'
FIELD_SHA='61c91721d8764a743fa0ffc8a5a3b08e39402d09ea36857125f4353c3c38a7db'

def need(b,msg):
    if not b:raise ValueError(msg)

def arithmetic():
    need(hashlib.sha256(FIELD.read_bytes()).hexdigest()==FIELD_SHA,'field input changed')
    spec=importlib.util.spec_from_file_location('prior_exact_tower',FIELD);f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
    return f

def generate():
    f=arithmetic();z=(0,0,0,0)
    M=[(z,z),((12,0,0,0),z),((6,0,0,0),(0,6,0,0)),((18,0,0,0),(0,6,0,0)),
       ((10,0,0,0),(0,0,2,0)),((5,0,0,-1),(0,5,1,0)),((15,0,0,-1),(0,5,3,0))]
    unit=lambda a,b:f.distance(a,b)==(144,0,0,0)
    C=set();circles=[]
    for i,j in combinations(range(7),2):
        common=[r for r in range(7) if unit(M[i],M[r]) and unit(M[j],M[r])]
        if common:
            r=common[0];p=M[r];q=tuple(f.minus(f.plus(M[i][c],M[j][c]),p[c]) for c in (0,1))
        else:
            need(unit(M[i],M[j]),'unsupported pair')
            x,y=(f.minus(M[j][c],M[i][c]) for c in (0,1));sx=f.times((0,1,0,0),x);sy=f.times((0,1,0,0),y)
            roots=[]
            for sign in (-1,1):
                xx=f.minus(x,tuple(sign*v for v in sy));yy=f.plus(y,tuple(sign*v for v in sx))
                need(all(v%2==0 for v in xx+yy),'nonintegral numerator')
                roots.append((f.plus(M[i][0],tuple(v//2 for v in xx)),f.plus(M[i][1],tuple(v//2 for v in yy))))
            p,q=roots
        need(p!=q and all(unit(t,M[i]) and unit(t,M[j]) for t in (p,q)),'invalid circle witnesses')
        C.update((p,q));circles.append((i,j,p,q))
    C=sorted(C);D=sorted(set(C)-set(M));ci={p:i for i,p in enumerate(C)}
    near=[[i for i,m in enumerate(M) if unit(p,m)] for p in D]
    E=[list(e) for e in combinations(range(18),2) if unit(D[e[0]],D[e[1]])]
    long=[list(e) for e in combinations(range(18),2) if f.distance(D[e[0]],D[e[1]])==(1008,0,0,0)]
    three=[list(e) for e in combinations(range(18),2) if f.distance(D[e[0]],D[e[1]])==(1296,0,0,0)]
    colours=[0,1,2,3,1,3,2];lists=[sorted(set(range(4))-{colours[i] for i in ns}) for ns in near]
    cert={'scale':12,'basis':['1','sqrt3','sqrt11','sqrt33'],'M':M,'C':C,
        'circle_pairs':[[i,j,ci[p],ci[q]] for i,j,p,q in circles],
        'D_indices':[ci[p] for p in D],'D_neighbours':near,'D_unit_edges':E,
        'D_sqrt7_pairs':long,'D_distance3_pairs':three,'M_colours':colours,'D_lists':lists}
    return cert

def encoded(x):return (json.dumps(x,separators=(',',':'),sort_keys=True)+'\n').encode()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--discover',action='store_true');a=p.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);start=time.monotonic();raw=encoded(generate())
    if not a.discover:need(raw==(HERE/'certificate.json').read_bytes(),'certificate mismatch')
    (out/'certificate.json').write_bytes(raw)
    result={'status':'PASS','certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'native_solver_calls':0,'seconds':time.monotonic()-start}
    (out/'build.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
