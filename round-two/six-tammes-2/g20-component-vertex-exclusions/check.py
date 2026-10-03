"""Primary complete identities and six exact whole-box Bernstein signs."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import argparse,hashlib,json,signal
from exact import identities,parts
from scope import validate,require
HERE=Path(__file__).resolve().parent
def bernstein(p,box):
    require(not any(k[2] for k in p.c),'bivariate sign obligation')
    a,b,c,d=box;n=max(k[0] for k in p.c);m=max(k[1] for k in p.c)
    first=[[Q(0) for _ in range(m+1)] for _ in range(n+1)]
    for (i,j,_),v in p.c.items():
        for r in range(i+1):first[r][j]+=v*comb(i,r)*a**(i-r)*(b-a)**r
    power=[[Q(0) for _ in range(m+1)] for _ in range(n+1)]
    for i in range(n+1):
        for j in range(m+1):
            for k in range(j+1):power[i][k]+=first[i][j]*comb(j,k)*c**(j-k)*(d-c)**k
    along_t=[[sum((power[r][j]*Q(comb(i,r),comb(n,r)) for r in range(i+1)),Q(0)) for j in range(m+1)] for i in range(n+1)]
    return [[sum((along_t[i][k]*Q(comb(j,k),comb(m,k)) for k in range(j+1)),Q(0)) for j in range(m+1)] for i in range(n+1)]
def produce(s,document,parent_bytes):
    coverage=validate(s,parent_bytes);f,ids=identities(s,document);box=tuple(map(Q,s['t_interval']+s['z_interval']));signs=[]
    for name,part in s['strict_sign_obligations']:
        A,B=parts(f[name]);p=B if part=='B' else A
        co=bernstein(p,box);vals=[v for row in co for v in row]
        require(all(v>0 for v in vals),'strict closed-box coefficient: '+name+'-'+part)
        stream=(json.dumps([[str(v) for v in row] for row in co],separators=(',',':'))+'\n').encode()
        signs.append({'name':name+'-'+part,'strict_positive':True,'complete_coefficients':len(vals),'lower':str(min(vals)),'upper':str(max(vals)),'whole_coefficient_array_sha256':hashlib.sha256(stream).hexdigest()})
    require(len(signs)==6 and sum(r['complete_coefficients'] for r in signs)==458,'all six complete signs')
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'COMPLETE_FIVE_COMPONENT_EXCLUSIONS_NECESSARY255',
            'coverage':coverage,'whole_identity_checks':ids,'whole_closed_box_Bernstein_signs':signs,'complete_strict_coefficients':458,
            'remaining_feasibility':'UNRESOLVED','capacity_claimed':False,'global_bound_claimed':False,'independent_review':'pending','ordinary_imports_and_bridge_formalized':False}
if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('fixed20s primary guard')));signal.alarm(20)
    parser=argparse.ArgumentParser();parser.add_argument('--emit');args=parser.parse_args()
    out=produce(json.loads((HERE/'SYSTEM.json').read_text()),json.loads((HERE/'FACTORS.json').read_text()),(HERE/'PARENT_SYSTEM.json').read_bytes())
    data=(json.dumps(out,separators=(',',':'))+'\n').encode()
    if args.emit:Path(args.emit).write_bytes(data)
    else:require(out==json.loads((HERE/'CERTIFICATE.json').read_text()),'entire primary expected artifact')
    print(json.dumps({'status':out['status'],'remaining':255,'strict_coefficients':458,'whole_certificate_sha256':hashlib.sha256(data).hexdigest(),'capacity_claimed':False},indent=2))
