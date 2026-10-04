"""Own literal epsilon factor, entire symbolic t, and separate original roots.

Written formulas exposed; no target native programs, fixtures or certificates.
Own 10220 cyclotomic engine is credited and extended to epsilon degree nine.
"""
import argparse,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as Q
from math import comb
sys.path.insert(0,str(Path(__file__).resolve().parent))
from algebra import F,R,J,W,I,C,S,zproduct,zeval,inverse_sqrt
from signs import equal,require,bound,ratio,cube_coordinates

def constants():
 y=1/(3*(1+C));x=F(Q(2,3))-y;H=14*y
 k=-7*(1+2*C)/18;rho=(C-5)/3;d=3*k+rho
 uz=-F(Q(37,36))+20*C/9-20*C*C/9;up=uz-rho*H/2
 alpha=-F(Q(527,360))+41*C/90+13*C*C/90
 kappa=(k+rho)**2/2+10*alpha/27
 wstar=F(Q(2512,27))+5840*C/9-21392*C*C/27;w2=wstar/8
 dstar=-F(Q(4270,27))-29492*C/27+4012*C*C/3
 gamma=F(Q(13,36))+1253*C/72-50*C*C/3
 bstar=F(Q(2311,108))+4934*C/27-1976*C*C/9
 tstar=-F(Q(60800959,17496))-307083769*C/17496+10980067*C*C/486
 mu0=-F(Q(17403419,34992))-45702565*C/17496+180635*C*C/54
 mu2=F(Q(35,81))-2086*C/81+616*C*C/27
 beta0=-F(Q(1162307,23328))-5484833*C/11664+52426519*C*C/93312
 beta2=F(Q(14537,1512))-3889*C/756-1661*C*C/756
 beta4=-F(Q(2,49))-4*C/49-2*C*C/49
 nu1=-F(Q(17983,972))-25711*C/486+4564*C*C/81;nu3=F(Q(28,81))+56*C/81
 sigma1=-F(Q(1967,81))+5479*C/432-5375*C*C/162
 sigma3=-F(Q(55,189))+11*C/63+88*C*C/189
 mstar=F(Q(8148040331,629856))+78878749667*C/1259712-51194418673*C*C/629856
 betastar=F(Q(27821775167,17915904))+80418819893*C/8957952-12650091319*C*C/1119744
 gstar=F(Q(183619658945,2519424))+444829186913*C/1259712-288729410449*C*C/629856
 nustar=-F(Q(2424695,13122))-136157*C/4374+144046*C*C/6561
 sigmastar=-F(Q(536333191,1119744))-805399537*C/559872+891296017*C*C/559872
 motionA=-F(Q(13638695,972))-16011613*C/243+20901119*C*C/243
 motionB=S*(1448+6982*C-8224*C*C)/243
 motionQ=F(Q(8,162))+25*C/162+20*C*C/162
 return locals()

def family(damage='none',t=None,repairs=None):
 c=constants();t=R([0,1]) if t is None else R(t)
 e=J([0,1]);eta=e*e;r=e*(t/(3*c['H']))
 mu=c['mu0']+c['mu2']*r*r;beta=c['beta0']+c['beta2']*r*r+c['beta4']*(r**4)
 nu=c['nu1']*r+c['nu3']*(r**3);sigma=c['sigma1']*r+c['sigma3']*(r**3)
 q1=c['gamma']-4*r*r/(3*c['H']);v2=3*c['k']*c['H']*r/7
 M=c['mstar']+(damage=='M');b=c['betastar']+(damage=='beta')
 if repairs is not None:M=M+repairs[0];b=b+repairs[1]
 ns=c['nustar']+(damage=='odd-common');ss=c['sigmastar']+(damage=='odd-pair')
 inward=0 if damage=='no-inward' else 1
 A=(c['uz']-I*r/3)*eta+(c['w2']+I*v2)*(eta**2)+(mu+I*nu)*(eta**3)+(M+I*ns*r)*(eta**4)+inward*(e**9)
 B=(c['up']+I*r)*eta+(c['w2']+I*v2)*(eta**2)+(mu+I*nu)*(eta**3)+(M+I*ns*r)*(eta**4)+inward*(e**9)
 K=I*(1+q1*eta+beta*(eta**2)+b*(eta**3))+c['d']*r*eta+sigma*(eta**2)+ss*r*(eta**3)
 derivative=[J(1)]
 for unused in range(6):derivative=zproduct(derivative,[-A,J(1)])
 pair=[B*B-eta*c['H']/2*K*K,-2*B,J(1)]
 derivative=[9*v for v in zproduct(derivative,pair)]
 if damage=='multiplicity':derivative[8]=J(8)
 primitive=[J()]+[v/(j+1) for j,v in enumerate(derivative)]
 anchor=1-eta if damage!='anchor' else 1-2*eta
 primitive[0]=-zeval(primitive,anchor)
 return c,e,t,A,B,K,derivative,primitive

