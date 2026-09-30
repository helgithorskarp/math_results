# Uniform capped H matrices for completion-bijective twofold triple systems

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: complete written incidence proof, with exact rational finite validation;
author-checked, unformalized, and not independently reviewed. The design inputs,
ordinary layered certificates, elementary PSD principles and base strict EKR
are prior ingredients. General Spectral Chvátal Conjectures H and I remain open.

## 1. Precise input class and conclusions

Let U be a simple 2-(v,3,2) design, v>=13: every unordered pair of distinct
points lies in exactly two distinct triples. Define pi(P) to be the unordered
pair of their two third points. **Assume pi is a bijection on all unordered
pairs.** This extra hypothesis is essential to this proof; no assertion for
all twofold designs, arbitrary two-STS(13) unions, or all rank-three downsets
is made. No automorphism hypothesis is imposed.

Let D contain the empty set, every singleton and pair, and the triples U. Put

```
m=v(v-1)/2,   b=v(v-1)/3,   N=1+v+m+b=(5v^2+v+6)/6,
s=2v-1,      delta=N-7v=(5v^2-41v+6)/6>0.
```

All v stars have size s. There is an explicit rational symmetric matrix Q_c
with empty row/column one, nonempty diagonal s, zero entries on distinct
intersecting sets, and

```
Q_c 1=N1,        0<=Q_c<=NI,
rank Q_c=N-v-1,  rank(NI-Q_c)=N-1,
Q_c|_(1 perpendicular) <= (N-delta)I.
```

Thus M_c=(Q_c-sI)/(N-s) satisfies H and the additional cap M_c<=I.
Every finite product of these downsets on disjoint coordinate supports
satisfies capped H by the established tensor mechanism.

For every U in the same class there is an explicit rational pair-layer
perturbation Q_r, requiring no Steiner decomposition, with

```
rank Q_r=N-v,     rank(NI-Q_r)=N-1,
Q_r|_(1 perpendicular) <= (N-delta/2)I.
```

This is the greatest possible H rank. The only maximum intersecting families
are coordinate stars. For products consisting of such repaired factors, write
N_* for the product of their N_j, p=max_j(s_j/N_j), and
r=sum_(j:s_j/N_j=p) v_j. The product has maximal rank N_*-r and precisely
those r largest coordinate stars as equality cases. The product statement
also allows any previously established capped maximal-rank factor with simple
upper endpoint and 0<s_j<N_j/2, substituting its number of maximum coordinate
stars for v_j. This density condition excludes cube endpoint degeneracies.

In particular the centered conclusion holds for the equilateral design over
**every finite field F_q with q>=13 and q=1 mod3**, including characteristic
two. The repaired maximal-rank conclusion holds for **all these q**, including
even orders and odd prime powers. Finite fields and the
affine Mendelsohn design are classical, not newly constructed designs.

## 2. The eight-weight formula and the incidence identities

For a triple A and point x outside it, let f_A(x) be the number of pairs
P inside A whose other completing point is x. Count multiplicities: f_A(x)
can equal three in characteristic two. Define

```
a=-2/3,
w=1+4v(2v-5)/(3(v-2)(v-3)(v-4)),
c=1+4/(3(v-2)(v-3)),
d=(v^2-v-4)/((v-3)(v-4)),
h=(v^2-7)/((v-3)(v-4)),
t=(v-1)/(v-4).
```

Set all empty entries to one and nonempty diagonal entries to s. On distinct
intersecting sets set Q_c to zero. On disjoint nonempty sets use

| Sizes | Entry |
|---|---|
| 1,1 | a |
| 1,2 | w-d if their union is a triple, otherwise w |
| 1,3 | h-t f_A(x) |
| 2,2 | c |
| 2,3 | d |
| 3,3 | t |

The new completion term in sizes 1,3 lies outside the seven-weight template
excluded in [TEMPLATE_OBSTRUCTION.md](TEMPLATE_OBSTRUCTION.md). That earlier
obstruction remains valid and does not obstruct this construction.

