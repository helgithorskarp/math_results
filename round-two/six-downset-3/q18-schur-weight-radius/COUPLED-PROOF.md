# A fixed-column refinement of the exact q18 aggregate radius

Actual **six-downset-3 / researcher**, 2026-10-05. Complete ordinary
author proof, **UNFORMALIZED and independently UNREVIEWED**. This is
one component of the credited self-contained combined source. NEW
reader delivery observations are in [VALIDATION.json](VALIDATION.json);
source integrity, computational reproduction, mathematical proof and
actual graph commitment are separate. No original-candidate PSD factor
or peer executable is imported.

## Domain, units and credited premises

Use exactly the N278/s58 carrier, fixed comparison and rational witness
of the [published NS-fiber proof](https://github.com/helgithorskarp/math_results/blob/782bc9042896c0f3887b1807dbd991f75fa13c9b/round-two/six-downset-3/q18-ns-fiber-obstruction/PROOF.md).
The ground set is {a,b,c} union Z union W, with nine points in each pool.
The downset contains all sets of size at most two and triples with at
least two core points, except bcZ. The actual empty vertex and loop
remain present. The unique maximum proper star S=S(a) has 58 vertices;
the bad family B consists of 36 ZZ pairs, 36 WW pairs and nine bcW
triples. No different carrier or comparison is considered.

For every real tau in [0,1/256], F_tau consists of ALL original real
symmetric disjoint-supported stochastic M with

    L=220M+58I positive semidefinite,
    M_AB >= tau/220 at every allowed position, including the empty loop.

There is no rational, invariant or rank restriction on competitors.
Write C=L_proper-J277. The original star forcing and kernel give

    C positive semidefinite,     Ch=0,     C_SS=58I-J58,
    h=1_S,     v(M)=C_SB 1_B,     sum_S v_s(M)=0.       (1)

On an intersecting proper pair, support forces M_AB=0 and C_AB=-1.
On every S/B off-diagonal pair, differences in C equal 220 times
differences in the ORIGINAL M entries.

The sharp minimum repair cost is P0+41tau, P0=476335/32768, by the
same-carrier sharp theorem LEMMA10296 and complete parent REVIEW10312.
P is the sum of positive C-C_old changes on unordered disjoint NN
edges, using the fixed original comparison of LEMMA10276. Put

    Delta(M)=P(M)-P0-41tau,
    cap=1_B^T C_old,BB 1_B=4998177/1024.

The published all-real Schur/dual estimate for u=1_B is

    Delta(M) >= ( ||v(M)||^2/58 - cap )_+/2.           (2)

In particular every sharp optimizer satisfies ||v(M)||^2<=58cap.
The same fixed rational M_dagger is feasible for every stated tau;
its paid feasibility proof is a premise, not replayed here. Its source
is public and verified, while its original graph broadcast remains
accepted pending actual commitment. No review of that witness or of
this successor is inherited from the reviewed sharp parent theorem.

Define v^dagger=v(M_dagger), and the original-entry radius

    d(M)=max_{s in S,A in B} |M_sA-M_dagger,sA|.

The exact canonical decoder and full original row-count derivation are
in [radius.py](radius.py), [EXPECTED.json](EXPECTED.json) and
[BASIC-RADIUS-PROOF.md](BASIC-RADIUS-PROOF.md). The decoder is an openly credited adaptation of
the published original-entry recipe. It pins the whole CANDIDATE.json
and COMPARISON.json as defining DATA, reconstructs the 277 proper masks
and 143 free keys, all 58 original aggregate coordinates and all 81-by-81
comparison positions. It executes no parent program or spectral factor.

Let n_s be the number of B vertices disjoint from s and k_s=220n_s.
The exact counts are 81 on {a}; 72 on ab,ac,abc and the nine aW pairs;
73 on the nine aZ pairs; and 64 on the 36 abZ,acZ,abW,acW triples.
For d(M)<=e, the necessary original row boxes are

    |v_s(M)-v^dagger_s| <= k_s e for EVERY s in S.      (3)

All 58 v^dagger coordinates are nonzero. Its positive set P has 20
vertices {a},abc,9aZ,9aW. Its negative set N has 38 vertices ab,ac,
9abZ,9acZ,9abW,9acW. These are fixed sets determined by the witness;
no sign assumption on v(M) is made. The exact positive sum is

    V=sum_{s in P}v^dagger_s=2912214312567/1073741824.  (4)

## The nine original bcW columns fix a group mass

Every vertex of N contains b or c. Therefore every pair in
N times {bcW} intersects: ALL 38*9=342 such original C entries are -1
for EVERY feasible M. Equation (1), in the column A=bcw, gives

    sum_{s in P} C_s,bcw = -sum_{s in N} C_s,bcw = 38 (5)

for each of the nine individual w in W. Hence the total bcW contribution
to sum_P v_s is always 342. This is an exact original column identity;
an aggregate-coordinate box alone does not impose it.

Only the P/ZZ and P/WW entries can change that positive group sum.
There are exactly 1296 allowed original positions: {a} and abc each
have 72 disjoint pure-pair neighbors; each of the 18 aZ/aW pairs has
64. Thus 2*72+18*64=1296. For comparison each bcW column has 18 allowed
P positions: {a}, the nine aZ and the eight aW pairs with other W point.
Those nine*18=162 apparently movable positions have total change zero
in the group sum by (5).

For EVERY real e>=0 and EVERY M in F_tau with d(M)<=e,

    T(M):=sum_{s in P}v_s(M) >= V-Ke,
    K=220*1296=285120.                               (6)

Indeed the bcW part has zero total change from the witness. Each of the
1296 remaining allowed C positions changes by at most 220e in absolute
value; the intersecting entries do not change. This proves (6) without
permutation averaging or a sign condition on an individual coordinate.
The [new coupled checker](coupled_radius.py) pays all 342 fixed N/bcW
positions, all 1296 allowed P/pure-pair positions, each of the nine
allowed-column counts and the complete support partition independently
of the basic row-box scalar check.

## A stronger necessary cost curve on a whole real interval

For a zero-sum real vector v with positive-set sum T, Cauchy's inequality
on each of the two fixed groups gives

    ||v||^2 >= T^2/20 + T^2/38 = 58T^2/760.           (7)

The term "positive-set" refers to the fixed witness set P only.
Equation (7) holds without assuming the signs of the new vector.
The exact check V-K/320>0, together with K>0, proves V-Ke>0 for EVERY
real e in [0,1/320]. Equations (6)-(7) therefore imply

    ||v(M)||^2 >= 58(V-Ke)^2/760.                    (8)

Combining (2) and (8) proves the quantified necessary bound

    Delta(M) >= max(0,Psi(e)),
    Psi(e)=((V-285120e)^2/760-cap)/2,                 (9)

for EVERY real tau in [0,1/256], EVERY real e in [0,1/320], and EVERY
individual-real M in F_tau with d(M)<=e. The exact coefficients are

    Psi(e) = 4204132468121045492829009/1752440687002407403520
             -2594782952497197/2550136832 *e
             +1016167680/19 *e^2.

It is strictly decreasing on the entire displayed interval, since
Psi'(e)=-K(V-Ke)/760<0 there. Fresh exact rational checks imply

    d(M)<=1/1280 => Delta(M)>1600,
    d(M)<=1/640  => Delta(M)>900,
    d(M)<=1/500  => Delta(M)>450,
    d(M)<=1/400  => Delta(M)>180,
    d(M)<=1/363  => Delta(M)>0.                      (10)

These clean strict constants follow from the exact Psi values in
[EXPECTED.json](EXPECTED.json). The two-group Cauchy step
discards witness within-group variance at zero radius, so it does not
replace the separate complete fixed-fiber >2493 theorem. The basic
Gamma curve remains valid on its original interval; where both apply,
their maximum is also a necessary bound.

## Exact minimum energy in the coupled original-coordinate boxes

For ANY real e>=0 define the relaxation R_e by the constraints

    |q_s-v^dagger_s|<=k_s e for EVERY s in S,
    sum_S q_s=0,
    sum_{s in P}q_s >= V-Ke,
    ||q||^2 <= 58cap.                               (11)

Every sharp original optimizer at distance at most e maps into R_e.
The new group-mass inequality is a consequence of original NS-column
equations, but (11) still does not impose all individual NS columns,
entry floors, stochastic rows or original PSD conditions.

For real e in [1/500,1/320], put

    q_s(e)=(V-Ke)/20  for s in P,
           -(V-Ke)/38 for s in N.                   (12)

This vector has zero sum, positive-set sum V-Ke and norm squared
58(V-Ke)^2/760. Every one of its 58 original lower/upper box conditions
holds at BOTH endpoints, checked exactly in all 116 positions. Each
condition is affine in e, so those endpoints prove every original
condition for EVERY real e in the entire window. This ordinary
affine-interval bridge is explicit; finite sampling is not substituted
for real coverage.

Consequently (12) is the minimum-energy vector in the boxes with zero
sum and the group-mass constraint, on this entire real window. The
lower bound (7)-(8) is attained. Since V-Ke>0, equality requires T=V-Ke
and constant coordinates in each group, proving uniqueness directly;
strict convexity of the squared norm gives the same conclusion.

## The exact threshold and complete all-radius classification

Define

    r_c=(V-sqrt(760cap))/285120,
    760cap=474826815/128.                            (13)

The fresh exact signs are Psi(1/363)>0 and Psi(1/362)<0. Both endpoints
lie strictly inside [1/500,1/320], where V-Ke is positive and Psi is
strictly decreasing. Equivalently their positive squared group sums
straddle 760cap. Thus (13) is exactly the smaller root and

    1/500 < 1/363 < r_c < 1/362 < 1/320.             (14)

For a completely integer root description, a positive multiple of
Psi has primitive coefficients in increasing degree

    c0=467125829791227276981001,
    c1=-198124585265667247051898880,
    c2=10413880627186213366372761600.

The exact integer check gives c1^2-4c0c2>0 and nonsquare, so r_c is
irrational and also equals (-c1-sqrt(c1^2-4c0c2))/(2c2). No floating
root approximation is needed to identify it.

If 0<=e<r_c, then e<1/320 and the lower bound (8) is strictly greater
than 58cap. Hence R_e is empty. At e=r_c, vector (12) is in all original
boxes, has zero sum, attains the group constraint and has norm squared
exactly 58cap, so it belongs to R_{r_c}. For EVERY e>=r_c the SAME vector
q(r_c) remains in the widened boxes; its positive-set sum V-Kr_c is at
least V-Ke, and its zero sum and norm remain unchanged. This proves

    R_e is feasible IFF e>=r_c, for ALL real e>=0.    (15)

Thus r_c is the exact critical radius of the entire coupled relaxation
(11), not merely of a one-dimensional surrogate. Its primal explicitly
includes all 58 original row boxes.

Every original sharp optimizer therefore satisfies

    d(M)>=r_c>1/363, for EVERY real tau in [0,1/256]. (16)

The earlier exact basic box threshold between 1/408 and 1/407 is a
different, weaker relaxation and remains correct. There is no claimed
original NS matrix at r_c, sharp distance to the original optimizer
set, complete original-fiber criterion, general H/I theorem or signed
H/I counterexample. All ordinary completeness, Cauchy, interval and
root arguments are unformalized and independently unreviewed. Standard
Schur, dual, Cauchy, convexity and algebraic-root mechanisms are prior
mathematics; this is a precise new deduction for the one credited q18
exceptional witness, with no priority assertion.
