"""Exact author evidence for equal-radius light opening in a heavy cone.

Author six-sendov-1, researcher. Python3.10+ standard library only.
This proves fresh finite signs/identities, not the two prior mathematical
premises or the ordinary analytic deductions. Gaussian/control patterns
retain the a729b0d source attribution in LITERATURE.md.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod,lcm
import importlib.util,hashlib,json,copy,sys
ROOT=Path(__file__).resolve().parent

def module(n,file):
    s=importlib.util.spec_from_file_location(n,ROOT/file)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=module('equal_light_algebra','algebra.py')
B=module('equal_light_certificate','certificate.py')
K=module('equal_light_kernel','kernel.py')
def require(x,msg):
    if not x:raise ArithmeticError(msg)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def phash(p):return digest(A.canonical(p))

PATHS=[[(0,0)],[(0,1),(2,1)],[(0,1),(2,0),(0,1)],
       [(0,1),(2,0),(0,0),(2,1)],[(0,1),(2,0),(0,0),(2,0),(0,0)],
       [(0,1),(2,0),(0,0),(2,0),(0,1)]]

def certificates(data):
    p=data['margin'];v,d,g=B.bernstein(p)
    require(g==(28,14,6,0) and len(v)==3045,'Wrong complete tensor inventory')
    require(B.invert(v,d,g)==p,'Complete global inverse fails')
    leaves={tuple(path) for path in PATHS}
    def cover(prefix):
        if prefix in leaves:return 1
        descendants=[q for q in leaves if q[:len(prefix)]==prefix]
        require(descendants,'Incomplete subdivision cover')
        axes={q[len(prefix)][0] for q in descendants}
        require(len(axes)==1,'Inconsistent split axis')
        axis=axes.pop()
        return cover(prefix+((axis,0),))+cover(prefix+((axis,1),))
    require(cover(())==6,'Incorrect leaf count')
    rows=[];volume=F(0);fraction_refs=0
    for path in PATHS:
        cv,cd=v,d;box=[(F(0),F(1)) for _ in range(4)]
        for axis,side in path:
            cv,cd=B.split(cv,cd,g,axis)[side]
            lo,hi=box[axis];mid=(lo+hi)/2;box[axis]=(lo,mid) if side==0 else (mid,hi)
        require(len(cv)==prod(x+1 for x in g) and min(cv)>0,'Missing or nonpositive complete cell coefficient')
        direct=p
        for axis,(lo,hi) in enumerate(box):
            if (lo,hi)!=(0,1):
                ref=B.affine_cell(direct,axis,lo,hi)
                direct=B.affine_cell_integer(direct,axis,lo,hi)
                require(ref==direct,'Complete Fraction/integer affine identity fails')
                fraction_refs+=1
        require(B.invert(cv,cd,g)==direct,'Complete cell inverse fails')
        av,ad,ag=B.bernstein(direct,g)
        require(ag==g and len(av)==len(cv) and all(x*ad==y*cd for x,y in zip(cv,av)),
                'Complete affine/de Casteljau entry comparison fails')
        volume+=prod(hi-lo for lo,hi in box)
        rows.append({'path':[list(x) for x in path],'b':list(map(str,box[0])),
             'y':list(map(str,box[1])),'z':list(map(str,box[2])),'degrees':list(g),
             'coefficients':len(cv),'minimum':str(F(min(cv),cd)),
             'sha256':digest([str(F(x,cd)) for x in cv])})
    require(volume==1 and sum(q['coefficients'] for q in rows)==18270,'Incomplete exact closed cover')
    require(fraction_refs==11,'Wrong complete affine reference inventory')
    return rows,fraction_refs

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
    require(gn(x)>0,'Gaussian division by zero');return gs(gc(x),1/gn(x))
def unit(k):return ((1-k*k)/(1+k*k),2*k/(1+k*k))

def linear_product(points,offset,slope):
    out=[(F(1),F(0))]
    for z in points:
        new=[(F(0),F(0)) for _ in range(len(out)+1)]
        for j,c in enumerate(out):
            new[j]=ga(new[j],gs(c,offset));new[j+1]=ga(new[j+1],gs(gm(c,z),slope))
        out=new
    return out
def integrate(points,offset,slope,weight=F(1)):
    p=linear_product(points,offset,slope)
    return tuple(weight*sum(c[k]/(j+1) for j,c in enumerate(p)) for k in range(2))
def moments(b,U):
    p=linear_product([U]*6,F(1),-b)
    return [tuple(9*b**l*sum(c[k]/(j+l+1) for j,c in enumerate(p)) for k in range(2)) for l in range(3)]

def evaluator(p):
    den=lcm(*(v.denominator for v in p.values()));terms=[(e,int(v*den)) for e,v in p.items()]
    degrees=[max(e[i] for e in p) for i in range(4)]
    def calc(values):
        common=prod(values[i].denominator**degrees[i] for i in range(4))
        pw=[[values[i].numerator**j*values[i].denominator**(degrees[i]-j)
              for j in range(degrees[i]+1)] for i in range(4)]
        return F(sum(v*prod(pw[i][e[i]] for i in range(4)) for e,v in terms),den*common)
    return calc

def origin_controls(data):
    evalT=evaluator(data['T']);evalQ=evaluator(data['margin']);evaltb=evaluator(data['T_over_b'])
    rows=[];nonreal=0;opened=0;shifted=0;mean_eligible=0;faces=0
    units=[(F(1),F(0)),(F(99,101),F(20,101)),(F(99,101),F(-20,101)),
           (F(3,5),F(4,5)),(F(3,5),F(-4,5)),(F(5,13),F(12,13)),(F(5,13),F(-12,13))]
    centers=[(F(1),F(0)),unit(F(1,100000)),unit(F(-1,100000))]
    halfangles=[(F(1),F(0)),(F(99,101),F(20,101)),(F(3,5),F(4,5)),
                (F(5,13),F(12,13)),(F(0),F(1))]
    for b in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
      for y in [F(0),F(1,2),F(1)]:
        r=1+b*y/(3*(1+b));s=4-3*r
        for u in units:
          U=gs(u,r);x=U[0]
          if x<r-(1-b):continue
          z=1-(r-x)/(1-b) if b<1 else F(0)
          require(0<=z<=1 and gn(U)==r*r,'Original heavy cone bridge fails')
          AA,BB,CC=moments(b,U);Ione=ga(ga(AA,gs(BB,-2*s)),gs(CC,s*s))
          Tone=gm(BB,gc(Ione))[0]
          require(evalT([b,r,x,F(0)])==Tone,'Original reflection Gram control fails')
          require(Tone>=b/128,'Original reflection sign fails')
          tb=evaltb([b,r,x,F(0)])
          require((b==0 and tb==F(81,2)) or (b>0 and b*tb==Tone),'Exact b quotient fails')
          require(evalQ([b,y,z,F(0)])==(1+b)**14*(tb-F(1,128)),'Original-to-cube margin control fails')
          require(gn(AA)<=81 and gn(BB)<=(9*b/2)**2 and gn(CC)<=(3*b*b)**2,'Moment modulus controls fail')
          require(r**12*s**4<=1 and s>=F(1,2),'Normalization denominator controls fail')
          for q in centers:
            h2=gn(ga(q,(F(-1),F(0))));require(gn(q)==1 and h2<=F(1,13824)**2,'Center predicate fails')
            D=ga(gm(BB,gc(AA)),gs(gm(gc(BB),CC),s*s))
            I1=ga(ga(AA,gs(gm(q,BB),-2*s)),gs(gm(gp(q,2),CC),s*s))
            T=gm(gm(q,BB),gc(I1))[0]
            require(T==gm(q,D)[0]-2*s*gn(BB) and gn(D)<=(54*b)**2,'Center Gram/modulus identity fails')
            require(T>=b/256,'Robust center sign control fails')
            require(I1==integrate([U]*6+[gs(q,s)]*2,F(1),-b,F(9)),'Direct merged eight-factor identity fails')
            N1=gn(I1)/(r**12*s**4)
            for c,h in halfangles:
              require(c*c+h*h==1 and 0<=c<=1,'Halfangle first signs fail')
              v=gm(q,(c,h));w=gm(q,(c,-h))
              require(ga(v,w)==gs(q,2*c) and gm(v,w)==gp(q,2),'Full phase pair identities fail')
              Ic=ga(ga(AA,gs(gm(q,BB),-2*s*c)),gs(gm(gp(q,2),CC),s*s))
              require(Ic==integrate([U]*6+[gs(v,s),gs(w,s)],F(1),-b,F(9)),'Direct opened eight-factor identity fails')
              diff=gn(Ic)-gn(I1)
              require(diff==4*s*(1-c)*T+4*s*s*(1-c)**2*gn(BB),'Exact opening norm identity fails')
              N=gn(Ic)/(r**12*s**4)
              require(N-N1>=b*(1-c)/128,'Uniform robust opening gain control fails')
              if q==(F(1),F(0)):require(N-N1>=b*(1-c)/64,'Reflection opening gain control fails')
              mu=(6*x+s*v[0]+s*w[0])/8
              merged=(6*x+2*s*q[0])/8
              require(merged>=mu,'Signed merged real mean control fails')
              if merged>=b:
                require(N1>=1 and (b==1 or N1>1),'Control conflicts with cited6+2 premise')
                mean_eligible+=1
              if u[1]:nonreal+=1
              if c<1:opened+=1
              if q[1]:shifted+=1
              if b in [0,1]:faces+=1
              rows.append(list(map(str,[b,y,z,r,s,*u,*q,c,h,T,N1,N,mu,merged])))
    require(len(rows)>500 and nonreal>100 and opened>300 and shifted>300 and faces>100,'Insufficient complete signed controls')
    return {'original_controls':len(rows),'nonreal_heavy_controls':nonreal,'opened_controls':opened,
            'shifted_center_controls':shifted,'eligible_merged_mean_controls':mean_eligible,
            'b_face_controls':faces,'sha256':digest(rows)}

def analytic_identities():
    b,r=[A.variable(i) for i in range(2)]
    heavy=A.add(A.ONE,A.scale(A.mul(b,r),-2),A.scale(A.mul(b,A.add(A.ONE,A.scale(b,-1))),2),
                A.mul(A.power(b,2),A.power(r,2)))
    e0=K.substitute(A,heavy,1,A.ONE)
    e1=K.substitute(A,heavy,1,A.scale(A.ONE,F(7,6)))
    require(e0==A.add(A.ONE,A.scale(A.power(b,2),-1)),'First complete heavy modulus endpoint identity fails')
    require(e1==A.add(A.ONE,A.scale(b,F(-1,3)),A.scale(A.power(b,2),F(-23,36))),
            'Second complete heavy modulus endpoint identity fails')
    cone=A.add(A.mul(A.add(A.ONE,A.scale(b,6)),A.add(A.scale(A.ONE,3),A.scale(b,4))),
               A.scale(A.mul(b,A.add(A.scale(A.ONE,4),A.scale(b,3))),-7))
    require(cone==A.scale(A.power(A.add(A.ONE,A.scale(b,-1)),2),3),'Simpler cone sufficiency identity fails')
    require(54*256==13824 and F(1,128)-F(54,13824)==F(1,256),'Uniform center constants fail')
    return {'heavy_endpoint_sha256':[phash(e0),phash(e1)],'cone_identity_sha256':phash(cone),
            'robust_center_constant':'1/13824','reflection_gain':'1/64','robust_gain':'1/128'}

def poly_value(p,x):
    out=(F(0),F(0))
    for c in reversed(p):out=ga(gm(out,x),c)
    return out
def anchored(points,a):
    dp=[gs(c,9) for c in linear_product(points,F(1),F(-1))][::-1]
    p=[(F(0),F(0))]+[gs(c,F(1,j+1)) for j,c in enumerate(dp)]
    p[0]=gs(poly_value(p,(a,F(0))),-1);return p,dp

def examples_and_barrier():
    a=F(19,20);H=(F(1,100),F(1,1000));L1=(F(-1,100),F(1,4));L2=gc(L1)
    hd=gn(ga((a,F(0)),gs(H,-1)));ld=gn(ga((a,F(0)),gs(L1,-1)))
    cone=a*(4+3*a)/(3+4*a)
    require(hd<ld and a-H[0]>0 and (a-H[0])**2>=cone**2*hd,'Example original cone/heavy predicates fail')
    U=gi(ga((a,F(0)),gs(H,-1)));V=gi(ga((a,F(0)),gs(L1,-1)));W=gi(ga((a,F(0)),gs(L2,-1)))
    lightchord=gn(ga(V,gs(W,-1)))/gn(V)
    require(lightchord>F(1,4),'Example half-angle opening is too small')
    examples=[];scale_rows=[]
    for k in [F(0),F(1,100000)]:
        alpha=unit(k);Vnew=gm(alpha,V);Wnew=gm(alpha,W)
        E1=ga((a,F(0)),gs(gi(Vnew),-1));E2=ga((a,F(0)),gs(gi(Wnew),-1))
        require(gn(Vnew)==gn(Wnew)==gn(V),'Original equal-radius example fails')
        require(ga(Vnew,Wnew)==gs(alpha,2*V[0]) and V[0]>0,'Signed center direction fails')
        h2=gn(ga(alpha,(F(-1),F(0))));require(h2<=F(1,13824)**2,'Shifted example center predicate fails')
        points=[H]*6+[E1,E2];p,dp=anchored(points,a)
        require(poly_value(p,(a,F(0)))==(0,0) and [gs(p[j+1],j+1) for j in range(9)]==dp,'Full example polynomial/derivative fails')
        require(poly_value(dp,(a,F(0)))!=(0,0),'Example marked root is not simple')
        require(len({H,E1,E2})==3 and H[1] and p[8][1],'Example stays in the old radial/real locus')
        if k:require(E2!=gc(E1),'Shifted example remains reflected')
        bound=sum(abs(q[0])+abs(q[1]) for q in p[:-1]);require(bound<1,'Exact example Rouche bound fails')
        integral=integrate([U]*6+[Vnew,Wnew],F(1),-a,F(9))
        product=gm(gp(U,6),gm(Vnew,Wnew))
        require(gm(integral,gi(product))==gs(p[0],-1/a),'Original example origin identity fails')
        polar=integrate([U]*6+[Vnew,Wnew],a,1-a*a)
        rhs=gs(gm(gs(poly_value(p,(1/a,F(0))),a/(1-a*a)),gi(poly_value(dp,(a,F(0))))),a**8)
        require(polar==rhs,'Original example polar identity fails')
        for m in [F(1,3),F(2,3),F(1)]:
            scaled,sd=anchored([gs(z,m) for z in points],a*m)
            require(scaled==[gs(q,m**(9-j)) for j,q in enumerate(p)] and
                    sd==[gs(q,m**(8-j)) for j,q in enumerate(dp)],'Full example scaling fails')
            scale_rows.append([str(k),str(m),[[str(x) for x in q] for q in scaled]])
        examples.append({'k':str(k),'heavy':list(map(str,H)),'lights':[list(map(str,E1)),list(map(str,E2))],
          'rouche_l1_bound':str(bound),'center_chord_squared':str(h2),
          'polynomial_sha256':digest([[str(x) for x in q] for q in p])})
    b=F(1,2);r=F(501,500);s=4-3*r;u=(F(33,65),F(56,65));q=(F(4,5),F(-3,5));c=F(4,5)
    U=gs(u,r);v=gm(q,(c,F(3,5)));w=gm(q,(c,F(-3,5)));AA,BB,CC=moments(b,U)
    I1=ga(ga(AA,gs(gm(q,BB),-2*s)),gs(gm(gp(q,2),CC),s*s))
    Ic=ga(ga(AA,gs(gm(q,BB),-2*s*c)),gs(gm(gp(q,2),CC),s*s));T=gm(gm(q,BB),gc(I1))[0]
    disks=[gn(ga((b,F(0)),gs(gi(z),-1))) for z in [U,gs(v,s),gs(w,s)]]
    mu=(6*U[0]+s*v[0]+s*w[0])/8;M45=b+(1-b)/(45*b*(1+b))
    weak=T+s*(1-c)*gn(BB);delta=gn(Ic)-gn(I1)
    N=gn(Ic)/(r**12*s**4);N1=gn(I1)/(r**12*s**4)
    require(all(gn(z)==1 for z in [u,q,v,w]) and 6*r+2*s==8 and 1<r<1+b/(3*(1+b)),
            'Barrier normalization/first signs fail')
    require(s>=1/(1+b) and all(z<1 for z in disks) and mu>M45,'Barrier necessary physical predicates fail')
    require(T<0 and weak<0 and delta<0 and N1>N>1,'Barrier claim/scope fails')
    require(delta==4*s*(1-c)*T+4*s*s*(1-c)**2*gn(BB),'Barrier opening identity fails')
    require(Ic==integrate([U]*6+[gs(v,s),gs(w,s)],F(1),-b,F(9)) and
            I1==integrate([U]*6+[gs(q,s)]*2,F(1),-b,F(9)),'Direct barrier integrals fail')
    return {'marked_a':str(a),'heavy_distance_squared':str(hd),'light_distance_squared':str(ld),
       'heavy_cone_floor':str(cone),'light_phase_chord_squared':str(lightchord),
       'examples':examples,'full_scaling_controls':len(scale_rows),'scaling_sha256':digest(scale_rows),
       'opening_barrier':{'b':str(b),'r':str(r),'s':str(s),'u':list(map(str,u)),'q':list(map(str,q)),
         'c':str(c),'v':list(map(str,v)),'w':list(map(str,w)),'disk_squared':list(map(str,disks)),
         'mu':str(mu),'M45':str(M45),'T':str(T),'weaker_sign':str(weak),'opening_difference':str(delta),
         'actual_origin_squared':str(N),'merged_origin_squared':str(N1)}}

def compute():
    data=K.build(A,require);cells,refs=certificates(data)
    return {'result':'PASS','agent':'six-sendov-1','role':'researcher','opening_T_over_b_lower_bound':'1/128',
      'new_certified_sign_coefficients':18270,'clear_D_power':data['clear'],
      'kernel_terms':len(data['T']),'mapped_margin_terms':len(data['margin']),
      'kernel_sha256':phash(data['T']),'margin_sha256':phash(data['margin']),
      'gram_sha256':[phash(p) for p in data['grams']],
      'complete_cells':cells,'complete_fraction_affine_references':refs,
      'origin_controls':origin_controls(data),'analytic_identities':analytic_identities(),
      'examples_and_barrier':examples_and_barrier(),
      'prior_logical_premises_reproved_by_this_checker':False,'rejected_corruptions':11}

def validate(result,fixture):require(result==fixture,'Complete compact fixture mismatch')
def corruptions(result):
    paths=[('new_certified_sign_coefficients',),('opening_T_over_b_lower_bound',),('clear_D_power',),
      ('kernel_sha256',),('margin_sha256',),('complete_cells',0,'minimum'),('complete_cells',5,'sha256'),
      ('origin_controls','nonreal_heavy_controls'),('analytic_identities','robust_center_constant'),
      ('examples_and_barrier','opening_barrier','weaker_sign'),('examples_and_barrier','examples',1,'rouche_l1_bound')]
    for path in paths:
        obj=copy.deepcopy(result);node=obj
        for key in path[:-1]:node=node[key]
        node[path[-1]]='altered'
        try:validate(result,obj)
        except ArithmeticError:continue
        raise ArithmeticError('Altered fixture accepted')
    require(len(paths)==result['rejected_corruptions'],'Wrong corrupted-fixture inventory')

if __name__=='__main__':
    require(len(sys.argv)==1,'No verifier options; compact fixture is mandatory')
    result=compute();fixture=json.loads((ROOT/'expected.json').read_text())
    validate(result,fixture);corruptions(result);print(json.dumps(result,sort_keys=True))
