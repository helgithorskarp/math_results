# Maximal-rank H for every simple triple design of order at least thirteen

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: complete author-checked ordinary written proof with exact scalar
certificates; unformalized and not independently reviewed. General Spectral
Chvátal Conjectures H and I remain open. Classical strict EKR, designs, the
sparse trade, equality criterion and tensor rule are credited ingredients.

## 1. Quantified theorem and separate cap range

Let U be **any simple 2-(v,3,l) design**, with integers **v>=13,l>=2**.
Every pair belongs to exactly l distinct triples; repeated triples are
excluded. Necessarily l<=v-2, r=l(v-1)/2 and b=lv(v-1)/6 are integers.
There is no symmetry, completion-bijection or STS-decomposition assumption.
Let D consist of empty, all v singletons, all pairs and U. Put

```
m=v(v-1)/2, b=lv(v-1)/6, r=l(v-1)/2, u=l(l-1)/2,
N=1+v+m+b, s=v+r, k=(v-2)(v-3)/2.
```

Every coordinate star has size s. The explicit rational matrix Q_c below
has nonempty diagonal s, zero distinct-intersection entries, Q_c1=N1,
is PSD, and has rank **N-v-1**. For **every real 0<eta<=1/(8v^2)**,
Q_m=Q_c+eta E is PSD, satisfies the same linear conditions, and has rank
**N-v**, greatest possible among the PSD slacks of all real H matrices
on D. Taking rational eta supplies a rational H witness
M=(Q_m-sI)/(N-s). Its kernel is exactly the v independent centered stars.
Only coordinate stars are maximum intersecting families. This last classical
conclusion is not claimed as new.

The additional upper cap is quantified separately. For **v>=24l**,

```
Q_c restricted to 1-perpendicular < 2l^2 v I,
delta=N-2l^2 v>v^2/4.
```

With eta=1/(8v^2), Q_m has a strict upper gap at least delta/2, so
0<=Q_m<=NI and M<=I. Both NI-Q_c and NI-Q_m have rank N-1.
Prior sharper bounds for the **same centered matrix** give

| Additional hypothesis | Centered cap B | Source |
|---|---:|---|
| l=2, v>=13 | 28v/5 | independent twofold review, graph8010 |
| l=3, v>=13 | 25v/2 | [threefold proof](UNIFORM_THREEFOLD_PROOF.md), graph8028 |
| arbitrary l>=2, v>=24l | 2l^2 v | Section5 below |

For any of these caps, delta=N-B>0 and
eta=min(1/(8v^2),delta/(8mk)) yield a strict upper gap delta/2 for Q_m.
For l>=4 and 13<=v<24l, the theorem asserts H and maximal lower-slack
rank; it makes **no upper-cap claim** for this formula. Absence of that
claim is not nonexistence of a cap. Product conclusions in Section6 apply
only to capped factors. No design existence or exhaustive census is claimed.

The increment over the prior l=2 and l=3 formulas is the all-multiplicity
incidence correction, a two-parameter positive Schur margin, a universal
repair interval, and the stated new cap range. The earlier
[order-nine twofold extension](TWOFOLD_SMALL_ORDERS.md) remains
outside the present v>=13 theorem.

## 2. Explicit formula and all incidence bridges

For a pair p let T(p) be its l distinct completing points. Set Z_xx=0
and, for x!=y,

```
Z_xy=|{p:x,y in T(p)}|-u.
```

For x outside a triple A let f_A(x) count its pairs p with x in T(p),
with multiplicity across the three pairs. Set f_A(x)=0 inside A. Define

```
D0=l(v^2-10v+27)-6,
E0=3lv^2-3lv-16l+6v,
a=-l/3,
c=[v^2-(l+3)v+11l/3]/[(v-2)(v-3)],
d=(v^2-v-4)/[(v-4)(v-3)],
t=(v-1)[l(v-3)-6]/D0,
w=s-(v-3)c-(r-2l)d,
h=s-(v-4)d-(r-3l)t.
```

All denominators are positive in the theorem's range. Convenient expanded
forms, also checked exactly, are

```
w=[lv^2+11lv-36l+3v^3-21v^2+36v]/[3(v-4)(v-3)(v-2)],
h=[3l^2(v-1)(v-3)+l(v^3-12v^2+11v+36)+12v-24]/[(v-3)D0].
```

Set every empty entry of Q_c to one, nonempty diagonal s, and distinct
intersecting entries zero. On disjoint nonempty sets use

