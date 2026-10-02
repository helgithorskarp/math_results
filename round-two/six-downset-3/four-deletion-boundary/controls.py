"""Reject concrete damaged hypotheses, pairings, operators and floors."""
from fractions import Fraction as F
import inputs
from matrices import core_data,original,closed_whole_entry,member,action,quadratic,require,digest
from exact import schur_psd
from orbits import grams


def run():
    rejected=[]
    def reject(label,fn):
        try:fn()
        except ValueError:rejected.append(label)
        else:raise ValueError('Damaged certificate accepted: '+label)
    reject('changed pinned entry input',lambda:inputs.setup(dict(inputs.PINS,**{'small-deletion-boundary/literal.py':'0'*64})))
    reject('deleted bcx retained',lambda:require(member(12,4,14),'deleted original vertex'))
    reject('out-of-ground-set bitmask',lambda:member(12,4,1<<15))
    X,N,s,C,D,R,U=core_data(12);n=N-1
    Sa=[F(bool(A&1)) for A in X[1:]]
    Sb=[F(bool(A&2)) for A in X[1:]];Sc=[F(bool(A&4)) for A in X[1:]]
    FF=[F(A.bit_count()==3 or A.bit_count()==2 and A&7==A) for A in X[1:]]
    z=[1-Sb[i]-Sc[i]+FF[i] for i in range(n)]
    bad=[row[:] for row in C];bad[0][0]+=1
    reject('changed largest-star diagonal',lambda:require(not any(action(bad,Sa)),'star kernel'))
    badD=[row[:] for row in D];badD[0][0]-=1000000
    reject('reversed lower Delta orientation',lambda:require(quadratic(z,badD)>0,'lower dual orientation'))
    badR=[row[:] for row in R];ix={A:i for i,A in enumerate(X[1:])}
    badR[ix[1]][ix[2]]=badR[ix[2]][ix[1]]=-1
    w=[F(11 if A&7==1 and (A>>3).bit_count()==1 else 12) for A in X[1:]]
    reject('one repaired trade sign reversed',lambda:require(quadratic(w,badR)==0,'repair pairing'))
    reject('discarded pair correction in upper dual',lambda:require(quadratic([F(12)]*n,U)<0,'strict negative upper pairing'))
    L00,_=closed_whole_entry(13,0,0)
    reject('empty loop incorrectly removed',lambda:require(L00==0,'actual empty loop'))
    _,keys,size,G,H=grams(13)
    reject('missing outside orbit',lambda:require(len(keys[:-1])==23,'complete fixed space'))
    badG=[row[:] for row in G];badG[0][0]-=1000000
    reject('negative lower Gram direction',lambda:schur_psd(badG))
    badH=[[H[i][j]-1000000*size[i]*int(i==j) for j in range(23)] for i in range(23)]
    reject('unsupported cap floor',lambda:schur_psd(badH))
    rec={'agent':'six-downset-3','role':'researcher','damage_rejections':len(rejected),'rejected':rejected,
         'status':'same-author mathematical input/certificate controls; not independent review'}
    rec['record_sha256']=digest(rec);return rec
