"""Two-valued original PSD dual for every real kappa,t at q4..12."""
from fractions import Fraction as F
import json
from matrices import core_data,action,quadratic,require,digest


def check(q):
    X,N,s,C,D,R,U=core_data(q);n=N-1;h=F(1,3*q+5)
    alpha=F(q*(q+1),2)+3*(q+1)*h
    Sa=[F(bool(A&1)) for A in X[1:]]
    Sb=[F(bool(A&2)) for A in X[1:]];Sc=[F(bool(A&4)) for A in X[1:]]
    FF=[F(A.bit_count()==3 or A.bit_count()==2 and A&7==A) for A in X[1:]]
    z=[1-Sb[i]-Sc[i]+FF[i] for i in range(n)]
    require(not any(action(C,z)) and not any(action(R,z)), 'original lower dual kernels')
    require(quadratic(z,D)==alpha>0,'original lower dual positive orientation')
    require(not any(action(D,Sa)) and not any(action(R,Sa)), 'unmoved largest-star kernels')
    y=[F(A&7==1 and (A>>3).bit_count()==1) for A in X[1:]]
    w=[12-v for v in y]
    p0=quadratic(w,U);pd=quadratic(w,D);pr=quadratic(w,R)
    empty=F(q*q-11*q+6,2);cross=9*q+4-F(8,q)
    require(sum(y)==q and sum(map(sum,C))==4*(s-4),'original pair and empty census')
    require(sum(action(U,y))==cross,'original mean-pair cross term')
    require(quadratic(y,U)==q*(N-s) and not quadratic(y,D),'original pair diagonal block')
    require(sum(action(D,y))==q*h,'original mean-pair derivative cross')
    require(p0==144*empty-24*cross+q*(N-s)<0,'closed negative upper dual')
    require(pd==144*(alpha-8*h)-24*q*h>0 and pr==0,'all-real upper dual orientations')
    return {'q':q,'k':4,'N':N,'s':s,'lower_Delta_pairing':str(alpha),
            'upper_U0_pairing':str(p0),'upper_Delta_pairing':str(pd),'upper_R_pairing':str(pr),
            'integer_dual':'11 on every pair ax,12 on every other surviving nonempty member',
            'all_original_actions_and_pairings_verified':True}


def run():
    from matrices import original
    from literal import core_data as prior
    fresh=original(8,k=3);old=prior(8,3)
    require((fresh[0],fresh[1],fresh[2],fresh[3],fresh[4])==(old[0],old[1],old[2],old[3],old[6]),
            'all original q8,k3 baseline entries')
    rec={'agent':'six-downset-3','role':'researcher','baseline':'published q8,k3 original entries reproduced; not new',
         'all_real_ansatz_exclusions':[check(q) for q in range(4,13)],
         'bridge':'lower PSD forces kappa>=0; upper dual is p0-kappa*pd<0 for every real t; ordinary unformalized'}
    rec['record_sha256']=digest(rec);return rec


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
