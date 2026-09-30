"""Reconstruct the complete signed-sheet gain and exact obstruction.

Python 3.10+ standard library. Run from any directory, including with -I/-O.
The finite coefficient proof is checked with explicit exceptions.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import hashlib,importlib.util,json,sys

ROOT=Path(__file__).resolve().parent
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/file)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj
A=module('phase_sheet_algebra','algebra.py')
B=module('phase_sheet_certificate','certificate.py')

def require(condition,message):
    if not condition:raise ArithmeticError(message)

def unit(p):
    out=defaultdict(F)
    for e,v in p.items():
        f=list(e);f[1]=0;out[tuple(f)]+=v
    return {e:v for e,v in out.items() if v}

def derivative(p,axis):
    out={}
    for e,v in p.items():
        if e[axis]:
            f=list(e);f[axis]-=1;out[tuple(f)]=v*e[axis]
    return out

def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def tensor_hash(values,den):
    h=hashlib.sha256()
    for v in values:h.update((str(F(v,den))+'\n').encode())
    return h.hexdigest()

def gauss_add(z,w):return (z[0]+w[0],z[1]+w[1])
def gauss_mul(z,w):return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def gauss_scale(z,k):return (z[0]*k,z[1]*k)
def norm(z):return z[0]*z[0]+z[1]*z[1]

def direct_integral(a,U,V,polar=False):
    # Eight linear convolutions, distinct from the symbolic pair fourth power.
    coefficients=[(F(1),F(0))]
    for z in [U]*4+[V]*4:
        factors=[(a,F(0)),gauss_scale(z,1-a*a)] if polar else [(F(1),F(0)),gauss_scale(z,-a)]
        out=[(F(0),F(0))]*(len(coefficients)+1)
        for j,v in enumerate(coefficients):
            for k,f in enumerate(factors):out[j+k]=gauss_add(out[j+k],gauss_mul(v,f))
        coefficients=out
    value=(F(0),F(0))
    for j,v in enumerate(coefficients):value=gauss_add(value,gauss_scale(v,F(1,j+1)))
    return value if polar else gauss_scale(value,9)

def phases(c,d,x,y,eta):
    w=(x,y);u=gauss_mul(w,(c,d));v=gauss_mul(w,(c,-d))
    return gauss_scale(u,1+eta),gauss_scale(v,1-eta)

PATHS=[[[2,0]],[[2,1],[1,0]],[[2,1],[1,1],[1,0]],
       [[2,1],[1,1],[1,1],[2,0]],[[2,1],[1,1],[1,1],[2,1]]]
BOXES=[[(F(0),F(1)),(F(0),F(1)),(F(0),F(1,2)),(F(0),F(1))],
       [(F(0),F(1)),(F(0),F(1,2)),(F(1,2),F(1)),(F(0),F(1))],
       [(F(0),F(1)),(F(1,2),F(3,4)),(F(1,2),F(1)),(F(0),F(1))],
       [(F(0),F(1)),(F(3,4),F(1)),(F(1,2),F(3,4)),(F(0),F(1))],
       [(F(0),F(1)),(F(3,4),F(1)),(F(3,4),F(1)),(F(0),F(1))]]

def derive():
    P,J,Ps,Qs=A.norm_polynomials()
    P2,Q2=A.alternate_integral_coefficients()
    require(Ps==P2 and Qs==Q2,'Nine direct integral coefficients disagree')
    E2,J2=A.alternate_norm(P2,Q2)
    R=A.add(A.power(A.variable(1),2),A.scale(A.variable(4),-1))
    E=A.add(P,A.power(R,8))
    require(E==E2 and J==J2,'Two complete norm constructions disagree')
    E,J=unit(E),unit(J);q=A.variable(4)
    K=A.add(A.mul(A.add(A.ONE,A.scale(q,-1)),derivative(E,4)),A.scale(E,8))
    target=B.transform(A.add(K,A.scale(A.ONE,-7)))
    whole,den,degrees=B.bernstein(target)
    require(degrees==(15,16,16,7),'Unexpected complete degree inventory')
    require(B.invert(whole,den,degrees)==target,'Global basis inversion fails')
    # Explicit five rectangles cover the full c,x square, with disjoint interiors.
    require(sum((r[1]-r[0])*(s[1]-s[0]) for _,r,s,_ in BOXES)==1,'Cell area is wrong')
    for i,box in enumerate(BOXES):
        for j in range(i):
            overlap=all(max(box[k][0],BOXES[j][k][0])<min(box[k][1],BOXES[j][k][1]) for k in [1,2])
            require(not overlap,'Cell interiors overlap')
    records=[];count=0
    for path,box in zip(PATHS,BOXES):
        values,d=whole,den;decoded=[(F(0),F(1))]*4
        for axis,side in path:
            values,d=B.split(values,d,degrees,axis)[side]
            l,r=decoded[axis];mid=(l+r)/2
            decoded[axis]=(l,mid) if side==0 else (mid,r)
        require(decoded==box,'Subdivision path and rectangle disagree')
        direct=target
        for axis,(l,r) in enumerate(box):direct=B.affine_cell(direct,axis,l,r)
        recovered=B.invert(values,d,degrees)
        require(recovered==direct,'Complete cell basis inversion fails')
        other,dother,degreeother=B.bernstein(direct,degrees)
        require(degreeother==degrees,'Cell degree changed')
        require(all(v*dother==w*d for v,w in zip(values,other)),'Independent cell transform disagrees')
        require(min(values)>0,'A complete K-7 coefficient is not positive')
        count+=len(values)
        records.append({'box':[[str(l),str(r)] for l,r in box],'degrees':list(degrees),
                        'coefficients':len(values),'minimum':str(F(min(values),d)),
                        'zero_count':sum(v==0 for v in values),'sha256':tensor_hash(values,d)})
    controls=[]
    for k in range(20):
        c,d=[(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(1),F(0)),(F(399,401),F(40,401))][k%4]
        x,y=[(F(4,5),F(3,5)),(F(20,29),F(21,29)),(F(99,101),F(20,101))][k%3]
        b=F(k%6+1,7);eta=[F(0),F(1,5),F(1,2)][k%3]
        vals=[b,F(1),c,x,eta*eta];ep=A.evaluate(E,vals);jp=A.evaluate(J,vals)
        norms=[]
        for sign in [-1,1]:
            U,V=phases(c,d,x,y,sign*eta);z=direct_integral(b,U,V)
            actual=norm(z);lam=-sign*eta*d*y
            require(actual==ep+lam*jp,'Direct Gaussian norm control fails')
            norms.append(actual)
        require(sum(norms)==2*ep,'Signed-sheet cancellation fails')
        controls.append([k,str(ep),str(jp),*[str(v) for v in norms]])
    obstruction=obstruction_record()
    return {'agent':'six-sendov-1','role':'researcher',
            'status':'author exact finite evidence; cited balanced lemma and written analytic integration are separate proof inputs',
            'domain':'0<=b<=c*x<=1;0<=c,x<=1;0<=Q<=1/4',
            'norm_terms':{'E':len(E),'J':len(J),'K':len(K)},
            'norm_sha256':canonical_hash({'E':A.canonical(E),'J':A.canonical(J)}),
            'K_sha256':canonical_hash(A.canonical(K)),
            'cell_count':len(records),'coefficient_count':count,
            'complete_cell_inversions':len(records),'complete_cell_algorithm_comparisons':len(records),
            'cell_records':records,'gaussian_signed_controls':20,'controls_sha256':canonical_hash(controls),
            'obstruction':obstruction}

def obstruction_record():
    a=F(4,5);c,d=F(399,401),F(40,401);x,y=F(99,101),F(20,101);eta=F(1,10**6)
    require(c*c+d*d==1 and x*x+y*y==1,'Obstruction phases not unit')
    U,V=phases(c,d,x,y,eta);U0,V0=phases(c,d,x,y,F(0))
    O=direct_integral(a,U,V);O0=direct_integral(a,U0,V0)
    C=direct_integral(a,U,V,True);C0=direct_integral(a,U0,V0,True)
    n=norm(O)/(1-eta*eta)**8;n0=norm(O0);difference=n-n0
    xi=(U[0]+V[0])/2;D=1-a*a;kappa=F(256,32955)
    slacks=[2*a*z[0]+D*norm(z)-1 for z in [U,V,U0,V0]]
    require(min(slacks)>0,'Critical reciprocal disk slack fails')
    require(1-eta>=1/(1+a),'Lower reciprocal radius fails')
    require(xi>a+kappa*D/a and c*x>=a,'Actual mean filter fails')
    require(-eta*d*y<0,'Skew is not strictly negative')
    require(F(-1,5*10**9)<difference<F(-1,10**10),'Origin decrease bracket fails')
    require(F(3,2)<n<n0<F(8,5),'Origin norm controls fail')
    require(all(F(9,8)<norm(z)<F(5,4) for z in [C,C0]),'Polar controls fail')
    values={'N':str(n),'N0':str(n0),'difference':str(difference),'C2':str(norm(C)),
            'C02':str(norm(C0)),'mean':str(xi),'disk_slacks':[str(v) for v in slacks]}
    return {'a':str(a),'m':'1','eta':str(eta),'c':str(c),'d':str(d),'x':str(x),'y':str(y),
            'lambda_sign':'negative','difference_bracket':['-1/5000000000','-1/10000000000'],
            'norm_bracket':['3/2','8/5'],'polar_bracket':['9/8','5/4'],
            'critical_disk_filters':'all four strict','forced_mean':'xi>a+(256/32955)*(1-a^2)/a',
            'exact_records_sha256':canonical_hash(values),
            'limitation':'abstract necessary-channel data; N>1; no disk-root polynomial or conjecture counterexample'}

def compare(actual,expected):
    require(actual==expected,'Required complete expected manifest differs')

def main():
    actual=derive();p=ROOT/'expected.json'
    if '--write-expected' in sys.argv:
        require(not p.exists(),'Expected manifest already exists')
        p.write_text(json.dumps(actual,indent=2)+'\n')
        print(json.dumps(actual,indent=2));return
    require(p.is_file(),'Required expected manifest is missing')
    expected=json.loads(p.read_text());compare(actual,expected)
    import copy
    corruptions=[]
    for field in ['K_sha256','coefficient_count','cell_count','norm_sha256','gaussian_signed_controls']:
        bad=copy.deepcopy(expected);bad[field]='corrupted';corruptions.append(bad)
    bad=copy.deepcopy(expected);bad['cell_records'][0]['minimum']='-1';corruptions.append(bad)
    bad=copy.deepcopy(expected);bad['obstruction']['lambda_sign']='positive';corruptions.append(bad)
    for bad in corruptions:
        rejected=False
        try:compare(actual,bad)
        except ArithmeticError:rejected=True
        require(rejected,'Manifest corruption was not rejected')
    print(json.dumps({'result':'PASS','cells':actual['cell_count'],'coefficients':actual['coefficient_count'],
                      'all_cell_entries_compared':True,'all_cells_inverted':True,
                      'gaussian_signed_controls':actual['gaussian_signed_controls'],'rejected_corruptions':len(corruptions),
                      'K_sha256':actual['K_sha256'],'obstruction_sha256':actual['obstruction']['exact_records_sha256']},sort_keys=True))

if __name__=='__main__':main()