Use matrices P (point/pair incidence), B (point/triple incidence), R
(pair/triple containment), C (point/completing-pair incidence), and H with
H_(x,A)=f_A(x) outside A and zero inside A. They have dimensions v by m,
v by b, m by b, v by m, and v by b respectively. Here J always has the
required rectangular dimensions. Direct counting gives

```
PP^T=CC^T=(v-2)I+J,       BB^T=(v-3)I+2J,
PC^T=CP^T=2(J-I),         PR=2B,
RB^T=2P^T+C^T,            CR=B+H,
BH^T=HB^T=3(J-I).
```

Only CC^T uses the completion-bijection hypothesis: C is a column permutation
of P. For x!=y, (PC^T)_(x,y) counts the two triples through x,y, choosing
their pair containing x and excluding y. Its diagonal vanishes. Each pair's
two blocks prove RB^T=2P^T+C^T. Each of a triple's three pairs contributes
its third point inside the triple and one outside, proving CR=B+H. Finally

```
BH^T=B(R^TC^T-B^T)=2PC^T+CC^T-BB^T=3(J-I).
```

P,C,B,H all have row sum v-1; their column sums are respectively 2,2,3,3.
For H use H1=CR1-B1=2C1-B1. R has row sum two and column sum three.
All these matrices have nonnegative entries, even if H has repeated counts.
Consequently ||R||<=sqrt(6) and ||H||<=sqrt(3(v-1)), by weighted
Cauchy--Schwarz or the nonnegative row/column norm bound.

The six row/star scalar equations are

```
h+(v-4)d+(v-7)t=s,
1+s+(v-3)h-3t+(v-3)(v-4)d/2+(v-4)(v-6)t/3=N,
w+(v-3)c+(v-5)d=s,
1+s+(v-2)w-2d+(v-2)(v-3)c/2+(v-3)(v-4)d/3=N,
a+(v-2)w-2d+(v-3)h-3t=s,
1+s+(v-1)a+(v-1)(v-2)w/2-(v-1)d
    +(v-1)(v-3)h/3-(v-1)t=N.
```

Their derivation uses the displayed incidences and inclusion-exclusion.
For example an outside point x has v-7+f_A(x) triples in its star disjoint
from A, so the terms -t f_A(x) and +t f_A(x) cancel in the first equation.
An outside point x for a pair P has v-5+1_(P+x in U) disjoint triples,
giving the third equation. At a point coordinate, BH^T supplies the last
completion correction. Substitution verifies all six identities over Q(v).
The equations for a star coordinate inside the indexed set follow directly
from the diagonal/support rule. Empty row and star sums are N and s.
Thus Q_c1=N1 and Q_c x_i=s1 for every star indicator x_i.

## 3. A uniform PSD factorization and exact rank

Let L be the nonempty principal matrix of Q_c-J_N. The star identities give

```
L [ I_v ; P^T ; B^T ]=0.
```

The bottom principal block K, on pairs and triples, therefore determines L:

```
F=[ -P -B ; I_m 0 ; 0 I_b ],       L=F K F^T,
K22=(s+c)I-cP^TP+(c-1)J,
K23=dR-dP^TB+(d-1)J,
K33=(s-t)I+tR^TR-tB^TB+(t-1)J.
```

The disjoint-triple matrix is J-B^TB+R^TR-I; this identity uses simplicity,
so distinct triples can share zero, one, or two points. The disjoint pair
and pair/triple identities are J-P^TP+I and J-P^TB+R. These give K above.
F has full column rank. Thus L is PSD exactly when K is, with the same rank.

Regular row/column sums separate the two layer-constant vectors from the
pair/triple spaces having sum zero in each layer. In normalized constant
bases, K has the matrix

```
[ 8/3       -sqrt(8/3) ]
[ -sqrt(8/3)      1    ],
```

which is PSD of rank one. Indeed K22 has constant row sum 8/3, K23 has
row sum -4/3 (from 2d-2d(v-1)+(d-1)b), and K33 has row sum one; m/b=3/2.
Its kernel is (1_m,2*1_b), so F^T1=(-1_m,-2*1_b) proves L1=0.

