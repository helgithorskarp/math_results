"""Exact portable arithmetic for a uniform real near-balanced angular collar.

All pointwise spectral/IVT/Taylor bridges are in the ordinary written proof.
No sampled root locations, floating-point or solver theorem is used.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json

checks={}
def require(ok,label):
    if not ok:raise ValueError(label)
    checks[label]=True
def add(*ps):
    out={}
    for p in ps:
        for i,c in p.items():out[i]=out.get(i,F(0))+c
    return {i:c for i,c in out.items()if c}
def sc(p,k):return {i:c*k for i,c in p.items()if c*k}
def mul(p,q):
    out={}
    for i,c in p.items():
        for j,d in q.items():out[i+j]=out.get(i+j,F(0))+c*d
    return {i:c for i,c in out.items()if c}
def pw(p,n):
    out={0:F(1)}
    for _ in range(n):out=mul(out,p)
    return out
def der(p):return {i-1:i*c for i,c in p.items()if i}
def ev(p,x):return sum(c*x**i for i,c in p.items())
one={0:F(1)};r={1:F(1)}
a1={0:F(1),1:F(-1),2:F(1)}
a2={0:F(1),1:F(-2),2:F(3)}
require(add(mul(add(one,r),a1),sc(one,-1))=={3:F(1)},
        'entire inverse-odd Taylor remainder')
require(add(mul(pw(add(one,r),2),a2),sc(one,-1))=={3:F(4),4:F(3)},
        'entire inverse-cubic Taylor remainder')
num={0:F(4),1:F(3)}
require(add(mul(der(num),add(one,r)),sc(num,-2))=={0:F(-5),1:F(-3)},
        'entire monotone inverse-cubic remainder ratio derivative')

Dmax=F(1,729);tau=F(1,27);m=F(29,100);B=F(41,100)
R=F(1,480);L=F(40);c=F(1,8);Tmax=8*tau
require(tau*tau==Dmax,'entire exact square-root endpoint')
require(c-tau>m*m,'all original lower magnitude license')
require(c+tau<B*B,'all original upper magnitude license')
require(3*B<5*m,'entire strict four-plus-four sign-count comparison')
require(L*tau**3<R<m,'whole central root search collar')
deriv_lower=8/(B+R)**2;S1coef=512/m
require(L*deriv_lower>S1coef,'strict IVT signs for all 0<D<=Dmax')
require(ev({0:F(-5),1:F(-3)},-Tmax)<0 and Tmax<1,
        'ratio monotone over entire dimensionless deviation interval')
ratio_max=ev(num,-Tmax)/(1-Tmax)**2
require(ratio_max==F(2268,361),'whole sharp endpoint inverse-cubic remainder envelope')
S3coef=B*c**(-5)*ratio_max
K1=2*L*S3coef
K2=24*L**2/(m-R)**4
K=F(12_500_000)
require(K1+K2<K,'complete sum of two central-mass Taylor losses')
bound=2/(c-tau)+(K/32)*Dmax**2
require(bound==F(237004387,10097379),'whole final angular rational bound')
require(bound<F(47,2),'strict high-C exclusion')
margin=F(47,2)-bound
require(margin==F(568039,20194758),'whole threshold separation margin')

# Pointwise elementary strict inequality for q>0, cleared without divisions.
# 2q(1+q)^2 - [(1+q)^2-1] = 3q^2+2q^3.
require(add(sc(mul(r,pw(add(one,r),2)),2),sc(pw(add(one,r),2),-1),one)
        =={2:F(3),3:F(2)},'entire mass-to-angular upper comparison')

# Whole sharp-limit even family, variable d denotes D here.
# Since D is a parameter, regenerate coefficients by nested QQ[D][z].
fc=[{0:F(1)}, {}, {0:F(-1,2)}, {}, {0:F(3,32),1:F(-1,4)}, {},
    {0:F(-1,128),1:F(1,16)}, {}, {0:F(1,4096),1:F(-1,256)}]
powers=[{0:F(8)}]
for k in range(1,6):
    powers.append(sc(add(*[mul(fc[i],powers[k-i])for i in range(1,k)],sc(fc[k],k)),-1))
require(powers[1]==powers[3]==powers[5]=={},'whole sharp even-family odd moments')
require(powers[2]==one,'whole sharp even-family norm')
require(powers[4]=={0:F(1,8),1:F(1)},'whole sharp even-family fourth moment')
# Independent even factorization of all nine QQ[D][z] coefficients.
base=[{0:c*c},{0:-2*c},{0:F(1)}]
second=[{0:c*c,1:F(-1,4)},{0:-2*c},{0:F(1)}]
prod=[{}for _ in range(5)]
for i,x in enumerate(base):
    for j,y in enumerate(second):prod[i+j]=add(prod[i+j],mul(x,y))
require([prod[4-i//2]if i%2==0 else {}for i in range(9)]==fc,
        'all nine coefficients of literal sharp even family')
# The literal inverse-square sum at the even family's central root is
# 4/c+2/(c-sqrt(D)/2)+2/(c+sqrt(D)/2).
# Clear the paired denominator c^2-D/4 over QQ[D].
base_den={0:c*c,1:F(-1,4)}
S2_num=add(sc(base_den,4/c),{0:4*c})
m_num={0:F(1),1:F(-16)};m_den={0:F(1),1:F(-8)}
require(sc(mul(base_den,m_den),64)==mul(m_num,S2_num),
        'entire central mass of literal sharp even family')
p_num={1:F(8)}
require(add(m_den,sc(m_num,-1))==p_num,
        'entire complementary mass of sharp even family')
lower_num={0:F(16),1:F(-256)}
upper_num={0:F(16),1:F(-192)}
require(add(pw(m_den,2),sc(pw(m_num,2),-1),sc(pw(p_num,2),-1))
        ==mul(r,lower_num),'entire sharp-family lower squeeze')
require(add(pw(m_den,2),sc(pw(m_num,2),-1))==mul(r,upper_num),
        'entire sharp-family upper squeeze')
require(lower_num[0]==upper_num[0]==16,'whole two sharp-limit squeeze constants')
require(add(upper_num,sc(lower_num,-1))=={1:F(64)},
        'whole nonnegative sharp-limit squeeze gap')
require(1-16*Dmax>0,'sharp even-family positive-root domain')

generic_upper=F(12,329);repeated_upper=F(5,141)
require(F(47,2)*generic_upper==1-F(1,7),
        'whole seven-mass high-C endpoint')
require(F(47,2)*repeated_upper==1-F(1,6),
        'whole six-mass high-C endpoint')
require(Dmax<repeated_upper<generic_upper,
        'whole nonempty necessary high-C bands')

def coeffs(p):return [str(p.get(i,F(0)))for i in range(max(p,default=0)+1)]
record={'actual_agent':'six-sendov-2','role':'researcher','domain':'QQ; characteristic0; whole polynomial identities and rational endpoint signs',
 'parameters':{k:str(v)for k,v in [('Dmax',Dmax),('sqrt_Dmax',tau),('m',m),('B',B),('R',R),('L',L),('c',c)]},
 'whole_identities':{'inverse_odd_remainder':[str(v)for v in [0,0,0,1]],
                    'inverse_cubic_remainder':[str(v)for v in [0,0,0,4,3]],
                    'ratio_derivative':coeffs({0:F(-5),1:F(-3)}),
                    'mass_upper_comparison':coeffs({2:F(3),3:F(2)}),
                    'entire_even_family_octic_coefficients_descending':[coeffs(p)for p in fc],
                    'entire_even_family_moments':[coeffs(p)for p in powers],
                    'even_family_central_S2_numerator':coeffs(S2_num),
                    'even_family_central_S2_denominator':coeffs(base_den),
                    'even_family_central_mass_numerator':coeffs(m_num),
                    'even_family_central_mass_denominator':coeffs(m_den),
                    'even_family_lower_squeeze_numerator':coeffs(lower_num),
                    'even_family_upper_squeeze_numerator':coeffs(upper_num)},
 'bounds':{k:str(v)for k,v in [('central_derivative_lower',deriv_lower),('S1_coefficient',S1coef),
   ('S3_ratio_max',ratio_max),('S3_coefficient',S3coef),('K1',K1),('K2',K2),('K1_plus_K2',K1+K2),('K',K),
   ('angular_upper',bound),('threshold_margin',margin),('generic_upper_D',generic_upper),('repeated_upper_D',repeated_upper)]},
 'whole_checks':checks,'check_count':len(checks),'uniform_domain':'all real eight-vectors with mu1=mu3=mu5=0,mu2=1,0<D=mu4-1/8<=1/729; all multiplicities retained',
 'estimate':'C<16/(1-8sqrt(D))+390625 D^2<=237004387/10097379<47/2',
 'central_critical_root_bound':'abs(sigma)<40 D^(3/2)<1/480',
 'calibrating_leading_constant':16,'limit16_prior_art':'8753 and independent REVIEW8806, stronger full balanced sphere','sharp_family':'(z^2-1/8)^2[(z^2-1/8)^2-D/4]',
 'ordinary_bridges':['real symmetric full spectral compression','IVT/strict logarithmic derivative','Taylor with signed original-root distance license','full spectral masses grouped by eigenspace','sharp-limit squeeze'],
 'unformalized':True,'independently_unreviewed':True,'proof_status':'ordinary author proof; not formally verified'}

def canonical(value):
    return json.dumps(value,sort_keys=True,indent=2)+'\n'
def unique_object(pairs):
    out={}
    for key,value in pairs:
        if key in out:raise ValueError('duplicate expected field: '+key)
        out[key]=value
    return out
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('EXPECTED.json'))
parser.add_argument('--generate',action='store_true',help='emit fresh record without a fixture comparison')
args=parser.parse_args()
raw=canonical(record).encode()
if not args.generate:
    saved=json.loads(args.expected.read_text(),object_pairs_hook=unique_object)
    if canonical(saved)!=raw.decode():raise ValueError('entire expected record/type mismatch')
if args.output:args.output.write_bytes(raw)
print(json.dumps({'actual_agent':'six-sendov-2','role':'researcher','engine':'stdlib Fraction',
                  'check_count':len(checks),'entire_expected_compared':not args.generate,
                  'K1_plus_K2':str(K1+K2),'bound':str(bound),'margin':str(margin),
                  'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},sort_keys=True))
