# Weighted separation from the original q18 sharp optimizer set

Actual **six-downset-3 / researcher**, 2026-10-05. PRIVATE ordinary
author-complete proof, **unformalized and independently unreviewed**.
Finite rational checks and the all-real argument below are separate
evidence. New source-before-import, isolated cold, remote reader and
publication gates remain unpaid. There is no new source commit or
graph packet. The earlier graph-delivery dependencies remain pending.

For the fixed original witness and cost defined below, we prove that
EVERY sharp original optimizer, for EVERY real tau in[0,1/256], has
original S/B entry distance at least rho, where

    3180020/10^9 < rho < 3180021/10^9,
    1/315 < rho < 1/314.

We also give a necessary cost curve for EVERY individual-real competitor
within each radius e in[0,1/300]. This is a bound for one specified
original carrier and witness, not an optimal-distance classification.

## Original domain and explicit ordinary premises

The ground is {a,b,c} union Z union W, |Z|=|W|=9. The downset consists
of all sets of size at most two and the triples with at least two core
points except bcZ. The actual empty vertex and its loop are retained.
Its N=278 vertices have unique largest proper star S=S(a), of size58.
There are220 nonstar vertices. The bad family B consists of36 ZZ pairs,
36 WW pairs and nine bcW triples. All sets, entries and distances below
refer to these original vertices, without a quotient-matrix convention.

For each real tau in[0,1/256], F_tau consists of ALL real symmetric,
disjoint-supported stochastic original matrices M satisfying

    220M+58I is positive semidefinite,
    M_AB>=tau/220 on EVERY allowed entry, including the empty loop.

No symmetry, rationality or rank assumption is placed on competitors.
For the277 proper vertices define C=(220M+58I)_proper-J277. The original
star-forcing theorem gives C PSD, C1_S=0, and C_SS=58I-J58. Intersecting
distinct proper entries equal-1 and diagonal entries equal57.
Put A=C_SB. Thus every original column of A sums to zero.

