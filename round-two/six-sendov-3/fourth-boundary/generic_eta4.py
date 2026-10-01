#!/usr/bin/env python3
"""six-sendov-3 researcher: complete generic real fourth-order moment jet.

Gaussian rational Newton ring, epsilon,z, fifteen independent real moment
symbols and five imaginary moment symbols. Imaginary products start past
epsilon8. Analytic order bounds are a separately written bridge.
"""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import importlib.util,json,time
SOURCE=Path(__file__).with_name('arithmetic.py')
spec=importlib.util.spec_from_file_location('moment_arithmetic',SOURCE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.NV=22;m.ORDER=8;m.ZERO_EXP=(0,)*m.NV
pc,pv,add,mul,pow,scale=m.pc,m.pv,m.padd,m.pmul,m.ppow,m.pscale
eps,z=pv(0),pv(1);eta=pow(eps,2)
names=['U','H','W','D','J21','U3','J4','J22','J41','J6','U4','J23','J42','J61','J8']
U,H,W,D,J21,U3,J4,J22,J41,J6,U4,J23,J42,J61,J8=[pv(j) for j in range(2,17)]
ims=[pv(j) for j in range(17,22)]
t0=time.monotonic();checks=0
def check(a,b,label):
    global checks
    if a!=b:raise RuntimeError(label)
    checks+=1
im=lambda j,n:scale(mul(ims[j],pow(eps,n)),0,1)
powers=[pc(),
    add(mul(U,eta),mul(W,pow(eta,2)),im(0,5)),
    add(scale(mul(H,eta),-1),mul(D,pow(eta,2)),im(1,5)),
    add(scale(mul(J21,pow(eta,2)),-3),mul(U3,pow(eta,3)),im(2,5)),
    add(mul(J4,pow(eta,2)),scale(mul(J22,pow(eta,3)),-6),
        mul(U4,pow(eta,4)),im(3,7)),
    add(scale(mul(J41,pow(eta,3)),5),scale(mul(J23,pow(eta,4)),-10),im(4,7)),
    add(scale(mul(J6,pow(eta,3)),-1),scale(mul(J42,pow(eta,4)),15)),
    scale(mul(J61,pow(eta,4)),-7),mul(J8,pow(eta,4))]
es=[pc(1)]
for n in range(1,9):
    es.append(scale(add(*(scale(mul(es[n-j],powers[j]),(-1)**(j-1))
                          for j in range(1,n+1))),F(1,n)))
der=scale(add(*(scale(mul(es[j],pow(z,8-j)),(-1)**j) for j in range(9))),9)
prim=m.pint(der,1);marked=add(pc(1),scale(eta,-1))
p=add(prim,scale(m.psubst(prim,1,marked),-1))
check(m.psubst(p,1,marked),{},'complete generic anchor')
# Independent generating-product route: coefficients of
# exp(sum (-1)^(j-1) P_j t^j/j), as a product of eight truncated
# exponentials. This does not call the Newton recurrence above.
from math import factorial
partition=[pc(1)]+[pc() for _ in range(8)]
for j in range(1,9):
    factor={j*r:scale(pow(powers[j],r),
                     F((-1)**((j-1)*r),j**r*factorial(r)))
            for r in range(8//j+1)}
    next_partition=[pc() for _ in range(9)]
    for a,pa in enumerate(partition):
        for b,pb in factor.items():
            if a+b<=8:next_partition[a+b]=add(next_partition[a+b],mul(pa,pb))
    partition=next_partition
check(partition,es,'all elementary coefficients: Newton versus partition expansion')
partition_der=scale(add(*(scale(mul(partition[j],pow(z,8-j)),(-1)**j)
                          for j in range(9))),9)
partition_prim=m.pint(partition_der,1)
partition_pol=add(partition_prim,scale(m.psubst(partition_prim,1,marked),-1))
check(partition_pol,p,'entire anchored complex jet: independent partition route')
real={e:(a,F(0)) for e,(a,b) in p.items() if a}
check(all(e[0]%2==0 for e in real),True,'entire real jet epsilon-even')
check(all(not any(e[17:]) for e in real),True,'all independent imaginary products omitted only beyond eta4')
check(all(e[0]>=5 for e,(a,b) in p.items() if b),True,'entire imaginary coefficient order at least epsilon5')
check({e:v for e,v in real.items() if e[0]==0},add(pow(z,9),pc(-1)),
      'limiting nonagon')
g8={tuple([0]+list(e[1:])):v for e,v in real.items() if e[0]==8}

# Independently sum all one-point binomial scalar coefficients through eta4.
hh,uu=pv(2),pv(3);q=add(pc(1),uu)
ds=add(pow(add(pc(1),scale(mul(eta,q),-1)),2),mul(eta,hh,hh))
delta=add(ds,pc(-1))
inverse=add(*(scale(pow(delta,j),a) for j,a in enumerate(
    [F(1),F(-1,2),F(3,8),F(-5,16),F(35,128)])))
a4=add(pow(q,4),scale(mul(pow(hh,2),pow(q,3)),-5),
    scale(mul(pow(hh,4),pow(q,2)),F(45,8)),
    scale(mul(pow(hh,6),q),F(-35,16)),scale(pow(hh,8),F(35,128)))
check({tuple([0]+list(e[1:])):v for e,v in inverse.items() if e[0]==8},a4,
      'complete scalar fourth coefficient')
record={'agent':'six-sendov-3','role':'researcher','status':'complete generic real eta4 and scalar identities',
    'epsilon_order':8,'variables':22,'real_moments':names,'imaginary_moments':5,
    'checks':checks,'derivative_terms':len(der),'anchored_terms':len(p),
    'g8_terms':len(g8),'derivative_hash':m.phash(der),'anchored_hash':m.phash(p),
    'g8_hash':m.phash(g8),'g8_complete_record':m.precord(g8),
    'scalar_eta4_record':m.precord(a4)}
