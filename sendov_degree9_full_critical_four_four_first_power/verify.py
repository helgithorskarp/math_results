"""Complete exact finite checks for the degree-nine critical 4+4 theorem.

Python 3.10+ standard library; one process; no assert-based proof guards.
All tensor entries are regenerated and full polynomial inversions checked.
The analytic interpretation and credited lemmas remain written mathematics.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod,lcm
import hashlib,importlib.util,json,copy

ROOT=Path(__file__).resolve().parent
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/file)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj
A=module('full44_origin_algebra','algebra.py')
B=module('full44_tensor_certificate','certificate.py')
W=module('full44_weighted_algebra','weighted.py')

def require(condition,message):
    if not condition:raise ArithmeticError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def tensor_hash(values,den):
    h=hashlib.sha256()
    for v in values:h.update((str(F(v,den))+'\n').encode())
    return h.hexdigest()

PATHS=[[(2,1)],[(2,0),(3,0)],[(2,0),(3,1),(3,0)]]
EVEN_PATHS=[[(2,0)],[(2,1),(1,0)],[(2,1),(1,1)]]

def decode(path):
    box=[(F(0),F(1))]*4
    for axis,side in path:
        require(axis in [1,2,3] and side in [0,1],'Invalid subdivision')
        low,high=box[axis];mid=(low+high)/2
        box[axis]=(low,mid) if side==0 else (mid,high)
    return box

def coverage(boxes):
    require(all(b[0]==b[1]==(F(0),F(1)) for b in boxes),'Incomplete t/c interval')
    for i,b in enumerate(boxes):
        for other in boxes[:i]:
            require(not all(max(b[k][0],other[k][0])<min(b[k][1],other[k][1]) for k in [2,3]),'Envelope cell interiors overlap')
    xs=sorted({F(0),F(1)}|{a for b in boxes for a in b[2]})
    zs=sorted({F(0),F(1)}|{a for b in boxes for a in b[3]})
    for xl,xh in zip(xs,xs[1:]):
        for zl,zh in zip(zs,zs[1:]):
            x=(xl+xh)/2;z=(zl+zh)/2
            hit=sum(b[2][0]<=x<=b[2][1] and b[3][0]<=z<=b[3][1] for b in boxes)
            require(hit==int(x>=F(1,2) or z<=F(3,4)),'Envelope domain coverage fails')
    require(sum((b[2][1]-b[2][0])*(b[3][1]-b[3][0]) for b in boxes)==F(7,8),'Wrong envelope area')

def certify_even(p):
    target=W.q_unit(p)
    whole,den,deg=B.bernstein(target)
    require(deg==(16,16,16,16) and len(whole)==83521,'Wrong even degree/count')
    require(B.invert(whole,den,deg)==target,'Full even tensor inversion fails')
    boxes=[decode(path) for path in EVEN_PATHS]
    require(sum((b[1][1]-b[1][0])*(b[2][1]-b[2][0]) for b in boxes)==1,'Wrong even coverage area')
    for i,b in enumerate(boxes):
        require(b[0]==b[3]==(F(0),F(1)),'Incomplete even t/Q intervals')
        for other in boxes[:i]:
            require(not all(max(b[k][0],other[k][0])<min(b[k][1],other[k][1]) for k in [1,2]),'Even cell interiors overlap')
    for c in [F(1,4),F(3,4)]:
        for x in [F(1,4),F(3,4)]:
            require(sum(b[1][0]<=c<=b[1][1] and b[2][0]<=x<=b[2][1] for b in boxes)==1,'Even grid coverage fails')
    shape=[d+1 for d in deg];stride=[prod(shape[j+1:]) for j in range(4)];records=[]
    for path,box in zip(EVEN_PATHS,boxes):
        vals,d=whole,den
        for axis,side in path:vals,d=B.split(vals,d,deg,axis)[side]
        direct=target
        for axis,(lo,hi) in enumerate(box):
            if (lo,hi)!=(F(0),F(1)):direct=B.affine_cell(direct,axis,lo,hi)
        require(B.invert(vals,d,deg)==direct,'Complete even cell inversion fails')
        other,dother,degother=B.bernstein(direct,deg)
        require(degother==deg and len(other)==len(vals)==83521,'Incomplete even tensor')
        require(all(v*dother==w*d for v,w in zip(vals,other)),'Even affine/de Casteljau entries differ')
        require(min(vals)>=0,'Negative even cell coefficient')
        zeros={tuple((i//stride[j])%shape[j] for j in range(4)) for i,v in enumerate(vals) if not v}
        corner=box[1][1]==box[2][1]==1
        require(zeros==({(16,16,16,0)} if corner else set()),'Wrong even equality corner')
        zc=[v for i,v in enumerate(vals) if (i//stride[1])%shape[1]==0]
        zx=[v for i,v in enumerate(vals) if (i//stride[2])%shape[2]==0]
        require(min(zc)>0 and min(zx)>0,'Even strictness support fails')
        records.append({'path':[list(z) for z in path],
          'box':[[str(a),str(b)] for a,b in box],'degrees':list(deg),'coefficients':len(vals),
          'minimum':str(F(min(vals),d)),'minimum_positive':str(F(min(v for v in vals if v>0),d)),
          'zeros':len(zeros),'zeroth_c_minimum':str(F(min(zc),d)),
          'zeroth_x_minimum':str(F(min(zx),d)),'sha256':tensor_hash(vals,d)})
    return records

def certify_envelope(p):
    whole,den,deg=B.bernstein(p)
    require(deg==(16,19,19,32) and len(whole)==224400,'Wrong envelope degree/count')
    require(B.invert(whole,den,deg)==p,'Full envelope tensor inversion fails')
    boxes=[decode(path) for path in PATHS];coverage(boxes)
    shape=[d+1 for d in deg];stride=[prod(shape[j+1:]) for j in range(4)]
    records=[]
    for path,box in zip(PATHS,boxes):
        vals,d=whole,den
        for axis,side in path:vals,d=B.split(vals,d,deg,axis)[side]
        direct=p
        for axis,(lo,hi) in enumerate(box):
            if (lo,hi)!=(F(0),F(1)):direct=B.affine_cell(direct,axis,lo,hi)
        require(B.invert(vals,d,deg)==direct,'Full envelope cell inversion fails')
        other,dother,degother=B.bernstein(direct,deg)
        require(degother==deg and len(other)==len(vals)==224400,'Incomplete envelope cell tensor')
        require(all(v*dother==w*d for v,w in zip(vals,other)),'Affine and de Casteljau entries differ')
        require(min(vals)>=0,'Negative envelope cell coefficient')
        zc=[v for i,v in enumerate(vals) if (i//stride[1])%shape[1]==0]
        zx=[v for i,v in enumerate(vals) if (i//stride[2])%shape[2]==0]
        require(min(zc)>0 and min(zx)>0,'Strictness on zeroth phase indices fails')
        zeros=[tuple((i//stride[j])%shape[j] for j in range(4)) for i,v in enumerate(vals) if not v]
        if box[2][1]<1:require(not zeros,'Unexpected low-x zero coefficient')
        else:require(len(zeros)==3374 and all(e[1]>=16 and e[2]>=16 for e in zeros),'Corner zero support differs')
        records.append({'path':[list(z) for z in path],
          'box':[[str(a),str(b)] for a,b in box],'degrees':list(deg),'coefficients':len(vals),
          'minimum':str(F(min(vals),d)),'minimum_positive':str(F(min(v for v in vals if v>0),d)),
          'zeros':len(zeros),'zero_indices_sha256':digest(zeros),
          'zeroth_c_minimum':str(F(min(zc),d)),'zeroth_x_minimum':str(F(min(zx),d)),
          'sha256':tensor_hash(vals,d)})
    return records

def gadd(z,w):return z[0]+w[0],z[1]+w[1]
def gscale(z,k):return z[0]*k,z[1]*k
def gmul(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def gnorm(z):return z[0]*z[0]+z[1]*z[1]

def direct_integral(b,u,v):
    coeff=[(F(1),F(0))]
    for z in [u]*4+[v]*4:
        out=[(F(0),F(0))]*(len(coeff)+1)
        for i,k in enumerate(coeff):
            out[i]=gadd(out[i],k)
            out[i+1]=gadd(out[i+1],gscale(gmul(k,z),-b))
        coeff=out
    value=(F(0),F(0))
    for i,k in enumerate(coeff):value=gadd(value,gscale(k,F(9,i+1)))
    return value

def exact_evaluator(p,nvars):
    """Evaluate with a shared integer denominator; no per-term rounding."""
    degrees=[max(e[j] for e in p) for j in range(nvars)]
    denominator=lcm(*(k.denominator for k in p.values()))
    terms=[(e,k.numerator*(denominator//k.denominator)) for e,k in p.items()]
    def value(values):
        require(len(values)==nvars,'Wrong exact-evaluation variable count')
        powers=[[v.numerator**i*v.denominator**(n-i) for i in range(n+1)]
                for v,n in zip(values,degrees)]
        total=0
        for e,k in terms:
            for j in range(nvars):k*=powers[j][e[j]]
            total+=k
        return F(total,denominator*prod(v.denominator**n for v,n in zip(values,degrees)))
    return value

def gaussian_controls(even,odd,delta,skew):
    de=exact_evaluator(delta,5);ds=exact_evaluator(skew,5)
    ep=exact_evaluator(even,4);et=exact_evaluator(odd,4)
    phase_pairs=[(F(3,5),F(4,5),F(5,13),F(12,13)),
                 (F(399,401),F(40,401),F(99,101),F(20,101)),
                 (F(1),F(0),F(3,5),F(4,5)),
                 (F(0),F(1),F(0),F(1)),
                 (F(1),F(0),F(1),F(0)),
                 (F(5,13),F(12,13),F(3,5),F(4,5))]
    rows=[]
    for c,d,x,y0 in phase_pairs:
        require(c*c+d*d==x*x+y0*y0==1,'Nonunit Gaussian control')
        for sign in [-1,1]:
            y=sign*y0
            for eta in [F(0),F(1,8),F(3,8),F(1,2)]:
                u=gscale(gmul((x,y),(c,d)),1+eta)
                v=gscale(gmul((x,y),(c,-d)),1-eta)
                lam=-eta*d*y;q=eta*eta;mu=c*x+lam
                for t in [F(0),F(1,3),F(1)]:
                    b=t*mu;R=(1-q)**8
                    direct=gnorm(direct_integral(b,u,v))-R
                    old=de([b,F(1),c,x,q])+lam*ds([b,F(1),c,x,q])
                    new=ep([t,c,x,q])+lam*et([t,c,x,q])
                    if len(rows) in {5,17,23,53,71,95,119,143}:
                        reference=W.evaluate(even,[t,c,x,q])+lam*W.evaluate(odd,[t,c,x,q])
                        require(reference==new,'Shared-denominator and Fraction reference evaluation differ')
                    require(direct==old==new,'Signed weighted Gaussian norm reconstruction fails')
                    eligible=lam>=0 and (x>=F(1,2) or eta<=F(3,8))
                    if eligible:
                        require(direct>=0,'Direct eligible control violates the minimum')
                        require((direct==0)==(b==c==x==1 and eta==0),'Eligible equality control fails')
                    rows.append([str(z) for z in [t,c,d,x,y,eta,b,lam,direct]])
    require(len(rows)==144,'Wrong Gaussian-control count')
    return {'count':len(rows),'sha256':digest(rows)}

def polynomial_control():
    # Explicit nonreal disk-root polynomial outside the old covariance sector.
    a=F(3,4);z1=(F(0),F(1,20));z2=(F(1,40),F(1,40))
    coeff=[(F(1),F(0))]
    for z in [z1]*4+[z2]*4:
        out=[(F(0),F(0))]*(len(coeff)+1)
        for i,k in enumerate(coeff):
            out[i]=gadd(out[i],gscale(gmul(k,z),-1));out[i+1]=gadd(out[i+1],k)
        coeff=out
    primitive=[(F(0),F(0))]+[gscale(k,F(9,i+1)) for i,k in enumerate(coeff)]
    value=(F(0),F(0))
    for i,k in enumerate(primitive):value=gadd(value,gscale(k,a**i))
    primitive[0]=gscale(value,-1)
    check=(F(0),F(0))
    for i,k in enumerate(primitive):check=gadd(check,gscale(k,a**i))
    require(check==(F(0),F(0)) and primitive[-1]==(F(1),F(0)),'Primitive/root control fails')
    require([gscale(k,i) for i,k in enumerate(primitive) if i]==[gscale(k,9) for k in coeff],'Derivative control fails')
    bound=sum(abs(k[0])+abs(k[1]) for k in primitive[:-1])
    require(bound<1,'Explicit polynomial Rouche bound fails')
    w1=(a-z1[0],-z1[1]);w2=(a-z2[0],-z2[1]);d1=gnorm(w1);d2=gnorm(w2)
    require(d2<d1<1,'Explicit reciprocal-radius ordering fails')
    require(w2[0]**2/d2>w1[0]**2/d1 and w1[0]>0 and w2[0]>0,'Positive radius/direction covariance fails')
    return {'marked_root':str(a),'critical_points':[[str(z) for z in z1],[str(z) for z in z2]],
            'rouche_l1_bound':str(bound),'coefficient_sha256':digest([[str(z) for z in k] for k in primitive]),
            'positive_radius_direction_covariance':True}

def build():
    delta,skew,ip,iq=A.norm_polynomials()
    altp,altq=A.alternate_integral_coefficients()
    require((ip,iq)==(altp,altq),'Integral coefficient constructions differ')
    norm,altj=A.alternate_norm(altp,altq)
    r=A.add(A.power(A.variable(1),2),A.scale(A.variable(4),-1))
    require(A.add(norm,A.scale(A.power(r,8),-1))==delta and altj==skew,'Norm constructions differ')
    even,odd=W.binomial_reduce(delta,skew)
    require((even,odd)==W.horner_reduce(delta,skew),'Binomial and quadratic-extension Horner reductions differ')
    require((len(even),len(odd))==(7415,5474),'Unexpected weighted kernel inventory')
    H=W.envelope(even,odd)
    require(len(H)==35890,'Unexpected Newton envelope inventory')
    even_cells=certify_even(even);cells=certify_envelope(H)
    controls=gaussian_controls(even,odd,delta,skew)
    f=lambda eta:-1+2*eta+6*eta**3-3*eta**4
    require(f(F(3,8))==F(29,4096),'Physical imbalance separation constant fails')
    return {'agent':'six-sendov-1','role':'researcher',
            'proof_status':'ordinary author mathematics and exact finite evidence; unformalized; independent review pending',
            'weighted_terms':{'even':len(even),'skew':len(odd),'envelope':len(H)},
            'weighted_sha256':digest([W.canonical(even),W.canonical(odd)]),
            'envelope_sha256':digest(W.canonical(H)),
            'even_cells':even_cells,'envelope_cells':cells,
            'certified_coefficients':sum(c['coefficients'] for c in even_cells+cells),
            'gaussian_controls':controls,'physical_separation':'29/4096',
            'polynomial_control':polynomial_control()}

def accept(actual,expected):require(actual==expected,'Compact expected manifest mismatch')

def rejection_controls(actual):
    rejected=0
    for change in range(7):
        bad=copy.deepcopy(actual)
        if change==0:bad['weighted_terms']['even']+=1
        elif change==1:bad['even_cells'][0]['minimum']='-1'
        elif change==2:bad['envelope_cells'][0]['zeroth_c_minimum']='0'
        elif change==3:bad['envelope_cells'][1]['path'][0][1]=1
        elif change==4:bad['gaussian_controls']['sha256']='0'*64
        elif change==5:bad['physical_separation']='-29/4096'
        else:bad['polynomial_control']['positive_radius_direction_covariance']=False
        try:accept(actual,bad)
        except ArithmeticError:rejected+=1
        else:raise ArithmeticError('Malformed fixture was accepted')
    return rejected

def main():
    actual=build();expected=json.loads((ROOT/'expected.json').read_text())
    accept(actual,expected);n=rejection_controls(actual)
    print(json.dumps({'result':'PASS','certified_coefficients':actual['certified_coefficients'],
      'envelope_cells':len(actual['envelope_cells']),'gaussian_controls':actual['gaussian_controls']['count'],
      'weighted_sha256':actual['weighted_sha256'],'envelope_sha256':actual['envelope_sha256'],
      'all_envelope_entries_compared':True,'all_cells_inverted':True,
      'physical_imbalance_constant_checked':True,'explicit_polynomial_control_checked':True,
      'rejected_corruptions':n},sort_keys=True))

if __name__=='__main__':main()
