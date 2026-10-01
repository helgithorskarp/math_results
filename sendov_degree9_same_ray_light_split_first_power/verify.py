"""Exact author evidence for complex-heavy same-ray light splitting.

Actual author six-sendov-1, researcher. Python3.10+ standard library.
This checker proves the finite dominance signs, not its three explicitly
cited prior mathematical premises or the ordinary analytic deductions.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod
import importlib.util,hashlib,json,copy,sys
ROOT=Path(__file__).resolve().parent

def module(n,file):
    s=importlib.util.spec_from_file_location(n,ROOT/file)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=module('same_ray_algebra','algebra.py')
B=module('same_ray_certificate','certificate.py')
K=module('same_ray_kernel','kernel.py')
def require(x,msg):
    if not x:raise ArithmeticError(msg)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def phash(p):return digest(A.canonical(p))

def certificates(data):
    p=data['margin'];v,d,g=B.bernstein(p)
    require(g==(32,16,6,0) and len(v)==3927,'Wrong complete tensor inventory')
    require(B.invert(v,d,g)==p,'Complete global inverse fails')
    cells=[(F(0),F(1,2)),(F(1,2),F(1))]
    require(cells[0][0]==0 and cells[0][1]==cells[1][0] and cells[1][1]==1,'Incomplete closed cover')
    halves=B.split(v,d,g,0);rows=[]
    for i,(lo,hi) in enumerate(cells):
        cv,cd=halves[i]
        require(len(cv)==prod(x+1 for x in g) and min(cv)>0,'Missing or nonpositive complete cell coefficient')
        direct=B.affine_cell_integer(p,0,lo,hi)
        require(direct==B.affine_cell(p,0,lo,hi),'Complete Fraction/integer affine identity fails')
        require(B.invert(cv,cd,g)==direct,'Complete cell inverse fails')
        av,ad,ag=B.bernstein(direct,g)
        require(ag==g and len(cv)==len(av) and all(x*ad==y*cd for x,y in zip(cv,av)),
                'Complete affine/de Casteljau entry comparison fails')
        rows.append({'b':[str(lo),str(hi)],'y':['0','1'],'z':['0','1'],
          'degrees':list(g),'coefficients':len(cv),'minimum':str(F(min(cv),cd)),
          'sha256':digest([str(F(x,cd)) for x in cv])})
    require(sum(r['coefficients'] for r in rows)==7854,'Incomplete dominance sign count')
    return rows

def ga(x,y):return (x[0]+y[0],x[1]+y[1])
def gs(x,k):return (x[0]*k,x[1]*k)
def gm(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def gc(x):return (x[0],-x[1])
def gn(x):return x[0]*x[0]+x[1]*x[1]
def gp(x,n):
    out=(F(1),F(0))
    for _ in range(n):out=gm(out,x)
    return out
def gi(x):
    require(gn(x)>0,'Division by zero Gaussian')
    return gs(gc(x),1/gn(x))
def poly_value(p,x):
    out=(F(0),F(0))
    for c in reversed(p):out=ga(gm(out,x),c)
    return out

def linear_product(points,offset,slope):
    out=[(F(1),F(0))]
    for z in points:
        new=[(F(0),F(0)) for _ in range(len(out)+1)]
        for j,c in enumerate(out):
            new[j]=ga(new[j],gs(c,offset))
            new[j+1]=ga(new[j+1],gs(gm(c,z),slope))
        out=new
    return out

def integrate(points,offset,slope,weight=F(1)):
    p=linear_product(points,offset,slope)
    return tuple(weight*sum(c[k]/(j+1) for j,c in enumerate(p)) for k in range(2))

def moments(b,U):
    p=linear_product([U]*6,F(1),-b)
    return [tuple(9*b**l*sum(c[k]/(j+l+1) for j,c in enumerate(p)) for k in range(2)) for l in range(3)]

def evaluator(p):
    """Shared integer direct evaluation; separately derived from transforms."""
    from math import lcm
    den=lcm(*(v.denominator for v in p.values()))
    terms=[(e,int(v*den)) for e,v in p.items()];degrees=[max(e[i] for e in p) for i in range(4)]
    def calc(values):
        common=prod(values[i].denominator**degrees[i] for i in range(4))
        pw=[[values[i].numerator**j*values[i].denominator**(degrees[i]-j)
              for j in range(degrees[i]+1)] for i in range(4)]
        return F(sum(v*prod(pw[i][e[i]] for i in range(4)) for e,v in terms),den*common)
    return calc

def origin_controls(data):
    evalE=evaluator(data['E']);evalQ=evaluator(data['margin'])
    evalN=list(map(evaluator,data['norms']))
    units=[(F(1),F(0)),(F(99,101),F(20,101)),(F(99,101),F(-20,101)),
           (F(3,5),F(4,5)),(F(3,5),F(-4,5)),(F(5,13),F(12,13)),(F(5,13),F(-12,13))]
    rows=[];nonreal=0;split=0;faces=0
    for b in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
      for y in [F(0),F(1,2),F(1)]:
        r=1+b*y/(3*(1+b));S=8-6*r;P0=S*S/4;lo=1/(1+b)
        for fraction in [F(0),F(1,2),F(1)]:
          delta=(S/2-lo)*fraction;s=S/2-delta;t=S/2+delta;P=s*t
          require(lo<=s<=t and 6*r+s+t==8 and r>=1,'Original radius normalization fails')
          for u in units:
            U=gs(u,r);x=U[0]
            for v in units:
              mu=(6*x+S*v[0])/8
              if mu<b:continue
              require(x>=r-F(4,3)*(1-b),'Necessary heavy mean floor fails')
              z=1-F(3,4)*(r-x)/(1-b) if b<1 else F(0)
              require(0<=z<=1,'Heavy phase cube bridge fails')
              AA,BB,CC=moments(b,U)
              E=gn(AA)-2*S*S*gn(BB)-2*P0*P0*gn(CC)
              require(evalE([b,r,x,F(0)])==E and E>=F(1,128),'Original dominance control fails')
              require([f([b,r,x,F(0)]) for f in evalN]==[gn(q) for q in [AA,BB,CC]],'Original complex norm controls fail')
              require(evalQ([b,y,z,F(0)])==(1+b)**16*(E-F(1,128)),'Complete original-to-map control fails')
              KK=ga(AA,gs(gm(v,BB),-S));vv=gp(v,2)
              II=ga(KK,gs(gm(vv,CC),P));I0=ga(KK,gs(gm(vv,CC),P0))
              direct=integrate([U]*6+[gs(v,s),gs(v,t)],F(1),-b,F(9))
              merged=integrate([U]*6+[gs(v,S/2)]*2,F(1),-b,F(9))
              require(II==direct and I0==merged,'Original eight-factor integral controls fail')
              N=gn(II)/(r**12*P*P);N0=gn(I0)/(r**12*P0*P0)
              lam=1/P-1/P0;cross=gm(I0,gc(KK))[0]
              require(gn(KK)>=P0*P0*gn(CC)+E/2 and cross>=E/4,'First-sign dominance controls fail')
              require(N-N0==(2*lam*cross/P0+lam*lam*gn(KK))/r**12,'Exact splitting identity fails')
              require(N-N0>=E*(P0-P)/(2*r**12*P*P*P0)>=(t-s)**2/7168,'Quantitative split bound control fails')
              require(N0>=1 and (b==1 or N0>1),'Merged origin control conflicts with cited premise')
              if s<t:require(N>N0,'Strict split control fails');split+=1
              if u[1]:nonreal+=1
              if b in [0,1]:faces+=1
              rows.append(list(map(str,[b,y,z,r,s,t,*u,*v,E,N,N0])))
    require(len(rows)>400 and nonreal>100 and split>100 and faces>100,'Insufficient signed/degenerate origin controls')
    return {'original_controls':len(rows),'nonreal_heavy_controls':nonreal,'unequal_light_controls':split,
            'degenerate_b_face_controls':faces,'sha256':digest(rows)}

def derivative(points):return [gs(c,9) for c in linear_product(points,F(1),F(-1))][::-1]
# linear_product gives product(1-z*t); reversing gives product(t-z).
def anchored(points,a):
    dp=derivative(points);p=[(F(0),F(0))]+[gs(c,F(1,j+1)) for j,c in enumerate(dp)]
    p[0]=gs(poly_value(p,(a,F(0))),-1)
    return p,dp

def example_and_barrier():
    a=F(19,20);d=(F(1,100),F(1,1000));c=(F(-1,100),F(1,100));delta=F(1,100)
    ac=ga((a,F(0)),gs(c,-1));e1=ga(c,gs(ac,-delta));e2=ga(c,gs(ac,delta))
    points=[d]*6+[e1,e2];p,dp=anchored(points,a)
    require(poly_value(p,(a,F(0)))==(0,0),'Example marked root fails')
    require([gs(p[j+1],j+1) for j in range(9)]==dp,'Complete example derivative fails')
    require(poly_value(dp,(a,F(0)))!=(0,0),'Example marked root is not simple')
    require(len({d,e1,e2})==3 and d[1] and e1[1] and e2[1] and p[8][1], 'Example does not leave radial/real sector')
    require(ga((a,F(0)),gs(e1,-1))==gs(ac,1+delta) and ga((a,F(0)),gs(e2,-1))==gs(ac,1-delta),
            'Example common ray fails')
    hd=gn(ga((a,F(0)),gs(d,-1)));light_floor=(1-delta*delta)**2*gn(ac)
    require(hd<light_floor,'Exact example heavier-reciprocal predicate fails')
    bound=sum(abs(q[0])+abs(q[1]) for q in p[:-1]);require(bound<1,'Example Rouche certificate fails')
    U,V,W=[gi(ga((a,F(0)),gs(z,-1))) for z in [d,e1,e2]]
    integral=integrate([U]*6+[V,W],F(1),-a,F(9))
    q0=gs(p[0],-1/a);product=gm(gp(U,6),gm(V,W))
    require(gm(integral,gi(product))==q0,'Example original origin identity fails')
    polar=integrate([U]*6+[V,W],a,1-a*a)
    qex=gs(poly_value(p,(1/a,F(0))),a/(1-a*a));qa=poly_value(dp,(a,F(0)))
    require(polar==gs(gm(qex,gi(qa)),a**8),'Example original polar identity fails')
    rows=[]
    for m in [F(1,3),F(2,3),F(1)]:
        scaled,sd=anchored([gs(z,m) for z in points],a*m)
        require(scaled==[gs(q,m**(9-j)) for j,q in enumerate(p)] and
                sd==[gs(q,m**(8-j)) for j,q in enumerate(dp)],'Full polynomial/derivative scaling control fails')
        for point,Q in zip([d,e1,e2],[U,V,W]):
            require(gi(ga((m*a,F(0)),gs(point,-m)))==gs(Q,1/m),'Example reciprocal scaling fails')
        rows.append([str(m),[[str(x) for x in q] for q in scaled]])
    # Exact valid lower-r countercomparison, not a first-power failure.
    b=F(1);r=F(1,2);S=F(5);P=F(9,4);P0=F(25,4)
    AA,BB,CC=moments(b,(r,F(0)));KK=ga(AA,gs(BB,-S))
    II=ga(KK,gs(CC,P));I0=ga(KK,gs(CC,P0))
    N=gn(II)/(r**12*P*P);N0=gn(I0)/(r**12*P0*P0);cross=gm(I0,gc(KK))[0]
    require(N==1 and N0>1 and cross<0,'Exact unrestricted splitting obstruction fails')
    require(7**12<7*6**12,'Uniform splitting denominator bound fails')
    return {'nonreal_example':{'a':str(a),'heavy':list(map(str,d)),
       'lights':[list(map(str,e1)),list(map(str,e2))],'rouche_l1_bound':str(bound),
       'heavy_distance_squared':str(hd),'light_criterion_rhs':str(light_floor),
       'full_scaling_controls':len(rows),'scaling_sha256':digest(rows),
       'polynomial_sha256':digest([[str(x) for x in q] for q in p])},
       'split_barrier':{'b':'1','r':'1/2','s':'1/2','t':'9/2','original_ratio':str(N),
                       'merged_ratio':str(N0),'cross':str(cross)}}

def robust_controls_and_example():
    rows=[]
    units=[(F(1),F(0)),(F(99,101),F(20,101)),(F(99,101),F(-20,101)),
           (F(3,5),F(4,5)),(F(3,5),F(-4,5))]
    for b in [F(1,2),F(3,4)]:
      for y in [F(0),F(1,2)]:
        r=1+b*y/(3*(1+b));s=1/(1+b);t=8-6*r-s;dd=t-s
        for u in units:
          U=gs(u,r)
          for v in units:
            for k in [F(1,10**8),F(-1,10**8)]:
              alpha=((1-k*k)/(1+k*k),2*k/(1+k*k));w=gm(v,alpha)
              h2=gn(ga(v,gs(w,-1)));mu=(6*U[0]+s*v[0]+t*w[0])/8
              if mu<=b or (8*(mu-b)/t)**2<h2:continue
              require(h2<=(dd*dd/645120)**2 and h2>0,'Robust exact chord predicate fails')
              require((6*U[0]+(s+t)*v[0])/8>=b,'Robust reference mean fails')
              AA,BB,CC=moments(b,U);J=ga(BB,gs(gm(v,CC),-s))
              require(gn(BB)<=(45*b/8)**2 and gn(CC)<=(15*b*b/4)**2,'Robust heavy-moment modulus bounds fail')
              require(gn(J)/(r**12*s*s)<=225,'Robust amplitude error constant fails')
              Iref=integrate([U]*6+[gs(v,s),gs(v,t)],F(1),-b,F(9))
              Iactual=integrate([U]*6+[gs(v,s),gs(w,t)],F(1),-b,F(9))
              diff=ga(Iactual,gs(Iref,-1))
              require(diff==gs(gm(ga(w,gs(v,-1)),J),-t) and gn(diff)==t*t*h2*gn(J),
                      'Robust exact perturbation integral identity fails')
              N=gn(Iactual)/(r**12*s*s*t*t)
              require(N>1+dd*dd/21504,'Robust actual squared origin control fails')
              rows.append(list(map(str,[b,y,*u,*v,k,h2,mu,N])))
    require(len(rows)>=50,'Insufficient signed robust controls')
    b=A.variable(0)
    f1=A.add(A.ONE,A.scale(b,F(2,3)),A.scale(A.power(b,2),F(-5,3)))
    f2=A.add(A.ONE,A.scale(b,F(1,3)),A.scale(A.power(b,2),F(-47,36)))
    require(f1==A.add(A.scale(A.ONE,F(16,15)),A.scale(A.power(A.add(b,A.scale(A.ONE,F(-1,5))),2),F(-5,3))),
            'Complete first heavy modulus identity fails')
    require(f2==A.add(A.scale(A.ONE,F(48,47)),A.scale(A.power(A.add(b,A.scale(A.ONE,F(-6,47))),2),F(-47,36))),
            'Complete second heavy modulus identity fails')
    require(F(48,47)<F(16,15) and F(16,15)**3<F(5,4) and 15*43008==645120,
            'Robust rational constants fail')
    a=F(19,20);d=(F(1,100),F(1,1000));c=(F(-1,100),F(1,100));delta=F(1,100)
    ac=ga((a,F(0)),gs(c,-1));e1=ga(c,gs(ac,-delta));e2=ga(c,gs(ac,delta));k=F(1,10**12)
    alpha=((1-k*k)/(1+k*k),2*k/(1+k*k));a2=ga((a,F(0)),gs(e2,-1))
    enew=ga((a,F(0)),gs(gm(alpha,a2),-1))
    anew=ga((a,F(0)),gs(enew,-1));a1=ga((a,F(0)),gs(e1,-1))
    require(gn(anew)==gn(a2) and gm(anew,gi(a1))[1]!=0,'Perturbed polynomial lights remain collinear')
    h2=4*k*k/(1+k*k);gap2=4*delta*delta/((1-delta*delta)**2*gn(ac))
    radial_tolerance=gap2/645120;mean_tolerance=4*(1-a)/(45*a*(1+a))
    require(h2>0 and h2<radial_tolerance**2 and h2<mean_tolerance**2,'Actual perturbed polynomial sector predicate fails')
    hd=gn(ga((a,F(0)),gs(d,-1)))
    require(hd<(1-delta*delta)**2*gn(ac),'Actual perturbed heavier predicate fails')
    p,dp=anchored([d]*6+[e1,enew],a);bound=sum(abs(q[0])+abs(q[1]) for q in p[:-1])
    require(bound<1 and poly_value(p,(a,F(0)))==(0,0) and poly_value(dp,(a,F(0)))!=(0,0),
            'Perturbed Rouche/marked simplicity fails')
    require([gs(p[j+1],j+1) for j in range(9)]==dp,'Complete perturbed polynomial derivative fails')
    return {'exact_signed_origin_controls':len(rows),'sha256':digest(rows),
      'perturbed_noncollinear_example':{'phase_parameter':str(k),'chord_squared':str(h2),
        'original_light_radius_gap_squared':str(gap2),'rouche_l1_bound':str(bound),
        'strict_angular_predicates_checked_by_positive_squares':True,
        'polynomial_sha256':digest([[str(x) for x in q] for q in p])}}

def compute():
    data=K.build(A,require);cells=certificates(data)
    return {'result':'PASS','agent':'six-sendov-1','role':'researcher',
       'dominance_lower_bound':'1/128','splitting_gain_constant':'1/7168',
       'robust_gain_constant':'1/21504','robust_phase_chord_denominator':645120,
       'new_certified_sign_coefficients':7854,'clear_D_power':data['clear'],
       'kernel_terms':len(data['E']),'mapped_margin_terms':len(data['margin']),
       'kernel_sha256':phash(data['E']),'margin_sha256':phash(data['margin']),
       'moment_norm_sha256':[phash(p) for p in data['norms']],
       'complete_cells':cells,'complete_fraction_affine_references':2,
       'origin_controls':origin_controls(data),'exact_examples':example_and_barrier(),
       'robust_sector':robust_controls_and_example(),
       'prior_logical_premises_reproved_by_this_checker':False,'rejected_corruptions':10}

def validate(result,fixture):require(result==fixture,'Complete compact fixture mismatch')
def corruptions(result):
    cases=[]
    for path in [('new_certified_sign_coefficients',),('dominance_lower_bound',),('splitting_gain_constant',),
      ('clear_D_power',),('kernel_sha256',),('margin_sha256',),
      ('complete_cells',0,'minimum'),('complete_cells',1,'sha256'),
      ('origin_controls','nonreal_heavy_controls'),('exact_examples','split_barrier','merged_ratio')]:
        obj=copy.deepcopy(result);node=obj
        for key in path[:-1]:node=node[key]
        node[path[-1]]='altered';cases.append(obj)
    for obj in cases:
        try:validate(result,obj)
        except ArithmeticError:continue
        raise ArithmeticError('Altered fixture accepted')
    require(len(cases)==result['rejected_corruptions'],'Wrong corruption inventory')

if __name__=='__main__':
    require(len(sys.argv)==1,'No verifier options; compact fixture is mandatory')
    result=compute();fixture=json.loads((ROOT/'expected.json').read_text())
    validate(result,fixture);corruptions(result);print(json.dumps(result,sort_keys=True))
