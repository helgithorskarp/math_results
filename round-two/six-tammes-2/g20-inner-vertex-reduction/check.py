"""Primary whole-coefficient identity/Bernstein/reduction replay."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import json,hashlib,signal,argparse
from exact import derive,obligations,require
from coverage import census,elementary,validate
from branches import certificate as circuits
HERE=Path(__file__).resolve().parent

def bernstein(p,box):
    # Credited tensor conversion from the author's10088 signs.py; exact fractions.
    require(not any(k[2] for k in p.c),'bivariate strict-sign polynomial')
    a,b,c,d=box;n=max(k[0] for k in p.c);m=max(k[1] for k in p.c)
    first=[[Q(0) for _ in range(m+1)] for _ in range(n+1)]
    for (i,j,_),v in p.c.items():
        for r in range(i+1):first[r][j]+=v*comb(i,r)*a**(i-r)*(b-a)**r
    power=[[Q(0) for _ in range(m+1)] for _ in range(n+1)]
    for i in range(n+1):
        for j in range(m+1):
            for s in range(j+1):power[i][s]+=first[i][j]*comb(j,s)*c**(j-s)*(d-c)**s
    along_t=[[sum((power[r][j]*Q(comb(i,r),comb(n,r)) for r in range(i+1)),Q(0)) for j in range(m+1)] for i in range(n+1)]
    return [[sum((along_t[i][s]*Q(comb(j,s),comb(m,s)) for s in range(j+1)),Q(0)) for j in range(m+1)] for i in range(n+1)]

def produce(s,factors):
    tt,zz=validate(s);f,ids=derive(factors,s);counts=census(s);elem=elementary(s);signs=[]
    for name,p,sign in obligations(f):
        co=bernstein(p,(*tt,*zz));vals=[v for row in co for v in row]
        require(all(sign*v>0 for v in vals),'non-strict closed-box sign: '+name)
        stream=(json.dumps([[str(v) for v in row] for row in co],separators=(',',':'))+'\n').encode()
        signs.append({'name':name,'sign':sign,'coefficient_count':len(vals),'coefficient_min':str(min(vals)),'coefficient_max':str(max(vals)),'whole_array_sha256':hashlib.sha256(stream).hexdigest()})
    require(len(signs)==17 and signs[-1]['coefficient_count']==75,'all16 structural signs plus critical75')
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'COMPLETE_NECESSARY_INNER_260_VERTEX_REDUCTION','whole_identities':ids,'coverage':counts,'elementary_closed_bounds':elem,'whole_box_signs':signs,'all_Bernstein_coefficients_checked':sum(r['coefficient_count'] for r in signs),'branch_circuits':circuits(s['residual_triples']),'residual_feasibility':'UNRESOLVED','conditional_capacity_proved':False,'new_global_bound':False,'independent_review':'pending','ordinary_geometric_bridge_formalized':False}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('20s fixed primary guard')));signal.alarm(20)
    parser=argparse.ArgumentParser();parser.add_argument('--emit');args=parser.parse_args()
    s=json.loads((HERE/'SYSTEM.json').read_text());f=json.loads((HERE/'FACTORS.json').read_text());out=produce(s,f)
    if args.emit:Path(args.emit).write_text(json.dumps(out,separators=(',',':'))+'\n')
    else:require(out==json.loads((HERE/'CERTIFICATE.json').read_text()),'whole certificate equality')
    print(json.dumps({'status':out['status'],'residual_branches':260,'all_Bernstein_coefficients_checked':out['all_Bernstein_coefficients_checked'],'whole_certificate_sha256':hashlib.sha256((json.dumps(out,separators=(',',':'))+'\n').encode()).hexdigest(),'conditional_capacity_proved':False,'new_global_bound':False},indent=2))
