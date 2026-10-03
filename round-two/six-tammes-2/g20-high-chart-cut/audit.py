"""Different arithmetic: bounded interpolation, Taylor and monotonicity.

No sparse polynomial class, division, expansion or Bernstein routine is
used. Exact values on a full degree-sized integer grid prove polynomial
identities by interpolation; these are not heuristic sample checks.
The displayed coordinate formulas and factor literals are shared inputs.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import json,hashlib,signal
from frame import make
from schema import validate,require
HERE=Path(__file__).resolve().parent

class Degree:
    """Uncancelled degree upper bounds, separated by radical exponent."""
    def __init__(self,parts=None):self.parts=parts or {}
    @staticmethod
    def cv(x):
        if isinstance(x,Degree):return x
        require(type(x)is int,'degree compiler accepts only integer constants')
        return Degree({0:(0,0)}) if x else Degree()
    def __add__(self,x):
        x=Degree.cv(x);v=dict(self.parts)
        for k,(a,b) in x.parts.items():
            old=v.get(k,(0,0));v[k]=(max(a,old[0]),max(b,old[1]))
        return Degree(v)
    __radd__=__add__
    def __neg__(self):return Degree(dict(self.parts))
    def __sub__(self,x):return self+-Degree.cv(x)
    def __rsub__(self,x):return Degree.cv(x)+-self
    def __mul__(self,x):
        x=Degree.cv(x);v={}
        for i,(a,b) in self.parts.items():
            for j,(c,d) in x.parts.items():
                old=v.get(i+j,(0,0));v[i+j]=(max(old[0],a+c),max(old[1],b+d))
        return Degree(v)
    __rmul__=__mul__
    def __pow__(self,n):
        require(type(n)is int and n>=0,'integer degree power');v=Degree.cv(1)
        for _ in range(n):v=v*self
        return v
    def component(self,k):return Degree({0:self.parts[k]}) if k in self.parts else Degree()

def literals(document):
    require(document.get('schema_version')==1 and document.get('variable_order')==['t','z','w'] and document.get('coefficient_domain')=='Z','audit factor ring')
    require(set(document)=={'schema_version','variable_order','coefficient_domain','rows'} and set(document['rows'])=={'L5','M6','H10','H12'},'audit factor fields')
    ans={}
    for name,rows in document['rows'].items():
        keys=[];out=[]
        for row in rows:
            require(type(row)is list and len(row)==4,'audit coefficient row');i,j,k,v=row
            require(type(i)is int and type(j)is int and i>=0 and j>=0 and type(k)is int and k==0,'audit exponents')
            require(type(v)is str and str(int(v))==v and int(v)!=0,'audit coefficient');keys.append((i,j));out.append((i,j,int(v)))
        require(bool(out) and keys==sorted(set(keys)),'audit canonical polynomial');ans[name]=out
    return ans

def value(rows,t,z):
    # Independent dense Horner evaluation, including its degree compiler.
    n=max(i for i,j,v in rows);m=max(j for i,j,v in rows);data={(i,j):v for i,j,v in rows}
    cols=[]
    for j in range(m+1):
        acc=t*0
        for i in range(n,-1,-1):acc=acc*t+data.get((i,j),0)
        cols.append(acc)
    answer=t*0
    for j in range(m,-1,-1):answer=answer*z+cols[j]
    return answer

def raw(t,z,w):
    m=make(t,z,w)
    def metric(a,b):return (1-t)*sum(x*y for x,y in zip(a,b))+t*sum(a)*sum(b)
    return [metric(m['points'][i],m['B_num'][j])-t*(1+t)**2*m['Omega'] for i,j in ((5,12),(6,8))],m['root_squared']

def residuals(t,z,A5,B5,A6,B6,R,f):
    a,b,c=1+t,1-t,1+2*t;D=b*b*c;C=1+D*z*z;J=9*t**3-t*t-t+1
    F5=t*a**10*b*c*(3*t-1);F6=a**5*b*c*(3*t-1)*(3*t+1)
    Z=t*(3*t+1)*z-(1+2*t);M5=1+2*t-t*t-2*t*b*c*z
    quadratic=a*D*z*z-2*D*z+2*t*t-t+1
    L5,M6,H10,H12=[value(f[n],t,z) for n in ('L5','M6','H10','H12')]
    return [
        A5-F5*2*D*(b*z+1)*C*L5,
        B5-F5*(-2)*(b*z+1)*C*M5,
        B6-F6*2*(b*z+1)*M6,
        A5*A5-B5*B5*R-F5**2*a*b**5*c**3*J*C**2*32*(b*z+1)**2*(1-b*z)*(b*c*z+t)*Z*quadratic,
        A6*A6-B6*B6*R-F6**2*a**2*b**4*c**3*J*4*(b*z+1)**2*quadratic*H10*H12,
        a*quadratic-D*(a*z-1)**2-4*t*t,
        b*(1+2*t-t*t)-2*t*b*c-b*(1-5*t*t)]

def identity_audit(document):
    f=literals(document);td=Degree({0:(1,0)});zd=Degree({0:(0,1)});wd=Degree({1:(0,0)})
    qs,R=raw(td,zd,wd)
    require(all(set(q.parts)<= {0,1} for q in qs) and set(R.parts)<= {0},'whole expression is affine in w, and R is w-free')
    bounds=residuals(td,zd,qs[0].component(0),qs[0].component(1),qs[1].component(0),qs[1].component(1),R,f)
    require(all(set(x.parts)<= {0} for x in bounds),'bivariate interpolation residuals')
    degrees=[list(x.parts.get(0,(0,0))) for x in bounds];n=max(x[0] for x in degrees);m=max(x[1] for x in degrees)
    # n+1 different integer t values and m+1 different integer z values.
    # t=-1,0,1 include exceptional clearing factors, without division.
    grids=0;checks=0;digest=hashlib.sha256()
    for t in range(-1,n):
        for z in range(m+1):
            q0,r0=raw(t,z,0);q1,r1=raw(t,z,1);require(r0==r1,'w-free radical square')
            rs=residuals(t,z,q0[0],q1[0]-q0[0],q0[1],q1[1]-q0[1],r0,f)
            require(len(rs)==7 and all(type(v)is int and v==0 for v in rs),'nonzero full-grid exact residual')
            grids+=1;checks+=len(rs);digest.update((str(t)+','+str(z)+':'+','.join(map(str,rs))+'\n').encode())
    return {'proof_method':'full_degree_sized_tensor_interpolation','independent_uncancelled_residual_degree_bounds':degrees,'tensor_grid_degrees':[n,m],'complete_grid_points_actually_checked':grids,'integer_zero_residuals_actually_checked':checks,'whole_ordered_grid_digest_sha256':digest.hexdigest(),'radical_affinity_checked_by_degree_compiler':True,'exceptional_t_minus1_0_1_included':True}

def taylor(rows,box,sign):
    a,b,c,d=box;x,y=(a+b)/2,(c+d)/2;rx,ry=(b-a)/2,(d-c)/2;co={}
    for i,j,v in rows:
        for p in range(i+1):
            for q in range(j+1):co[p,q]=co.get((p,q),Q(0))+v*comb(i,p)*comb(j,q)*x**(i-p)*y**(j-q)
    center=co.get((0,0),Q(0));error=sum((abs(v)*rx**i*ry**j for (i,j),v in co.items() if i or j),Q(0))
    low,high=center-error,center+error
    require(low>0 if sign==1 else high<0,'closed-box centered Taylor sign not strict')
    stream=(json.dumps([[i,j,str(co[i,j])] for i,j in sorted(co)],separators=(',',':'))+'\n').encode()
    return {'box':list(map(str,box)),'sign':sign,'power_coefficients_actually_checked':len(co),'lower_bound':str(low),'upper_bound':str(high),'whole_translated_coefficient_sha256':hashlib.sha256(stream).hexdigest()}

def audit(system,document):
    cells=validate(system);f=literals(document);identities=identity_audit(document)
    ta,tb=map(Q,system['t_interval']);za,zb=map(Q,system['excluded_z_interval']);boxes={r['name']:tuple(map(Q,r['box'])) for r in system['closed_cover']}
    checks=[]
    for name,box,sign in [('L5',(ta,tb,za,zb),1),('M6',boxes['lower-corner'],1),('H10',boxes['lower-corner'],-1),('H12',boxes['lower-corner'],1)]:checks.append({'name':name}|taylor(f[name],box,sign))
    monotone=[]
    for name in ('upper-t','upper-z'):
        a,b,c,d=boxes[name];dt=(6*a+1)*c-2;dz=a*(3*a+1);minimum=a*(3*a+1)*c-(1+2*a)
        require(a>0 and c>0 and dt>0 and dz>0 and minimum>0,'whole-box Z monotonicity and corner minimum')
        monotone.append({'name':'Z-'+name,'box':list(map(str,boxes[name])),'dt_lower':str(dt),'dz_lower':str(dz),'whole_box_lower_bound':str(minimum)})
    require(1-5*ta*ta==Q(-71,125),'closed chart-equality radical sign')
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'COMPLETE_ALTERNATE_IDENTITY_AND_SIGN_AUDIT','closed_boxes':3,'elementary_cells_including_boundaries':cells,'identity_audit':identities,'Taylor_signs':checks,'all_Taylor_coefficients_actually_checked':sum(x['power_coefficients_actually_checked'] for x in checks),'monotone_Z_signs':monotone,'chart_equality_M5_upper_bound':'-71/125','shared_inputs':'Published9912 coordinate formulas; four new factor literals; scope schema. No primary sparse polynomial, division or Bernstein arithmetic.','independent_peer_review':False,'no_unresolved_case':True,'new_global_bound':False}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('20s alternate audit guard')));signal.alarm(20)
    s=json.loads((HERE/'SYSTEM.json').read_text());f=json.loads((HERE/'FACTORS.json').read_text());print(json.dumps(audit(s,f),indent=2))