Use the fixed rational witness M_dagger and comparison C_old of the
explicitly credited [public q18 witness source](https://github.com/helgithorskarp/math_results/blob/782bc9042896c0f3887b1807dbd991f75fa13c9b/round-two/six-downset-3/q18-ns-fiber-obstruction/PROOF.md)
and [combined source87c1](https://github.com/helgithorskarp/math_results/blob/87c1eba73573ab49ed9131f6496c6703ce03fd1e/round-two/six-downset-3/q18-schur-weight-radius/COUPLED-PROOF.md).
Their original feasibility, star-forcing and sharp-cost theorems are
ordinary premises. Sharp theorem10296 and comparison10276 are committed
parents; parent review10312 concerns the sharp theorem only and confers
no verdict on this child. Define

    d(M)=max_{s in S,B_i in B}|M_s,B_i-M_dagger,s,B_i|,
    Delta(M)=P(M)-476335/32768-41tau.

Here P is the published unordered disjoint NN positive-increment cost
relative to C_old. Its sharp minimum is476335/32768+41tau, attained
throughout this interval. A change in an original S/B C entry is220
times the corresponding original M-entry change.

The full original sharp dual identity, equation(3) in the public witness
proof, has nonnegative terms and in particular gives

    Delta>=0,
    sum_{E2}(C_e-C_old,e)_+<=Delta,                 (1)

where E2 comprises ALL2628 unordered disjoint edges inside B. This
all-real sharp dual statement is an explicit premise, not inferred
from this child's finite output or from a factor certificate.

The original Schur complement of C on S union B gives

    C_BB-A^T A/58 is positive semidefinite.         (2)

The singular star direction is legitimate here: C_SS acts as58I on
1_S perpendicular, and every original A column sums to zero. Completing
the square on that perpendicular subspace proves(2).

## The weighted Schur/dual inequality on the original edges

For any nonnegative original81-vector u, set

    alpha_u=max_{e={i,j} in E2}u_i u_j.

Intersecting and diagonal B/B entries are fixed. Symmetry, nonnegative
weights and(1) therefore imply

    u^T C_BB u <= u^T C_old,BB u
                  +2 alpha_u sum_{E2}(C_e-C_old,e)_+
                <=u^T C_old,BB u+2 alpha_u Delta.  (3)

If alpha_u>0, combining(2),(3) proves

    Delta >= (||Au||^2/58-u^T C_old,BB u)_+/(2 alpha_u).  (4)

The factor2 uses unordered E2 edges and both symmetric entries in the
quadratic form. It does not use a PSD hypothesis on C_old itself.

Let t be the original indicator of the nine bcW triples and choose

    u(lambda)=1_B+lambda t, for lambda>=0.

Among ALL original2628 disjoint bad edges,2052 join two pure pairs and
576 join a pure pair to a triple. No two bcW triples are disjoint.
Their weight products are respectively1 and1+lambda, so

    alpha_u=1+lambda.                              (5)

The fresh defining-DATA decoder reconstructs all6561 comparison B/B
entries and checks EACH of the nine original triple row sums

    (C_old,BB1_B)_bcw=R=186731/4096.

The triple block has diagonal57 and every off-diagonal entry-1, hence
t^T C_old,BB t=9*57-9*8=441. Consequently

    cap(lambda)=u^T C_old,BBu
               =4998177/1024+18R lambda+441lambda^2.  (6)

The executable checks both coefficients on the whole original block;
the absence of triple/triple support is not assumed from an orbit name.

## Fixed original column equations give weighted group lower bounds

Let v_dagger=C_dagger,SB1_B. Its fixed positive group consists of
a,abc,nine aZ,nine aW. Write J for those19 vertices other than abc;
write N for the remaining38 star vertices. The constants are

    alpha0=v_dagger,abc=148830682779/1073741824,
    V=sum_{s in J union{abc}}v_dagger,s=2912214312567/1073741824,
    a(e)=alpha0-15840e,
    b(e)=V-alpha0-269280e,
    T(e)=a(e)+b(e).

EVERY original star vertex in N union{abc} intersects EVERY bcW triple.
All351 corresponding entries of A are-1. Since each of the nine whole
columns sums to zero, EACH triple column has sum39 on J. Therefore

    (At)_abc=-9,
    (At)_s=-9 for EVERY s in N,
    sum_J At=351,
    sum_S At=0.                                    (7)

For d(M)<=e, the72 movable abc/pure positions and1224 movable J/pure
positions give v_abc>=a(e) and sum_J v>=b(e), where v=A1_B. The triples
in these two group sums are fixed by(7); only the pure entries move.
These bounds require no sign assumption on the unknown coordinates v.
For q=Au(lambda)=v+lambda At, put x=q_abc,y=sum_J q. Then

    x>=a(e)-9lambda,
    y>=b(e)+351lambda,
    sum_N q=-(x+y).                                (8)

Whenever the two displayed lower bounds are positive, group Cauchy and
strict monotonicity of x^2+y^2/19+(x+y)^2/38 in positive x,y imply

    ||q||^2>=E_lambda(e)
       =(a-9lambda)^2+(b+351lambda)^2/19
                           +(T+342lambda)^2/38.   (9)

The individual J and N coordinates need not be equal. Cauchy bounds
their squared norms by their actual group masses. Positivity licences
the lower-bound substitution in(9); it is checked for the chosen
lambda on the whole interval below, not inferred from a sample.

## Exact concave optimization of the unnormalized violation

Let cap=4998177/1024 and Gamma=(a^2+b^2/19+T^2/38)/116-cap/2, the
proved unweighted subset curve in[PROOF.md](PROOF.md). Expansion of
(6),(9) gives the exact identity in BOTH real parameters

    F_lambda(e):=E_lambda(e)/58-cap(lambda)
       =2Gamma(e)+18lambda*(b(e)/19-R)-(5220/19)lambda^2.  (10)

Thus the concave unnormalized quadratic in lambda has its vertex at

    lambda(e)=(b(e)-19R)/580
              =458331453943/155692564480-(13464/29)e.  (11)

All three affine expressions lambda(e), a(e)-9lambda(e), and
b(e)+351lambda(e) are positive at BOTH e=0 and e=1/300. The exact
endpoint values appear in WEIGHTED.json. Affinity then proves strict
positivity for EVERY real e in this closed interval. The selected
lambda is therefore nonnegative and valid for(5),(8),(9) throughout.
It maximizes the formal unnormalized quadratic(10); since it is valid,
it also attains that maximum within this licensed weight family.
We do not assert optimization of the normalized cost bound in(4) or
of arbitrary81-variable positive-radius weight choices.

Substitution gives

    F(e)=2Gamma(e)+9*(b(e)-19R)^2/11020
        =91211746346430036217583571/12705194980767453675520
          -(25756116822218871/9244246016)e
          +(91593089280/551)e^2.                   (12)

Combining(4),(5),(9)-(12) proves, for EVERY real tau in[0,1/256], EVERY
real e in[0,1/300], and EVERY original individual-real M in F_tau with
d(M)<=e,

    Delta(M)>=max(0,F(e))/(2*(1+lambda(e))).        (13)

For example at e=1/315 the right-hand side is the strictly positive

    833375057001732878132933/439333551995126059892736.  (14)

This is a necessary gap in the specified cost P, not a floating-point
eigenvalue test or a claim of infeasibility of F_tau itself.

## The exact new root and an explicit uniform separation

The quadratic coefficient of F is positive, and its derivative at
1/300 is negative. Its affine derivative is therefore negative on
the entire interval[0,1/300]. The exact values satisfy

    F(1/315)=833375057001732878132933/88936364865372175728640 >0,
    F(1/314)=-2540039900855392540408009941/313170351080936965647892480 <0.

Continuity and strict decrease give one root rho between these two
rational radii. A positive multiple of F has primitive coefficients
in increasing degree

    c0=10134638482936670690842619,
    c1=-3933215268387039896854855680,
    c2=234665871787304147493480038400.

Its positive nonsquare discriminant is checked with exact integers.
The derivative is negative at the identified root, so it is the smaller
root, exactly

    rho=(-c1-sqrt(c1^2-4c0c2))/(2c2),
    3180020/10^9 < rho <3180021/10^9.               (15)

If a sharp M had d<rho, taking e=d in(13) would give Delta>0, a
contradiction. Therefore every sharp original optimizer has d>=rho.
This conclusion is unconditional on its distance being at most1/300:
any putative violation d<rho automatically falls in the licensed
interval. In particular d>1/315 for EVERY permitted tau and optimizer.
No original sharp matrix is constructed at rho, and equality at rho
or exact best original distance is not asserted.

The earlier full original S/B transport relaxation has exact threshold
r_* with r_*<2757399/10^9. It remains a weaker relaxation whose original
entry/floor/column/aggregate-energy constraints are fully solved;
the weighted bad-block test adds information beyond that relaxation.
The earlier universal critical-completion exclusion and compactness
gap in[CRITICAL-EXTENSION.md](CRITICAL-EXTENSION.md) remain correct.
The present argument supplies an EXPLICIT gap valid uniformly:

    eta0=1/315-2757399/10^9=26283863/63000000000>0,
    d(M)>r_*+eta0 for EVERY original sharp M and permitted tau.  (16)

Indeed r_*+eta0<1/315<rho<=d(M). No compactness or continuity of the
optimizer selector is needed for this explicit numerical separation.

## Finite checks, reproducibility and scope

weighted_radius.py reads only the whole-pinned defining CANDIDATE.json
and COMPARISON.json from the published87c1 directory. It openly shares
the NEW local census.py original decoder and this author's canonical
143-key comparison convention. It checks ALL81 weights, ALL2628
original disjoint bad edges, ALL6561 comparison entries, ALL351 fixed
positions, all nine separate J column sums, support counts72/1224,
entire bivariate and univariate coefficient identities, whole-window
endpoint licences, exact derivative signs and integer root cages.
There is no float, solver, PSD-factor replay, imported ancestor program,
imported EXPECTED record or peer mathematical input.

Use POSIX CPython3.11 or newer, standard library only. From this directory,
with defining sibling data present, generate outputs outside the source:

```sh
python3 -B weighted_radius.py > /tmp/q18-weighted-normal.json
python3 -B -O weighted_radius.py > /tmp/q18-weighted-O.json
python3 -B weighted_radius.py --check /tmp/q18-weighted-normal.json
python3 -B weighted_adverse.py --out /absolute/workspace/scratch/q18-weighted-check
```

The optional checker compares the ENTIRE freshly regenerated record,
with six named mathematical field gates first. Matching normal/O
outputs and designated semantic damages are author verification,
not independent review or formalization. This private source has no
new source-binding, isolated cold or remote delivery certificate.
Those gates remain a separate publication task; no graph submission
is authorized by their absence. Earlier published source and accepted
but actually uncommitted graph packets are retained without retries.

The primary target remains [EFF Section4 Conjecture H](https://arxiv.org/html/2609.28404v1#S4),
live reverified2026-10-05. Ordinary Chvatal is already proved; signed
H and inertia I are separate conjectures. Our explicit nonnegative
F_tau restriction, fixed carrier/comparison/witness and necessary
radius bound do not settle either conjecture. Cauchy, Schur, quadratic
optimization and integer-root isolation are classical mechanisms.
All real-parameter and original-dual bridges here are ordinary,
unformalized and independently unreviewed; no historical priority
or global optimality is claimed.