| Sizes | Entry |
|---|---|
| 1,1 | a+t Z_xy |
| 1,2 | w-d*1_(union in U) |
| 1,3 | h-t f_A(x) |
| 2,2 | c |
| 2,3 | d |
| 3,3 | t |

In the 1,2 row this means **w-d*1_(union in U)**. Let P,B,R be
point/pair incidence, point/triple incidence and pair/triple containment,
of dimensions v by m, v by b, m by b. Let C_xp=1_(x in T(p)) and
H_xA=f_A(x), of dimensions v by m and v by b. J has the indicated
rectangular size. Direct counting gives

```
PP^T=(v-2)I+J,             BB^T=(r-l)I+lJ,
CC^T=(r-u)I+uJ+Z,         PC^T=CP^T=l(J-I),
PR=2B,                    RB^T=lP^T+C^T,
CR=B+H,                   BH^T=HB^T=3u(J-I)+Z.
```

Indeed a point completes its opposite pair once in each of its r blocks,
so C has row sums r and column sums l. The diagonal of CC^T is r;
its off-diagonal is the defining codegree. Since lr-(r-u)-uv=0,
CC^T1=lr1 implies Z1=0. For x!=y, PC^T counts the l triples through
x,y, and its diagonal is zero. A pair's l blocks give RB^T=lP^T+C^T.
Each of a triple's pairs has exactly one completing point inside that
triple, proving CR=B+H. Finally

```
BH^T=lPC^T+CC^T-BB^T=3u(J-I)+Z.
```

P,C,B,H have row sums v-1,r,r,(l-1)r and column sums
2,l,3,3(l-1). R has row sum l and column sum3. These identities are
valid for every simple input, including ones with f_A(x)=2 or3.

The complete six row/star equations are

```
h+(v-4)d+(r-3l)t=s,
1+s+(v-3)h-3(l-1)t+(v-3)(v-4)d/2+(b-3r+3l-1)t=N,
w+(v-3)c+(r-2l)d=s,
1+s+(v-2)w-ld+(v-2)(v-3)c/2+(b-2r+l)d=N,
a+(v-2)w-ld+(r-l)h-3ut=s,
1+s+(v-1)a+(v-1)(v-2)w/2-rd+(b-r)h-(l-1)rt=N.
```

For an outside star coordinate x, the numbers of triples in its star
disjoint from a pair p or a triple A are r-2l+1_(p+x in U) and
r-3l+f_A(x), respectively. Inclusion-exclusion proves these counts;
the completion corrections cancel those in the 1,2 and 1,3 entries.
For a singleton x and a different star coordinate y, the correction
tZ_xy cancels -tZ_xy in the triple sum through y, by BH^T above.
Z1=0 removes the singleton row correction. The pair and triple row
counts of disjoint blocks are b-2r+l and b-3r+3l-1. Total outside
completion multiplicity in a triple row is3(l-1); in a point row it is
(l-1)r. These prove the displayed equations' interpretations. Star
coordinates inside the indexed set follow from diagonal and support;
empty sums are N and s. Exact substitution in Q(v,l) proves all six,
hence Q_c1=N1 and Q_c x_i=s1 for every star indicator x_i.

## 3. Complete lower PSD and kernel proof

Let L be Q_c-J_N, including its empty zero row. Star annihilation
determines its nonempty blocks from the pair/triple principal matrix K:

```
L=F K F^T,  F=[0 0; -P -B; I_m 0; 0 I_b],
K22=(s+c)I-cP^TP+(c-1)J,
K23=dR-dP^TB+(d-1)J,
K33=(s-t)I+tR^TR-tB^TB+(t-1)J.
```

F has full column rank. Pair disjointness is J-P^TP+I, pair/triple
disjointness is J-P^TB+R, and triple disjointness is
J-B^TB+R^TR-I. The last uses simplicity: distinct triples share at
most two points. Thus K is exactly the bottom principal block and
L annihilates [0;I_v;P^T;B^T]. No fitted incidence spectrum is assumed.

Regularity splits constants from vectors having sum zero in each layer.
In normalized pair/triple constant coordinates K is

```
[ 4l/3           -2sqrt(l/3) ]
[ -2sqrt(l/3)     1         ].
```

This is PSD of rank one. Its kernel in original coordinates is
(1_m,2*1_b), since b=lm/3. Its three scalar identities are

```
s+c-2c(v-1)+(c-1)m=4l/3,
ld-2dr+(d-1)b=-2l/3,
s+(3l-1)t-3rt+(t-1)b=1.
```

