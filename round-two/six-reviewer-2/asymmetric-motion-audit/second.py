"""Fresh two-generator field; direct derivative-product integration and residual audit.
Imports no primary algebra/generator or producer source. Python stdlib only.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys

def require(ok,why):
    if not ok:raise ValueError(why)

class H:
    __slots__=('a',)
    def __init__(self,x=0):
        if isinstance(x,H):self.a=x.a
        elif isinstance(x,(list,tuple)):
            require(len(x)==12,'second complete twelve basis');self.a=tuple(map(F,x))
        else:self.a=(F(x),)+(F(0),)*11
    def __bool__(self):return any(self.a)
    def __eq__(self,o):
        if not isinstance(o,(H,int,F,list,tuple)):return NotImplemented
        return self.a==H(o).a
    def __add__(self,o):
        if not isinstance(o,(H,int,F,list,tuple)):return NotImplemented
        return H(tuple(a+b for a,b in zip(self.a,H(o).a)))
    __radd__=__add__
    def __neg__(self):return H(tuple(-a for a in self.a))
    def __sub__(self,o):
        if not isinstance(o,(H,int,F,list,tuple)):return NotImplemented
        return self+-H(o)
    def __rsub__(self,o):return H(o)+-self
    def __mul__(self,o):
        if not isinstance(o,(H,int,F,list,tuple)):return NotImplemented
        o=H(o);acc=[[F(0)]*11 for _ in range(2)]
        for i,a in enumerate(self.a):
            if not a:continue
            for j,b in enumerate(o.a):
                if b:
                    ie=i//6+j//6;we=i%6+j%6
                    acc[ie%2][we]+=a*b*((-1)**(ie//2))
        for z in acc:
            for d in range(10,5,-1):z[d-3]-=z[d];z[d-6]-=z[d]
        return H(tuple(acc[0][:6]+acc[1][:6]))
    __rmul__=__mul__
    def __truediv__(self,n):return self*F(1,n)
    def __pow__(self,n):
        require(type(n)is int and n>=0,'second exponent');ans=H(1)
        for _ in range(n):ans=ans*self
        return ans
    def conj(self):return sum((a*((W**8)**(j%6))*((-J)**(j//6))for j,a in enumerate(self.a)),H())
    def enc(self):return list(map(str,self.a))
W=H((0,1)+(0,)*10);J=H((0,)*6+(1,)+(0,)*5)
T=J*(W**7);c=-(W**4+W**5)/2;d=2*c*c-1
require(W**9==1 and W**6+W**3+1==0 and J*J==-1,'second defining field')
require(T**12-T**6+1==0 and T**4==W and T**9==J,'exact representation homomorphism')
IMAGES=[T**j for j in range(12)]
# Rational Gaussian rank guarantees no coefficient information was discarded.
matrix=[[IMAGES[col].a[row]for col in range(12)]for row in range(12)]
rank=0
for col in range(12):
    pivot=next((j for j in range(rank,12)if matrix[j][col]),None)
    if pivot is None:continue
    matrix[rank],matrix[pivot]=matrix[pivot],matrix[rank]
    q=matrix[rank][col];matrix[rank]=[x/q for x in matrix[rank]]
    for j in range(12):
        if j!=rank:
            q=matrix[j][col];matrix[j]=[x-q*y for x,y in zip(matrix[j],matrix[rank])]
    rank+=1
require(rank==12,'representation bridge full rank12')

class R:
    __slots__=('v',)
    def __init__(self,x=0):
        if isinstance(x,R):self.v=x.v.copy()
        elif isinstance(x,dict):self.v={k:H(v)for k,v in x.items()if H(v)}
        else:self.v={(0,0):H(x)}if H(x)else{}
    def __bool__(self):return bool(self.v)
    def __eq__(self,o):return self.v==R(o).v
    def __add__(self,o):
        ans=self.v.copy()
        for k,v in R(o).v.items():ans[k]=ans.get(k,H())+v
        return R(ans)
    __radd__=__add__
    def __neg__(self):return R({k:-v for k,v in self.v.items()})
    def __sub__(self,o):return self+-R(o)
    def __rsub__(self,o):return R(o)+-self
    def __mul__(self,o):
        ans={}
        for k,v in self.v.items():
            for h,b in R(o).v.items():
                e=(k[0]+h[0],k[1]+h[1]);ans[e]=ans.get(e,H())+v*b
        return R(ans)
    __rmul__=__mul__
    def __truediv__(self,n):return self*F(1,n)
    def conj(self):return R({k:v.conj()for k,v in self.v.items()})
    def at(self,m,b):return sum((v*(m**k)*(b**l)for(k,l),v in self.v.items()),H())
    def enc(self):
        require(set(self.v)<={(0,0),(1,0),(0,1)},'second affine full map')
        return[self.v.get(k,H()).enc()for k in [(0,0),(1,0),(0,1)]]
P=R({(1,0):1});B=R({(0,1):1})

def const(x):return[R(x)]+[R()for _ in range(4)]
def plus(a,b):return[x+y for x,y in zip(a,b)]
def times(a,b):return[sum((a[j]*b[n-j]for j in range(n+1)),R())for n in range(5)]
def mulnum(a,k):return[x*k for x in a]
def bar(a):return[x.conj()for x in a]
def se(a):return[x.enc()for x in a]
def hf(v):
    require(type(v)is list and len(v)==12,'input whole field row')
    require(all(type(x)is str and str(F(x))==x for x in v),'canonical exact rational row')
    return sum((F(x)*h for x,h in zip(v,IMAGES)),H())
def rf(v):
    require(type(v)is list and len(v)==3,'input all affine columns')
    return R({k:hf(a)for k,a in zip([(0,0),(1,0),(0,1)],v)})
def sf(v):
    require(type(v)is list and len(v)==5,'input all jet orders')
    return[rf(x)for x in v]
def collection(v,n):
    require(type(v)is list and len(v)==n,'input every physical label')
    return[sf(x)for x in v]
def check(v):
    fields={'status','field','basis_degrees','parameter_monomials','polynomial_z_degrees','s_degrees','whole_polynomial','critical_mean','critical_large','critical_small','anchor','all_nine_roots','all_nine_half_normals','whole_first_objective','second_objective_affine','closing_parameters','closing_second_coefficient','repair_domain','embedding_c_bracket','counts'}
    require(type(v)is dict and set(v)==fields,'complete record schema')
    require(v['status']=='COMPLETE_INDEPENDENT_CYCLOTOMIC36_JETS' and v['field']=='QQ[T]/(T^12-T^6+1),T=exp(pi*i/18)','declared primary representation')
    require(v['basis_degrees']==list(range(12))and v['s_degrees']==list(range(5))and v['polynomial_z_degrees']==list(range(10))and v['parameter_monomials']==[[0,0],[1,0],[0,1]],'whole basis orders')
    require(v['counts']=={'active_normals':4,'critical_multiplicities':[1,7],'field_coordinates':12,'free_real_parameters':2,'individual_normals':9,'jet_orders':5,'original_jets':9,'primitive_coefficients':10},'whole counts')
    iv=(8*c*c-8*c+2)/3;cv=(4*c*c+2*c-2)*iv/3
    require((1+c)*iv==1 and (c+d)*cv==1,'second scalar inverse identities')
    lam=12*(1+c);k=-7*(1+2*c)/18;g=48*k;x=F(2,3)-iv/3
    mean=[R(),R(),R(-x*lam),R(J*g),P]
    small=plus(mean,[R(),R(-J),R(-6*k),-J*B,R()]);large=plus(mean,[R(),R(7*J),R(42*k),7*J*B,R()])
    anchor=[R(1),R(),R(-lam),R(),R()]
    require(sf(v['critical_mean'])==mean and sf(v['critical_small'])==small and sf(v['critical_large'])==large and sf(v['anchor'])==anchor,'all original family coefficients')
    # Multiply eight linear factors, then integrate, then subtract value at a.
    dp=[const(1)]
    for zeta in [large]+[small]*7:
        ans=[const(0)for _ in range(len(dp)+1)]
        for j,a in enumerate(dp):
            ans[j]=plus(ans[j],times(a,mulnum(zeta,-1)))
            ans[j+1]=plus(ans[j+1],a)
        dp=ans
    poly=[const(0)]+[mulnum(a,F(9,j+1))for j,a in enumerate(dp)]
    def horner(coefs,z):
        acc=const(0)
        for a in reversed(coefs):acc=plus(times(acc,z),a)
        return acc
    poly[0]=mulnum(horner(poly,anchor),-1)
    require(collection(v['whole_polynomial'],10)==poly,'all direct product/integration polynomial columns')
    roots=collection(v['all_nine_roots'],9);normals=collection(v['all_nine_half_normals'],9)
    for j,z in enumerate(roots):
        require(z[0]==R(W**j)and z[1]==0,'every root label and linear zero')
        require(horner(poly,z)==const(0),'every full formal root residual')
        n=mulnum(plus(times(z,bar(z)),const(-1)),F(1,2))
        require(n==normals[j],'every root curvature and individual normal')
        require([((-1)**n)*r for n,r in enumerate(z)]==bar(roots[(-j)%9]),'all nine full conjugate parity')
    require(roots[0]==anchor,'marked anchor is actual branch')
    # D*u^2=1 recursively, entirely independent of binomial formula.
    objective=const(0)
    for zeta,weight in [(large,1),(small,7)]:
        diff=plus(anchor,mulnum(zeta,-1));dist=times(diff,bar(diff));require(dist[0]==1,'actual distance constant')
        inv=const(1)
        for n in range(1,5):inv[n]=-times(dist,times(inv,inv))[n]/2
        require(times(dist,times(inv,inv))==const(1),'all inverse-square-root coefficients')
        objective=plus(objective,mulnum(inv,weight))
    require(sf(v['whole_first_objective'])==objective,'full original first-power objective')
    K=objective[4]*(iv*iv/144);require(rf(v['second_objective_affine'])==K,'physical eta conversion whole objective')
    require(objective[1]==0 and objective[3]==0,'actual objective even jet')
    mstar=-(512+1684*c+1328*c*c)/9;bstar=(86-261*c-172*c*c)/18
    require(type(v['closing_parameters'])is list and len(v['closing_parameters'])==2 and list(map(hf,v['closing_parameters']))==[mstar,bstar],'displayed physical parameters')
    target=(19935+47482*c-62948*c*c)/972
    require(hf(v['closing_second_coefficient'])==target and K.at(mstar,bstar)==target,'displayed entire second coefficient')
    active=[3,4,5,6]
    for j in active:require(normals[j][2]==0 and normals[j][3]==0 and normals[j][4].at(mstar,bstar)==-1,'each of four active constraints')
    for j in [3,6]:require(roots[j][3]==R(-3*J*g*(W**j)),'both cube motions')
    r=v['repair_domain'];require(set(r)=={'normal3_affine','normal4_affine','determinant','positive_dual_weights','infimum_second_objective','zero_normal_parameters','closed_to_zero_shifts'},'complete repair domain schema')
    n3,n4=normals[3][4],normals[4][4];w4=cv;w3=F(2,3)*(7-(1-d)*cv)
    require(rf(r['normal3_affine'])==n3 and rf(r['normal4_affine'])==n4 and hf(r['determinant'])==12*(c+d),'all affine normal rows and invertibility')
    require(list(map(hf,r['positive_dual_weights']))==[w3,w4],'dual weights')
    inf=K+(w3*n3+w4*n4)*(iv*iv/144)
    require(set(inf.v)<={(0,0)}and rf(r['infimum_second_objective'])==inf,'entire dual equality including zero parameter columns')
    require(inf.at(0,0)==H(F(6653,324))+F(23915,486)*c-F(15839,243)*c*c,'explicit real-cubic repair infimum')
    require(w3==H(F(52,9))-F(4,9)*c-F(8,9)*c*c and w4==H(-F(2,3))+F(4,3)*c,'explicit real-cubic dual weights')
    dm=-(1+2*d)*cv/3;db=(2*c-1)*cv/24;m0=mstar+dm;b0=bstar+db
    require(list(map(hf,r['closed_to_zero_shifts']))==[dm,db]and list(map(hf,r['zero_normal_parameters']))==[m0,b0],'unique intersection parameters')
    require(n3.at(m0,b0)==0 and n4.at(m0,b0)==0 and K.at(m0,b0)==inf.at(0,0),'zero-normal boundary')
    repairs=[]
    for kap in [F(1,2),F(1),F(2)]:
        m=m0-kap*dm;b=b0-kap*db
        require(n3.at(m,b)==-kap and n4.at(m,b)==-kap,'multiple positive repair slacks')
        require(K.at(m,b)==inf.at(0,0)+kap*(w3+w4)*iv*iv/144,'multiple exact repaired objective')
        repairs.append({'equal_slack':str(kap),'M':m.enc(),'beta':b.enc(),'K':K.at(m,b).enc()})
    require(v['embedding_c_bracket']==['15/16','47/50'],'physical scalar interval')
    def cubic(q):return 8*q**3-6*q-1
    lo=F(15,16);hi=F(47,50)
    require(cubic(lo)==-F(17,512)and cubic(hi)==F(73,15625)and lo*lo>F(3,4),'physical strictly monotone real cubic isolation')
    # Ordinary physical sign proof: c,d positive, c+d>0 and 0<(1-d)/(c+d)<1.
    require(2*lo*lo-1>0 and 2*lo*lo+lo-2>0,'positive dual weights')
    klo=(19935+47482*hi-62948*hi*hi)/972;khi=(19935+47482*lo-62948*lo*lo)/972
    require(47482-125896*lo<0 and 9<klo<khi<10,'target objective strict bounds')
    increment_bound=F(16,3)/(12*(1+lo))**2
    require(9<klo-increment_bound and khi+increment_bound<10,'all three positive repairs have9<K<10')
    return {'status':'COMPLETE_DIRECT_FACTOR_RESIDUAL_AUDIT','basis':'W^0..W^5,IW^0..IW^5; W6+W3+1=0,I2=-1','bridge_rank':rank,'full_polynomial':[se(a)for a in poly],'full_original_roots':[se(z)for z in roots],'full_normals':[se(n)for n in normals],'full_objective':se(objective),'normal_rows':[n3.enc(),n4.enc()],'objective_infimum':inf.enc(),'dual_weights':[w3.enc(),w4.enc()],'positive_repair_checks':repairs,'closed_K_bounds':[str(klo),str(khi)],'three_repair_K_bounds':[str(klo-increment_bound),str(khi+increment_bound)],'real_cubic_infimum_coefficients':['6653/324','23915/486','-15839/243'],'checks':'all10 polynomial coefficients/all5 orders/all12 coordinates/all3 parameter columns, all9 residuals/normals/parities, actual8 critical factors/objective and full affine repair dual'}
if __name__=='__main__':
    require(len(sys.argv)==2,'usage: second.py PRIMARY.json')
    print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())),sort_keys=True,separators=(',',':')))