On the sum-zero pair space the eigenvalues of K22 are

```
alpha1=s-c(v-3)=(3v^2-16)/(3(v-2))>0  on range(P^T),
alpha2=s+c>2v                       on ker(P).
```

Range here means the image of sum-zero point vectors. For a sum-zero triple
vector z, PRz=2Bz, so the projection of Rz onto that range is
2P^TBz/(v-2). The exact Schur complement of K22 is

```
S=(s-t)I+beta R^TR-gamma B^TB,
beta=t-d^2/alpha2,
gamma=t-4d^2/(alpha2(v-2))+d^2(v-4)^2/((v-2)alpha1).
```

For v>=13, 1<t<=4/3 and 0<d<=2, so beta>1-2/v>0.
From PR=2B and PP^T=(v-2)I on sum-zero points,
R^TR>=4B^TB/(v-2) on sum-zero triples. Hence

```
S >= (s-t)I-[t(v-6)/(v-2)+d^2(v-4)^2/((v-2)alpha1)] B^TB
  >= mu I,
mu=v(3v^3-13v^2+32)/((v-3)(v-2)(3v^2-16))>0.
```

The bracket is positive. The second inequality uses BB^T=(v-3)I on
sum-zero points, so B^TB<=(v-3)I on sum-zero triples. For z=v-13>=0,
the cubic in mu is 4426+1183z+104z^2+3z^3, strictly positive.
All divided quantities are positive: v-2,v-3,v-4,alpha1,alpha2.
This closes both Schur inequalities, without assumptions on R's remaining
singular values or on an automorphism group.

K is positive definite on the sum-zero pair/triple space and rank one on
constants, so rank K=m+b-1. Extend L by an empty zero row/column. Since
L1=0 and Q_c=J_N+L, Q_c is PSD with rank m+b=N-v-1. Its kernel is
exactly the v centered stars z_i=x_i-(s/N)1 and
w_0=e_empty-(1/N)1: these are v+1 independent vectors, as seen by comparing
empty, singleton and pair coordinates. This kernel calculation will be used
in the repair, not inferred from numerical ranks.

## 4. A strict upper cap by elementary block norm bounds

The subspace of vectors constant on each of the three nonempty size levels
is invariant. On it L is PSD of rank one and trace
(v-1)/3+8/3+1=(v+10)/3<7v. Its orthogonal complement consists of vectors
having sum zero on each level and is also invariant. On that complement
the diagonal blocks are bounded above by

```
L11<2v I,       L22<=(2v+1/3)I,       L33<=(2v+17/3)I.
```

For the latter two drop -cP^TP and -tB^TB and use ||R||^2<=6. The weights
obey 0<w<=3/2, 0<c<=4/3, 0<d<=2, 0<h<=2, 1<t<=4/3. Their upper-bound
numerators, over positive denominators, have coefficients in z=v-13 of

```
w<=3/2:   786+521z+74z^2+3z^3,
c<=4/3:   106+21z+z^2,
d<=2:     28+13z+z^2,
h<=2:     18+12z+z^2.
```

On layer-sum-zero vectors the J terms vanish. The off-diagonal norms satisfy

```
||L12||=||-wP-dC|| <= (w+d)sqrt(v-2) <= (7/2)sqrt(v),
||L13||=||-hB-tH|| <= h sqrt(v-3)+t sqrt(3(v-1)) <= (13/3)sqrt(v),
||L23||=||dR-dP^TB|| <= d[sqrt(6)+sqrt((v-2)(v-3))] <=2v+5.
```

The second bound uses sqrt(3)<7/4; the last uses sqrt(6)<5/2.
Bound the quadratic form by the three by three matrix of these diagonal
upper bounds and off-diagonal norms. Its largest eigenvalue is at most its
largest row sum. Using sqrt(v)<=v/3, valid for v>=13, the three row sums are
bounded by

