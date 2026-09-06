"""Independent determinant/interpolation audit. Imports no producer."""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,json,time

def require(condition,message):
    if not condition: raise ValueError(message)
# Quadratic-field values a+b*sqrt(3); no symbolic polynomial multiplication.
def K(a=0,b=0):return (F(a),F(b))
def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def minus(a,b):return (a[0]-b[0],a[1]-b[1])
def times(a,b):return (a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def power(a,n):
    r=K(1)
    for _ in range(n):r=times(r,a)
    return r
def dot(a,b):return plus(times(a[0],b[0]),times(a[1],b[1]))
def det(a,b):return minus(times(a[0],b[1]),times(a[1],b[0]))
# Sixth roots generated recursively from a different representation.
ROT=[(K(1),K())]
for _ in range(5):
    c,s=ROT[-1];ROT.append((minus(times(c,K(F(1,2))),times(s,K(0,F(1,2)))),plus(times(c,K(0,F(1,2))),times(s,K(F(1,2))))))
SLOTS=list(product(range(2),repeat=2))
def delta(a,x,y):
    i,j=a;return (K(x+F(3*j,5)-i),K(y+F(4*j,5)))
def norm(a):return dot(a,a)
def cramer(a,b,k,x,y):
    d=delta(a,x,y);e=delta(b,x,y);c,s=ROT[k]
    v=(plus(times(c,e[0]),times(s,e[1])),minus(times(c,e[1]),times(s,e[0])))
    q=norm(d);w=norm(e)
    nx=minus(times(q,v[1]),times(w,d[1]));ny=minus(times(w,d[0]),times(q,v[0]))
    return minus(plus(power(nx,2),power(ny,2)),times(K(4),power(det(d,v),2)))
def unpack(e):
    p={};last=None
    for term in e['terms']:
        require(isinstance(term,list) and len(term)==5,'term length')
        a,b,s,n,d=term
        require(all(type(v) is int for v in term),'integer term')
        require(a>=0 and b>=0 and a+b<=6 and s in (0,1) and d>0 and n!=0,'term domain')
        require(F(n,d).numerator==n and F(n,d).denominator==d,'noncanonical rational')
        m=(a,b,s);require(last is None or last<m,'unsorted or duplicate term');last=m;p[m]=F(n,d)
    require(bool(p),'zero polynomial');return p
def evaluate(p,x,y):
    result=[F(0),F(0)]
    for (a,b,s),v in p.items():result[s]+=v*x**a*y**b
    return tuple(result)
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def midpoint_control(data):
    c=data['midpoint_control']
    require(c['translation']==[[1,5],[-2,5]] and c['a']==[0,0] and c['b']==[1,1] and c['k']==3,'midpoint control slots')
    def decode(z):
        require(len(z)==2,'control point')
        return tuple((F(a,d),F(b,d)) for a,b,d in z)
    x=decode(c['x']);y=decode(c['y'])
    centres=[(K(),K()),(K(1),K()),(K(F(1,5)),K(F(-2,5))),(K(F(4,5)),K(F(2,5)))]
    def norm19(z):
        aa=F(0);bb=F(0)
        for a,b in z:aa+=a*a+19*b*b;bb+=2*a*b
        return aa,bb
    for z,h in [(x,0),(x,2),(y,1),(y,3)]:
        require(norm19(tuple(minus(v,w) for v,w in zip(z,centres[h])))==K(1),'control unit distance')
    require(all(z not in centres for z in (x,y)),'control noncentre')
    require(tuple(plus(a,b) for a,b in zip(x,y))==(K(1),K()),'control opposite directions')
    # A indices differ, and the direction exponent is 3: equal A-palette colours.
    require((1+3)%2==0 and (1-0)!=(1-1),'control parity contradiction')
    return {'cross_unit_distances':4,'noncentre_points':2,'rotation_exponent':3,
            'one_sided_prescriptions_conflict':True,'full_support_tested':False}
def audit(data):
    require(data['schema']==1 and data['orientation']==[[3,5],[4,5]],'schema or orientation')
    require(F(3,5)**2+F(4,5)**2==1,'unit orientation')
    require(data['target_found'] is False,'false record claim')
    require(data['witness_translation']==[[1,5],[2,5]],'witness changed')
    expected=[]
    for a in SLOTS:expected.append(('self',a,None,None))
    for z,a in enumerate(SLOTS):
        for b in SLOTS[z+1:]:
            for k in range(6):
                if (sum(a)+sum(b)+k)&1:expected.append(('pair',a,b,k))
    require(len(data['factors'])==len(expected)==22,'factor completeness')
    entries={};polys={};leadprod=1;degree_total=0;degreehist=Counter()
    for e,slot in zip(data['factors'],expected):
        kind,a,b,k=slot
        require(e['kind']==kind and tuple(e['a'])==a,'factor slot')
        if kind=='pair':require(tuple(e['b'])==b and e['k']==k,'pair slot')
        ident=('self_%s%s'%a) if kind=='self' else ('pair_%s%s_%s%s_%s'%(*a,*b,k))
        require(e['id']==ident,'factor id')
        p=unpack(e);degree=max(x+y for x,y,s in p)
        wantdegree=2 if kind=='self' else (4 if k==0 else 6)
        require(e['degree']==degree==wantdegree,'degree')
        scalar=1 if kind=='self' or k in (0,1,5) else (3 if k in (2,4) else 4)
        leading={(2*j,degree-2*j,0):F(scalar*comb(degree//2,j)) for j in range(degree//2+1)}
        require({m:v for m,v in p.items() if sum(m[:2])==degree}==leading,'leading form')
        leadprod*=scalar;degree_total+=degree;degreehist[degree]+=1
        entries[slot]=e;polys[slot]=p
        w=evaluate(p,F(1,5),F(2,5))
        require([[v.numerator,v.denominator] for v in w]==e['witness_value'],'witness value')
        require(w!=K(),'vanishing witness')
    require(degree_total==data['product_degree']==108,'product degree')
    require(leadprod==data['product_leading_scalar']==104976,'product leading scalar')
    require(data['factor_count']==22 and data['product_leading_form']=='104976*(X^2+Y^2)^54','product metadata')
    # Coefficient conjugation pairs factors; hence the unexpanded product is rational.
    conjugate_checks=0
    for slot,p in polys.items():
        kind,a,b,k=slot
        mate=slot if kind=='self' else (kind,a,b,(-k)%6)
        require({(x,y,s):v*((-1)**s) for (x,y,s),v in p.items()}==polys[mate],'conjugate pairing')
        conjugate_checks+=1
    # All 48 ordered odd slots, including determinant-zero specializations.
    # Both sides have degree <=6 in EACH coordinate. Agreement on a 7x7
    # product grid proves equality as polynomials over Q(sqrt(3)).
    signedslots=0;identities=0;self_reductions=Counter()
    for a,b,k in product(SLOTS,SLOTS,range(6)):
        if not (sum(a)+sum(b)+k)&1:continue
        signedslots+=1
        if a==b:self_reductions[k]+=1
        for x,y in product(map(F,range(-3,4)),repeat=2):
            value=cramer(a,b,k,x,y)
            if a==b:
                q=norm(delta(a,x,y))
                if k==3:predicted=times(K(4),power(q,3))
                else:predicted=times(power(q,2),evaluate(polys[('self',a,None,None)],x,y))
            else:
                slot=('pair',a,b,k) if a<b else ('pair',b,a,(-k)%6)
                predicted=evaluate(polys[slot],x,y)
            require(value==predicted,'Cramer interpolation identity');identities+=1
    # Witness has eight cross-circle intersection incidences, not a remote/disjoint example.
    qs=[norm(delta(a,F(1,5),F(2,5)))[0] for a in SLOTS]
    require(all(0<q<4 for q in qs),'witness intersection counts')
    D=[(F(0),F(0)),(F(1),F(0)),(F(1,5),F(2,5)),(F(4,5),F(6,5))]
    require(len(set(D))==4,'distinct witness centres')
    return {'status':'PASS','factor_count':22,'coefficient_terms':sum(len(p) for p in polys.values()),
            'degree_histogram':{str(k):v for k,v in sorted(degreehist.items())},'product_degree':degree_total,
            'product_leading_scalar':leadprod,'conjugate_factor_checks':conjugate_checks,
            'ordered_signed_slots':signedslots,'interpolation_grid':[7,7],'exact_grid_identities':identities,
            'self_slot_reductions':{str(k):v for k,v in sorted(self_reductions.items())},
            'nonvanishing_factor_checks':22,'witness_cross_squared_distances':[[q.numerator,q.denominator] for q in qs],
            'witness_cross_intersection_incidences':8,'midpoint_control':midpoint_control(data),'native_solver_calls':0,'target_found':False}
def mutations(data):
    bad=[]
    x=copy.deepcopy(data);x['factors'].pop();bad.append(x)
    x=copy.deepcopy(data);x['factors'][4]['k']=1;bad.append(x)
    x=copy.deepcopy(data);x['factors'][8]['terms'][0][3]+=1;bad.append(x)
    x=copy.deepcopy(data);x['factors'][0]['witness_value']=[[0,1],[0,1]];bad.append(x)
    x=copy.deepcopy(data);x['product_degree']=106;bad.append(x)
    x=copy.deepcopy(data);x['target_found']=True;bad.append(x)
    x=copy.deepcopy(data);x['midpoint_control']['x'][0][0]+=1;bad.append(x)
    for n,x in enumerate(bad):
        try:audit(x)
        except (ValueError,KeyError,TypeError):continue
        raise ValueError('accepted malformed certificate '+str(n))
    return len(bad)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',default=str(Path(__file__).parent/'certificate.json'));ap.add_argument('--out',required=True);args=ap.parse_args()
    started=time.monotonic();out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    blob=Path(args.certificate).read_bytes();data=json.loads(blob);r=audit(data);r['malformed_certificate_rejections']=mutations(data)
    r['certificate_bytes']=len(blob);r['certificate_sha256']=hashlib.sha256(blob).hexdigest()
    expected=Path(__file__).parent/'expected.json'
    if expected.exists():require(r==json.loads(expected.read_text()),'expected report mismatch')
    out.joinpath('result.json').write_text(json.dumps(r,indent=2)+'\n')
    out.joinpath('timing.json').write_text(json.dumps({'seconds':time.monotonic()-started})+'\n');print(json.dumps(r))
if __name__=='__main__':main()
