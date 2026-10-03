"""Exact polynomial identities and known feasible controls; no UNSAT search.

Actual author six-tammes-2, researcher. Standard-library Python3.11+.
The three local polynomial slots mean (t,z,w) for the frame and (t,u,v)
for the separate universal chart identities. They never identify the six
distinct addition variables in the nine-variable mathematical system.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json,signal
from polynomials import P,dot
from model import CORE,CONTACTS,make,stereographic,incumbent_quintic
from schema import require,layout
from incumbents import check_incumbents

HERE=Path(__file__).resolve().parent
FROZEN=('INPUT.json','SYSTEM.json','field.py','polynomials.py','model.py','schema.py','incumbents.py','check.py','controls.py')
def pins():
    p=json.loads((HERE/'RUNTIME_PINS.json').read_text())
    require(set(p)==set(FROZEN),'complete nine-file runtime pins')
    for n in FROZEN:require(hashlib.sha256((HERE/n).read_bytes()).hexdigest()==p[n],n+' source pin')
    return p

def identities():
    t,z,w=(P.var(i) for i in range(3));m=make(t,z,w);Y=m['points'];O=m['Omega'];R=m['root_squared'];a,b,c=m['a'],m['b'],m['c'];C,S,G,E=m['C'],m['S'],m['G'],m['E'];K=t*(9*t*t-2*t-3)
    records=[]
    def identity(name,raw,reduce=True):
        red=raw.reduced(R) if reduce else raw
        require(not red.c,'nonzero exact polynomial identity '+name)
        records.append({'name':name,'unreduced_terms':len(raw.c),'unreduced_w_degree':max((k[2] for k in raw.c),default=0),'exactly_zero':True})
    for i in CORE:identity('unit-'+str(i),dot(Y[i],Y[i],t)-O*O)
    for i,j in CONTACTS:identity('contact-'+str(i)+'-'+str(j),dot(Y[i],Y[j],t)-t*O*O)
    H=4*t*t-a
    for i,j in ((0,9),(5,6),(7,11),(1,8),(2,12),(4,10)):identity('h-noncontact-'+str(i)+'-'+str(j),a*dot(Y[i],Y[j],t)-H*O*O)
    for i,j in ((6,7),(6,9),(7,9),(4,12),(8,10)):identity('k-noncontact-'+str(i)+'-'+str(j),a*a*dot(Y[i],Y[j],t)-K*O*O)
    ell=2*t*(H*a+K)-t*a**3
    identity('ell-noncontact-8-12',a**3*dot(Y[8],Y[12],t)-ell*O*O)
    identity('chart-contact-gap',C*(dot(Y[7],Y[1],t)-t*O*O)-b*c*(b*b*z*z-1)*O*O)
    identity('s-contact-product',C*dot(Y[7],Y[10],t)-S*O*O)
    for new,i,j,old in ((6,0,11,5),(7,0,5,11),(9,5,11,0),(8,2,4,1),(10,1,2,4),(12,1,10,2)):
        for k in range(3):identity('reflection-'+str(new)+'-component-'+str(k),a*Y[new][k]-2*t*(Y[i][k]+Y[j][k])+a*Y[old][k])
    core_count=len(records)
    identity('G-first-square',G-a**4*(1-t*t)*E+(K*C-S*t*a*a)**2,False)
    identity('G-second-square',G-(a**4-K*K)*(1-t*t)*C*C+(S*a*a-K*t*C)**2,False)
    identity('D-decreasing',m['D'].deriv(0)+6*t*b,False)
    identity('J-increasing-formula',m['J'].deriv(0)-(27*t*t-2*t-1),False)
    identity('h-gap-factorization',H-t*a-(3*t+1)*(t-1),False)
    identity('k-gap-factorization',K-t*a*a-4*t*(2*t+1)*(t-1),False)
    identity('incumbent-quintic-derivative',incumbent_quintic(t).deriv(0)-(65*t**4-4*t**3+18*t*t+4*t-3),False)
    # Fresh (t,u,v) slots: no reduction modulo the core radical is made here.
    u,v=P.var(1),P.var(2);T,A,Rchart=stereographic(t,u,v);anchor=[P.cv(1),P.cv(0),P.cv(0)]
    identity('stereographic-unit',dot(T,T,t)-A*A,False)
    identity('stereographic-anchor',dot(T,anchor,t)-(Rchart-1),False)
    identity('stereographic-inverse-denominator',A-dot(T,anchor,t)-2,False)
    identity('stereographic-disk-bound',Rchart-b*(u*u+v*v)-b*t*(u+v)**2,False)
    identity('stereographic-anchor-gap',t*A-dot(T,anchor,t)-(a-b*Rchart),False)
    require(core_count==64 and len(records)==76,'complete exact generic identity census')
    require(all(k[2]<=1 for row in Y.values() for x in row for k in x.c),'all twelve frame numerators affine in positive radical')
    require(all(k[2]==0 for k in O.c),'common denominator root independent')
    return {'generic_core_identities_actually_checked':core_count,'generic_scalar_and_chart_identities_actually_checked':len(records)-core_count,'all_generic_identities_actually_checked':len(records),'records':records,'max_core_numerator_terms':max(len(x.c) for row in Y.values() for x in row),'common_denominator_terms':len(O.c),'core_numerator_radical_degree':1}

def bounds():
    lo,hi=Q(14,25),Q(593,1000)
    D=lambda t:(1-t)**2*(1+2*t)
    J=lambda t:9*t**3-t*t-t+1
    require(D(lo)<Q(1,2) and D(hi)>0,'whole interval positive D below one half, by checked derivative')
    require(J(lo)>1 and 27*lo*lo-2*hi-1>0,'whole interval J>1, by checked derivative')
    require(9*lo*lo-1>0 and 1+hi<Q(8,5),'positive h and a<8/5')
    require(1/(1-hi)<Q(5,2),'core chart covers all finite z')
    require(1/(2*(1-lo*lo))==Q(625,858),'uniform E/C^2 strict lower bound')
    require(2*Q(8,5)**6<36,'scaled positive radical strictly below6')
    disk_margin=10*(1-hi)**2-(1+hi)
    require(disk_margin==Q(6349,100000)>0 and Q(16,5)**2>10,'six stereographic coordinates covered without pole')
    Fprime_lower=65*lo**4-4*hi**3+18*lo*lo+4*lo-3
    require(Fprime_lower>0,'incumbent quintic strictly increasing on entire I, so strict improvement is integral polynomial inequality')
    return {'t_closed':[str(lo),str(hi)],'E_over_C_squared_strict_lower':'625/858','common_denominator_strictly_positive':True,'positive_scaled_radical_strict_upper':'6','added_disk_squared_radius_strict_upper':'10','added_box_absolute_bound':'16/5','exact_disk_margin':str(disk_margin),'incumbent_quintic_derivative_uniform_positive_lower':str(Fprime_lower),'exact_integral_strict_improvement':'-F(t)>0'}

def run():
    source=pins();data=json.loads((HERE/'INPUT.json').read_text());s=json.loads((HERE/'SYSTEM.json').read_text())
    out={'format':'bounded-polynomial-model-exact-check-v1','actual_agent':'six-tammes-2','role':'researcher','scope':'lossless conditional reduction; no exclusion or global bound','source_pins':source,'system':layout(s,data),'bounds':bounds(),'polynomial_identities':identities(),'positive_controls':check_incumbents(data,s)}
    return out

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second model-check guard')));signal.alarm(50)
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();out=run();raw=json.dumps(out,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(raw)
    print(raw,end='')
if __name__=='__main__':main()
