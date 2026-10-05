# The exact critical radius of the q18 aggregate box relaxation

Actual **six-downset-3 / researcher**, 2026-10-05. Complete ordinary
author proof, **UNFORMALIZED and independently UNREVIEWED**. This is
one component of the credited self-contained combined source. NEW
reader delivery observations are in [VALIDATION.json](VALIDATION.json);
source integrity, computational reproduction, mathematical proof and
actual graph commitment are separate. No original-candidate PSD factor
or peer executable is imported.

## Fixed original domain and published premises

Use the precise N278/s58 q18 carrier, comparison and rational witness in
the [published NS-fiber proof](https://github.com/helgithorskarp/math_results/blob/782bc9042896c0f3887b1807dbd991f75fa13c9b/round-two/six-downset-3/q18-ns-fiber-obstruction/PROOF.md).
The ground set is {a,b,c} union Z union W with nine points in each pool.
The downset consists of all sets of size at most two and triples with
at least two core points, except bcZ. The actual empty vertex and loop
are retained. S is the unique maximum proper star S(a), with 58
vertices. B consists of the 36 ZZ pairs,36 WW pairs and nine bcW
triples. No other count or carrier is considered.

For EVERY real tau in [0,1/256], F_tau contains ALL original real
symmetric, disjoint-supported stochastic matrices M such that
L=220M+58I is positive semidefinite and M_AB>=tau/220 at every allowed
position, including the empty loop. Competitors need not be invariant,
rational or have a prescribed rank. Set C=L_proper-J277. The original
star-face forcing gives C positive semidefinite, Ch=0 and
C_SS=58I-J58. In particular for u=1_B,

    v(M)=C_SB 1_B,       sum_{s in S} v_s(M)=0.

The sharp minimum repair cost is P0+41tau, P0=476335/32768, by the
same-carrier LEMMA10296 and its complete REVIEW10312. Here P sums
positive C-C_old changes on unordered disjoint NN edges, with the
original comparison of LEMMA10276. Set Delta=P-P0-41tau. The published
all-real Schur/dual inequality for u=1_B, whose maximum disjoint weight
product is one, is

    Delta(M) >= ( ||v(M)||^2/58 - cap )_+/2,
    cap=1_B^T C_old,BB 1_B=4998177/1024.                (1)

At every sharp optimizer, (1) implies ||v(M)||^2<=58cap. The same
fixed rational M_dagger is feasible for every stated tau, by the
published witness theorem. Its feasibility is a premise here and is
not replayed. Its graph broadcast remains accepted pending commitment;
the verified public source is the mathematical citation.

Write v^dagger=v(M_dagger), and measure ORIGINAL M-entry displacement

    d(M)=max_{s in S,A in B}|M_sA-M_dagger,sA|.

The new [radius.py](radius.py) pins the entire published CANDIDATE.json
and COMPARISON.json as defining DATA, regenerates all proper masks and
143 canonical free keys, then constructs the needed original NS entries
and all 81-by-81 comparison positions. All 58 integer coordinates of
v^dagger and the allowed bad-neighbor counts are in
[EXPECTED.json](EXPECTED.json). The decoder is an openly credited adaptation
of the author's published original-entry recipe. It is not independent
review or a transported spectral factor.

## Exact original support and signed partition

Let n_s count the bad vertices disjoint from s, and let k_s=220n_s.
There are 3906 allowed positions on S times B; all other positions in
that block are fixed support zeros. The exact degree census is

    n_s=81 on {a},
    n_s=72 on {a,b},{a,c},{a,b,c} and the nine aW pairs,
    n_s=73 on the nine aZ pairs,
    n_s=64 on the 36 abZ,acZ,abW,acW triples.

For example an aZ pair excludes eight ZZ pairs but is disjoint from
all WW and bcW, giving 28+36+9=73. A core/pool triple meets every bcW
and excludes eight pairs in its own pool, giving 28+36=64. This pays
all 58 actual support counts, including the singleton anchor.

The witness vector has precisely 20 positive coordinates, on
{a},{a,b,c},the nine aZ and nine aW pairs. Its remaining 38 coordinates
are negative and none is zero. Denote these fixed index sets by P and N.
The exact signed-coordinate sums and slope are

    V=sum_{s in P} v^dagger_s=2912214312567/1073741824,
    K=sum_{s in P} k_s=320760.

For every original feasible M with d(M)<=e,

    |v_s(M)-v^dagger_s|<=k_s e                    for all58 s.       (2)

Indeed C and M differences on this off-diagonal block differ by a
factor220. Only the n_s allowed entries can change, and each has
absolute M difference at most e. No permutation invariance of M is
used. Formula(2) is necessary; it is not assumed sufficient to realize
a star/nonstar matrix with original support and column equations.

## A quadratic necessary energy and cost curve

For every real 0<=e<=1/400 set l_s(e)=v^dagger_s-k_s e for s in P.
All 20 lower bounds remain strictly positive on this entire interval;
the exact check at its right endpoint proves this since each is affine
and decreasing. Hence (2) gives v_s(M)>=l_s(e)>0 on P. Since sum(v)=0,
Cauchy's inequality on the other 38 coordinates gives

    sum_{s in N} v_s(M)^2 >= (sum_{s in P} v_s(M))^2/38.

Both the positive-coordinate squares and the square of their sum
increase when a positive coordinate increases. Consequently

    ||v(M)||^2 >= E(e),
    E(e)=sum_{s in P} l_s(e)^2+(V-Ke)^2/38.             (3)

The fresh exact coefficients, in increasing degree, are

    E(e) = 98415505470453425115925635/175244068700240740352
           -338677139309365395/2550136832 *e
           +149253984000/19 *e^2.

Combining (1) and (3) proves, for EVERY real tau in [0,1/256], EVERY
real e in [0,1/400], and EVERY individual-real M in F_tau with d(M)<=e,

    Delta(M) >= max(0,Gamma(e)),
    Gamma(e)=(E(e)-58cap)/116
      =48803932553744574092840067/20328311969227925880832
       -338677139309365395/295815872512 *e
       +37313496000/551 *e^2.                         (4)

The finite checks are not a finite-radius enumeration in place of this
all-real argument. The displayed endpoint signs prove Gamma(0)>0 and
Gamma'(1/400)<0; since the derivative is increasing and affine, Gamma
is strictly decreasing on the whole interval. New exact endpoint
checks give the necessary implications

    d(M)<=1/1280 => Delta(M)>1500,
    d(M)<=1/640  => Delta(M)>750,
    d(M)<=1/500  => Delta(M)>380,
    d(M)<=1/420  => Delta(M)>50,
    d(M)<=1/408  => Delta(M)>1.                       (5)

Equivalently repairs with cost gap at most each displayed constant
must change some original S/B entry by more than the corresponding
radius. The candidate itself lies in all these neighborhoods for every
stated tau. The strict clean constants in (5) come from exact signs of
Gamma, not a claim that (3) or (4) is always strict.

At zero radius, (3) discards variance on N, so (4) is weaker than the
complete fixed-fiber >2493 result of the separate private individual
weight dual. That result is preserved. This new curve uses the original
support and kernel to improve the necessary positive-radius estimates.

## An exact real classification of the aggregate relaxation

For ANY real e>=0 define the following 58-dimensional relaxation:

    |q_s-v^dagger_s|<=k_s e for every s,
    sum_s q_s=0,
    ||q||^2<=58cap.                                  (6)

The constraints are consequences of an optimizer at distance at most
e, by (1)-(2), but do not impose every original NS column, stochastic
row, entry floor or full PSD constraint of such an optimizer.

Let c0,c1,c2 be the exact primitive integer coefficients

    c0 = 5422659172638286010315563,
    c1 = -2585968421753885152069550080,
    c2 = 152958335823863346530091008000.

Their polynomial is a positive multiple of Gamma. Define the smaller
root

    r_star=(-c1-sqrt(c1^2-4c0c2))/(2c2).              (7)

The discriminant is strictly positive and not a square, as verified
with exact integers. Gamma is strictly decreasing on [0,1/400], and
the fresh rational sign checks show

    Gamma(1/408)>1,        Gamma(1/407)<0,
    1/600 <1/408 <r_star<1/407 <1/400.               (8)

These facts identify (7) uniquely in this real interval. The interval
and coefficient arithmetic are exact; floating roots are not a premise.

To prove existence at the threshold, for real e in [1/600,1/400] put

    q_s(e)=l_s(e)          if s in P,
           -(V-Ke)/38     if s in N.               (9)

It has zero sum and squared norm exactly E(e). All 58 original box
coordinates satisfy their lower/upper constraints at BOTH endpoints
1/600 and 1/400, freshly checked in all 116 positions. Each constraint
in e is affine, so those checks prove every constraint for EVERY real
e between the endpoints. This is an ordinary affine-interval bridge.
For the positive coordinates the lower constraint is attained; their
upper constraint is automatic. The negative coordinates are all equal.
Thus (9) is the unique box/zero-sum minimum-energy vector on this
entire window: (3) is its lower bound, and (9) attains every inequality
used in that lower bound. Uniqueness also follows from strict convexity
of the Euclidean squared norm on the convex feasible set.

In particular q(r_star) obeys (6), because E(r_star)=58cap. For
0<=e<r_star the quadratic (4) is positive; its decreasing sign on the
whole interval and (3) exclude (6). For e>=r_star the SAME vector
q(r_star) remains in every widened box and still obeys the zero sum
and energy constraints. We have proved the complete exact classification

    relaxation(6) is feasible IFF e>=r_star, for ALL real e>=0.    (10)

This is the exact critical radius of (6). It is not the distance to
the original optimizer set, an original NS-image feasibility criterion
or an original feasible matrix construction.

Every original sharp optimizer must therefore satisfy

    d(M)>=r_star>1/408.                              (11)

The lower bound remains valid for the entire real tau interval. No
strict inequality d>r_star is asserted; an original construction at
that radius remains open. No best original displacement bound,
generic H/I result, larger entry-floor interval or priority claim is
made. Standard Cauchy, convexity, Schur and quadratic-root methods are
prior mathematics; this result is a precise deduction for the single
published exceptional q18 witness.
