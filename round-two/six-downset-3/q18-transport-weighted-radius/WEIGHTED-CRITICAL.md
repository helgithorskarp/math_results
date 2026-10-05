# No sharp original completion at the new weighted radius

Actual **six-downset-3 / researcher**, 2026-10-05. PRIVATE ordinary
author-complete deduction, unformalized and independently unreviewed.
New source/cold/publication gates remain unpaid. No source commit or
graph packet exists. The exact original domain, witness, comparison,
cost Delta, distance d and weighted root rho are those in
[WEIGHTED-PROOF.md](WEIGHTED-PROOF.md), with ALL its ordinary premises.

For EVERY real tau in[0,1/256] and EVERY original sharp optimizer,

    d(M)>rho.

There is also ONE eta_rho>0, uniformly over all such tau and optimizers,
with d(M)>=rho+eta_rho. This extra gap is existential; the previously
proved explicit gap eta0 above r_* remains valid. Neither an exact
best original distance nor a realization at a new endpoint is claimed.

## Sharp weighted equality fixes every bad-block entry

Suppose a sharp M had d<=rho. The necessary curve excludes d<rho.
At e=rho put lambda=lambda(rho)>0 and u=1_B+lambda1_bcW. Use

    x=a(rho)-9lambda,
    y=(b(rho)+351lambda)/19,
    z=-(T(rho)+342lambda)/38.

The licensed weighted group lower bounds, group Cauchy, weighted Schur
and sharp dual give

    E_lambda(rho)<=||Au||^2<=58*u^T C_BB u
                 <=58*u^T C_old,BB u=E_lambda(rho).

Thus equality holds throughout. Strict monotonicity in the positive
group masses and equality in group Cauchy force the ENTIRE original
58-vector q=Au:

    q_abc=x, q_s=y for each s in J, q_s=z for each s in N.  (1)

The mass lower bounds are attained. Every one of the72 original
abc/pure and1224 original J/pure movable entries individually has
decrement at most220rho. Equality of each corresponding sum therefore
forces ALL1296 entries to attain their radius lower bound:

    A_s,p=C_dagger,s,p-220rho on EVERY disjoint
                (J union{abc})/pure-pair position.       (2)

Intersecting entries stay-1. The nine triple J column sums remain39;
they are not individually forced to have a common entry decrement.

For sharp M, every disjoint B/B increment relative to C_old is
nonpositive by the full sharp dual identity. Every weight product
u_i u_j is strictly positive. Equality of the weighted bad-block
quadratic form therefore forces EACH of the2628 increments to vanish:

    C_BB=C_old,BB.                                      (3)

The original Schur complement K=C_BB-A^T A/58 is PSD and u^T K u=0,
so Ku=0. The PSD-kernel implication follows, for example, by applying
nonnegativity to (u+t h)^T K(u+t h) for every real t. Consequently

    C_old,BBu=A^T q/58 on ALL81 original bad columns.    (4)

No particular transport recipe, invariance or factorization of the
unknown original M is assumed. Conditions(1)-(4) hold for ANY possible
critical full sharp completion.

## A pure original column gives a rational contradiction

For a pure bad pair p, set Aabc,p=C_dagger,abc,p-220rho and
Jp=sum_J C_dagger,s,p-3740rho. There are exactly17 disjoint J vertices
for EACH of the72 original pure pairs, so3740=220*17. Using its whole
column kernel to eliminate the N sum, equation(4) becomes

    (C_old,BB1_B)_p+lambda*(C_old,BB1_bcW)_p
       =((x-z)Aabc,p+(y-z)Jp)/58.                       (5)

For EVERY ZZ pair the defining-data census gives

    (C_old,BB1_B)_p=255373/4096,
    (C_old,BB1_bcW)_p=-2835/16384,
    C_dagger,abc,p=2198899277/1073741824,
    sum_J C_dagger,s,p=132782138143/4294967296.

