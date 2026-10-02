"""Exact symbolic congruences and exact upper-bound bridge controls."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time,signal,resource
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom,rational_value
from exact import require,matvec,dot,psd_rank
from model import parameters,fixed,base_pairing

def links_certificate():
    signal.alarm(60)
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    u,v=R(P({(1,0):1})),R(P({(0,1):1}));l,q=2+u,8+4*u+v
    N=2*q+12+2*l;J=(N-q-2)*(N-4)-3*(q-1)
    for z in (l,l-1,l+1,l+7,q,q-1,q+1,q+2,q+3,N-1,N-7,N-q-7,N-q-4,N-1-(q+3),J):atom(z.num)
    frac=lambda a,b=1:R(a)/b
    aug,tail,p,info=fixed(q,l,frac,upper_bounds=True)
    S3,b,EE,src=base_pairing(q,l,frac)
    rho=p['rho'];e=[R(1),-rho,R(0)]
    cross=[b[i]+sum(S3[i][j]*e[j] for j in range(3)) for i in range(3)]
    last=info['tau_bound']-EE+2*dot(e,b)+dot(e,matvec(S3,e))
    change=[[R(1),R(6),R(-6)],[R(-1),l,-l],[R(0),R(0),R(1)]]
    arr=[[sum(change[a][i]*S3[a][b0]*change[b0][j] for a in range(3) for b0 in range(3))
          for j in range(3)] for i in range(3)]
    xc=[sum(change[a][i]*cross[a] for a in range(3)) for i in range(3)]
    require(arr==[row[:3] for row in aug[:3]],'all9 symbolic arrow positions')
    require(xc==aug[3][:3] and last==aug[3][3],'all4 symbolic augmented positions')
    require(29*l*l-4*(2*l*l+6*l+9)==3*(7*l+6)*(l-2),'exact uniform Cfloor simplification')
    controls=[]
    for L,Q in ((2,8),(2,9),(3,12),(3,16),(4,16),(5,32),(10,100),(100,100000)):
        actual=parameters(Q,L);bound=parameters(Q,L,upper_bounds=True)
        require(actual['mu']>F(Q,6) and actual['etaP']>F(2*Q,3),'strict residual floors')
        require(actual['C']>bound['Cfloor']>=F(2*Q,29*L),'lower harmonic mean floor')
        require(actual['C']<bound['C'],'upper harmonic mean cap')
        require(0<actual['nuT']<bound['nuT'],'triangle norm bound')
        require(0<actual['nuL']<bound['nuL'],'pendant norm bound')
        for key in ('triangle','pendant'):
            diff=[[actual[key][i][j]-bound[key][i][j] for j in range(2)] for i in range(2)]
            require(psd_rank(diff)==1,'actual smaller Schur difference rank1 '+key)
            require(psd_rank(actual[key])==psd_rank(bound[key])==2,'exact closed cap control '+key)
        a0,t0,_,_=fixed(Q,L);a1,t1,_,_=fixed(Q,L,upper_bounds=True)
        require(a0==a1,'inverse bound independent of mean')
        diff=[[t0[i][j]-t1[i][j] for j in range(2)] for i in range(2)]
        require(psd_rank(diff)==1,'final mean-cap Schur domination')
        controls.append({'q':Q,'l':L,'C':str(actual['C']),'Cfloor':str(bound['Cfloor']),
                         'nuT':str(actual['nuT']),'nuT_bound':str(bound['nuT'])})
    signal.alarm(0)
    out={'agent':'six-downset-1','role':'researcher','symbolic_arrow_positions':9,
         'symbolic_augmented_positions':4,'uniform_mean_floor_identity':True,
         'bound_controls':controls,
         'status':'exact bridge controls; complete ordinary original-space proof in PROOF.md'}
    return out
