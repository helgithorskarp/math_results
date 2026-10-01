"""Self-contained exact author evidence for radial critical6+1+1.

Python3.10+ standard library. Complete rational identities, sign
tensors, zero supports, inverses, independent affine entries, polar
quotient and original-coordinate controls. No assert-based guards.
Ordinary geometric deductions remain in PROOF.md; independent review
and formalization are not implied by this replay.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod
import importlib.util,json,hashlib,copy
ROOT=Path(__file__).resolve().parent
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/file)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
A=module('radial611_algebra','algebra.py')
B=module('radial611_certificate','certificate.py')
K=module('radial611_kernel','kernel.py')
P=module('radial611_polar','polar.py')
def require(x,message):
    if not x:raise ArithmeticError(message)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tensor_hash(v,d):return digest([str(F(x,d)) for x in v])
CELLS=[(F(0),F(3,4)),(F(3,4),F(1))]
DEGREES={'H':(32,16,4,0),'disk':(64,32,8,2)}
CLEAR={'H':16,'disk':32}

def coverage():
    require(CELLS==[(F(0),F(3,4)),(F(3,4),F(1))],'Wrong complete alpha cover')
    require(CELLS[0][0]==0 and CELLS[0][1]==CELLS[1][0] and CELLS[1][1]==1,
            'Closed cells have a gap or overlap of interiors')

def zero_indices(v,g):
    shape=[d+1 for d in g];stride=[prod(shape[j+1:]) for j in range(4)]
    return {tuple((i//stride[j])%shape[j] for j in range(4)) for i,x in enumerate(v) if not x}

def certify(mapped,progress=None):
    coverage();records=[];whole={}
    for name,(p,clear) in mapped.items():
        v,d,g=B.bernstein(p)
        require(g==DEGREES[name] and clear==CLEAR[name],'Wrong map inventory')
        require(B.invert(v,d,g)==p,'Complete global inverse fails '+name)
        whole[name]=(v,d,g)
    fraction_controls=0
    for cell,(lo,hi) in enumerate(CELLS):
      for name in ['H','disk']:
        v,d,g=whole[name]
        halves=B.split_at(v,d,g,1,F(3,4));cv,cd=halves[cell]
        p,clear=mapped[name]
        direct=B.affine_cell_integer(p,1,lo,hi)
        # Complete Fraction references for both degrees; complements the
        # entrywise integer-affine/de Casteljau comparison on every cell.
        if cell==0:
            require(B.affine_cell(p,1,lo,hi)==direct,'Complete Fraction affine reference differs')
            fraction_controls+=1
        require(B.invert(cv,cd,g)==direct,'Complete cell inverse differs')
        av,ad,ag=B.bernstein(direct,g)
        require(ag==g and len(cv)==len(av)==prod(d+1 for d in g),'Incomplete tensor')
        require(all(x*ad==y*cd for x,y in zip(cv,av)),
                'Every-entry affine/de Casteljau identity fails')
        require(min(cv)>=0,'Negative complete cell coefficient')
        zeros=zero_indices(cv,g)
        if name=='H':require(not zeros,'Unexpected first-sign zero')
        else:
            expected={(64,i,j,2) for i in ([31,32] if cell==0 else [0,1]) for j in [7,8]}
            if cell==0:expected|={(64,0,0,k) for k in range(3)}
            require(zeros==expected,'Wrong complete exact equality support')
        records.append({'cell':cell,'target':name,'alpha':[str(lo),str(hi)],
          'b':['0','1'],'beta':['0','1'],'phase':['0','1'],
          'degrees':list(g),'clear_D_power':clear,'coefficients':len(cv),
          'minimum':str(F(min(cv),cd)),'minimum_positive':str(F(min(x for x in cv if x>0),cd)),
          'zeros':len(zeros),'zero_indices':[list(e) for e in sorted(zeros)],
          'zero_indices_sha256':digest(sorted(zeros)),'sha256':tensor_hash(cv,cd)})
      if progress:progress('cell'+str(cell)+' full signs, inverses and every affine entry PASS')
    require(fraction_controls==2,'Missing complete Fraction affine references')
    require(sum(r['coefficients'] for r in records)==121440,'Incomplete origin sign inventory')
    return records

def gadd(x,y):return (x[0]+y[0],x[1]+y[1])
def gscale(x,c):return (x[0]*c,x[1]*c)
def gmul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def gnorm(x):return x[0]*x[0]+x[1]*x[1]
def gpower(x,n):
    out=(F(1),F(0))
    for _ in range(n):out=gmul(out,x)
    return out

def direct_integral(U,V,W,offset,slope,weight=F(1)):
    """Sequential eight-linear-factor Gaussian polynomial integration."""
    out=[(F(1),F(0))]
    for z in [U]*6+[V,W]:
        result=[(F(0),F(0)) for _ in range(len(out)+1)]
        for j,c in enumerate(out):
            result[j]=gadd(result[j],gscale(c,offset))
            result[j+1]=gadd(result[j+1],gscale(gmul(c,z),slope))
        out=result
    return tuple(weight*sum(c[k]/(j+1) for j,c in enumerate(out)) for k in range(2))

def evaluator(p):
    """Preclear coefficients; independent direct polynomial evaluation."""
    from math import lcm
    den=lcm(*(v.denominator for v in p.values()))
    terms=[(e,int(v*den)) for e,v in p.items()]
    degrees=[max(e[j] for e in p) for j in range(4)]
    def calc(values):
        common=prod(values[j].denominator**degrees[j] for j in range(4))
        powers=[[values[j].numerator**k*values[j].denominator**(degrees[j]-k)
                 for k in range(degrees[j]+1)] for j in range(4)]
        return F(sum(v*prod(powers[j][e[j]] for j in range(4)) for e,v in terms),den*common)
    return calc

def original_controls(d,mapped):
    moments=list(map(evaluator,d['moments']))
    maps={n:evaluator(p) for n,(p,clear) in mapped.items()}
    rows=[];maprows=[]
    phases=[(F(1),F(0)),(F(99,101),F(20,101)),(F(3,5),F(4,5)),(F(5,13),F(-12,13))]
    for b in [F(1,3),F(2,3),F(1)]:
      for alpha in [F(0),F(3,8),F(3,4),F(1)]:
       for beta in [F(0),F(1,2),F(1)]:
        r=(1+F(4,3)*b*alpha)/(1+b)
        s=(1+4*b*(1-alpha)*beta)/(1+b);t=8-6*r-s
        require(F(1,1+b)<=r and F(1,1+b)<=s<=t and 6*r+s+t==8,
                'Original radius parametrization control fails')
        disk=(1-(1-b*b)*s*s)/(2*b*s)
        AA,BB,CC=[m([b,r,s,F(1)]) for m in moments]
        R=r**12*s*s*t*t
        for v in phases:
            q=v[0]
            if q<disk:continue
            require(gnorm(v)==1,'Bad Gaussian unit phase')
            KK=gadd((AA,F(0)),gscale(v,-s*BB))
            JJ=gadd((BB,F(0)),gscale(v,-s*CC))
            PA=gnorm(KK);PJ=gnorm(JJ);L=PA+t*t*PJ-R;FF=L*L-4*t*t*PA*PJ
            require(L>=R/8 and FF>=0,'Original first/squared sign control fails')
            H=AA*AA+s*s*BB*BB+t*t*(BB*BB+s*s*CC*CC)-2*s*BB*(AA+t*t*CC)-F(9,8)*R
            z=(q-disk)/(1-disk) if disk<1 else F(0)
            require(0<=z<=1,'Original disk coordinate outside box')
            for name,raw in [('H',H),('disk',FF)]:
                actual=maps[name]([b,alpha,beta,z])
                require(actual==(1+b)**CLEAR[name]*raw,'Complete original-to-map control differs')
                maprows.append([name,*map(str,[b,alpha,beta,z,actual])])
            for w in phases+[(F(-1),F(0))]:
                ii=gadd(KK,gscale(gmul(w,JJ),-t))
                raw=direct_integral((r,F(0)),gscale(v,s),gscale(w,t),F(1),-b,F(9))
                require(raw==ii,'Original complex integral control differs')
                ratio=gnorm(ii)/R;require(ratio>=1,'Original radial-sector norm control fails')
                rows.append(list(map(str,[b,r,s,t,*v,*w,*ii,ratio])))
    require(len(rows)>=200 and len(maprows)>=80,'Insufficient original complex controls')
    return {'integral_controls':len(rows),'integral_sha256':digest(rows),
            'map_controls':len(maprows),'map_sha256':digest(maprows)}

def polar_coordinate_controls():
    """Exact physical Gaussian moduli, radius variance and mean variables.

    These are controls on ordinary bridges, not substitutes for the
    complete quotient signs or the written geometric proof.
    """
    rows=[];count=0;low_mean=0;high_mean=0
    env=evaluator(P.integral(A))
    def mul(x,y):
        out=[F(0)]*(len(x)+len(y)-1)
        for i,c in enumerate(x):
            for j,d in enumerate(y):out[i+j]+=c*d
        return out
    def envelope(a,radii,projections):
        D=1-a*a
        quadratics=[[a*a,2*a*D*x,D*D*r*r] for r,x in zip(radii,projections)]
        X,Y,Z=quadratics
        raw=mul(mul(mul(X,X),X),[u+v for u,v in zip(Y,Z)])
        return sum(v/F(2*(j+1)) for j,v in enumerate(raw))
    units=[(F(1),F(0)),(F(3,5),F(4,5)),(F(5,13),F(-12,13))]
    for a in [F(1,4),F(1,2),F(3,4)]:
      D=1-a*a;eps=1-a
      for v in [F(0),F(1,3),F(1)]:
       R0=1+F(4,3)*a*v;S0=1+8*a*(1-v)
       r=R0/(1+a);lo=1/(1+a);total=(1+S0)/(1+a)
       for split in [F(0),F(2,5),F(1)]:
        s=lo+(total-2*lo)*split;t=total-s
        require(s*s+t*t<=(1+S0*S0)/(1+a)**2,'Physical light-radius convexity control fails')
        for pu,pv,pw in [(units[1],units[2],units[1]),(units[2],units[1],units[2])]:
            U=gscale(pu,r);V=gscale(pv,s);W=gscale(pw,t)
            xi=(6*U[0]+V[0]+W[0])/8
            radii=[r,s,t];original=[U[0],V[0],W[0]]
            projections=original.copy();need=8*(a-xi)
            for i,weight in enumerate([6,1,1]):
                if need>=0:
                    amount=min(need/weight,radii[i]-projections[i])
                else:
                    amount=-min(-need/weight,projections[i]+radii[i])
                projections[i]+=amount;need-=weight*amount
            require(need==0 and 6*projections[0]+projections[1]+projections[2]==8*a,
                    'Physical polar mean saturation control fails')
            theta=F(3,4)*(r-projections[0])/eps
            require(0<=theta<=1,'Physical polar theta outside cube')
            before=envelope(a,radii,original);after=envelope(a,radii,projections)
            upper=env([a,v,theta,F(0)])
            require(0<=after<=upper<=1-F(8,9)*eps*eps,'Saturated physical polar envelope control fails')
            if xi<=a:
                low_mean+=1
                require(0<=before<=after,'Polar coordinate monotonicity control fails')
            else:
                high_mean+=1
                Q=(1+F(4,3)*a*eps)**2;PP=(1+8*a*eps)**2
                require(Q<=F(16,9) and PP<=9 and Q<=PP,'Polar modulus caps fail')
                require(before-after<=4*a*D*Q*Q*PP*(xi-a),
                        'Physical polar derivative-gap control fails')
            for tau in [F(0),F(1,3),F(1)]:
                mod=[gnorm(gadd((a,F(0)),gscale(z,D*tau))) for z in [U,V,W]]
                real=[a*a+2*a*D*tau*z[0]+D*D*tau*tau*gnorm(z) for z in [U,V,W]]
                require(mod==real,'Original polar Gaussian modulus identity fails')
            c=direct_integral(U,V,W,a,D)
            require(before>=0 and gnorm(c)<=before*before,'Original complex polar triangle/envelope control fails')
            rows.append(list(map(str,[a,v,split,*U,*V,*W,xi,theta,before,after,upper,*c])));count+=1
    require(count==54,'Incomplete polar physical control inventory')
    require(low_mean>0 and high_mean>0,'Missing low/high polar mean controls')
    return {'count':count,'low_mean':low_mean,'high_mean':high_mean,
            'saturation_variance_derivative_and_original_envelope_checked':True,'sha256':digest(rows)}

def example_and_relaxation():
    a=F(19,20);d=(F(0),F(1,40));e=(F(1,50),F(1,25))
    c8=gscale(gadd(d,e),F(-9,8));c7=gscale(gmul(d,e),F(9,7))
    fa=gadd((a**9,F(0)),gadd(gscale(c8,a**8),gscale(c7,a**7)))
    c0=gscale(fa,-1)
    rouche=sum(abs(x)+abs(y) for x,y in [c8,c7,c0])
    require(rouche<1 and c8[1]!=0,'Nonreal disk-root example Rouché bound fails')
    require(gnorm(d)>0 and d!=e and gnorm(gadd((a,F(0)),gscale(d,-1)))>0
            and gnorm(gadd((a,F(0)),gscale(e,-1)))>0,'Example critical distinctness/simple root fails')
    require(6/a+2/(1+a)<8,'Example already forced by the elementary radial lower bound')
    b=F(1);r=s=F(1,2);t=F(9,2)
    v=(F(99,101),F(20,101));w=(F(999831,1000169),F(26000,1000169))
    require(gnorm(v)==gnorm(w)==1,'Bad obstruction unit phases')
    ii=direct_integral((r,F(0)),gscale(v,s),gscale(w,t),F(1),-b,F(9))
    ratio=gnorm(ii)/(r**12*s*s*t*t)
    require(ratio<1 and v[0]<1,'Disk-free light-phase obstruction fails')
    return {'nonreal_example':{'marked_root':str(a),'critical_light_1':list(map(str,d)),
      'critical_light_2':list(map(str,e)),'coefficient_z8':list(map(str,c8)),
      'coefficient_z7':list(map(str,c7)),'constant':list(map(str,c0)),
      'unit_circle_Rouche_L1_bound':str(rouche)},
      'free_both_light_phases_obstruction':{'b':'1','r':'1/2','s':'1/2','t':'9/2',
      'v':list(map(str,v)),'w':list(map(str,w)),'N':str(ratio),
      'violates_smaller_light_disk':True,'is_polynomial_counterexample':False}}

def build(progress=None):
    d=K.data(A);K.check_kernel(A,d,require)
    mapped=K.mapped(A,d,require,progress)
    cells=certify(mapped,progress)
    polar=P.certify(A,B,require,digest,tensor_hash)
    controls=original_controls(d,mapped)
    physical=polar_coordinate_controls();examples=example_and_relaxation()
    return {'agent':'six-sendov-1','role':'researcher',
      'proof_status':'ordinary author proof with complete exact finite evidence; unformalized; independent review pending',
      'radial_sector':'degree9 disk-root polynomial; critical point of multiplicity at least6 on the line from origin to marked nonzero root',
      'abstract_domain':'0<b<=1,r,s,t>=1/(1+b),s<=t,6r+s+t=8; heavy phase1; smaller light phase obeys its critical disk; other light phase arbitrary',
      'first_sign_constant':'1/8','complete_Horner_identities':3,
      'kernel_sha256':digest([A.canonical(d[k]) for k in ['R','L','F','H']]),
      'mapped_sha256':{n:digest(A.canonical(p)) for n,(p,clear) in mapped.items()},
      'cells':cells,'polar':polar,'original_controls':controls,'polar_physical_controls':physical,
      'examples':examples,'origin_sign_coefficients':121440,'certified_coefficients':122115,
      'first_power_radial_sector_claimed':True,'full_complex_polar_mean_gap_claimed':True,
      'full_complex_six_one_one_origin_claimed':False,'unrestricted_degree_nine_claimed':False}

def accept(actual,expected):require(actual==expected,'Complete compact fixture mismatch')
def rejection_controls(actual):
    rejected=0
    for change in range(12):
        bad=copy.deepcopy(actual)
        if change==0:bad['certified_coefficients']-=1
        elif change==1:bad['first_sign_constant']='0'
        elif change==2:bad['complete_Horner_identities']-=1
        elif change==3:bad['cells'].pop()
        elif change==4:bad['cells'][1]['minimum']='-1'
        elif change==5:bad['cells'][1]['zero_indices_sha256']='0'*64
        elif change==6:bad['mapped_sha256']['disk']='0'*64
        elif change==7:bad['original_controls']['integral_sha256']='0'*64
        elif change==8:bad['polar']['uniform_gamma']='1'
        elif change==9:bad['examples']['free_both_light_phases_obstruction']['is_polynomial_counterexample']=True
        elif change==10:bad['full_complex_six_one_one_origin_claimed']=True
        else:bad['unrestricted_degree_nine_claimed']=True
        try:accept(actual,bad)
        except ArithmeticError:rejected+=1
        else:raise ArithmeticError('Corrupted fixture accepted')
    return rejected

def main():
    actual=build();expected=json.loads((ROOT/'expected.json').read_text());accept(actual,expected)
    rejected=rejection_controls(actual)
    print(json.dumps({'result':'PASS','certified_coefficients':actual['certified_coefficients'],
      'radial_cells':2,'complete_Horner_identities':3,
      'all_global_and_cell_inverses_and_affine_entries_checked':True,
      'kernel_sha256':actual['kernel_sha256'],
      'original_integral_controls':actual['original_controls']['integral_controls'],
      'original_map_controls':actual['original_controls']['map_controls'],
      'polar_physical_controls':actual['polar_physical_controls']['count'],
      'first_power_radial_sector_claimed':True,'full_complex_polar_mean_gap_claimed':True,
      'full_complex_six_one_one_origin_claimed':False,'unrestricted_degree_nine_claimed':False,
      'rejected_corruptions':rejected},sort_keys=True))
if __name__=='__main__':main()