Substitute the affine x(e),y(e),z(e),lambda(e) from the weighted theorem
into the left side minus right side of(5), with e in place of rho.
Call the resulting exact quadratic H_ZZ(e). Division by F(e) from
WEIGHTED-PROOF.md gives the exact remainder

    H_ZZ(e)-(-1272126240/551)/(91593089280/551)*F(e)
       =79062341267566127785921/101641559846139629404160
        -(26939671381557/295815872512)e.                 (6)

The checker reconstructs the two complete polynomial coefficient
lists and verifies their subtraction exactly. Since F(rho)=0, the
required equality H_ZZ(rho)=0 would force

    rho=79062341267566127785921/9256400603901956204789760
        >1/150>1/314,                                   (7)

whereas the proved root satisfies rho<1/314. All quantities in this
contradiction are rational except the specified root itself; the
rational inequality alone excludes equality. Alternatively, the
nonzero affine remainder has only a rational zero while rho is
irrational. One original ZZ column already suffices.

The fresh code checks EVERY original column. All36 ZZ remainders are
the displayed one, and all36 WW remainders are exactly its negative;
both force the same incompatible rational radius(7). ALL nine bcW
equations are IDENTICALLY zero for the selected lambda, as expected
from lambda=(b-19R)/580. Thus the new pure-class obstruction is not
the earlier triple-column obstruction at r_*. It excludes EVERY
critical full sharp completion at rho. With the necessary d>=rho,
this proves d>rho for every permitted original optimizer.

The opposite pure-class remainders suggest allowing different ZZ/WW
weights as a concrete next direction. No third-weight improvement,
weight-family completeness, normalized optimum or best original
distance follows from that suggestion; those claims remain unpaid.

## Uniform separation and exact evidence

The same joint optimizer set used in CRITICAL-EXTENSION.md is

    K_all={(tau,M):0<=tau<=1/256,M in F_tau,
                          P(M)=476335/32768+41tau}.

It is nonempty by the credited sharp attainment theorem. Original
nonnegative stochastic entries lie in[0,1]; symmetry, support, row
equations, floors, PSD and continuous sharp-cost equality are closed.
Thus K_all is compact. The original finite maximum distance d is
continuous and attains its minimum mu on K_all. The just-proved
strict inequality applies also to a minimizer, so mu>rho. Taking
eta_rho=(mu-rho)/2 proves the uniform existential gap above rho.
It does not give a numerical value of that gap or an optimal distance.

weighted_critical.py reads the same whole-pinned defining CANDIDATE
and COMPARISON data and openly shares only the NEW local census
decoder. It reconstructs all6561 comparison entries, all81 critical
column equations, the correct72/9 pure/triple licences, the full
polynomial coefficients and affine remainders. Exact normal/O whole
outputs agree at4379B, with SHA256
b55751964c3e5ef6ddf55e99b6424f73a660b857dcce0fd6241d2954bd1a58dd.
The compact record classifies ALL81 original masks with36/36/9 actual
multiplicities; every member was checked, not inferred from an orbit
representative. Standard-library rational arithmetic and integer
square-root checks suffice; no floating solver or PSD factor is used.

The first exploratory scratch calculation incorrectly decremented
the triple J sums by18*220e and is preserved as an unlicensed failed
trial. It supports no theorem. The fresh checker keeps ALL nine
triple sums constant39 and verifies their exact zero remainders.
Reproduce the new finite record with

```sh
python3 -B weighted_critical.py > /tmp/q18-weighted-critical-normal.json
python3 -B -O weighted_critical.py > /tmp/q18-weighted-critical-O.json
```

Weighted equality, individual-entry saturation, singular Schur,
PSD-kernel, polynomial division and compactness are ordinary proof
bridges, unformalized and independently unreviewed. Source-before-import,
isolated cold and remote delivery are unpaid. No general H/I theorem,
full original construction, inherited review or historical priority
is claimed.
