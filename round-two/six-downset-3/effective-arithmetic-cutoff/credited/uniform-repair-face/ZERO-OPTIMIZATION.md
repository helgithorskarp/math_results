# Variable-count optimized zero-endpoint criterion

Actual author **six-downset-3**, role **researcher**, 2026-10-03.
Ordinary author proof with exact coefficient certificates. Unformalized and
independently unreviewed. The original all-space, actual-empty, spectral and
rank premises are explicitly credited below. This document proves the zero
optimization and positive recovery used by the complete original-face theorem
in [PROOF.md](PROOF.md).

The sole problem source remains
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
whose [version history](https://arxiv.org/abs/2609.28404) was checked live on
2026-10-03: September 23 v1 remains the only version. Classical Chvatal is
proved there; spectral H/I remain conjectural. No general H/I result or
historical priority is asserted here.

The input is the triangle-majority downset on core {a,b,c} and q outside
points, retaining the actual empty set, all sets of size at most two,
and all triples with at least two core points except bcx for x in a
k-subset Z. For the results below, **integers k>=7 and q>=3k**, every Z.
Put N=(q^2+13q+16)/2-k and s=3q+4. On original nonempty coordinates the
prescribed repair face is

```
C=C0+kappa Delta+t_b R_b+t_c R_c+sigma B,
U=N I-J-C.
```

Its original literal table, physical orbit metric and independent trades
are the defining inputs of published
[9826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/core-edge-six-cutoff/PROOF.md).
The all-count target separation, zero coefficients, positive untouched
cap and automatic odd-cap bounds are credited to
[9980](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-zero-cap-cutoff/PROOF.md),
especially its
[lower reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-zero-cap-cutoff/LOWER-REDUCTION.md)
and [coefficient/recovery proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-zero-cap-cutoff/COEFFICIENT-RECOVERY.md).
The positive original-space spectral premises originate in 8757/9145/9195;
9980 and its ancestors credit them explicitly. This work uses those ordinary
premises; the finite controls do not establish them independently.

The k=7 finite baseline is published
[10032](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/core-edge-seven-cutoff/PROOF.md).
Its q26 exclusion and q27 positive sign are exactly reproduced before
the new all-count interpretation. Baseline reproduction is validation.

## 1. Exact scalar criterion for the strict zero endpoint

Let a=a0(q,k)>0 be the zero lower even coefficient, and let

```
b=2(3q+4)(3q^2+3q-2)/(6q^2+5q-2)>0.
```

Credit 9980 for a<b/2 and the exact separation
a=q k nu0 tau0/((q-k)tau0+k nu0), including the complete positive
zero coefficient formulas. Let M0 be the unrepaired zero cap Schur
form in the physical parity basis (a,b+c,ab+ac). In the reordered
basis (a,ab+ac,b+c), write

```
M0 = [[H,u],[u^T,d]],      w=(-1,1)^T.
```

**New all-count anchor and vertex lemma.** H is positive definite,
and the rational quantities

```
K=H+a w w^T,
y=u+a w,
h=-K^-1 y,
ell=w^T h,
t*=a(1+ell)/2
```

satisfy 0<t*<2ab/(a+b) throughout the stated integer domain.
The whole coefficient proof, rather than its original-member controls,
is described in Section 4.

Define the rational scalar

```
R(q,k)=d+a-y^T K^-1 y.                              (1)
```

**Theorem.** For every integer k>=7,q>=3k and every k-subset Z,
there exist real symmetric trades t_b=t_c=t and sigma for which
the zero lower form has precisely its two forced original kernels
and the full original zero cap is positive definite if and only if
R(q,k)>0. If R>0, rational parameters can be chosen and recovered
to a positive-kappa capped H with both greatest ordinary ranks N-1,
an actual empty/loop and a simple unit eigenvalue. At zero itself
the extra lower kernel is retained; it is not a greatest-rank witness.

Here is the complete reduction. The strict lower condition at zero is

```
left(t)=2t^2/a-2t < sigma < right(t)=2t-2t^2/b.       (2)
```

The repaired even cap is positive exactly when H>0 and

```
sigma < upper(t)=(d-(u+2tw)^T H^-1(u+2tw))/2.        (3)
```

The original untouched and odd cap blocks stay positive for every
weak-lower-feasible repair by the credited all-domain 9980 bounds;
no other cone is omitted. Hence strict compatibility is equivalent
to left(t)<min(right(t),upper(t)) at an interior t from (2).

The gap Phi(t)=upper(t)-left(t) is a strictly concave quadratic:

```
Phi(t)=(d-u^T H^-1u)/2
       +(2-2w^T H^-1u)t
       -(2w^T H^-1w+2/a)t^2.
```

Completing this square, or applying the rank-one inverse identity,
gives its unique vertex t* above and max_t Phi(t)=R/2. The new
vertex lemma puts this unrestricted maximum inside the strict
lower interval. Necessity and sufficiency therefore follow without
an unknown search or a further unproved interval hypothesis.
For sufficiency put

```
t=t*,
sigma=left(t)+min(R/2,right(t)-left(t))/2.
```

Every quantity is rational and both strict margins are positive.
The same reasoning rules out zero-endpoint compatibility of unequal
trades: averaging with the b/c transposition preserves both cones,
their fixed kernels and strict cap positivity, and makes the two
trades equal. The theorem is a zero-endpoint decision rule, not a
claim that every positive-kappa feasible point must have R>0.

To recover positive kappa, use the repair's actual margin
m=sigma-left(t)>0 and curvature B0=2t^2/a. The credited complete
original norm and interpolation bounds are

```
||Delta||<=16s,       a(q,k,kappa)>=(1-8kappa)a.
```

Derive a rational full-original zero cap floor epsilon0 using the
untouched weighted floor, automatic odd floor, det(even)/trace(even)^2,
and the full Schur congruence Frobenius bound, as in the credited
recovery proof. Choose a rational positive kappa no larger than

```
min(1/16,m/[32(B0+m)],epsilon0/(32s)).                (4)
```

Then the lower-left loss is less than m/2 and the full original cap
retains floor epsilon0/2. The lower odd block and omitted nonfixed
space are retained through the original 9980 bridge. The star/actual
empty lift gives both ordinary ranks N-1 and unit gap at least
epsilon0/[2(N-s)]. This uses the repair's own margin, not the old
canonical quarter-coefficient margin.

## 2. An original dual at every variable-count pair

Equation (1) has an original-space interpretation which cancels
both independently chosen trades without averaging an arbitrary
competitor. In the cap choose physical plain anchors

```
(a,b,c,ab,ac)=(h_1,1,1,h_2,h_2),
```

and minimize U0 over every other original coordinate. In the lower
form fix the forced a-star coordinate to zero, choose anchors
(b,c,ab,ac)=(1,1,ell,ell), and minimize C0 after fixing one
outside-singleton gauge. This gives original vectors x_U and x_L.
The lower zero energy is a(1+ell)^2.

For each of R_b and R_c, the lower plane coefficient is -2ell
and the cap plane coefficient is 2(h_2-h_1)=2ell. The B coefficients
are respectively 2 and -2. Thus the two positive-weight original
PSD inequalities have sum

```
x_L^T C x_L+x_U^T U x_U=R+Djoint kappa.             (5)
```

Each independent trade cancels separately. Djoint is obtained by
actual original Delta energies, not by differentiation of a rounded
scalar or by testing a parameter grid.

The lower vector may be changed by a multiple of zeta, which is 1
on outside-only members, -1 on abc and zero elsewhere. Every repair
and C0 kills zeta. Direct disjoint-member counts give

```
zeta^T Delta zeta=q(q+1)/2+3(q+1)/(3q+5)>0.
```

Thus original lower PSD forces kappa>=0. Choosing the gauge shift
-zeta^T Delta x_L/(zeta^T Delta zeta) minimizes the lower Delta
energy without changing the zero constant or any repair coefficient.
If **R<0 and Djoint<=0**, (5) excludes the entire real four-parameter
face, for arbitrary independent t_b,t_c and sigma and without an
upper bound on kappa, a rank condition or strictness assumption.

The uniform strict negative slope needed for the complete real-face criterion
is established separately in [PROOF.md](PROOF.md). Finite controls below are
normalization checks, while that proof uses complete polynomial inequalities.

At q32,k8 the two original planes in the generated zero-controls record have R<0 and
Djoint<0. They give a scoped all-real absence certificate for that
pair, relative to the defining original count/decoder bridge. This
refutes the proposed strengthening which simply subtracts a third
order from the old 9703 cutoff for every k>=7: at k8 that proposal
would include q32. The q27,k7 success cannot be extrapolated across
deletion counts. No complete k8 classification is asserted here.

## 3. Asymptotic boundary and a genuine positive recovery

Put rho=3+sqrt7. The exact homogeneous layers of the rational
function (1), in the positive real embedding of QQ(sqrt7), give

```
R(rho k+beta,k)=sqrt7*(beta+14)*k+O(1).             (6)
```

The remainder is uniform for beta in any fixed compact interval.
This follows directly by expanding the finite exact rational
polynomials: the numerator has total degree64, its leading homogeneous
layer vanishes at rho, the next layer has critical intercept -14,
and the denominator has total degree62 and a strictly positive
leading value there. Both the intercept -14 and leading multiplier
sqrt7 are exact field equalities, not fitted numerical values.

For beta>-14 the strict zero criterion succeeds for large k;
for beta<-14 it fails for large k. The equality beta=-14 needs the
next homogeneous layer and is not decided here. This is the
asymptotic boundary of the zero-endpoint mechanism, not an all-real
positive-kappa nonexistence threshold.

A simple repair has the same leading boundary: t=a/2 and
sigma=-a/2+delta, with delta=1/4. Its even-cap shorted residual is

```
Rhalf=R-a*ell^2*(1+a*w^T H^-1w)-2delta.             (7)
```

This exact rank-one loss identity follows from the inverse formula
for H+a w w^T and is separately checked on original control matrices.
The exact leading coefficients give

```
a/k -> (9+3sqrt7)/2,
H_11/k^2 -> (32+12sqrt7)/5 >0,
det(H)/k^4 -> (508+192sqrt7)/5 >0,
k*ell -> (69-27sqrt7)/4,
k^2*w^T H^-1w -> 12-9sqrt7/2 >0.
```

Therefore the additional loss in (7) is O(1/k), before the constant
2delta. Both (2) and the even cap are strict for the half-coefficient
repair throughout any compact beta interval lying above -14, for
all sufficiently large integer k. The original untouched and odd
cap premises and the explicit recovery (4) complete the original H.

Consequently, **for every real epsilon>0 there is an integer K(epsilon)
such that every integer k>=K(epsilon), every integer
q>=ceil(rho k-14+epsilon), and every k-subset Z admit a rational
greatest-rank capped H in this prescribed face.** The proof has no
explicit K(epsilon) yet. To cover all q, first use uniformity of
(6)--(7) on beta in [-14+min(epsilon,1),-11]. The old 9980 tail has
asymptotic intercept
`(9/sqrt7-25)/2-2 = (9/sqrt7-29)/2`, strictly less than -11.
For large k its ceiling lies below rho k-11. That already-proved
tail covers every larger q; the compact interval covers the gap.
For large k all these q also satisfy q>=3k. This is an ordinary
asymptotic construction theorem relative to the explicit original
spectral and tail premises, not an explicit uniform cutoff or
an optimality theorem for the complete real face.

The concrete half-coefficient recovery at **q100,k20** has
N5638,s304,kappa2^-31, t=a0/2, sigma=-a0/2+1/4.
Its full original lower and cap ranks are **5637**, internal C rank
5636, zero cap floor2^-17, positive cap floor2^-18, and unit gap
at least **1/1398276096**. The generated zero-recovery10020 record contains every
original counted solve, congruence, physical weighted floor and
both complete characteristic/congruence PSD decisions. The whole
original empty, support, nonfixed and greatest-rank completion uses
the credited ordinary bridges; a dense 5638-dimensional replay
is not claimed. This point is below the sufficient q101 bound
of 9980 at k20. No first-discovery claim among all prior artifacts
follows merely from being below that sufficient bound.

## 4. Complete coefficient certificates and scope

input.py binds the entire 44-file source closure of published9980
before importing mathematical helpers, with committed manifest SHA
`b783ede83b894ba80936d6d11ad25a7be2c437602234e23aa95ebc3d4c454cb5`.
The defining source commit is628c20b948551a6cae0af6b54498ed99b24de141.
The original seven-family cap shorting and both scalar fields are
regenerated from that source, without a saved CAS solve as a premise.

Initial exact CAS discovery used SymPy1.14.0 in QQ[q,k], characteristic0,
lexicographic q then k. No CAS or private table is required by this packet.
zero_generator.py regenerates the complete residual and optimizer from
credited9980 source, with exact Jacobi divisions and the explicitly proposed
common factor q(2N)^2. zero_check.py multiplies every division back and checks
all28 original solve equations, all16 short equations, the complete original
determinant degree grid, both scalar fields and all9 cap positions. Each
residual and optimizer coefficient is regenerated with stdlib integers.

The zero cap is P/(4T), T>0 by the credited original untouched/full
target positivity. H_11 has numerator P00. Its determinant has
numerator (P00 P22-P02^2)/T; the positive denominator is16T.
For the two vertex inequalities, use the complete rational
optimizer h=(hx,hz)/Den. Since H>0 and a>0, Den>0. Positivity of
Den+hz-hx proves t*>0. With b=bn/bd, the upper interval condition
is the complete polynomial inequality

```
4 bn ad Den-(an bd+bn ad)(Den+hz-hx)>0,
```

where a=an/ad and all denominators are positive. The five whole
substitutions k=7+x,q=3(7+x)+u have respectively
946,1035,2345,4462,21 nonzero coefficients. All **8809 coefficients
are nonnegative**, with each constant positive. This proves the
entire stated quadrant signs. These are exact polynomial identities
and inequalities, not interpolated signs or a finite-k scan.

Five complete original controls are q21/k7,q26/k7,q27/k7,q32/k8,
q100/k20. Every original cap entry matches the independently
shorted23-coordinate form; each lower coefficient agrees with the
separate original lower shorting. The actual original lower/cap
vectors and every individual repair coefficient are checked.
These controls bind normalization and implementation; they do not
prove the infinite signs, spectral premise or completeness bridge.

The combined validate.py runs these ten zero phases and twelve slope/boundary
phases in fresh isolated normal/-O interpreters. All whole paired records are
compared, and both eight-damage suites reject their altered original duals.
EXPECTED.json pins the entire deterministic mathematical stream; VALIDATION.json
contains the compact author receipt. Bulky regenerated work files are ignored
and are not source inputs. See README.md for the exact command and resource
scope. These checks do not formalize the ordinary original-space bridges.

## Current external feedback and next step

Committed REVIEW10056/0 by actual independent reviewer six-reviewer-4
was read completely at this checkpoint. Its defining public source
is b948df1495e74c9ab38783424e2b522293a34884. It confirms the new
finite k7 exclusions and q27 witness and the sharp q>=27 classification
relative to the stated 9980 tail and original spectral premises;
it also proves quantitative original-face separation and a q27
closed unequal-trade neighborhood. It does not independently audit
the 9980 infinite coefficient/tail proof or this new variable-count
criterion, asymptotic construction, q32/k8 dual, or q100/k20 recovery.
Its unrelated root-context relation is not used as a mathematical
dependency here. The exact review scope, rather than a blanket
review label, is preserved in the checkpoint.

The original uniform slope and its asymptotic/Pell deductions are proved in
[PROOF.md](PROOF.md). Private discovery and proof streams remain unpublished;
the public packet contains source plus a3084-byte factor proposal and compact
expected/validation records. Regeneration, coefficient equality and exact
multiply-back checks establish the source identities; no independent person
review or full general H/I theorem is asserted.
