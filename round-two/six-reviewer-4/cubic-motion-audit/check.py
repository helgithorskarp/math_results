"""Separate quadratic-tower reader; exponential elementary and forward roots."""
import json,sys
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parent))
from tower import T,c,s,I,w,z,read_field,need
def scalar(v):
 need(type(v)is list and len(v)==3 and all(type(a)is str for a in v),'typed cubic scalar')
 return sum((F(a)*c**n for n,a in enumerate(v)),T(0))
def validate(r):
 need(type(r)is dict and set(r)=={'schema','slots','elementary','primitive','roots','norms','active_rows','scalars','multiplicity_ratios','polynomial_certificates'},'whole schema census')
 need(r['schema']=='cubic-motion-audit-v1'and r['slots']==[[0,0],[2,0],[3,1],[3,2],[3,3]],'jet slot types and order')
 y=1/(3*(1+c));x=T(F(2,3))-y;H=14*y;U=-8*x;k=-7*(1+2*c)/18
 def rows(v,n):
  need(type(v)is list and len(v)==n,'whole row census');out=[]
  for a in v:need(type(a)is list and len(a)==5,'whole five-slot jet');out.append([read_field(q)for q in a])
  return out
 es=rows(r['elementary'],9);ps=rows(r['primitive'],10)
 # exp(-sum P_m u^m/m) has only its linear exponent through t^3;
 # e_n=(-1)^n [u^n] exp, no Newton recurrence imported or used.
 expected=[[T(0)]*5 for _ in range(9)];expected[0][0]=T(1)
 expected[1]=[T(0),U,I,T(0),T(0)]
 expected[2]=[T(0),H/2,T(0),-I/2,T(0)]
 expected[3]=[T(0),T(0),T(0),T(0),-I/3]
 need(es==expected,'all elementary coordinates, including zeros')
 # Closed integrated anchored columns; independent of producer recurrence.
 ep=[[T(0)]*5 for _ in range(10)];ep[9][0]=T(1);ep[0][0]=T(-1)
 ep[0][1]=9-9*x-9*y;ep[8][1]=9*x;ep[7][1]=9*y
 ep[8][2]=-9*I/8;ep[0][2]=9*I/8
 ep[7][3]=-9*I/14;ep[0][3]=9*I/14
 ep[6][4]=I/2;ep[0][4]=-I/2
 need(ps==ep,'all integrated anchor columns including all zeros')
 need(type(r['roots'])is list and len(r['roots'])==9,'all-nine root census')
 need(type(r['norms'])is list and len(r['norms'])==9,'all-nine norm census')
 need(type(r['active_rows'])is list and len(r['active_rows'])==9,'all-nine radial row census')
 normform=[T(0),(13+26*c+16*c*c)/324,(16+50*c+40*c*c)/324,(9+36*c+36*c*c)/324,(16+32*c+16*c*c)/324]
 for j,row in enumerate(r['roots']):
  need(type(row)is dict and set(row)=={'label','L','raw','W'}and type(row['label'])is int and row['label']==j,'unique ordered label')
  root=w**j;L=read_field(row['L']);need(L==-root/3-x-y/root,'canonical original quadratic displacement')
  need(type(row['raw'])is list and len(row['raw'])==3,'whole raw cubic row');raw=[read_field(a)for a in row['raw']]
  for col,v in enumerate([L,*raw],1):
   residual=9*root**8*v+sum((ps[n][col]*root**n for n in range(10)),T(0))
   need(residual==0,'full forward root residual '+str((j,col)))
  W=read_field(row['W']);formula=I*((3+4*c)*root-(1+2*c)*(1+1/root)-1/root**2)/18
  need(W==formula and W==raw[0]*(8*k/7)+raw[1]*(2*k)+raw[2],'closed cubic map and both closure coefficients')
  need(scalar(r['norms'][j])==W*W.flip(i=True)==normform[min(j,9-j)],'full norm and harmonic label')
  sin=lambda n:(root**n-(root**n).flip(i=True))/(2*I)
  need(type(r['active_rows'][j])is list and len(r['active_rows'][j])==3,'whole sine rows')
  need([read_field(a)for a in r['active_rows'][j]]==[sin(1),sin(2),sin(6)],'all radial sine columns')
  if j in (3,4,5,6):need((8*k/7)*sin(1)/8+2*k*sin(2)/14+sin(6)/18==0,'individual active row closure')
 # Independent determinant and two-row closure, no pair average.
 sin=lambda j,n:((w**j)**n-(w**j).flip(i=True)**n)/(2*I)
 determinant=sin(3,1)*sin(4,2)/112-sin(4,1)*sin(3,2)/112
 need(determinant!=0,'unaveraged active row invertibility')
 need(r['roots'][0]['raw']==[['0']*12]*3 and read_field(r['roots'][0]['L'])==-1,'marked root exact anchored jet')
 rho=(c-5)/3;alpha=T(F(-527,360))+41*c/90+13*c*c/90
 tau=T(F(1369,648))+74*c/81+8*c*c/81;need(tau==(k+rho)**2/2,'cost square completion')
 KE=T(F(6653,324))+23915*c/486-15839*c*c/243
 Bstar=T(F(2311,108))+4934*c/27-1976*c*c/9
 need(KE==Bstar-alpha*H*H/2+(43*alpha/56+9*tau/14)*H*H,'equality-profile necessary cost')
 lam=12*(1+c);d=2*c*c-1;w4=T(F(-2,3))+4*c/3;w3=T(F(52,9))-4*c/9-8*c*c/9
 Mstar=-(512+1684*c+1328*c*c)/9;bstar=(86-261*c-172*c*c)/18
 M0=Mstar-(1+2*d)/(3*(c+d));b0=bstar+(2*c-1)/(24*(c+d))
 need(H*lam==56,'actual family norm matches universal H')
 need(F(3,2)*w3+(1+c)*w4==8 and 12*w3+8*(1-d)*w4==56,'affine repair dual parameter columns')
 need(-(431+320*c+320*c*c)/3-F(3,2)*M0+12*b0==0,'zero-slack row3')
 need(-(1636+2842*c+1980*c*c)/9-(1+c)*M0+8*(1-d)*b0==0,'zero-slack row4')
 normmax=normform[2]
 ex={'H':H,'lambda':lam,'k':k,'tau':tau,'KE':KE,'Jstar_squared':T(F(9,14))*H**3,'Astar_squared':H**3*(8+25*c+20*c*c)/252,'gamma_squared':2*H*normmax/7,'w3':w3,'w4':w4,'M0':M0,'beta0':b0,'repair_determinant':12*(c+d)}
 need(type(r['scalars'])is dict and set(r['scalars'])==set(ex),'complete scalar census')
 for a,v in ex.items():need(scalar(r['scalars'][a])==v,'exact scalar '+a)
 need(r['multiplicity_ratios']==['9/14','1/6','1/30','0','1/30','1/6','9/14'],'all seven stationary multiplicities')
 # Independently check supplied entire residual support (not just nonzero terms).
 need(type(r['polynomial_certificates'])is list and len(r['polynomial_certificates'])==8,'all-index certificate coverage')
 def key(i,n,b):a=[0]*9;a[i]=n;a[8]=b;return tuple(a)
 # Reader polynomial multiplication uses full exponent-vector convolution.
 class Poly:
  def __init__(self,v):self.a={k:F(x)for k,x in v.items()if x}
  def __add__(self,o):
   d=dict(self.a)
   for k,x in o.a.items():d[k]=d.get(k,F(0))+x
   return Poly(d)
  def __mul__(self,o):
   d={}
   for k,x in self.a.items():
    for l,y in o.a.items():
     a=tuple(v+u for v,u in zip(k,l,strict=True));d[a]=d.get(a,F(0))+x*y
   return Poly(d)
  def scale(self,n):return Poly({k:x*n for k,x in self.a.items()})
  def square(self):return self*self
 zero=Poly({});b=Poly({key(0,0,1):1});vs=[Poly({key(i,1,0):1})for i in range(8)]
 total=sum(vs,zero);norm=sum((v.square()for v in vs),zero);cubes=sum((v*v*v for v in vs),zero)
 deficit=sum(((b.scale(7)+v.scale(-1))*(v+b).square()for v in vs),zero)+b*b*b.scale(-336)+cubes
 rhs=b*norm.scale(5)+b*b*b.scale(-280)+b*b*total.scale(13)
 need((deficit+rhs.scale(-1)).a=={},'reader global cubic deficit identity')
 for index,row in enumerate(r['polynomial_certificates']):
  need(type(row)is dict and set(row)=={'index','deficit_residual','distance_residual'}and type(row['index'])is int and row['index']==index,'certificate index census')
  for name,powers in [('deficit_residual',[(3,0),(2,1),(1,2)]),('distance_residual',[(2,0),(1,1)])]:
   support={key(i,n,b)for i in range(8)for n,b in powers}|{key(0,0,3 if name=='deficit_residual'else 2)}
   got=row[name];need(type(got)is list and len(got)==len(support),'whole residual support')
   need([tuple(q[0])for q in got]==sorted(support),'ordered residual monomials')
   need(all(type(q)is list and len(q)==2 and type(q[0])is list and len(q[0])==9 and all(type(t)is int for t in q[0])and q[1]=='0'for q in got),'all residuals exactly typed zero')
  distance=sum(((v+b.scale(-7 if i==index else 1)).square()for i,v in enumerate(vs)),zero)
  distance_rhs=b*b.scale(112)+b*vs[index].scale(-16)+norm+b*b.scale(-56)+b*total.scale(2)
  need((distance+distance_rhs.scale(-1)).a=={},'reader all-index distance identity')
 # Fresh real root isolation, exact rational interval, no float sign inference.
 lo,hi=F(15,16),F(47,50)
 f=lambda a:8*a**3-6*a-1
 need(f(lo)<0<f(hi)and 24*lo**2-6>0,'unique physical c embedding')
 for _ in range(48):
  mid=(lo+hi)/2
  if f(mid)<0:lo=mid
  else:hi=mid
 def bound(v):
  need(type(v)is list and len(v)==3,'sign cubic coefficients');ls=[];hs=[]
  for n,a in enumerate(map(F,v)):
   aa,bb=a*lo**n,a*hi**n;ls.append(min(aa,bb));hs.append(max(aa,bb))
  return sum(ls),sum(hs)
 kel,keh=bound(r['scalars']['KE']);need(9<kel<keh<10,'KE strict 9..10')
 for a in ('H','lambda','w3','w4','repair_determinant','gamma_squared','Astar_squared'):need(bound(r['scalars'][a])[0]>0,'strict positivity '+a)
 for j in (0,1,3,4):
  vv=scalar(r['norms'][2])-scalar(r['norms'][j]);need(vv!=0,'strict max norm distinct')
  aa=[F(a)-F(b)for a,b in zip(r['norms'][2],r['norms'][j],strict=True)];need(bound(list(map(str,aa)))[0]>0,'strict largest harmonic sign')
 # Complete bridge faithfulness: row reduction of all12 image basis columns.
 columns=[(z**j).encode()for j in range(12)];mat=[[F(columns[j][i])for j in range(12)]for i in range(12)]
 for j in range(12):
  pi=next((i for i in range(j,12)if mat[i][j]),None);need(pi is not None,'faithful twelve-dimensional decoder');mat[j],mat[pi]=mat[pi],mat[j];v=mat[j][j];mat[j]=[q/v for q in mat[j]]
  for i in range(j+1,12):
   q=mat[i][j];mat[i]=[a-q*b for a,b in zip(mat[i],mat[j],strict=True)]
 return {'status':'verified','roots':9,'all_elementary_primitive_coordinates':1140,'all_root_raw_and_map_coordinates':540,'all_norm_labels':9,'all_individual_active_rows':4,'multiplicity_cases':7,'polynomial_identity_indices':8,'decoder_rank':12,'c_bracket':[str(lo),str(hi)],'KE_bracket':[str(kel),str(keh)]}
if __name__=='__main__':
 if len(sys.argv)!=2:raise ValueError('usage check.py RECORD')
 print(json.dumps(validate(json.loads(Path(sys.argv[1]).read_text())),sort_keys=True))
