"""Explicit positive parameters; no downset or large matrix allocation."""
from fractions import Fraction as F
import importlib.util
import bootstrap
from exact import require
from weights import scalar as two_tail

spec=importlib.util.spec_from_file_location('credited_adaptive_parameters',bootstrap.ROOT/'adaptive-deletions/parameters.py')
tail=importlib.util.module_from_spec(spec);spec.loader.exec_module(tail)

NORMS={(4,2):F(22,17),(5,2):F(59,50),(6,2):F(129,115),
       (9,3):F(2825,2688),(10,3):F(937,900),(11,3):F(19447,18810)}
ETA=F(1,4096)
RECTANGLE_ETA=F(1,2**20)


def parameters(q,k):
    require(type(q) is int and type(k) is int and q>=4 and k in (2,3), 'literal q>=4,k2/3 required')
    require(k==2 or q>=8, 'this ansatz is infeasible for k3,q4..7')
    N=(q*q+13*q+16)//2-k; s=3*q+4
    if (q,k) in NORMS:
        d=NORMS[q,k]; kap=min(F(1,8),ETA/(2*d)); gamma=ETA/2
        p={'q':q,'k':k,'N':N,'s':s,'kappa':kap,'tau':min(kap/24,gamma/4),
           'seed_gamma':gamma,'gap':gamma/2,'eta':ETA,'delta_norm':d,'method':'finite cap continuity'}
    elif (q,k)==(8,3):
        p={'q':q,'k':k,'N':N,'s':s,'kappa':F(1,4096),'tau':F(1,2),
           'gap':RECTANGLE_ETA,'method':'finite affine rectangle'}
    elif k==2:
        old=two_tail(q);p={**old,'k':k,'kappa':F(1,8),'seed_gamma':old['gamma'],
                          'gap':old['gamma']/2,'method':'credited9145 tail'}
    else:
        old=tail.parameters(q,k);p={**old,'seed_gamma':old['gamma'],
                                    'gap':old['gamma']/2,'method':'credited9195 tail'}
    require(p['N']==N and p['s']==s and 0<p['kappa']<=F(1,8) and p['tau']>0 and p['gap']>0,
            'positive scalar premises')
    return p


def record(q,k):
    return {key:str(x) if isinstance(x,F) else x for key,x in parameters(q,k).items()}
