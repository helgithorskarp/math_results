"""Alternate exact digit identities and translated Taylor signs.

Shared defining frame, literals and scope; no primary polynomial expansion,
division or Bernstein calculation. The unmodified credited generic digit
engine is from six-reviewer-3/source52fa998f. Its reuse is SAME-AUTHOR
alternate evidence for these NEW identities, not independent review.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import argparse,hashlib,json,signal
from digit import Expr,T,Z,expr,monomials,prove_zero
from frame import make
from polynomials import dot
from scope import validate,require
HERE=Path(__file__).resolve().parent
NAMES={'excess067','excess579','excess6911','excess067_square','excess579_square','R'}
def literals(d):
    require(set(d)=={'schema_version','variable_order','coefficient_domain','rows'} and type(d['schema_version'])is int and d['schema_version']==1 and d['variable_order']==['t','z','w'] and d['coefficient_domain']=='Z' and set(d['rows'])==NAMES,'alternate entire literal domain')
    out={}
    for name,rows in d['rows'].items():
        decoded=[];keys=[]
        for row in rows:
            require(type(row)is list and len(row)==4,'alternate literal shape')
            i,j,k,v=row
            require(all(type(x)is int and x>=0 for x in (i,j,k)) and i<=64 and j<=16 and k<=1,'alternate degree and radical slots')
            require(type(v)is str and str(int(v))==v and int(v)!=0,'alternate canonical integer')
            keys.append((i,j,k));decoded.append((i,j,k,int(v)))
        require(bool(keys) and keys==sorted(set(keys)),'alternate unique complete ordering');out[name]=decoded
    require(all(k==0 for n in ('R','excess067_square','excess579_square') for i,j,k,v in out[n]),'alternate bivariate squares')
    return out
def literal(rows,k=0):return monomials([(i,j,v) for i,j,w,v in rows if w==k])
class Pair:
    def __init__(self,a,b,R):self.a,self.b,self.R=expr(a),expr(b),R
    def cv(self,x):
        if isinstance(x,Pair):
            require(x.R is self.R,'one original radical relation');return x
        return Pair(expr(x),0,self.R)
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
        require(type(n)is int and n>=0,'integral nonnegative pair power');v=self.cv(1)
        for _ in range(n):v*=self
        return v
def multiplier(names,t,z):
    a,b,c=1+t,1-t,1+2*t;D=b*b*c;C=1+D*z*z;J=9*t**3-t*t-t+1;q=a*D*z*z-2*D*z+2*t*t-t+1
    base={'t':t,'a':a,'b':b,'c':c,'3t-1':3*t-1,'J':J,'C':C,'Q':q,'bz+1':b*z+1};p=t*0+1
    for n in names:require(n in base,'alternate positive-factor name');p*=base[n]
    return p
def identity_audit(s,f):
    original=make(T,Z,expr(0));R=original['root_squared'];tp,zp,wp=Pair(T,0,R),Pair(Z,0,R),Pair(0,1,R)
    m=make(tp,zp,wp);Y=m['points'];a,b,c=m['a'],m['b'],m['c'];L=7*tp*tp+2*tp-1;checks=[]
    def add(name,p):
        if isinstance(p,Pair):
            checks.extend([{'name':name+'-constant'}|prove_zero(p.a),{'name':name+'-radical'}|prove_zero(p.b)])
        else:checks.append({'name':name}|prove_zero(p))
    add('original-root-square',R-literal(f['R']))
    for name,(central,i,j,n,h) in {'excess067':(0,6,7,(-5,-14,20),15),'excess579':(5,7,9,m['B_num'][10],tp*a*a),'excess6911':(11,6,9,(-8,12,-5),9)}.items():
        vector=[tp*(a*a*(Y[i][v]+Y[j][v])-L*Y[central][v]) for v in range(3)]
        raw=(1-tp)*sum(vector[v]*n[v] for v in range(3))+tp*sum(vector)*sum(n)-h*b*b*c*m['Omega']
        data=Pair(literal(f[name]),literal(f[name],1),R)
        add(name,raw-multiplier(s['positive_factor_recipes'][name],tp,zp)*data)
    for name in ('excess067','excess579'):
        aa,bb=literal(f[name]),literal(f[name],1);hn=name+'_square'
        add(hn,bb*bb*R-aa*aa-s['square_integer_multipliers'][hn]*multiplier(s['positive_factor_recipes'][hn],T,Z)*literal(f[hn]))
    K=tp*(9*tp*tp-2*tp-3)
    for i,j in ((6,7),(6,9),(7,9)):
        add('A-Gram-'+str(i)+'-'+str(j),a*a*dot(Y[i],Y[j],tp)-K*m['Omega']**2)
    aa,bb,cc=1+T,1-T,1+2*T;kk=T*(9*T*T-2*T-3);ll=7*T*T+2*T-1;N=original['B_num']
    for i,j in ((4,12),(8,10)):add('B-Gram-'+str(i)+'-'+str(j),dot(N[i],N[j],T)-aa*aa*kk)
    add('intrinsic-determinant',(aa*aa-kk)*(aa*aa+kk-2*T*T*aa*aa)-bb**4*cc*(3*T+1)**2)
    add('central-active-equation',-ll+2*T*aa*aa-bb*bb*cc)
    add('side-active-equation',-ll*T+aa*aa+kk-bb*bb*cc)
    add('norm-numerator',-ll+2*aa*aa-bb*(5*T+3))
    add('strict-longness',T*T*(5*T+3)-bb*cc-aa*(5*T*T-1))
    for v in range(3):
        add('B8-'+str(v),aa*(N[8][v]+N[1][v])-2*T*(N[2][v]+N[4][v]))
        add('B10-'+str(v),aa*(N[10][v]+N[4][v])-2*T*(N[1][v]+N[2][v]))
        add('B12-'+str(v),aa*aa*N[12][v]-(2*T*aa+4*T*T)*N[1][v]-(4*T*T-aa*aa)*N[2][v]+2*T*aa*N[4][v])
    q=aa*original['D']*Z*Z-2*original['D']*Z+2*T*T-T+1
    add('positive-Q',aa*q-original['D']*(aa*Z-1)**2-4*T*T)
    require(len(checks)==32,'all32 separate complete zero polynomial components')
    return checks
def taylor(rows,k,box):
    p={(i,j):v for i,j,w,v in rows if w==k};a,b,c,d=map(Q,box);x,y=(a+b)/2,(c+d)/2;rx,ry=(b-a)/2,(d-c)/2;co={}
    for (i,j),v in p.items():
        for u in range(i+1):
            for vslot in range(j+1):co[u,vslot]=co.get((u,vslot),Q(0))+v*comb(i,u)*comb(j,vslot)*x**(i-u)*y**(j-vslot)
    center=co.get((0,0),Q(0));err=sum((abs(v)*rx**i*ry**j for (i,j),v in co.items() if i or j),Q(0))
    require(center-err>0,'strict whole closed Taylor enclosure')
    data=(json.dumps([[i,j,str(v)] for (i,j),v in sorted(co.items())],separators=(',',':'))+'\n').encode()
    return {'box':list(map(str,box)),'lower':str(center-err),'upper':str(center+err),'complete_translated_coefficients':len(co),'whole_translated_array_sha256':hashlib.sha256(data).hexdigest()}
def produce(s,document,parent_bytes):
    coverage=validate(s,parent_bytes,reverse=True);f=literals(document);ids=identity_audit(s,f);signs=[]
    for name,part in s['strict_sign_obligations']:
        signs.append({'name':name+'-'+part}|taylor(f[name],int(part=='B'),s['t_interval']+s['z_interval']))
    require(len(signs)==6 and sum(r['complete_translated_coefficients'] for r in signs)==458,'all six alternate signs')
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'COMPLETE_ALTERNATE_DIGIT_AND_TAYLOR_COMPONENT_EXCLUSIONS',
            'coverage':coverage,'full_identity_records':ids,'whole_closed_Taylor_signs':signs,'complete_translated_coefficients':458,
            'primary_polynomial_expansion_division_Bernstein_used':False,'digit_engine_credit':'six-reviewer-3/source52fa998fb094b40a8fe1f3824d43108a6b909c09; unchanged generic arithmetic, not its review verdict',
            'same_author_new_checks':True,'independent_review_of_new_result':False,'remaining_feasibility':'UNRESOLVED','capacity_claimed':False,'global_bound_claimed':False}
if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('fixed20s alternate guard')));signal.alarm(20)
    parser=argparse.ArgumentParser();parser.add_argument('--emit');args=parser.parse_args()
    out=produce(json.loads((HERE/'SYSTEM.json').read_text()),json.loads((HERE/'FACTORS.json').read_text()),(HERE/'PARENT_SYSTEM.json').read_bytes())
    data=(json.dumps(out,separators=(',',':'))+'\n').encode()
    if args.emit:Path(args.emit).write_bytes(data)
    else:require(out==json.loads((HERE/'AUDIT.json').read_text()),'entire alternate expected artifact')
    print(json.dumps({'status':out['status'],'full_identity_components':32,'strict_translated_coefficients':458,'whole_audit_sha256':hashlib.sha256(data).hexdigest(),'capacity_claimed':False},indent=2))
