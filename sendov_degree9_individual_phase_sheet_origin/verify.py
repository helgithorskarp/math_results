"""Check both individual phase-sheet origin minima by complete exact tensors.

Python 3.10+ standard library, one process, including under -I/-O.
All proof checks use exceptions; expected.json is required and read-only.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import comb,prod
import hashlib,importlib.util,json,sys

ROOT=Path(__file__).resolve().parent
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/file)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj
A=module('individual_phase_algebra','algebra.py')
B=module('individual_phase_certificate','certificate.py')

def require(condition,message):
    if not condition:raise ArithmeticError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def tensor_hash(values,den):
    h=hashlib.sha256()
    for v in values:h.update((str(F(v,den))+'\n').encode())
    return h.hexdigest()

def unit(p):
    out=defaultdict(F)
    for e,v in p.items():
        f=list(e);f[1]=0;out[tuple(f)]+=v
    return {e:v for e,v in out.items() if v}

def transform_eta(p,odd=False):
    # Coordinates t,c,x,z, with b=t*c*x and eta=z/2, Q=eta^2.
    out=defaultdict(F)
    for e,v in p.items():
        out[(e[0],e[0]+e[2],e[0]+e[3],2*e[4]+int(odd))]+=v*F(1,4)**e[4]*(F(1,2) if odd else 1)
    return {e:v for e,v in out.items() if v}

def add4(*items):
    out=defaultdict(F)
    for p in items:
        for e,v in p.items():out[e]+=v
    return {e:v for e,v in out.items() if v}

def gauss_add(z,w):return (z[0]+w[0],z[1]+w[1])
def gauss_mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def gauss_scale(z,k):return (z[0]*k,z[1]*k)
def norm(z):return z[0]*z[0]+z[1]*z[1]

def direct_integral(b,U,V):
    # Eight linear convolutions, distinct from symbolic pair expansion.
    coefficients=[(F(1),F(0))]
    for z in [U]*4+[V]*4:
        out=[(F(0),F(0))]*(len(coefficients)+1)
        for j,v in enumerate(coefficients):
            out[j]=gauss_add(out[j],v)
            out[j+1]=gauss_add(out[j+1],gauss_scale(gauss_mul(v,z),-b))
        coefficients=out
    value=(F(0),F(0))
    for j,v in enumerate(coefficients):value=gauss_add(value,gauss_scale(v,F(9,j+1)))
    return value

def phases(c,d,x,y,eta):
    w=(x,y);u=gauss_mul(w,(c,d));v=gauss_mul(w,(c,-d))
    return gauss_scale(u,1+eta),gauss_scale(v,1-eta)

PLUS_PATHS=[[[2,0]],[[2,1]]]
MINUS_PATHS=[[[2,0]],[[2,1],[1,0]],[[2,1],[1,1],[2,0]],[[2,1],[1,1],[2,1]]]

def decode(path):
    box=[(F(0),F(1))]*4
    for axis,side in path:
        require(axis in [1,2] and side in [0,1],'Invalid subdivision path')
        low,high=box[axis];mid=(low+high)/2
        box[axis]=(low,mid) if side==0 else (mid,high)
    return box

def certify(name,target,paths):
    degrees=(16,17,17,16)
    whole,den,degree=B.bernstein(target)
    require(degree==degrees,'Unexpected envelope degree inventory')
    require(B.invert(whole,den,degrees)==target,'Full-box tensor inversion fails')
    boxes=[decode(p) for p in paths]
    require(sum((r[1]-r[0])*(s[1]-s[0]) for _,r,s,_ in boxes)==1,'Cell coverage area fails')
    for i,box in enumerate(boxes):
        require(box[0]==box[3]==(F(0),F(1)),'Incomplete t or eta axis')
        for other in boxes[:i]:
            require(not all(max(box[k][0],other[k][0])<min(box[k][1],other[k][1]) for k in [1,2]),'Cell interiors overlap')
    shape=[d+1 for d in degrees];stride=[prod(shape[j+1:]) for j in range(4)]
    corner_zeros={(i,17,17,j) for i in range(17) for j in range(17)}
    corner_zeros.update((16,c,x,j) for c,x in [(16,17),(17,16)] for j in [0,1])
    records=[]
    for path,box in zip(paths,boxes):
        values,d=whole,den
        for axis,side in path:values,d=B.split(values,d,degrees,axis)[side]
        direct=target
        for axis,(low,high) in enumerate(box):direct=B.affine_cell(direct,axis,low,high)
        require(B.invert(values,d,degrees)==direct,'Complete cell inversion fails')
        other,dother,degreeother=B.bernstein(direct,degrees)
        require(degreeother==degrees and len(values)==len(other)==93636,'Incomplete cell tensor')
        require(all(v*dother==w*d for v,w in zip(values,other)),'Direct and de Casteljau entries disagree')
        require(min(values)>=0,'Negative complete envelope coefficient')
        zeros={tuple((i//stride[j])%shape[j] for j in range(4)) for i,v in enumerate(values) if v==0}
        corner=box[1][1]==box[2][1]==1
        require(zeros==(corner_zeros if corner else set()),'Strict-boundary zero pattern fails')
        # In a corner cell every c-index=0 and every x-index=0 coefficient
        # is positive. These carry positive basis weight if c<1 or x<1.
        require(all(e[1]!=0 and e[2]!=0 for e in zeros),'Strictness face check fails')
        records.append({'box':[[str(l),str(r)] for l,r in box],'path':path,'degrees':list(degrees),
                        'coefficients':len(values),'minimum':str(F(min(values),d)),
                        'minimum_positive':str(F(min(v for v in values if v>0),d)),
                        'zero_count':len(zeros),'zero_pattern':'upper c=x corner plus four first-neighbor entries' if corner else 'none',
                        'sha256':tensor_hash(values,d)})
    return {'name':name,'power_terms':len(target),'power_sha256':digest(sorted([[list(e),str(v)] for e,v in target.items()])),
            'cells':records,'complete_cell_entry_comparisons':sum(r['coefficients'] for r in records),
            'complete_cell_inversions':len(records),'full_box_inversions':1}

def corner_certificate(D):
    # At c=x=1 the signed term is zero; only b=t,Q=q/4 remain.
    p=defaultdict(F)
    for e,v in D.items():p[(e[0],0,0,e[4])]+=v*F(1,4)**e[4]
    p={e:v for e,v in p.items() if v}
    values,den,deg=B.bernstein(p)
    require(deg==(16,0,0,8) and len(values)==153,'Corner inventory fails')
    require(min(values)==0 and [i for i,v in enumerate(values) if v==0]==[144],'Corner strictness pattern fails')
    require(all(v>=0 for v in values),'Corner positivity fails')
    require(B.invert(values,den,deg)==p,'Corner inversion fails')
    return {'power_terms':len(p),'degrees':list(deg),'coefficients':len(values),
            'minimum':'0','minimum_positive':str(F(min(v for v in values if v>0),den)),
            'zero_index':[16,0,0,0],'sha256':tensor_hash(values,den)}

def mean_certificate():
    # Reconstruct the already credited weak polar mean, not a new result.
    def add(*ps):
        r=defaultdict(F)
        for p in ps:
            for k,v in p.items():r[k]+=v
        return {k:v for k,v in r.items() if v}
    def scale(p,k):return {e:k*v for e,v in p.items() if k*v}
    def mul(p,q):
        r=defaultdict(F)
        for i,v in p.items():
            for j,w in q.items():r[i+j]+=v*w
        return {k:v for k,v in r.items() if v}
    def power(p,n):
        r={0:F(1)}
        for _ in range(n):r=mul(r,p)
        return r
    a={1:F(1)};one={0:F(1)};D=add(one,scale(mul(a,a),-1));ap=power(add(one,a),2)
    pair=[mul(mul(a,a),ap),scale(mul(mul(mul(a,a),D),ap),2),
          mul(mul(D,D),add(ap,mul(a,a)))]
    coeff=[one]
    for _ in range(4):
        out=[{} for _ in range(len(coeff)+2)]
        for j,p in enumerate(coeff):
            for k,q in enumerate(pair):out[j+k]=add(out[j+k],mul(p,q))
        coeff=out
    numerator=add(power(add(one,a),8),scale(add(*(scale(p,F(1,k+1)) for k,p in enumerate(coeff))),-1))
    remainder=dict(numerator);quotient={};divisor={0:F(1),1:F(-2),2:F(1)}
    while remainder and max(remainder)>=2:
        n=max(remainder);v=remainder[n];term={n-2:v};quotient=add(quotient,term)
        remainder=add(remainder,scale(mul(divisor,term),-1))
    require(not remainder and mul(divisor,quotient)==numerator,'Weak-mean clearing identity fails')
    require(max(quotient)==22,'Weak-mean quotient degree fails')
    values=[sum(v*F(comb(i,k),comb(22,k)) for k,v in quotient.items() if k<=i) for i in range(23)]
    require(min(values)==F(8,9),'Credited weak-mean positivity fails')
    return {'degree':22,'coefficients':[str(v) for v in values],'minimum':'8/9',
            'quotient_sha256':digest([[k,str(v)] for k,v in sorted(quotient.items())]),
            'status':'credited weak polar mean, independently regenerated by author code'}

def derive():
    old,J,Ps,Qs=A.norm_polynomials();P2,Q2=A.alternate_integral_coefficients()
    require(Ps==P2 and Qs==Q2,'Complete integrated coefficients disagree')
    R=A.add(A.power(A.variable(1),2),A.scale(A.variable(4),-1))
    E=A.add(old,A.power(R,8));E2,J2=A.alternate_norm(P2,Q2)
    require(E==E2 and J==J2,'Two complete norm constructions disagree')
    E,J=unit(E),unit(J)
    require(len(E)==551 and len(J)==295,'Unexpected signed norm inventory')
    c,x,q=A.variable(2),A.variable(3),A.variable(4)
    R8=A.power(A.add(A.ONE,A.scale(q,-1)),8);D=A.add(E,A.scale(R8,-1))
    s=A.add(A.ONE,A.scale(A.mul(c,x),-1))
    g=A.mul(A.add(A.ONE,A.scale(A.mul(c,c),-1)),A.add(A.ONE,A.scale(A.mul(x,x),-1)))
    delta=A.add(c,A.scale(x,-1))
    require(A.add(A.mul(s,s),A.scale(g,-1))==A.mul(delta,delta),'Exact circle geometry identity fails')
    even=transform_eta(A.scale(A.mul(s,D),2))
    odd=transform_eta(A.mul(A.add(A.mul(s,s),g),J),True)
    targets=[add4(even,odd),add4(even,{e:-v for e,v in odd.items()})]
    require(add4(*targets)=={e:2*v for e,v in even.items()},'Both cleared margins do not recover the even part')
    tests=[certify('Hplus',targets[0],PLUS_PATHS),certify('Hminus',targets[1],MINUS_PATHS)]
    controls=[]
    for k in range(24):
        if k<20:
            c0,d0=[(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(1),F(0)),(F(399,401),F(40,401))][k%4]
            x0,y0=[(F(4,5),F(3,5)),(F(20,29),F(21,29)),(F(99,101),F(20,101))][k%3]
            b=F(k%6+1,7);eta=[F(0),F(1,5),F(1,2)][k%3]
        else:
            c0=x0=F(1);d0=y0=F(0)
            b,eta=[(F(1),F(0)),(F(1),F(1,2)),(F(1,2),F(0)),(F(1,2),F(1,2))][k-20]
        ep=A.evaluate(E,[b,F(1),c0,x0,eta*eta]);jp=A.evaluate(J,[b,F(1),c0,x0,eta*eta]);norms=[]
        for sign in [-1,1]:
            U,V=phases(c0,d0,x0,y0,sign*eta)
            actual=norm(direct_integral(b,U,V));lam=-sign*eta*d0*y0
            require(actual==ep+lam*jp,'Direct signed Gaussian norm control fails')
            norms.append(actual)
        require(sum(norms)==2*ep,'Physical-sheet average identity fails')
        controls.append([k,str(ep),str(jp),*[str(v) for v in norms]])
    return {'agent':'six-sendov-1','role':'researcher',
            'status':'complete author rational certificate; ordinary written geometry and polynomial deduction; independent review pending',
            'domain':'0<=b<=c*x<=1;0<=c,x<=1;0<=eta<=1/2',
            'norm_terms':{'E':len(E),'J':len(J)},'norm_sha256':digest({'E':A.canonical(E),'J':A.canonical(J)}),
            'envelopes':tests,'origin_coefficient_count':sum(r['complete_cell_entry_comparisons'] for r in tests)+153,
            'envelope_cells':6,'corner':corner_certificate(D),'gaussian_signed_controls':24,
            'controls_sha256':digest(controls),'weak_polar_mean':mean_certificate()}

def compare(actual,expected):require(actual==expected,'Required complete expected manifest differs')

def main():
    require(len(sys.argv)==1,'No mutable output mode is supported')
    actual=derive();p=ROOT/'expected.json';require(p.is_file(),'Required expected manifest is missing')
    expected=json.loads(p.read_text());compare(actual,expected)
    import copy
    corruptions=[]
    for key in ['norm_sha256','origin_coefficient_count','envelope_cells','gaussian_signed_controls']:
        bad=copy.deepcopy(expected);bad[key]='corrupted';corruptions.append(bad)
    bad=copy.deepcopy(expected);bad['envelopes'][0]['cells'][1]['zero_count']=0;corruptions.append(bad)
    bad=copy.deepcopy(expected);bad['corner']['zero_index']=[0,0,0,0];corruptions.append(bad)
    bad=copy.deepcopy(expected);bad['weak_polar_mean']['minimum']='-1';corruptions.append(bad)
    for bad in corruptions:
        rejected=False
        try:compare(actual,bad)
        except ArithmeticError:rejected=True
        require(rejected,'A corrupt expected manifest was accepted')
    print(json.dumps({'result':'PASS','envelope_cells':6,'origin_coefficients':actual['origin_coefficient_count'],
        'all_envelope_entries_compared':True,'all_cells_inverted':True,'strict_corner_patterns_checked':True,
        'gaussian_signed_controls':24,'weak_mean_coefficients':23,'rejected_corruptions':len(corruptions),
        'norm_sha256':actual['norm_sha256']},sort_keys=True))

if __name__=='__main__':main()