The last selects t from the otherwise free affine row/star equations;
it gives the displayed denominator D0. The familiar formula
(v-1)/(v-l-2) is valid at l=2,3 only and is not extrapolated here.
F^T1=(-1_m,-2*1_b), so L1=0. The sole positive eigenvalue on the
three nonempty layer-constant space, from its trace, is l(v+7)/6+1.

On sum-zero pairs, K22 has eigenvalues

```
alpha1=s-c(v-3)=E0/[6(v-2)]>lv/2,
alpha2=s+c>v.
```

They act on P^T of sum-zero points and ker P, respectively, by
PP^T=(v-2)I there. The exact scalar certificates also give
1<t<2 and0<d<2. Thus beta=t-d^2/alpha2>1-4/v>0.
For sum-zero triples z, PRz=2Bz, and projecting Rz onto the former
pair space gives 2P^TBz/(v-2). K23z=d(R-P^TB)z there. Resolving
these two orthogonal pair spaces gives the exact Schur complement

```
S=(s-t)I+beta R^TR-gamma B^TB,
gamma=t-4d^2/[alpha2(v-2)]+d^2(v-4)^2/[(v-2)alpha1].
```

The same orthogonal projection proves R^TR>=4B^TB/(v-2).
BB^T=(r-l)I on sum-zero points implies B^TB<=(r-l)I on
sum-zero triples. Since

```
red=gamma-4beta/(v-2)
   =t(v-6)/(v-2)+d^2(v-4)^2/[(v-2)alpha1]>0,
```

both inequality directions are justified and

```
S>=mu I,  mu=s-t-(r-l)red>1/l.
```

For clarity the complete scalar identity closing the singular boundary is

```
mu-1/l=P/[l(v-3)(v-2)D0 E0],
P=l^4(3v^5-15v^4+5v^3+55v^2-48v)
 +l^3(-19v^5+127v^4-203v^3-235v^2+618v)
 +l^2(3v^6-12v^5-68v^4+438v^3-223v^2-2034v+2592)
 +l(-6v^5+108v^4-642v^3+1452v^2-816v-576)
 +36v^3-180v^2+216v.
```

At v=13+x,l=2+y, the rows of its coefficient table below are the
coefficients of x^i y^j. Every entry is nonnegative and the constant
is positive. This is a certificate on the entire quadrant, not sampling.

| i / j | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| 0 | 15388632 | 11318544 | 2476440 | 1735968 | 705120 |
| 1 | 9129412 | 7297572 | 1564760 | 698464 | 300512 |
| 2 | 2228252 | 1900906 | 411488 | 110796 | 50950 |
| 3 | 286520 | 257534 | 57268 | 8651 | 4295 |
| 4 | 20480 | 19210 | 4429 | 332 | 180 |
| 5 | 772 | 750 | 180 | 5 | 3 |
| 6 | 12 | 12 | 3 | 0 | 0 |

D0 and E0 have nonnegative shifted coefficients with positive constants
126 and982. The other denominator factors are positive. The same portable
coefficient procedure proves the remaining strict scalar bounds used here.

K is positive definite on layer-sum-zero pairs/triples and rank one on
constants, giving rank K=m+b-1. L is PSD, L1=0, and Q_c=J_N+L is
therefore PSD of rank m+b=N-v-1. Its kernel is precisely the span of
the v centered stars x_i-(s/N)1 and e_empty-(1/N)1. To check their
independence, a vanishing linear combination's empty and singleton
coordinates make all its coefficients equal; a pair coordinate forces
this common value to zero. This accounts for the whole nullity.

## 4. Maximal rank for a universal real repair interval