```
(83/18)v,       (31/6)v+16/3,       (49/9)v+32/3,
```

each strictly below 7v. The last two margins have positive numerators
11v-32 and 14v-96. The empty extension has eigenvalue zero. Thus
Q_c|_(1 perpendicular)=L|_(1 perpendicular)<7v I.
Finally delta=N-7v>0 since its numerator at v=13+z is
318+89z+5z^2. Consequently NI-Q_c-delta(I-J_N/N) is PSD, has kernel
exactly the constant vector, and rank N-1. This proves the strict cap and
the stated buffer.

## 5. A universal maximal-rank perturbation and products

Put k=(v-2)(v-3)/2 and

```
eta=delta/(8mk)=(5v^2-41v+6)/(12v(v-1)(v-2)(v-3)),
Q_r=Q_c+eta E.
```

E has nonempty diagonal zero and is zero on all distinct intersecting sets.
Its only nonzero entries are

| Position | Entry of E |
|---|---:|
| empty,empty | mk |
| empty,singleton | -(v-1)k |
| empty,pair | k |
| disjoint singleton,singleton | 2k |
| disjoint singleton,pair | -(v-3) |
| disjoint pair,pair | 1 |

All other entries vanish; use symmetry. Thus the new nonempty weights are
a+2k eta, w-(v-3)eta, c+eta, with d,h,t unchanged. Empty row sums cancel
because v(v-1)=2m; singleton and pair row sums cancel as
-(v-1)k+2(v-1)k-(v-1)k and k-2k+k. Triple rows vanish. The corresponding
star sums cancel as well, including the empty star equation. Hence E1=0
and E x_i=0. Support, prescribed diagonal, row sum and centered-star
annihilation are preserved.

The absolute row sums of E on empty, singleton, pair and triple rows are
respectively 4mk, 4(v-1)k, 4k and zero. Therefore ||E||<=4mk, and Section 4
immediately gives the delta/2 upper buffer for Q_r. Positivity, which cannot
be inferred from that norm estimate at a singular Q_c, is proved next.

Extend the factor of Section 3 by one independent empty column:

```
F_0=[1 0 0 ; 0 -P -B ; 0 I_m 0 ; 0 0 I_b].
```

Q_r-J_N annihilates every uncentered star, so it is F_0 K_0 F_0^T, where
K_0 is its principal block on empty, pairs and triples. F_0 has full column
rank. On normalized layer constants, K_0 is the sum of the centered rank-one
PSD matrix from Section 3, extended by an empty zero row, and

```
eta*k [ sqrt(m) ; 1 ; 0 ] [ sqrt(m) ; 1 ; 0 ]^T.
```

These two rank-one directions are independent, so this constant block is
PSD of rank two. In original layer coordinates its kernel is
F_0^T1=(1,-1_m,-2*1_b), as also follows from the row sums. In normalized
constant coordinates the same vector is (1,-sqrt(m),-2sqrt(b)).
On sum-zero pair/triple vectors, only K22 changes, by
eta(I-P^TP). Its two eigenvalues become

```
alpha1'=alpha1-eta(v-3),       alpha2'=alpha2+eta.
```

To quantify the Schur margin, let A=(v-3)d^2(v-4)^2/(v-2). The same
projection calculation as Section 3 gives a lower bound

```
mu'=mu-A(1/alpha1'-1/alpha1).
```

Its R^TR coefficient stays positive because alpha2'>alpha2. We have
alpha1>v, A<4v^2, and mu>1: indeed

```
mu-1=2(v-4)(v^2+3v-12)/((v-3)(v-2)(3v^2-16))>0.
```

Also delta<v^2 and 8mk>v^4, so 0<eta<1/v^2. To check the latter
denominator inequality, write z=v-13; then
8mk-v^4=v(443+217z+27z^2+z^3)>0.
It follows that alpha1'>alpha1/2, and

```
A(1/alpha1'-1/alpha1)
 =A eta(v-3)/(alpha1 alpha1')
 <2*(4v^2)*(1/v^2)*v/v^2=8/v<1.
```

