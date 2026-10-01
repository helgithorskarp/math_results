"""Complete exact author checks for reflected-light degree-nine first power.

six-sendov-1, researcher. Standard library, Python3.10+. This checks
the new finite arithmetic and examples, not the cited polar premise
or all ordinary analytic deductions. No assert statement is used.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod,lcm,comb
import importlib.util,json,hashlib,copy,sys
ROOT=Path(__file__).resolve().parent
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/file)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out);return out
A=module('reflection_algebra','algebra.py')
B=module('reflection_certificate','certificate.py')
K=module('reflection_kernel','kernel.py')
def require(ok,message):
    if not ok:raise ArithmeticError(message)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def phash(p):return digest(A.canonical(p))
def evaluator(p):
    den=lcm(*(v.denominator for v in p.values()));terms=[(e,int(v*den)) for e,v in p.items()]
    deg=[max(e[i] for e in p) for i in range(4)]
    def calc(q):
        common=prod(q[i].denominator**deg[i] for i in range(4))
        pw=[[q[i].numerator**j*q[i].denominator**(deg[i]-j) for j in range(deg[i]+1)] for i in range(4)]
        return F(sum(v*prod(pw[i][e[i]] for i in range(4)) for e,v in terms),den*common)
    return calc

def certificates(data):
    rows=[]
    for label in ['nearer','farther']:
        chart=data['charts'][label];p=chart['margin'];v,d,g=B.bernstein(p)
        require(g==(32,16,8,2) and len(v)==15147,'Incomplete chart tensor')
        require(B.invert(v,d,g)==p,'Complete Bernstein inverse fails')
        require(min(v)>=0,'Negative complete chart coefficient')
        shape=[n+1 for n in g];stride=[prod(shape[i+1:]) for i in range(4)]
        zero={tuple((j//stride[i])%shape[i] for i in range(4)) for j,k in enumerate(v) if not k}
        expected={(32,j,k,l) for j in [0,1] for k in range(9) for l in range(3)}
        require(zero==expected and len(zero)==54,'Full zero support differs')
        require(sum(k>0 for k in v)==15093,'Incomplete strict support')
        rows.append({'chart':label,'degrees':list(g),'count':len(v),'negative':0,
                     'positive':15093,'zero':54,'minimum':'0',
                     'minimum_positive':str(F(min(k for k in v if k>0),d)),
                     'coefficient_sha256':digest([str(F(k,d)) for k in v]),
                     'zero_support_sha256':digest([list(e) for e in sorted(zero)]),
                     'mapped_sha256':phash(chart['mapped']),'margin_sha256':phash(p)})
    require(sum(row['count'] for row in rows)==30294,'Incorrect whole-domain certificate size')
    return rows

def ga(x,y):return (x[0]+y[0],x[1]+y[1])
def gs(x,k):return (x[0]*k,x[1]*k)
def gm(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def gc(x):return (x[0],-x[1])
def gn(x):return x[0]*x[0]+x[1]*x[1]
def gi(x):
    require(gn(x)>0,'Division by zero');return gs(gc(x),1/gn(x))
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
def value(p,z):
    out=(F(0),F(0))
    for c in reversed(p):out=ga(gm(out,z),c)
    return out
def anchored(points,a):
    dp=[gs(c,9) for c in linear_product(points,F(1),F(-1))][::-1]
    p=[(F(0),F(0))]+[gs(c,F(1,j+1)) for j,c in enumerate(dp)]
    p[0]=gs(value(p,(a,F(0))),-1);return p,dp

def cube_controls(data):
    rows=[];nonphysical=0;boundary=0
    raw=evaluator(data['raw']);calc={k:evaluator(data['charts'][k]['margin']) for k in data['charts']}
    # Direct integration in Q[Y]/(Y^2-Y2), independent of polynomial kernel.
    def mulY(p,q,Y2):return (p[0]*q[0]-Y2*p[1]*q[1],p[0]*q[1]+p[1]*q[0])
    for label in ['nearer','farther']:
      for b in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
       for y in [F(0),F(1,2),F(1)]:
        r=1+b*y/(3*(1+b)) if label=='nearer' else 1-b*y/(1+b)
        s=4-3*r
        for v in [F(0),F(1,3),F(1)]:
         for w in [F(0),F(1,2),F(1)]:
          x=r-F(4,3)*(1-b)*v;t=s-4*(1-b)*(1-v)*w;c=t/s;Y2=r*r-x*x
          require(Y2>=0 and s>0 and r>=1/(1+b),'Cube normalization/sign bridge fails')
          require(3*r+s==4 and (3*x+t)/4>=b,'Cube mean-loss bridge fails')
          hp=[(F(1),F(0))]
          for _ in range(6):
              out=[(F(0),F(0)) for _ in range(len(hp)+1)]
              for j,q in enumerate(hp):
                  out[j]=ga(out[j],q);out[j+1]=ga(out[j+1],gs(mulY(q,(x,F(1)),Y2),-b))
              hp=out
          out=[(F(0),F(0)) for _ in range(9)]
          for j,q in enumerate(hp):
              for k,z in enumerate([F(1),-2*b*t,b*b*s*s]):out[j+k]=ga(out[j+k],gs(q,z))
          II=tuple(9*sum(q[k]/(j+1) for j,q in enumerate(out)) for k in range(2))
          norm=II[0]**2+Y2*II[1]**2;R=r**12*s**4
          require(raw([b,r,x,t])==norm-R,'Direct quadratic-field origin control fails')
          margin=calc[label]([b,y,v,w])
          require(margin==(1+b)**16*(norm-R-(1-b)) and margin>=0,'Original-to-cube exact margin control fails')
          if not -1<=c<=1:nonphysical+=1
          if b in [0,1]:boundary+=1
          rows.append([label,*map(str,[b,y,v,w,r,s,x,c,norm,R,margin])])
    require(len(rows)==270 and nonphysical>0 and boundary==108,'Cube control inventory fails')
    return {'count':len(rows),'nonphysical_c':nonphysical,'b_faces':boundary,'sha256':digest(rows)}

def gaussian_controls(data):
    units=[(F(1),F(0)),(F(3,5),F(4,5)),(F(3,5),F(-4,5)),
           (F(5,13),F(12,13)),(F(5,13),F(-12,13)),(F(0),F(1)),(F(0),F(-1)),
           (F(-7,25),F(24,25)),(F(-7,25),F(-24,25)),(F(-1),F(0))]
    lights=[(F(1),F(0)),(F(99,101),F(20,101)),(F(3,5),F(4,5)),
            (F(0),F(1)),(F(-3,5),F(4,5)),(F(-1),F(0))]
    raw=evaluator(data['raw']);calc={k:evaluator(data['charts'][k]['margin']) for k in data['charts']}
    rows=[];nonreal=opened=negative_real=0
    for label in ['nearer','farther']:
     for b in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
      for y in [F(0),F(1,2),F(1)]:
       r=1+b*y/(3*(1+b)) if label=='nearer' else 1-b*y/(1+b);s=4-3*r
       for u in units:
        U=gs(u,r);x=U[0]
        for vv in lights:
         c=vv[0];V=gs(vv,s);W=gc(V);mu=(3*x+s*c)/4
         if mu<b:continue
         if b<1:
             v=3*(r-x)/(4*(1-b));remaining=4*(1-b)*(1-v)
             w=s*(1-c)/remaining if remaining else F(0)
             require(0<=v<=1 and 0<=w<=1 and (remaining or c==1),'Inverse loss-map bridge fails')
         else:
             require(x==r and c==1,'Boundary mean saturation fails');v=w=F(0)
         II=integrate([U]*6+[V,W],F(1),-b,F(9));R=r**12*s**4
         require(gn(U)==r*r and gn(V)==gn(W)==s*s,'Exact unit controls fail')
         require(raw([b,r,x,s*c])==gn(II)-R,'Direct eight-factor Gaussian squared norm fails')
         require(calc[label]([b,y,v,w])==(1+b)**16*(gn(II)-R-(1-b)), 'Gaussian map control fails')
         require(gn(II)>=R+(1-b) and R<=1,'Reflected mean-origin controls fail')
         if b==1:require((gn(II)==R)==(y==0),'Complete boundary equality control fails')
         nonreal+=bool(u[1]);opened+=c<1;negative_real+=x<0
         rows.append([label,*map(str,[b,y,v,w,*U,*V,mu,gn(II),R])])
    require(len(rows)>200 and nonreal>50 and opened>50 and negative_real>0,'Insufficient original Gaussian controls')
    return {'count':len(rows),'nonreal_heavy':nonreal,'opened':opened,'negative_heavy_real':negative_real,'sha256':digest(rows)}

def center_tube_controls():
    M=F(7,6)**6
    require(F(201,4)*2*60*M*M<40000,'Analytic center Lipschitz constant fails')
    rows=[];shifted=0
    for b in [F(1,4),F(1,2),F(3,4),F(1)]:
     for label in ['nearer','farther']:
      for y in [F(0),F(1,2),F(1)]:
       r=1+b*y/(3*(1+b)) if label=='nearer' else 1-b*y/(1+b);s=4-3*r
       for u in [(F(1),F(0)),(F(99,101),F(20,101)),(F(3,5),F(4,5))]:
        U=gs(u,r)
        if gn(ga((b,0),gs(gi(U),-1)))>1:continue
        hp=linear_product([U]*6,F(1),-b)
        AA,BB,CC=[tuple(9*b**l*sum(z[k]/(j+l+1) for j,z in enumerate(hp)) for k in range(2)) for l in range(3)]
        require(gn(AA)<=(9*M)**2 and gn(BB)<=(F(9,2)*b*M)**2 and gn(CC)<=(3*b*b*M)**2,'Disk-based moment modulus control fails')
        for vv in [(F(1),F(0)),(F(99,101),F(20,101)),(F(3,5),F(4,5))]:
         c=vv[0]
         for sign in [-1,0,1]:
          q=unit(sign*(1-b)/160000);h2=gn(ga(q,(F(-1),F(0))))
          mu=(3*U[0]+s*c*q[0])/4
          if mu<b:continue
          V=gs(gm(q,vv),s);W=gs(gm(q,gc(vv)),s)
          II=integrate([U]*6+[V,W],F(1),-b,F(9))
          Iref=ga(ga(AA,gs(BB,-2*s*c)),gs(CC,s*s));diff=ga(II,gs(Iref,-1))
          R=r**12*s**4
          require(h2<=((1-b)/80000)**2 and gn(q)==1,'Center tube phase predicate fails')
          require(gn(Iref)<=(F(201,4)*M)**2 and gn(diff)<=(60*M)**2*h2,'Center perturbation bound fails')
          require(gn(Iref)>=R+(1-b) and gn(II)>=R+F(1,2)*(1-b),'Actual center tube origin gap fails')
          shifted+=bool(q[1]);rows.append([label,*map(str,[b,y,*U,c,*q,mu,gn(II),R])])
    require(len(rows)>100 and shifted>50,'Insufficient center tube controls')
    return {'constant':80000,'gap':'(1-b)/2','count':len(rows),'shifted':shifted,'moment_cap':str(M),
            'squared_norm_lipschitz_cap':str(6030*M*M),'sha256':digest(rows)}

def one_example(k):
    half_angle=k
    a=F(1,2);delta=F(1,100);eta=F(1,50)
    H=(a,delta);alpha=unit(k)
    v=gm(alpha,(F(3,5),F(4,5)))
    w=gm(alpha,(F(3,5),F(-4,5)))
    L=ga((a,F(0)),gs(gc(v),-eta))
    LL=ga((a,F(0)),gs(gc(w),-eta))
    points=[H]*6+[L,LL];p,dp=anchored(points,a)
    require(value(p,(a,F(0)))==(0,0) and [gs(p[j+1],j+1) for j in range(9)]==dp,'Example marked root/derivative fails')
    require(any(q[1] for q in p) and gn(ga((a,0),gs(H,-1)))<gn(ga((a,0),gs(L,-1))), 'Nonreal/example distance predicates fail')
    require(gn(ga(L,(F(-1,2),F(0))))==gn(ga(LL,(F(-1,2),F(0))))==eta*eta,'Example equal light distances fail')
    chord2=gn(ga(alpha,(F(-1),F(0))))
    actual_v=gs(gi(ga((a,0),gs(L,-1))),eta)
    actual_w=gs(gi(ga((a,0),gs(LL,-1))),eta)
    require(actual_v==v and actual_w==w and gn(v)==gn(w)==1,
            'Example original unit reciprocals fail')
    require(ga(actual_v,actual_w)==gs(alpha,F(6,5)) and gn(ga(actual_v,actual_w))>0,
            'Example actual nonzero short center fails')
    require(chord2<=((1-a)/80000)**2 and (not k or LL!=gc(L)),'Example nonreflected center sector fails')
    centered_points=[(F(0),delta)]*6+[ga(L,(F(-1,2),F(0))),ga(LL,(F(-1,2),F(0)))]
    q,qdp=anchored(centered_points,F(0))
    translated=[(F(0),F(0)) for _ in range(10)]
    for j,co in enumerate(q):
        for k in range(j+1):translated[k]=ga(translated[k],gs(co,comb(j,k)*(-a)**(j-k)))
    require(translated==p,'Whole centered/original polynomial identity fails')
    radius=F(1,4);tail=sum((abs(z[0])+abs(z[1]))*radius**j for j,z in enumerate(q[:-1]))
    require(q[-1]==(1,0) and tail<radius**9 and a+radius<1,'Exact centered Rouche bound fails')
    ratios=[]
    for m in [F(1,2),F(3,4),F(1)]:
        b=m*a;scaled=[gs(z,m) for z in points]
        pm=[gs(co,m**(9-j)) for j,co in enumerate(p)]
        dpm=[gs(pm[j+1],j+1) for j in range(9)]
        recip=[gi(ga((b,0),gs(z,-1))) for z in scaled]
        I=integrate(recip,F(1),-b,F(9));recprod=(F(1),F(0))
        for z in recip:recprod=gm(recprod,z)
        origin=gs(gm(pm[0],recprod),-1/b)
        require(I==origin and value(pm,(b,0))==(0,0),'Scaled origin communication fails')
        N=gn(I)/prod(gn(z) for z in recip)
        require(N==m**16*gn(p[0])/(a*a),'Exact m16 origin normalization fails')
        polar=integrate(recip,b,1-b*b)
        target=gs(gm(value(pm,(1/b,0)),gi(value(dpm,(b,0)))),b**9/(1-b*b))
        require(polar==target and gn(polar)>=1,'Scaled polar communication fails')
        # The p''/p' = 2q'/q identity at a marked simple root.
        d2=[gs(dpm[j+1],j+1) for j in range(8)]
        qmono=[(F(0),F(0)) for _ in range(9)]
        qmono[8]=pm[9]
        for j in range(7,-1,-1):qmono[j]=ga(pm[j+1],gs(qmono[j+1],b))
        qprime=[gs(qmono[j+1],j+1) for j in range(8)]
        require(gm(value(d2,(b,0)),gi(value(dpm,(b,0))))==gs(gm(value(qprime,(b,0)),gi(value(qmono,(b,0)))),2),
                'Boundary reciprocal identity fails')
        ratios.append(list(map(str,[m,b,N,*polar])))
    return {'a':str(a),'H':list(map(str,H)),'L1':list(map(str,L)),'L2':list(map(str,LL)),
            'heavy_unit_real':'0','old_cone_required_real':str(a*(4+3*a)/(3+4*a)),
            'center_halfangle':str(half_angle),'center_chord_squared':str(chord2),
            'light_opening_cosine':'3/5','actual_unit_sum_norm_squared':'36/25',
            'centered_rouche_radius':str(radius),'centered_rouche_tail':str(tail),
            'centered_rouche_leading_bound':str(radius**9),
            'original_coefficients_sha256':digest([[str(x),str(y)] for x,y in p]),
            'communication_scalings':len(ratios),'communication_sha256':digest(ratios)}

def examples_and_communication():
    # The original antipodal illustration had no short center; reject it.
    alpha=unit(F(1,1000000));v=gm(alpha,(F(0),F(1)));w=gs(v,-1)
    require(gn(ga(v,w))==0 and ga(v,w)!=gs(alpha,F(6,5)),
            'Antipodal invalid-center control unexpectedly passes')
    return [one_example(k) for k in [F(0),F(1,1000000)]]

def compute():
    data=K.build(A,require);rows=certificates(data)
    return {'result':'PASS','author':'six-sendov-1','role':'researcher',
            'new_certified_sign_coefficients':30294,'positive_coefficients':30186,'zero_coefficients':108,
            'raw_terms':len(data['raw']),'phase_terms':len(data['phase']),'loss_terms':len(data['loss']),
            'raw_sha256':phash(data['raw']),'loss_sha256':phash(data['loss']),
            'origin_gap':'1-b','radius_clear':16,'charts':rows,
            'cube_controls':cube_controls(data),'gaussian_controls':gaussian_controls(data),
            'center_tube':center_tube_controls(),
            'example_and_communication':examples_and_communication()}

def validate_fixture(fresh,fixture):
    require(isinstance(fixture,dict) and fixture==fresh,'Compact expected proof record mismatch')

def corruptions(fresh):
    changes=[('new_certified_sign_coefficients',lambda x:x+1),('positive_coefficients',lambda x:x-1),
             ('zero_coefficients',lambda x:x-1),('origin_gap',lambda x:'0'),('radius_clear',lambda x:x-1),
             ('raw_sha256',lambda x:'0'*64),('loss_sha256',lambda x:'0'*64),
             ('charts',lambda x:[{**x[0],'zero':53},x[1]]),
             ('charts',lambda x:[x[0],{**x[1],'coefficient_sha256':'0'*64}]),
             ('cube_controls',lambda x:{**x,'nonphysical_c':0}),
             ('gaussian_controls',lambda x:{**x,'nonreal_heavy':0}),
             ('example_and_communication',lambda x:[{**x[0],'communication_sha256':'0'*64},x[1]]),
             ('center_tube',lambda x:{**x,'constant':79999})]
    rejected=0
    for key,fn in changes:
        bad=copy.deepcopy(fresh);bad[key]=fn(bad[key])
        try:validate_fixture(fresh,bad)
        except ArithmeticError:rejected+=1
        else:raise ArithmeticError('Changed proof fixture accepted')
    require(rejected==13,'Corrupt fixture inventory failed');return rejected

def main():
    fresh=compute();fixture=json.loads((ROOT/'expected.json').read_text());validate_fixture(fresh,fixture)
    fresh={**fresh,'rejected_corruptions':corruptions(fresh)}
    print(json.dumps(fresh,sort_keys=True,indent=2))
if __name__=='__main__':main()