The sparse trade is prior work of **six-downset-3**, graph7745,
[KERNEL_TRADE_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
with the general mechanism independently reviewed by **six-reviewer-1**,
graph7798,
[REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
Its nonzero entries, using symmetry, are

| Position | E entry |
|---|---:|
| empty,empty | mk |
| empty,singleton | -(v-1)k |
| empty,pair | k |
| disjoint singleton,singleton | 2k |
| disjoint singleton,pair | -(v-3) |
| disjoint pair,pair | 1 |

All triple rows and nonempty diagonals vanish. Direct row cancellation
uses2m=v(v-1). For a star: the empty row cancels
-(v-1)k+(v-1)k; an outside singleton cancels
2k-(v-2)(v-3); an outside pair cancels -(v-3)+(v-3).
Rows indexed in that star vanish by support. Hence E1=Ex_i=0.
Its absolute row sums on empty, singleton, pair, triple rows are
4mk,4(v-1)k,4k,0, so ||E||<=4mk.

The lower PSD proof needs more than this norm estimate. Extend F by
an independent empty column,

```
F0=[1 0 0; 0 -P -B; 0 I_m 0; 0 0 I_b].
```

The star kernel implies Q_m-J_N=F0 K0 F0^T, where K0 is its
empty/pair/triple principal block. On normalized constants K0 is
the rank-one PSD constant block of Section3 with an empty zero row,
plus eta k [sqrt(m);1;0][sqrt(m);1;0]^T. For eta>0 these are two
independent rank-one directions, giving PSD of rank two, with kernel
F0^T1=(1,-1_m,-2*1_b).

On sum-zero pairs/triples only K22 changes, by eta(I-P^TP), giving
alpha1'=alpha1-eta(v-3), alpha2'=alpha2+eta. For
0<eta<=1/(8v^2), alpha1'>alpha1/2>0. The same Schur argument
works because beta'=t-d^2/alpha2'>beta>0. Its loss is exactly

```
mu'=mu-A(1/alpha1'-1/alpha1),
A=(r-l)d^2(v-4)^2/(v-2)<2lv^2.
```

The last strict bound is another base-quadrant coefficient certificate.
Using alpha1>lv/2 and alpha1'>alpha1/2 gives

```
A eta(v-3)/(alpha1 alpha1')
 <2(2lv^2)(1/(8v^2))v/(l^2 v^2/4)=2/(lv),
mu'>(1-2/v)/l>0.
```

Thus K0 is positive definite on sum-zero pairs/triples and rank two
on constants: rank K0=m+b. Since Q_m-J_N is PSD and kills constants,
Q_m is PSD with rank m+b+1=N-v. Its kernel is exactly the centered
stars. Q_m(empty,empty)=1+eta mk. This proves the entire **real** eta
interval, not only the rational point used by the implementation.

## 5. Upper cap for every v>=24l

From nonnegative row/column sums,

```
||C||^2<=lr, ||H||^2<=3(l-1)^2 r, ||R||^2<=3l,
Z<=uv I on sum-zero points.
```

The last follows from CC^T=(r-u)I+Z there and
lr-(r-u)=uv. Simplicity gives l<=v-2; c decreases with l, so
c>=(8v-22)/[3(v-2)(v-3)]>0. Base certificates give c<4/3.
On v>=24l the further weight bounds are

```
0<w<3/2, 0<d<3/2, 0<h<2, 1<t<4/3.
```

All are exact positive-coefficient certificates after v=24l+x,l=2+y,
x,y>=0. No continuous parameter outside that quadrant is assumed.
L preserves layer constants and the three layer-sum-zero spaces by
regularity. On the latter, its diagonal blocks obey

```
L11=(s-a)I+tZ <= [s+l/3+(4/3)uv]I < l^2 v I,
L22=(s+c)I-cP^TP < [s+4/3]I < l^2 v I,
L33=(s-t)I+tR^TR-tB^TB < [s+(4/3)(3l-1)]I < l^2 v I.
```

The three final strict margins are certified in the same cap quadrant.
J terms disappear there. The off-diagonal blocks and bounds are

```
L12=-wP-dC,
||L12|| < (3/2)(1+l)sqrt(v) <= (1+l)v/4 < l^2 v/4,

L13=-hB-tH,
||L13|| < [3/2+(5/3)(l-1)]sqrt(lv)
        < (5l/3)sqrt(lv) <= 5lv/12 < l^2 v/4,

L23=d(R-P^TB),
||L23|| < (3/2)sqrt(l/2)[sqrt6+sqrt((v-2)(v-3))]
        < (3/2)sqrt(l/2)v <= (3/4)lv < l^2 v/2.
```

For L12 use ||P||=sqrt(v-2) and ||C||<=l sqrt((v-1)/2),
with sqrt(1/2)<3/4, sqrt(v)<=v/6 since v>=48, and l+1<l^2.
For L13 use ||B||=sqrt(l(v-3)/2), the H bound above,
sqrt(3/2)<5/4 and sqrt(lv)<=v/4 since v>=16l; 3l>5
closes the final inequality. For L23 use
sqrt6<5/2, sqrt((v-2)(v-3))<v-5/2, and
sqrt(l/2)<=l/2 for l>=2. The displayed scalar comparisons have
positive coefficients or the stated rational-square certificates.

A symmetric nonnegative 3-by-3 comparison matrix now has diagonal
l^2 v and off-diagonal l^2 v/4,l^2 v/4,l^2 v/2.
Its row sums are3l^2 v/2,7l^2 v/4,7l^2 v/4, all below2l^2 v.
It bounds L's full quadratic form by applying the block norms to the
three component norms. On layer constants, the sole nonzero eigenvalue
l(v+7)/6+1 is also below2l^2 v. This proves the stated strict cap.

An exact cap-quadrant certificate gives
delta=N-2l^2 v>v^2/4. For eta=1/(8v^2),

```
eta||E||<=mk/(2v^2)<v^2/8<delta/2,
```

because mk=v(v-1)(v-2)(v-3)/4<v^4/4. Since E1=0,
the repaired upper gap is at least delta/2 and the upper endpoint N
is simple. For the inherited l=2,3 caps, the alternative
eta=min(1/(8v^2),delta/(8mk)) has the same conclusion by
eta||E||<=delta/2. Their positive deltas follow from their published
proofs. [lambda_identities.py](lambda_identities.py) checks every one of
the six centered weights specializes exactly to both predecessors, so
their centered bounds apply without a new design assumption.

## 6. Maximality, classical equality and capped products

The star-kernel/rank criterion is credited to **six-downset-3**,
graph7627,
[REGULAR_SIX_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
Here is the bridge needed for the unrestricted real H claim. For any
feasible real H slack Q and an intersecting indicator z of size q,
support and nonempty diagonal give

```
(z-(q/N)1)^T Q (z-(q/N)1)=q(s-q)>=0.
```

Thus q<=s. At q=s its centered indicator lies in ker Q by PSD.
The v centered maximum stars are independent, using empty and singleton
coordinates, so every real feasible slack has rank<=N-v. Our Q_m
attains this bound. If a maximum family's centered indicator is a
linear combination of those stars, its empty coordinate makes the
coefficients sum to one; singleton coordinates make each coefficient
zero or one. Exactly one star is selected. The empty set cannot occur
in an intersecting family. This proves the equality assertion.

Classical strict EKR here already follows from
[Czabarka--Hurlbert--Kamat, Theorems1.4--1.5](https://arxiv.org/pdf/1703.00494).
For l>=3, s>=31 invokes Theorem1.5. For l=2, Theorem1.4's isolated
four-point exception contradicts the full pair layer. Its three-point
exception has |M|<=l (or l-1 if that triple is present), hence proposed
maximum size at most3l+4<s forv>=13. The spectral matrix, not a new
classical EKR theorem, is the research increment.

The capped tensor rule is credited to **six-downset-1**, graph7578,
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
For every input here,

```
N-2s=(v-1)[(v-2)/2+l(v-6)/6]>0.
```

For any finite collection of **capped** maximal factors on disjoint
supports, set N_*=product N_j, p=max(s_j/N_j),
r_*=sum_(j:s_j/N_j=p) v_j, and rho_j=s_j/(N_j-s_j)<1.
Each M_j has spectrum in [-rho_j,1], simple endpoint1, and lower
endpoint multiplicity v_j. The tensor preserves support, symmetry and
row sums. A negative product eigenvalue has magnitude at most
rho_*=max rho_j; equality requires exactly one factor at a tied largest
negative endpoint and all remaining factors at1, since rho_j<1 and
all nonconstant upper eigenvalues are strictly below1 in magnitude
except these already subunit lower endpoints. The tensor's H slack
therefore has rank N_*-r_*. The same centered-star equality argument
selects precisely the r_* coordinate stars of greatest density.
Mixed products can use any already proved capped maximal factor with
simple upper endpoint and density strictly below1/2, replacing v_j
by its number of independent maximum coordinate stars. Uncapped factors
in the remaining parameter range are excluded from this conclusion.

## 7. Portable certificate and literal validation boundary

[bivariate_certificates.py](bivariate_certificates.py) implements exact
sparse Fraction polynomials over Q(v,l), rational-function coefficient
cross-multiplication, and the two affine substitutions. It uses no CAS,
polynomial GCD, floating sample, solver or inferred denominator sign.
[lambda_identities.py](lambda_identities.py) verifies **27 zero identities**,
including all six row/star equations, the constant block, exact Schur
identity and12 predecessor-weight regressions. It verifies **30 strict
positive-coefficient certificates**,16 onv>=13,l>=2 and14 onv>=24l,l>=2.
For each rational bound it independently checks numerator and denominator
shifted coefficients are nonnegative with positive constant. The complete
33-term Schur numerator and coefficient counts/hashes are in
[uniform_lambda_expected.json](uniform_lambda_expected.json).
The exact radical comparisons are rational square inequalities.

[uniform_lambda.py](uniform_lambda.py) validates simplicity, replication
and every pair multiplicity literally before constructing the matrix.
It retains a nonbijective twofold13 input and the threefold13 tetrahedron
input, and supplies literal cyclic13 degree4/5 examples. These are
implementation controls, not a design census or new-design claims.
[verify_uniform_lambda.py](verify_uniform_lambda.py) checks every full
support/row/star equation, ten incidence identities, independent kernel
Gram ranks, hashes and nine rejection controls. It checks both full lower
matrices for all four inputs, and the two buffered upper matrices on each
degree2/3 input, by exact integer Schur: **12 full PSD forms**. Degree4's
centered lower is independently checked by Fraction Schur. The degree2/3
centered matrices are compared entry-for-entry with their predecessors.

| Literal input | l | N,s | Centered/maximal ranks | Buffered-upper ranks |
|---|---:|---|---|---|
| nonbijective twofold13 | 2 | 144,25 | 130,131 | 143,143 |
| nondecomposable threefold13 | 3 | 170,31 | 156,157 | 169,169 |
| cyclic degree4 at13 | 4 | 196,37 | 182,183 | not asserted |
| cyclic degree5 at13 | 5 | 222,43 | 208,209 | not asserted |

**None of the four literal inputs lies in the new v>=24l cap range.**
That universal cap is established by the coefficient/norm proof in
Section5, not a finite PSD fixture or extrapolation. The rejection
controls cover excluded order, impossible multiplicity, nonintegral
replication, missing/duplicate blocks, excessive eta, omission of Z,
clamping multiplicity-valued H to binary, and an indefinite zero-diagonal
matrix. No failed search is interpreted as mathematical nonexistence.

Reproduce from repository root with CPython3.11+ (tested3.11.2), assertions
enabled, standard library, one process/thread:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/lambda_identities.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_uniform_lambda.py --check
```

The initial full run passed in178.14s with32,172KiB maximum RSS; the
complete expected-output replay passed in182.06s with32,056KiB, one
thread. Optional [derive_lambda_sympy.py](derive_lambda_sympy.py), using
SymPy1.14.0 over Q(v,l), reproduces parameter selection and the exact
Schur rational expression; [lambda_symbolic.json](lambda_symbolic.json)
is its compact output. Neither is a dependency of the portable verifier.
The universal incidence/Schur/rank/norm/tensor interpretation is an
ordinary written proof, author checked, unformalized and unreviewed.
The scalar verifier and finite PSD fixtures do not formalize those bridges.

## 8. Attribution and current primary status

The prior degree-two v>=13 core is
[UNIFORM_TWOFOLD_PROOF.md](UNIFORM_TWOFOLD_PROOF.md), graph7956.
**six-reviewer-1** independently verified it and improved its cap to28v/5,
graph8010,
[twofold review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review1/REVIEW.md).
**six-reviewer-5** independently verified its v>=9 successor, graph7978,
and a larger repair interval at small orders, graph8034,
[small-order review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_twofold_review5/REVIEW.md).
Those verdicts concern degree2, and do not independently validate this
all-multiplicity theorem. The prior degree-three proof is graph8028.
Its25v/2 centered cap is inherited explicitly, not claimed new here.

Complete rank-three truncations (l=v-2) overlap the present input class,
but their prior all-small-order capped theorem, graph7930,
[six-downset-3's proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md),
has its own range and method. The present generic cap range does not cover
those dense inputs. The freshly committed all-rank complete-layer coupling
of **six-downset-3**, graph8064,
[PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md),
proves ordinary maximal-rank H on every complete rank-r truncation atn>=2r.
It overlaps the complete l=v-2 case at rank3, whereas the current theorem
allows arbitrary simple pair-balanced triple layers. Its explicitly uncapped
formula and the present restricted cap range have separate limitations.
Neither result supersedes the other's additional hypotheses or caps. The earlier
[seven-weight obstruction](TEMPLATE_OBSTRUCTION.md), graph7769, does not
exclude the completion-sensitive Z,H formula used here.

The primary target is
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
Its [arXiv record](https://arxiv.org/abs/2609.28404), refreshed2026-09-30,
lists onlyv1 and the text still states H/I as conjectures. No historical
priority, resolution of general H/I, universal cap beyond its displayed
range, or new classical rank-three EKR result is claimed.
