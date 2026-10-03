"""Different arithmetic: full bounded interpolation and closed Taylor signs.

No primary expansion, division, sparse polynomial or Bernstein arithmetic
is used. The integral frame formulas, factor literals and scope are shared
inputs. This is another SAME-AUTHOR check, not independent peer review.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import json,hashlib,signal,argparse
from frame import make
from coverage import validate,census,elementary
HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise ValueError(message)

class Degree:
    def __init__(self,parts=None):self.parts=parts or {}
    @staticmethod
    def cv(x):
        if isinstance(x,Degree):return x
        require(type(x)is int,'degree constant');return Degree({0:(0,0)}) if x else Degree()
    def __add__(self,x):
        x=Degree.cv(x);p=dict(self.parts)
        for k,(a,b) in x.parts.items():
            c,d=p.get(k,(0,0));p[k]=max(a,c),max(b,d)
        return Degree(p)
    __radd__=__add__
    def __neg__(self):return Degree(dict(self.parts))
    def __sub__(self,x):return self+-Degree.cv(x)
    def __rsub__(self,x):return Degree.cv(x)+-self
    def __mul__(self,x):
        x=Degree.cv(x);p={}
        for i,(a,b) in self.parts.items():
            for j,(c,d) in x.parts.items():
                e,f=p.get(i+j,(0,0));p[i+j]=max(e,a+c),max(f,b+d)
        return Degree(p)
    __rmul__=__mul__
    def __pow__(self,n):
        require(type(n)is int and n>=0,'nonnegative degree power');v=Degree.cv(1)
        for _ in range(n):v*=self
        return v

class Pair:
    # Exact integer arithmetic in Z[t,z][omega]/(omega^2-R), including R=0.
    def __init__(self,a,b,R):self.a,self.b,self.R=a,b,R
    def cv(self,x):
        if isinstance(x,Pair):return x
        require(type(x)is int,'pair integral scalar');return Pair(x,0,self.R)
    def __add__(self,x):
        x=self.cv(x);return Pair(self.a+x.a,self.b+x.b,self.R)
    __radd__=__add__
    def __neg__(self):return Pair(-self.a,-self.b,self.R)
    def __sub__(self,x):return self+-self.cv(x)
    def __rsub__(self,x):return self.cv(x)+-self
    def __mul__(self,x):
        x=self.cv(x);return Pair(self.a*x.a+self.R*self.b*x.b,self.a*x.b+self.b*x.a,self.R)
    __rmul__=__mul__
    def __pow__(self,n):
        require(type(n)is int and n>=0,'pair polynomial power');v=self.cv(1)
        for _ in range(n):v*=self
        return v

def literals(document):
    require(set(document)=={'schema_version','variable_order','coefficient_domain','rows'} and document['schema_version']==1 and document['variable_order']==['t','z','w'] and document['coefficient_domain']=='Z','audit whole domain')
    require(set(document['rows'])=={'bound0','bound1','bound2','delta','C0','C4','C6','margin','bound2_square_factor','critical_norm99','R'},'audit entire factor input')
    ans={}
    for name,rows in document['rows'].items():
        out=[];keys=[]
        for row in rows:
            require(type(row)is list and len(row)==4,'audit literal row');i,j,k,v=row
            require(all(type(x)is int and x>=0 for x in (i,j,k)) and k<=1 and type(v)is str and str(int(v))==v and int(v)!=0,'audit exponents/coefficient')
            keys.append((i,j,k));out.append((i,j,k,int(v)))
        require(bool(keys) and keys==sorted(set(keys)),'audit unique ordered monomials');ans[name]=out
    require(all(k==0 for n in ('R','critical_norm99','bound2_square_factor') for i,j,k,v in ans[n]),'audit bivariate derived inputs')
    return ans

def horner(rows,t,z,k=0):
    data={(i,j):v for i,j,l,v in rows if l==k};n=max((i for i,j in data),default=0);m=max((j for i,j in data),default=0)
    cols=[]
    for j in range(m+1):
        acc=t*0
        for i in range(n,-1,-1):acc=acc*t+data.get((i,j),0)
        cols.append(acc)
    ans=t*0
    for j in range(m,-1,-1):ans=ans*z+cols[j]
    return ans

def product(names,t,z):
    a,b,c=1+t,1-t,1+2*t;D=b*b*c;C=1+D*z*z;J=9*t**3-t*t-t+1;q=a*D*z*z-2*D*z+2*t*t-t+1
    factors={'a':a,'b':b,'c':c,'3t-1':3*t-1,'3t+1':3*t+1,'J':J,'C':C,'Q':q,'bz+1':b*z+1};v=t*0+1
    for n in names:require(n in factors,'audit positive factor name');v*=factors[n]
    return v

def critical_direct(t,z):
    # Independently organized 3x3 cofactor expansion of the physical Gram.
    m=make(t,z,t*0);d=m['W_den'];W=m['W_num'];n=(-5,-14,20)
    v=(1-t)*W[2]+t*sum(W);u=(1-t)*sum(W[i]*n[i] for i in range(3))+t*sum(W)*sum(n)
    q=621-620*t;s=20-19*t
    determinant=(q-s*s)*d*d-q*v*v+2*s*u*v-u*u
    numerator=t*t*((2*q-s*s)*d*d-u*u+2*d*(s*u-q*v))
    numerator+=30*t*(u*v-s*d*d+d*(s*v-u))+225*(d*d-v*v)
    return 99*determinant-100*numerator

def residuals(t,z,f,s):
    R=make(t,z,t*0)['root_squared'];tp,zp,wp=Pair(t,0,R),Pair(z,0,R),Pair(0,1,R)
    m=make(tp,zp,wp);Y=m['points'];a,b,c=1+tp,1-tp,1+2*tp;F=a**5*c*(3*tp-1)*(b*zp+1)
    # Compare coefficient pairs after monic root reduction; no inverse or sign.
    lit=lambda n:Pair(horner(f[n],t,z,0),horner(f[n],t,z,1),R)
    ans=[Pair(R-horner(f['R'],t,z),0,R)]
    for j in range(3):ans.append(-(Y[0][j]+2*Y[11][j])-F*lit('bound'+str(j)))
    F0=a**6*c*(3*tp-1)*(b*zp+1);F6=a**4*c*(3*tp-1)*(3*tp+1)*(b*zp+1)
    delta=Y[0][1]*Y[6][0]-Y[0][0]*Y[6][1]
    alpha=-2*Y[6][0]+13*Y[6][1];beta=2*Y[0][0]-13*Y[0][1]
    C0=m['Omega']*alpha;C6=m['Omega']*beta;C4=15*delta-alpha*Y[0][2]-beta*Y[6][2]
    raw={'delta':delta,'C0':C0,'C4':C4,'C6':C6,'margin':24*delta-tp*(C0+C4+C6)}
    for n,p in raw.items():ans.append(p-F0*F6*product(s['Farkas_positive_factors'][n],tp,zp)*lit(n))
    ans.append(Pair(critical_direct(t,z)-horner(f['critical_norm99'],t,z),0,R))
    for i,j,k,l in [(0,9,5,11),(5,6,0,11),(11,7,0,5),(1,8,2,4),(4,10,1,2),(2,12,1,10)]:
        for v in range(3):ans.append(a*(Y[i][v]+Y[j][v])-2*tp*(Y[k][v]+Y[l][v]))
    for v in range(3):ans.append(a*a*(Y[8][v]+Y[12][v])-(5*tp*tp-1)*(Y[1][v]+Y[2][v]))
    for v in range(3):ans.append(m['h']*Y[0][v]-a*(2*tp*Y[6][v]+2*tp*Y[7][v]+b*Y[9][v]))
    q=a*m['D']*zp*zp-2*m['D']*zp+2*tp*tp-tp+1
    ans.extend([m['C']-m['S']-b*c*(b*zp+1)**2,m['C']+m['S']-q,a*q-m['D']*(a*zp-1)**2-4*tp*tp])
    for v in range(3):ans.append([-13,-2,15][v]*delta-alpha*Y[0][v]-beta*Y[6][v]-(C4 if v==2 else tp*0))
    return ans

def identity_audit(f,s):
    td,zd=Degree({0:(1,0)}),Degree({0:(0,1)});rs=residuals(td,zd,f,s)
    degrees=[]
    for r in rs:
        require(all(set(x.parts)<={0} for x in (Degree.cv(r.a),Degree.cv(r.b))),'bivariate full-grid residual components')
        degrees.extend([list(Degree.cv(x).parts.get(0,(0,0))) for x in (r.a,r.b)])
    n=max(d[0] for d in degrees);m=max(d[1] for d in degrees);points=zeros=0;digest=hashlib.sha256()
    for t in range(-1,n):
        for z in range(m+1):
            vals=[v for r in residuals(t,z,f,s) for v in (r.a,r.b)]
            require(len(vals)==80 and all(type(v)is int and v==0 for v in vals),'nonzero full-degree tensor interpolation residual')
            points+=1;zeros+=len(vals);digest.update((str(t)+','+str(z)+':'+','.join(map(str,vals))+'\n').encode())
    return {'method':'full_uncancelled_degree_bounded_tensor_interpolation','residual_component_degrees':degrees,'full_grid_degrees':[n,m],'complete_grid_points_checked':points,'integer_zero_residuals_checked':zeros,'whole_grid_sha256':digest.hexdigest(),'exceptional_t_minus1_0_1_retained':True,'no_division_or_sample_inference':True}

def bivariate(rows,k=0):return {(i,j):v for i,j,l,v in rows if l==k}
def add(p,q,scale=1):
    r=dict(p)
    for k,v in q.items():r[k]=r.get(k,0)+scale*v
    return {k:v for k,v in r.items() if v}
def multiply(p,q):
    r={}
    for (i,j),v in p.items():
        for (a,b),w in q.items():r[i+a,j+b]=r.get((i+a,j+b),0)+v*w
    return {k:v for k,v in r.items() if v}

def taylor(p,box,sign):
    a,b,c,d=map(Q,box);x,y=(a+b)/2,(c+d)/2;rx,ry=(b-a)/2,(d-c)/2;co={}
    # Complete translated coefficients, not just a sampled center value.
    for (i,j),v in p.items():
        for k in range(i+1):
            for l in range(j+1):co[k,l]=co.get((k,l),Q(0))+v*comb(i,k)*comb(j,l)*x**(i-k)*y**(j-l)
    center=co.get((0,0),Q(0));error=sum((abs(v)*rx**i*ry**j for (i,j),v in co.items() if i or j),Q(0));lo,hi=center-error,center+error
    require(lo>0 if sign==1 else hi<0,'non-strict closed Taylor enclosure')
    data=(json.dumps([[i,j,str(v)] for (i,j),v in sorted(co.items())],separators=(',',':'))+'\n').encode()
    return {'box':list(map(str,(a,b,c,d))),'sign':sign,'translated_coefficients_checked':len(co),'lower':str(lo),'upper':str(hi),'whole_coefficient_sha256':hashlib.sha256(data).hexdigest()}

def sign_audit(f,s):
    box=(*s['t_interval'],*s['z_interval']);R=bivariate(f['R']);out=[]
    wanted=[('bound0','B',1),('bound0','H',1),('bound1','A',1),('bound1','B',1),('bound2','A',1),('delta','A',1),('delta','B',1),('C0','A',1),('C0','H',-1),('C4','A',1),('C4','H',-1),('C6','A',1),('C6','B',1),('margin','B',1),('margin','H',1)]
    for name,part,sign in wanted:
        A,B=bivariate(f[name]),bivariate(f[name],1);p=A if part=='A' else B if part=='B' else add(multiply(multiply(B,B),R),multiply(A,A),-1)
        out.append({'name':name+'-'+part}|taylor(p,box,sign))
    A,B=bivariate(f['bound2']),bivariate(f['bound2'],1);H=add(multiply(multiply(B,B),R),multiply(A,A),-1)
    # Different exact integer product, not the primary factor division.
    one={(0,0):1};a={(0,0):1,(1,0):1};b={(0,0):1,(1,0):-1};c={(0,0):1,(1,0):2};J={(0,0):1,(1,0):-1,(2,0):-1,(3,0):9}
    D=multiply(multiply(b,b),c);q=add(add(multiply(a,{(i,j+2):v for (i,j),v in D.items()}),{(i,j+1):-2*v for (i,j),v in D.items()}),{(0,0):1,(1,0):-1,(2,0):2})
    prod=J
    for factor in [c,c,b,b,b,b,a,a,a,a,q,bivariate(f['bound2_square_factor'])]:prod=multiply(prod,factor)
    require(H=={k:-8*v for k,v in prod.items()},'different integer convolution of the whole square factor')
    for i,cell in enumerate(s['alternate_bound2_closed_cover']):out.append({'name':'bound2-square-factor-cell'+str(i)}|taylor(bivariate(f['bound2_square_factor']),cell,1))
    out.append({'name':'critical-norm99'}|taylor(bivariate(f['critical_norm99']),box,1))
    require(len(out)==19,'all alternate signs, three closed cells for one factored sign')
    return out

def run(s,document):
    validate(s);f=literals(document);ids=identity_audit(f,s);signs=sign_audit(f,s)
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'COMPLETE_ALTERNATE_INTERPOLATION_AND_TAYLOR_AUDIT','coverage':census(s,reverse=True),'elementary_closed_bounds':elementary(s),'identity_audit':ids,'Taylor_signs':signs,'translated_coefficients_checked':sum(r['translated_coefficients_checked'] for r in signs),'shared_inputs':'integral9912 frame, exact new literals, closed scope','primary_sparse_division_or_Bernstein_used':False,'independent_peer_review':False,'conditional_capacity_proved':False,'new_global_bound':False}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('20s fixed alternate guard')));signal.alarm(20)
    parser=argparse.ArgumentParser();parser.add_argument('--emit');args=parser.parse_args()
    out=run(json.loads((HERE/'SYSTEM.json').read_text()),json.loads((HERE/'FACTORS.json').read_text()))
    data=(json.dumps(out,separators=(',',':'))+'\n').encode()
    if args.emit:Path(args.emit).write_bytes(data)
    else:require(out==json.loads((HERE/'AUDIT.json').read_text()),'whole alternate certificate equality')
    print(json.dumps({'status':out['status'],'residual_branches':260,'grid_points':out['identity_audit']['complete_grid_points_checked'],'zero_residual_components':out['identity_audit']['integer_zero_residuals_checked'],'translated_coefficients':out['translated_coefficients_checked'],'whole_audit_sha256':hashlib.sha256(data).hexdigest(),'conditional_capacity_proved':False},indent=2))