def packed(r):
 if isinstance(r,F):return [[j,ratio(a)] for j,a in enumerate(r.v) if a]
 if isinstance(r,R):return [[j,packed(a)] for j,a in enumerate(r.v) if a]
 if isinstance(r,J):return [[j,packed(a)] for j,a in enumerate(r.v) if a]
 raise TypeError('exact sparse record')

def core(damage):
 c,e,t,A,B,K,D,p=family(damage);eta=e*e;anchor=1-eta
 equal(W**12-W**6+1,F(),'Phi36');equal(W**18,F(-1),'physical embedding')
 equal(I*I,F(-1),'imaginary unit');equal(C*C+S*S,F(1),'sine cosine')
 equal(8*C**3-6*C-1,F(),'cubic')
 equal(p[9],J(1),'monic');equal(zeval(p,anchor),J(),'entire actual anchor')
 # Separate elementary-symmetric convolution through all eight slots.
 # Two literal slots are represented by their quadratic, with six A slots.
 elem=[J(1),-2*B,B*B-eta*c['H']/2*K*K]
 for unused in range(6):elem=zproduct(elem,[J(1),-A])
 for j in range(9):equal(D[j],9*elem[8-j],'all primitive derivative columns')
 YA=A.imag();YB=B.imag();YK=K.imag()
 skew=6*(YA**3)+2*(YB**3)+3*c['H']*eta*YB*YK*YK
 if damage=='skew-multiplicity':skew=skew-3*c['H']/2*eta*YB*YK*YK
 equal(skew.v[5],t,'whole cubic critical skew, six plus pair')
 for n in range(5):equal(skew.v[n],R(),'lower skew '+str(n))
 equal(skew.v[6],R(),'no next skew coefficient')
 VA=(anchor-A)*(anchor-A).conjugate()
 VB=(anchor-B)*(anchor-B).conjugate()+c['H']/2*eta*K*K.conjugate()
 X2=2*c['H']*eta*(((anchor-B)*K.conjugate()).real()**2)
 if damage=='pair-cross':X2=J()
 for n in range(8):equal(X2.v[n],R(),'all lower pair cross-distance coefficients')
 obj=6*inverse_sqrt(VA)+2*inverse_sqrt(VB)+Q(3,4)*X2
 wanted={0:R(8),2:R(F(Q(8,3))+c['y']),4:R(c['bstar']),6:R(c['tstar']),8:R(c['gstar'])+t*t*(c['kappa']/c['H']),9:R(8)}
 for n in range(10):equal(obj.v[n],wanted.get(n,R()),'entire actual first-power coefficient '+str(n))
 d0=C+2*C*C-1;w4=1/d0;w3=Q(2,3)*(7-(2-2*C*C)*w4)
 equal(Q(3,2)*w3+(1+C)*w4,F(8),'dual real column')
 equal(Q(3,2)*w3+(2-2*C*C)*w4,F(7),'dual pair column')
 q3=(F(77000544293)+371513219527*C-483693373045*C*C)/6718464-Q(3,2)*(c['mstar']-100)+c['H']*Q(3,14)*c['betastar']
 q4=(-F(17159240005)-90073161839*C+112464832314*C*C)/13436928-(1+C)*(c['mstar']-100)+c['H']/7*(2-2*C*C)*c['betastar']
 equal(q3,F(),'first independent repaired fourth normal');equal(q4,F(),'second independent repaired fourth normal')
 o3=-F(Q(589162435,839808))-2891972395*C/839808+315914389*C*C/69984
 o4=F(Q(1107533119,839808))+354297679*C/69984-2927333483*C*C/419904
 equal(o3+c['nustar']-c['H']/7*c['sigmastar'],F(),'first odd repair equation')
 equal(o4+c['nustar']-2*C*c['H']/7*c['sigmastar'],F(),'second odd repair equation')
 improvement=(-F(1876556269853)-9081527101813*C+11790694943635*C*C)/20155392
 mdagger=(-F(174567528253)-872760677921*C+1126922107823*C*C)/53747712
 gdagger=c['gstar']+8*(mdagger-c['mstar'])+c['H']*c['betastar']
 equal(gdagger-c['gstar'],improvement,'whole improvement over attributed prior construction')
 signed={'H':c['H'],'kappa':c['kappa'],'negative Gstar':-c['gstar'],'dual w3':w3,'dual w4':w4,'real determinant':2*C-1,'d0':d0,'improvement':improvement,'negative prior Gdagger':-gdagger,'motion A':c['motionA'],'motion Q':c['motionQ'],'motion B over sine':c['motionB']/S}
 intervals={}
 for name,v in signed.items():
  lo,hi=bound(v);require(lo>0,'physical positive sign '+name);intervals[name]=[ratio(lo),ratio(hi)]
 # Exact inverse dual cone: whole symbolic deficits, not numerical testing.
 u=R([0,1]);v=R([0,0,1]);db=(v-Q(2,3)*(1+C)*u)*(7/c['H']/d0);dm=Q(2,3)*u+db*(c['H']/7)
 equal(Q(3,2)*(dm-db*(c['H']/7)),u,'entire inverse cone first row')
 equal((1+C)*dm-(2-2*C*C)*db*(c['H']/7),v,'entire inverse cone second row')
 equal(8*dm-c['H']*db,u*w3+v*w4,'entire inverse cone cost')
 va=(2*(C-1)/(16*C-9),-7/(c['H']*(16*C-9)));vb=(F(1),7/c['H'])
 for deficit,point in ((u,va),(v,vb)):
  equal(8*point[0]-c['H']*point[1],F(1),'unit cost simplex vertex')
 equal(Q(3,2)*(va[0]-c['H']/7*va[1]),1/w3,'first vertex first deficit')
 equal((1+C)*va[0]-c['H']/7*(2-2*C*C)*va[1],F(),'first vertex second deficit')
 equal(Q(3,2)*(vb[0]-c['H']/7*vb[1]),F(),'second vertex first deficit')
 equal((1+C)*vb[0]-c['H']/7*(2-2*C*C)*vb[1],1/w4,'second vertex second deficit')
 for name,value in [('vertex denominator exceeds one',16*C-10),('vertex real lower bound',1+va[0]),('vertex real upper bound',1-va[0]),('vertex pair scaled lower bound',1+va[1]*c['H']/7),('vertex pair scaled upper bound',1-va[1]*c['H']/7)]:
  lo,hi=bound(value);require(lo>0,name);intervals[name]=[ratio(lo),ratio(hi)]
 # Injective Kronecker substitution on degree bounds u<=4, h<=8.
 gu=R([0]*9+[1]);gh=R([0,1]);ga=1+gu
 generic=inverse_sqrt((1-e*e*ga)**2+e*e*gh*gh).v[8]
 equal(generic,ga**4-5*(ga**3)*gh*gh+Q(45,8)*(ga**2)*(gh**4)-Q(35,16)*ga*(gh**6)+Q(35,128)*(gh**8),'whole generic rational fourth scalar')
 return dict(route='core',primitive=[packed(v) for v in p],objective=packed(obj),skew=packed(skew),generic_fourth=packed(generic),signs=intervals,dual=[packed(w3),packed(w4)],vertices=[[packed(v) for v in point] for point in (va,vb)],damage=damage)

