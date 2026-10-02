"""Separate H36 refinement, developed after the first independent H30/H32 seal.

No author inputs. Changed radius, mean coefficient, coarse Maclaurin tail,
absorption and final costs are rebuilt and checked in full.
"""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[k]='1'
import argparse,hashlib,json,signal,sys
from fractions import Fraction as F
from math import comb
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from polys import cast,symbol,need
from build import scalar
from verify import build,parse,same

def record():
    core=build();raw=json.dumps(core,sort_keys=True,separators=(',',':')).encode()
    need(hashlib.sha256(raw).hexdigest()=='bccbff984160d4a45bff596722abd391b79d16cb1d5d3df88de3f680a6061214','original sealed core changed')
    checks=[]
    def equal(a,b,label):need(a==b,label);checks.append(label)
    e,x,y,L,v1,v2,A,B=[symbol(s) for s in ['eta','x','y','L','v1','v2','A','B']]
    kap=F(7,32);beta=F(1,16);alpha=F(9,64)
    need(F(14,9)*kap-F(5,18)==beta,'new mean coefficient')
    left=F(8,9)*(1-e)*A+F(7,6)*B-F(14,9)*kap*y
    comparison=F(8,9)*(A+B)-beta*y+F(8,9)*e*x
    equal(comparison-left,F(5,18)*(y-B)+F(8,9)*e*(x+A),'entire new complex phase comparison')
    mean=F(45,8)*e+F(9,128)*y-9*e**2-F(8,9)*x**2-e*x
    D0=9*e+x+y+L
    diag=(18*(9*e-mean+8*e*x+7*e*y+L)+7*x*x+5*y*y+3*L*L)/9
    nx=diag+(D0*x+6*x*y+8*D0*v1+8*L*L+4*y*L)/9+v1
    ny=diag+(2*D0*y+7*D0*v2+7*L*L+3*y*L+5*x*L)/9+v2
    # Whole dropped envelopes are regenerated independently with changed
    # kappa, not assumed to retain the previous favorable coefficient.
    old_alpha=F(151,1024)
    def decode(poly):
        out=cast(0)
        for key,pair in poly.items():
            term=cast((F(pair[0]),F(pair[1])))
            if key!='1':
                for factor in key.split('*'):
                    z=factor.split('^');term*=symbol(z[0])**(int(z[1]) if len(z)>1 else 1)
            out+=term
        return out
    old=core['audit']['norm_bounds']
    equal(nx+alpha*y,decode(old[0])+old_alpha*y,'whole first changed-radius dropped envelope')
    equal(ny+alpha*y,decode(old[1])+old_alpha*y,'whole second changed-radius dropped envelope')
    H=F(36);Q=F(17,8);E=F(1,256);end=E*E;delta=F(1,1000)
    Y0=F(162);C0=F(13,4);X=F(19);Y=F(24);UC=F(17);cube=F(217);C=F(19,40)
    lower=[F(9,k)*comb(8,9-k)*Q**(9-k)*E**(7-k) for k in range(1,7)]
    need(H/8<=Q*Q and sum(lower)<C0 and max(lower[:2])<delta,'whole new initial Maclaurin bounds')
    need(H*(F(256,255)*E)**2<F(1,40)**2,'whole new critical circle radius')
    need(F(1,4)-F(5,4)*F(1,40)==kap and kap+F(3,4)<1,'new convergent square-tail energy')
    coarse=(nx+alpha*y).substitute({'y':Y0*e,'L':C0*e,'v1':delta*e})
    K0=18+14*Y0+F(5,9)*Y0*Y0+F(11,9)*C0*C0+F(4,9)*Y0*C0+F(8,9)*(9+Y0+C0)*delta
    eta_x=19+F(7,9)*Y0+C0/9+F(8,9)*delta
    equal(coarse,(F(27,4)+2*C0+delta)*e+K0*e**2+eta_x*e*x+F(8,3)*x*x,'whole widened first bootstrap')
    first=F(27,4)+2*C0+delta+end*K0
    lam=F(8,3)*9*Q*E+eta_x*end
    need(first<14 and lam<F(1,4),'new strict mean absorption')
    need(F(56,3)<X and F(8,9)*X<UC,'new mean scale')
    ybound=F(9,14)*(H+F(64,81)*X*X*end)
    need(ybound<Y and H**3<cube**2,'new second and third moments')
    tail=sum(lower[:5])+UC**3*end**2/4+F(3,4)*UC*H*end+cube*E/2
    need(tail<C,'new complete lower tail')
    subst={'x':X*e,'y':Y*e,'L':C*e,'v1':delta*e,'v2':delta*e}
    base=F(27,4)+2*C+delta
    costs=[]
    for name,p in [('x',nx),('y',ny)]:
        final=(p+alpha*y).substitute(subst)
        cost=scalar(final.coefficient('eta',2))[0];costs.append(cost)
        equal(final,base*e+cost*e**2,'entire widened final '+name+' cost')
        need(cost<2400,'new quadratic cost budget')
    cap=base+2400*end;need(cap<F(31,4),'strict new cap31/4')
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'original_sealed_record_sha256':hashlib.sha256(raw).hexdigest(),
            'energy_cutoff':36,'whole_identities':checks,
            'norm_bounds':[nx.record(),ny.record()],
            'initial_lower_bounds':[str(v) for v in lower],
            'budgets':{k:str(v) for k,v in {'radius':F(1,40),'kappa':kap,'mean_beta':beta,'favorable_alpha':alpha,'Q':Q,'C0':C0,'Y0':Y0,'first_constant':first,'lambda':lam,'first_x_cap':F(56,3),'x_cap':X,'y_bound':ybound,'y_cap':Y,'U_cap':UC,'third_moment_constant':cube,'full_lower_tail':tail,'lower_cap':C,'Kx':costs[0],'Ky':costs[1],'quadratic_budget':F(2400),'cap':cap,'strict_cap_margin':F(31,4)-cap}.items()},
            'trust_boundary':'ordinary binomial convergence, disk-root positivity, Fourier/norm/Maclaurin and monotonicity bridges; no author input or independent-before-author claim for this later refinement'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected',type=Path,default=Path(__file__).with_name('REFINEMENT.json'));ap.add_argument('--generate',action='store_true');ap.add_argument('--emit',action='store_true');a=ap.parse_args()
    signal.alarm(45);got=record();raw=json.dumps(got,sort_keys=True,separators=(',',':')).encode()
    if a.generate:a.expected.write_text(json.dumps(got,indent=2,sort_keys=True)+'\n')
    if not same(got,parse(a.expected.read_text())):raise ValueError('entire typed refinement fixture differs')
    if a.emit:sys.stdout.buffer.write(raw+b'\n')
    else:print('PASS H36 energy refinement '+hashlib.sha256(raw).hexdigest())

if __name__=='__main__':main()