Thus mu'>1-8/v>0 for v>=13. This proves positive definiteness on the
entire sum-zero pair/triple space, with no ordinary H certificate assumed.
K_0 consequently has rank (m+b-2)+2=m+b. Q_r-J_N has that same rank,
annihilates constants, and is PSD, so rank Q_r=m+b+1=N-v.
Its kernel is exactly the v centered-star span. The upper endpoint is
simple by the delta/2 buffer.

The general star-kernel/rank/equality criterion is credited to
**six-downset-3**, researcher,
[REGULAR_SIX_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
For clarity: support makes a size-a intersecting indicator's centered
quadratic form equal a(s-a), so a<=s. Centered maximum stars belong to every
H kernel and are independent by empty/singleton coordinates. Thus rank<=N-v.
At equality, a centered maximum-family indicator is a linear combination
of centered stars. Empty coordinates force the coefficient sum to one;
singleton coordinates force each coefficient to be zero or one, so precisely
one star is selected. This is a matrix equality argument, not a new classical
rank-three strict-EKR result: the base conclusion also follows from
[Czabarka--Hurlbert--Kamat, Theorem 1.4](https://arxiv.org/pdf/1703.00494).

The capped tensor rule is credited to **six-downset-1**, researcher,
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
Here N>7v>2s, so rho_j=s_j/(N_j-s_j)<1. The spectra of normalized capped
factors lie in [-rho_j,1]. Tensor support, symmetry and row sums hold exactly;
a negative product eigenvalue has magnitude at most max rho_j. For repaired
factors their upper endpoint one is simple. To attain the largest negative
endpoint precisely one factor must be at its tied largest negative endpoint
and all others at one: any extra nonunit factor decreases absolute value.
Its multiplicity is consequently sum_(ties) v_j. This proves the product
rank and the general star-kernel criterion proves all equality cases.
Centered factors have one extra negative-endpoint direction; their products
still satisfy capped H, but are outside this maximal-rank product assertion.

For comparison, when a two-STS decomposition is supplied one may also use
the older ordinary layered matrix of [PROOF.md](PROOF.md) and its trace
mixture from [MAXRANK_PROOF.md](MAXRANK_PROOF.md). The verifier retains exact
checks of this alternative at13 and definition/kernel comparisons at19,31.
That alternative is not required by the uniform perturbation theorem.

## 6. All finite-field examples, including odd prime powers

Let F_q be a finite field, q=1 mod3, and choose a root rho of
rho^2-rho+1=0. Such roots are distinct since the characteristic is not three.
Take U={ {x,x+d,x+rho*d}: x in F_q, d!=0 }. The two roots give the same
unordered triples. Rotating a triple replaces d by rho^2*d; there are exactly
three representations for each triple. In particular |U|=q(q-1)/3.
For a pair {a,b}, its completing points are

```
(1-rho)a+rho*b,       rho*a+(1-rho)b.
```

The six reorderings of a triple show these are all possible thirds, and they
are distinct and outside the pair. The linear map on ordered pairs displayed
here commutes with interchange and has determinant 1-2rho. This determinant
is one in characteristic two; in odd characteristic it could vanish only
if 3=0. It therefore bijects distinct ordered pairs and induces a bijection
of unordered pairs. All hypotheses of Sections 1--5 hold for q>=13.
These are the unordered affine Mendelsohn systems. Their classical algebraic
origin is, for example,
[Donovan--Griggs--McCourt--Opršal--Stanovský, Proposition 2.1](https://arxiv.org/pdf/1411.5194),
where the affine quasigroup condition is k-k^2=I; see also
[Nowak, Distributive Mendelsohn triple systems and the Eisenstein integers](https://arxiv.org/pdf/1908.04966).
Our new ingredient is the uniform capped spectral matrix, not that design.

Suppose q is odd. Then rho has order six. A triple's translation orbit has
size q: a nonzero translation stabilizing a three-element set would force
characteristic three. These orbits are indexed by d modulo the subgroup
C3=<rho^2>. Each orbit covers the three unordered difference classes
{+/-d}, {+/-rho*d}, {+/-rho^2*d}, exactly once each. The two orbits indexed
by d and -d are distinct and cover the same C6=<rho> coset of differences.
Choose one of the two orbits in each C6 coset, and put the other in the
second system. Different cosets cover disjoint difference classes; together
they cover every unordered pair exactly once. Both systems are STS(q), are
block-disjoint, and have union U. This supplies the alternative trace-mixture
input at every odd q>=13 with q=1 mod3, including odd prime powers.
It also gives 2^((q-1)/6) contained translation-invariant systems and
2^((q-1)/6-1) unordered decompositions; only one chosen decomposition is
needed for the matrix, so no exponential enumeration enters the theorem.

Even q=4^k have no STS(q) decomposition. Both their centered and maximal-rank
capped results follow from Sections 2--5 with multiplicity-counted H.

## 7. Reproduction and the exact trust boundary

[uniform_twofold.py](uniform_twofold.py) validates all blocks and the entire
completion permutation before constructing the rational weights and universal
pair-layer perturbation. Its alternative trace repair requires and checks a
supplied two-STS decomposition. It regenerates field
inputs at primes and F16=F2[X]/(X^4+X+1); the latter includes H entries three.
[twofold_identities.py](twofold_identities.py) independently checks twenty
identities by integer polynomial coefficient comparison after clearing
denominators over Q(v), and eleven positive-coefficient certificates at
v=13+z. It requires no CAS. The optional derivation script
[derive_twofold_sympy.py](derive_twofold_sympy.py) uses SymPy1.14.0 over Q(v);
its compact output is [twofold_symbolic.json](twofold_symbolic.json).
CAS identities do not prove the surrounding incidence or spectral bridges.

[verify_uniform_twofold.py](verify_uniform_twofold.py) regenerates the inputs,
checks ten incidence identities, full closure/support/diagonal/row/star
conditions, the completion multiplicities, and exact matrices/hashes. At
primes13,19,31 it checks both centered and maximal lower PSD and their
delta and delta/2 buffered upper PSD using
the previously proved [prime-affine reduction](AFFINE_REDUCTION.md), with
independent rational Schur, integer Schur and integer characteristic-polynomial
checks on the small restrictions. Their orders are12/15,17/20,27/30.
The proof of this reduction remains a written dependency; the uniform theorem
above does not use it. At16 all four full217-by-217 forms are checked by
fraction-free integer Schur with exact divisibility and zero-residual rules,
independently of a symmetry reduction. The alternative ordinary, trace-repaired
and buffered trace-repaired forms at13 are also checked in full. At19 and31 that alternative's PSD
and rank use the written convex/kernel bridge, with full definition and
kernel checks; they are not described as full elimination replays.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/twofold_identities.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_uniform_twofold.py --check
```

Use CPython3.11+ (tested3.11.2), assertions enabled, one process/thread,
standard library only. Compact output is
[uniform_twofold_expected.json](uniform_twofold_expected.json).
The complete validation passed in226.48 seconds with239,488 KiB maximum RSS;
these are measured costs, not runtime guarantees. It includes five rejection
controls for malformed inputs, a wrong entry and a non-PSD zero-diagonal form.
Finite validations reproduce the implementation and test the analytic
bridges; they do not extend quantifiers by extrapolation. All-orders scope
rests on Sections 2--6, an unformalized written proof.
The earlier floating flag search at13 and19 only suggested the formula;
it is outside the proof boundary and no optimizer is needed for reproduction.

Primary target: [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
with [arXiv record](https://arxiv.org/abs/2609.28404) live rechecked on2026-09-30.
This result replaces the former finite-only field scope in
[FIELD19_PROOF.md](FIELD19_PROOF.md) with a uniform certificate under the
explicit completion condition. Older fixed weights are retained for exact
comparison. No historical priority follows from a bounded literature check.