def root(label,damage,restricted=False):
 # Distinct powers encode two affine repair coordinates injectively.
 # Repairs first enter epsilon8, so every coefficient through epsilon9
 # is affine in them; their products begin epsilon16 and are absent.
 repair=(R([0,1]),R([0,0,1])) if restricted else None
 c,e,t,A,B,K,D,p=family(damage,t=0 if restricted else None,repairs=repair);o=W**(4*label)
 # All polynomial Taylor columns at the literal original omega.
 # Contractive coefficient substitution, rather than target Newton moments.
 tc=[]
 for m in range(5):tc.append(sum((p[j]*comb(j,m)*(o**(j-m)) for j in range(m,10)),J()))
 delta=J();inv=o/9
 # The nonlinear map raises the error's epsilon valuation by at least two.
 for unused in range(5):
  residual=tc[0]+(tc[1]-9*(o**8))*delta
  for m in range(2,5):residual=residual+tc[m]*(delta**m)
  delta=-residual*inv
 z=o+delta
 equal(zeval(p,z),J(),'all ten composed equations, original '+str(label))
 L=-o/3-c['x']-c['y']*o.conjugate()
 equal(z.v[1],R(),'no first epsilon drift');equal(z.v[2],R(L),'literal first original drift')
 # Canonical second motion from the written two polynomial columns.
 g2=[F()]*10;g2[0]=9-9*c['x']-9*c['y'];g2[7]=9*c['y'];g2[8]=9*c['x']
 g4=[F()]*10;g4[8]=-9*c['wstar']/8;g4[7]=9*(64*c['x']**2-c['dstar'])/14;g4[6]=6*c['x']*c['H']+3*c['H']*c['up']/2
 g4[0]=-36+72*c['x']+9*c['H']/2-sum(g4[1:],F())
 fixed=-(zeval(g4,o)+sum((j*g2[j]*(o**(j-1)) for j in range(1,10)),F())*L+36*(o**7)*L*L)*inv
 motion=I*((3+4*C)*o-(1+2*C)*(1+o.conjugate())-o.conjugate()**2)/18
 if damage=='motion':motion=motion+1
 equal(z.v[3],R(),'no cubic epsilon original drift');equal(z.v[4],R(fixed),'all fixed fourth motion')
 equal(z.v[5],t*motion,'entire fifth original motion')
 normal=(z*z.conjugate()-1)/2
 leading={0:F(-1),1:-(2+4*C-4*C*C)/3,2:-(2*C-1)**2/3,3:F(),4:F(),5:F(),6:F(),7:-(2*C-1)**2/3,8:-(2+4*C-4*C*C)/3}
 equal(normal.v[0],R(),'unit original');equal(normal.v[1],R(),'zero first epsilon normal');equal(normal.v[2],R(leading[label]),'first half-normal')
 if label in (3,4,5,6):
  for n in range(3,8 if restricted else 9):equal(normal.v[n],R(),'individual active normal '+str(n))
  if restricted:
   Aj=F(1)-(o+o.conjugate())/2;Bj=F(1)-(o*o+o.conjugate()**2)/2
   equal(normal.v[8],-Aj*repair[0]+c['H']/7*Bj*repair[1],'whole symbolic restricted fourth normal')
  equal(normal.v[9],R(-Q(3,2) if label in (3,6) else -(1+C)),'individual strict ninth normal')
 else:require(bound(-leading[label])[0]>0,'remaining original strictly inward')
 norm=fixed*fixed.conjugate();linear=(fixed*motion.conjugate()+fixed.conjugate()*motion).real();quad=motion*motion.conjugate()
 if label in (2,7):
  equal(norm,c['motionA'],'winning constant motion');equal(quad,c['motionQ'],'winning quadratic motion')
  equal(linear,c['motionB']*(1 if label==7 else -1),'winning first motion')
  gap=None
 else:
  gap=bound(c['motionA']-norm);require(gap[0]>0,'all other original motion gaps')
 if restricted:
  VA=(1-e*e-A)*(1-e*e-A).conjugate();VB=(1-e*e-B)*(1-e*e-B).conjugate()+c['H']/2*e*e*K*K.conjugate()
  obj=6*inverse_sqrt(VA)+2*inverse_sqrt(VB)
  equal(obj.v[8],R(c['gstar'])+8*repair[0]-c['H']*repair[1],'whole restricted fourth objective')
 return dict(route='restricted' if restricted else 'root',label=label,root=packed(z),normal=packed(normal),motion=[packed(norm),packed(linear),packed(quad)],gap=None if gap is None else [ratio(v) for v in gap],damage=damage)

def main():
 a=argparse.ArgumentParser();a.add_argument('--route',choices=['core','root','restricted'],required=True);a.add_argument('--label',type=int,default=3);a.add_argument('--damage',default='none');a.add_argument('--output',required=True);v=a.parse_args()
 require(0<=v.label<=8,'original label')
 require(v.damage in ('none','M','beta','odd-common','odd-pair','no-inward','multiplicity','anchor','pair-cross','skew-multiplicity','motion'),'known mathematical damage')
 out=core(v.damage) if v.route=='core' else root(v.label,v.damage,v.route=='restricted')
 b=json.dumps(out,sort_keys=True,separators=(',',':')).encode();Path(v.output).write_bytes(b+b'\n')
 print(json.dumps(dict(route=v.route,label=v.label if v.route=='root' else None,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())))
if __name__=='__main__':main()
