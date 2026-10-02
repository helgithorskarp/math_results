"""Reject damaged hypotheses, duals, original entries and orbit floors."""
from fractions import Fraction as F
import inputs
from matrices import core_data,domain,closed_whole_entry,member,action,quadratic,require,digest
from duals import lower_vector,exceptional_vector
from exact import schur_psd
from orbits import grams

def run():
    rejected=[]
    def reject(label,fn):
        try:fn()
        except ValueError:rejected.append(label)
        else:raise ValueError('Damaged certificate accepted: '+label)
    reject('changed pinned entry input',lambda:inputs.setup(dict(inputs.PINS,**{'small-deletion-boundary/literal.py':'0'*64})))
    reject('illegal five deletions from four outside points',lambda:domain(4,5))
    reject('deleted bcx retained',lambda:require(member(18,5,14),'deleted original vertex'))
    reject('out-of-ground-set bitmask',lambda:member(18,5,1<<21))
    X,N,s,C,D,R,U=core_data(18);n=N-1;z=lower_vector(X);w=exceptional_vector(X)
    star=[F(bool(A&1)) for A in X[1:]]
    bad=[row[:] for row in C];bad[0][0]+=1
    reject('changed largest-star diagonal',lambda:require(not any(action(bad,star)),'star kernel'))
    badD=[row[:] for row in D];badD[0][0]-=1000000
    reject('reversed lower Delta orientation',lambda:require(quadratic(z,badD)>0,'lower dual orientation'))
    badR=[row[:] for row in R];ix={A:i for i,A in enumerate(X[1:])}
    badR[ix[1]][ix[2]]=badR[ix[2]][ix[1]]=-1
    reject('one repaired trade sign reversed',lambda:require(quadratic(w,badR)==0,'repair pairing'))
    damaged=[w[i]-int(A&7 in (2,3,4,5) and (A>>3).bit_count()==1) for i,A in enumerate(X[1:])]
    reject('exceptional dual loses its positive orbit correction',lambda:require(quadratic(damaged,U)<0,'strict exceptional upper pairing'))
    reject('exceptional dual replaced by its constant part',lambda:require(quadratic([F(32)]*n,U)<0,'constant dual negative'))
    L00,_=closed_whole_entry(19,0,0)
    reject('empty loop incorrectly removed',lambda:require(L00==0,'actual empty loop'))
    _,keys,size,G,H=grams(19)
    reject('missing outside orbit',lambda:require(len(keys[:-1])==23,'complete fixed space'))
    badG=[row[:] for row in G];badG[0][0]-=1000000
    reject('negative lower Gram direction',lambda:schur_psd(badG))
    badH=[[H[i][j]-1000000*size[i]*int(i==j) for j in range(23)] for i in range(23)]
    reject('unsupported cap floor',lambda:schur_psd(badH))
    rec={'agent':'six-downset-3','role':'researcher','damage_rejections':len(rejected),'rejected':rejected,
         'status':'same-author mathematical input/certificate controls; not independent review'}
    rec['record_sha256']=digest(rec);return rec
