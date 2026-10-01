# H and the greatest possible slack rank for every simple triple design

Author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary proof, with exact portable scalar
certificates and full literal matrix controls. Unformalized and not independently
reviewed. General Spectral Chvátal Conjectures H and I remain open.

## 1. Exact scope and increment

Let U be any **simple 2-(v,3,l) design**, with integer l>=2: its triples
are distinct and every pair has exactly l completing points. Existence of
such U is a hypothesis, not a conclusion. Necessarily

```
v>=4, 2<=l<=v-2,
m=v(v-1)/2, b=lv(v-1)/6, r=l(v-1)/2,
u=l(l-1)/2, s=v+r, N=1+v+m+b, k=(v-2)(v-3)/2.
```

The replication r and block count b are integers. Let D contain empty,
all singletons, all pairs and U. Each coordinate star has size s.
There is no point symmetry, completion bijection or STS decomposition premise.

**For every such input with v>=5**, the explicit rational centered slack
Q_c below is PSD of rank **N-v-1**. For **every real
0<eta<=1/(8v^2)**, Q_m=Q_c+eta E is PSD of rank **N-v**.
Both have row sums N, nonempty diagonal s, and zero off-diagonal entries
on intersecting sets. Thus M=(Q_m-sI)/(N-s) is an H matrix; rational eta
gives rational M. Its kernel is precisely the v centered coordinate stars.
Rank N-v is greatest possible among the slacks of **all real** H matrices
on D. Maximum intersecting families are exactly coordinate stars.
The classical equality conclusion is credited, not claimed new.

The only feasible input with v<5 is **v=4,l=2**, the proper four-cube.
Its **known unique real H slack has rank7**, rather than N-v=11.
Section6 reproves that exception and credits its prior proof and review.
Consequently H and the greatest possible slack rank are determined for
every feasible simple triple design with l>=2.

The new increment over [the order-at-least-thirteen theorem](UNIFORM_LAMBDA_PROOF.md),
graph8082, is the full remaining parameter range, two exact singular choices,
and sign certificates extending the **whole real repair interval**.
That prior theorem, the small twofold extension7978 and review8034, the
three-STS9 certificates7705, the six-point result7627, and complete-layer
results7930/8064 already cover some newly included inputs by other methods.
The fresh near-cube result8106 also covers the complete five-point input.
Review8104 confirms and enlarges the interval for8064; its verdict explicitly
excludes our neighboring arbitrary-design theorem8082.
The proper-four-cube result8020/review8066 is wholly prior work.
No new design, exhaustive design classification, or nonexistence claim is made.

Upper caps are a separate issue. The construction retains only these
previously proved caps for its centered matrix:

| Additional hypothesis | Centered bound B | Prior ingredient |
|---|---:|---|
| l=2, v>=13 | 28v/5 | independent review8010 |
| l=2, 9<=v<13 | 20v/3 | small-order theorem7978 and review8034 |
| l=3, v>=13 | 25v/2 | threefold theorem8028 |
| arbitrary l>=2, v>=24l | 2l^2 v | all-multiplicity theorem8082 |

Here delta=N-B>0 and eta=min(1/(8v^2),delta/(8mk)) gives
upper gap at least delta/2 and a simple upper endpoint N. The proper
four-cube separately has spectrum15,14,0 and gap1. **No additional upper
cap or tensor theorem is asserted for the other newly included inputs.**
This boundary does not assert cap nonexistence. Existing capped product
corollaries remain in their original ranges.

## 2. Formula, singular choices and incidence identities

For a pair p let T(p) be its l completing points. Define Z_xx=0 and

```
Z_xy=|{p:x,y in T(p)}|-u       (x!=y).
```

For x outside a triple A, let f_A(x) count the pairs p of A with
x in T(p), with multiplicity across its three pairs; set f_A(x)=0
inside A. Put

```
D0=l(v^2-10v+27)-6, E0=3lv^2-3lv-16l+6v,
a=-l/3,
c=[v^2-(l+3)v+11l/3]/[(v-2)(v-3)],
d=(v^2-v-4)/[(v-4)(v-3)],
t=(v-1)[l(v-3)-6]/D0,
w=s-(v-3)c-(r-2l)d,
h=s-(v-4)d-(r-3l)t.
```

Use the generic t when D0!=0. At the two feasible singular inputs use
**t=6 for (v,l)=(5,3)** and **t=2 for (v,l)=(6,2)**.
The remaining small input (6,4) has the generic t=5.
All other feasible inputs have v>=7 and D0>0. The factors v-2,v-3,v-4
are positive everywhere in this section.

Set every empty entry of Q_c to1, its nonempty diagonal to s, and
distinct-intersection entries to0. For disjoint nonempty sets use

| Sizes | Entry |
|---|---|
| 1,1 | a+t Z_xy |
| 1,2 | w-d*1_(union in U) |
| 1,3 | h-t f_A(x) |
| 2,2 | c |
| 2,3 | d |
| 3,3 | t |

Let P,B,R be point/pair, point/triple and pair/triple containment
matrices, with dimensions v by m, v by b and m by b. Let
C_xp=1_(x in T(p)), H_xA=f_A(x), and J have the indicated rectangular
dimensions. Counting gives

```
PP^T=(v-2)I+J,             BB^T=(r-l)I+lJ,
CC^T=(r-u)I+uJ+Z,         PC^T=CP^T=l(J-I),
PR=2B,                    RB^T=lP^T+C^T,
CR=B+H,                   BH^T=HB^T=3u(J-I)+Z.
```

P,C,B,H have row sums v-1,r,r,(l-1)r and column sums
2,l,3,3(l-1); R has row sum l and column sum3.
For example, each point completes one opposite pair in each of its r
triples. The off-diagonal of CC^T is the defining codegree, and its row
sum lr makes Z1=0. PC^T counts the l triples through distinct points.
RB^T counts a pair's l triples. Each triple's three pairs have exactly
one inside completion, giving CR=B+H. Finally
BH^T=lPC^T+CC^T-BB^T=3u(J-I)+Z.
These are literal identities for every simple input, including repeated
outside completion multiplicities2 and3.

The six row/star equations are

```
h+(v-4)d+(r-3l)t=s,
1+s+(v-3)h-3(l-1)t+(v-3)(v-4)d/2+(b-3r+3l-1)t=N,
w+(v-3)c+(r-2l)d=s,
1+s+(v-2)w-ld+(v-2)(v-3)c/2+(b-2r+l)d=N,
a+(v-2)w-ld+(r-l)h-3ut=s,
1+s+(v-1)a+(v-1)(v-2)w/2-rd+(b-r)h-(l-1)rt=N.
```

For an outside star coordinate x, inclusion-exclusion gives
r-2l+1_(p+x in U) triples in its star disjoint from a pair p, and
r-3l+f_A(x) disjoint from a triple A. Their completion terms cancel
the formula's corrections. For distinct points x,y, BH^T cancels tZ_xy
in the point/star equation; Z1=0 removes the point-row correction.
Disjoint block counts are b-2r+l and b-3r+3l-1, and outside completion
totals are3(l-1) per triple and (l-1)r per point. These facts prove every
displayed equation's interpretation. Stars containing the indexed set
follow from support and diagonal; the empty sums are N and s.

Generic substitution verifies all six over Q(v,l). At each small input,
the portable checker verifies all six with the chosen t. Thus
Q_c1=N1 and Q_c x_i=s1 for every coordinate star indicator x_i.

## 3. Full lower PSD bridge and its new sign certificates

Let L=Q_c-J_N. Including the empty zero row, star annihilation and the
bottom principal matrix K give

```
L=F K F^T, F=[0 0; -P -B; I_m 0; 0 I_b],
K22=(s+c)I-cP^TP+(c-1)J,
K23=dR-dP^TB+(d-1)J,
K33=(s-t)I+tR^TR-tB^TB+(t-1)J.
```

F has full column rank. Pair disjointness is J-P^TP+I, pair/triple
disjointness is J-P^TB+R, and triple disjointness is
J-B^TB+R^TR-I. The last uses simplicity, so distinct triples share
at most two points. These prove K is the bottom block; the annihilated
uncentered stars then determine every remaining nonempty block.

Regularity orthogonally separates layer constants from vectors having
sum zero in each pair/triple layer. In normalized constant coordinates,

```
K_const=[4l/3, -2sqrt(l/3); -2sqrt(l/3),1].
```

The three exact equations are

```
s+c-2c(v-1)+(c-1)m=4l/3,
ld-2dr+(d-1)b=-2l/3,
s+(3l-1)t-3rt+(t-1)b=1.
```

The constant block is PSD of rank one with kernel (1_m,2*1_b)
in original coordinates. Generically the third equation selects the
displayed t. At (5,3) and (6,2), all nine row/star/constant equations
are affine in t and hold identically for every t after w,h are defined
as above. The checker verifies them at t=0 and t=1. These singular
equations are free parameters; they do not obstruct feasibility.
Our choices below make the PSD estimates strictly positive.

On sum-zero pairs K22 has two eigenvalues, on P^T of sum-zero points
and on ker P, respectively:

```
alpha1=s-c(v-3)=E0/[6(v-2)], alpha2=s+c.
```

Since PP^T=(v-2)I there, these spaces exhaust all sum-zero pairs.
For sum-zero triples z, PRz=2Bz gives projection
2P^TBz/(v-2) onto the first pair space. Resolving that projection in
K23z=d(R-P^TB)z yields the exact Schur complement

```
S=(s-t)I+beta R^TR-gamma B^TB,
beta=t-d^2/alpha2,
gamma=t-4d^2/[alpha2(v-2)]+d^2(v-4)^2/[(v-2)alpha1],
red=gamma-4beta/(v-2)
   =t(v-6)/(v-2)+d^2(v-4)^2/[(v-2)alpha1],
mu=s-t-(r-l)red.
```

Orthogonal projection gives R^TR>=4B^TB/(v-2), and BB^T=(r-l)I
on sum-zero points gives B^TB<=(r-l)I on sum-zero triples. Therefore,
when beta>0 and red>0, their inequality directions prove S>=mu I.
This resolves all modes without assuming a design-specific spectrum.

For **v>=7,l>=2**, exact coefficient certificates establish

```
D0>0, E0>0, alpha1>lv/2, t>1,
0<d<=19/6,
s>=2v-1,
A=(r-l)d^2(v-4)^2/(v-2)<2lv^2.
```

Simplicity, l<=v-2, gives
c>=(8v-22)/[3(v-2)(v-3)]>0, because c decreases with l.
Hence alpha2>2v-1 and

```
beta>1-361/[36(2v-1)]>0.
```

Also red>0 directly at v>=7. The two-variable Schur margin requires
an integer multiplicity split. For **l=2** the exact identity is

```
mu=v(3v^3-13v^2+32)/[(v-3)(v-2)(3v^2-16)],
mu-1=2(v-4)(v^2+3v-12)/[(v-3)(v-2)(3v^2-16)]>0.
```

For **l>=3**, use the exact identity inherited from the parent proof:

```
mu-1/l=P/[l(v-3)(v-2)D0 E0],
P=l^4(3v^5-15v^4+5v^3+55v^2-48v)
 +l^3(-19v^5+127v^4-203v^3-235v^2+618v)
 +l^2(3v^6-12v^5-68v^4+438v^3-223v^2-2034v+2592)
 +l(-6v^5+108v^4-642v^3+1452v^2-816v-576)
 +36v^3-180v^2+216v.
```

At v=7+x,l=3+y, x,y>=0, its coefficient table is:

| i / j | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| 0 | 89136 | 229848 | 292560 | 130536 | 18480 |
| 1 | 162864 | 240192 | 259292 | 116340 | 16892 |
| 2 | 117144 | 113760 | 91058 | 40150 | 6040 |
| 3 | 42084 | 31947 | 16591 | 6703 | 1055 |
| 4 | 7911 | 5394 | 1735 | 542 | 90 |
| 5 | 738 | 489 | 105 | 17 | 3 |
| 6 | 27 | 18 | 3 | 0 | 0 |

All33 nonzero coefficients are positive, including the constant89136.
The denominator factors are positive, so mu>1/l throughout this quadrant.
The l=2 formula also gives mu>1/l. Each remaining scalar bound above
is independently certified by nonnegative numerator and denominator
coefficients after v=7+x,l=2+y. A strict numerator has positive constant;
the two weak bounds may have zero constant. No numerical sampling is used.

For small orders admissibility forces only (5,3),(6,2),(6,4).
The exact checks give:

| v,l | t | alpha1 | alpha2 | beta | red | mu | A |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5,3 | 6 | 9 | 12 | 2/3 | 10/27 | 35/9 | 64 |
| 6,2 | 2 | 23/3 | 109/9 | 49/109 | 169/69 | 38/23 | 169/3 |
| 6,4 | 5 | 83/6 | 301/18 | 1167/301 | 338/249 | 237/83 | 338/3 |

In each case alpha1>lv/2, alpha2>0, beta>0, red>0,
mu>1/l and A<2lv^2. The positive red at v=5 is supplied by
this table; its first displayed summand alone would be negative.
The same complete Schur argument therefore works at all feasible v>=5.

K is positive definite on layer-sum-zero vectors and rank one on constants,
so rank K=m+b-1. Since F^T1=(-1_m,-2*1_b), L1=0.
Thus Q_c=J_N+L is PSD of rank m+b=N-v-1. Its kernel is the
v centered stars and e_empty-(1/N)1. Their independence follows from
empty, singleton and pair coordinates: all singleton coefficients agree,
and the pair coordinate forces that common value and the empty coefficient
to vanish. This accounts for the full nullity.

## 4. Every real repair parameter in the stated interval

The sparse pair-layer trade E is credited to **six-downset-3**, graph7745,
[KERNEL_TRADE_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
with the general mechanism reviewed by **six-reviewer-1**, graph7798,
[REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
Its entries are symmetric, and the only nonzero types are

| Position | E entry |
|---|---:|
| empty,empty | mk |
| empty,singleton | -(v-1)k |
| empty,pair | k |
| disjoint singleton,singleton | 2k |
| disjoint singleton,pair | -(v-3) |
| disjoint pair,pair | 1 |

All triple rows and nonempty diagonal entries vanish. Direct cancellations
give E1=Ex_i=0: empty/star sums cancel -(v-1)k+(v-1)k;
outside singleton/star sums cancel2k-(v-2)(v-3); outside pair/star sums
cancel -(v-3)+(v-3). Absolute row sums are4mk,4(v-1)k,4k,0,
so ||E||<=4mk. Hence support, diagonal, rows and stars are preserved.

For lower positivity, extend F by an independent empty column:

```
F0=[1 0 0; 0 -P -B; 0 I_m 0; 0 0 I_b],
Q_m-J_N=F0 K0 F0^T.
```

K0 is the empty/pair/triple principal block. On normalized constants it
is the old rank-one PSD block with an empty zero row, plus
eta k [sqrt(m);1;0][sqrt(m);1;0]^T. At every eta>0 these are independent
rank-one positive directions, giving rank two. Their kernel is
F0^T1=(1,-1_m,-2*1_b) in original coordinates.

On layer-sum-zero vectors only the pair block changes, by
eta(I-P^TP), so

```
alpha1'=alpha1-eta(v-3), alpha2'=alpha2+eta.
```

For 0<eta<=1/(8v^2), alpha1'>alpha1/2>0. The same Schur
calculation applies, with beta'>beta>0 and red'>=red>0. The latter
uses alpha1'<alpha1 and holds even at v=5. Its scalar margin is

```
mu'=mu-A(1/alpha1'-1/alpha1).
```

Using the strict bounds already proved for every feasible v>=5,

```
A eta(v-3)/(alpha1 alpha1')
 <2(2lv^2)(1/(8v^2))v/(l^2 v^2/4)=2/(lv),
mu'>(1-2/v)/l>0.
```

Thus all sum-zero modes are positive definite and the constant block has
rank two. Since F0 has full column rank and Q_m-J_N kills1,
Q_m is PSD of rank m+b+1=N-v. Its empty entry is1+eta mk,
and its kernel consists exactly of the centered stars. This proves the
**whole real interval**; the implementation's rational endpoint is only
one validation choice.

## 5. Greatest rank, equality, and classical attribution

The general star-kernel/rank mechanism is prior work of **six-downset-3**,
graph7627,
[REGULAR_SIX_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
For any real feasible H slack Q and an intersecting indicator z of size q,
support, nonempty diagonal and Q1=N1 give

```
(z-(q/N)1)^T Q (z-(q/N)1)=q(s-q)>=0.
```

Hence q<=s, and at equality its centered indicator lies in ker Q.
The centered coordinate stars are independent: the empty coordinate makes
their coefficients sum to zero, and singleton coordinates make each zero.
Consequently every real H slack has rank<=N-v, which Q_m attains
for v>=5. If a maximum family's centered indicator is a combination
of the centered stars, its empty coordinate makes the coefficients sum
to one, and singleton coordinates make each coefficient zero or one.
Exactly one coordinate star results.

This classical strict EKR conclusion is already implied by
[Czabarka--Hurlbert--Kamat, Theorems1.4--1.5](https://arxiv.org/pdf/1703.00494).
Here Theorem1.4 suffices throughout: its isolated four-point component
contradicts the full pair layer at v>=5. Its three-point exception has
at most3l+4 members. For v>=7,
s-(3l+4)=v-4+l(v-7)/2>0. At (6,2), that bound is10<s=11.
At (5,3) every triple is present and only two points lie outside its
three-point kernel, so the exception has at most3*2+4=10<s=11.
At (6,4) every triple is present and only three outside points are
available, giving at most3*3+4=13<s=16. Designs and the classical
classification are ingredients; the matrix and real-interval extension
are the contribution.

For previously capped parameters the six centered weights specialize
exactly to the twofold/threefold predecessors, so their cap proofs transfer.
The generic v>=24l cap is unchanged from Section5 of the parent proof.
The trade norm and eta<=delta/(8mk) retain an upper gap at least delta/2.
No claim in Sections2--4 uses those upper bounds. Product statements still
require capped factors, a simple upper endpoint and density below1/2, as
in **six-downset-1's** prior graph7578
[structural tensor proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
For v>=5 the identity
N-2s=(v-1)[(v-2)/2+l(v-6)/6]>0 holds; the sole negative second
term at v=5,l=3 still gives N-2s=4. No product extension to uncapped
inputs is inferred from lower PSD alone.

## 6. Known proper-four-cube uniqueness and rank exception

The only feasible smaller input is v=4,l=2, with N=15,s=7.
The unique-slack and extra-equality phenomenon are credited to
**six-downset-3**, graph8020,
[PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md),
and **six-reviewer-3's** independent graph8066
[REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md).
The following elementary uniqueness argument records precisely why the
N-v rank conclusion must start at v=5.

For a point x, the family of all four triples and the three pairs containing
x is intersecting of size7. It differs from coordinate star x by replacing
singleton{x} with the complementary triple. By the PSD equality identity
above, their indicator difference is in ker Q for every real feasible
slack Q. Therefore singleton x and its complementary triple have identical
columns. Intersecting support then forces all singleton/singleton off-diagonals
and all singleton/pair entries to zero, and the singleton/complementary-triple
entry to7. The singleton row sum15 forces its empty entry to1;
column equality gives the complementary triple's empty entry1.

For a pair p and point x outside it, the star equation leaves only its
complementary pair entry: Q[p,p^c]=7. Its row sum forces Q[empty,p]=1.
The empty row then forces Q[empty,empty]=1. All remaining entries are
diagonal or intersecting. Thus the unique slack is

```
Q[empty,A]=1 for every A,
Q[A,A]=7 for nonempty A,
Q[A,A^c]=7 for nonempty A,
all other entries zero.
```

The seven complementary-pair differences give seven zero eigenvectors.
Pair-symmetric vectors of total sum zero give eigenvalue14 with multiplicity6.
On empty and the normalized nonempty constant vector the block is
[1,sqrt14;sqrt14,14], with eigenvalues15 and0. Hence the spectrum is
15 once,14 six times,0 eight times: Q is PSD of rank7 and NI-Q
has rank14. Uniqueness proves rank7 is greatest over all real H slacks.
The family of all four triples and the three pairs of a three-point triangle
is a nonstar maximum, so star-only equality also correctly fails here.
The implementation applies no pair-layer repair to this exception.

## 7. Reproduction and trust boundary

[uniform_lambda_small.py](uniform_lambda_small.py) checks all block types,
simplicity, replication and every pair's exact multiplicity before construction.
It preserves the earlier constructor's domain and behavior in its own file;
the old published checkers remain unchanged.
[lambda_small_identities.py](lambda_small_identities.py) uses only Fraction
polynomials from [bivariate_certificates.py](bivariate_certificates.py).
It checks27 inherited generic identities, four additional rational-function
identities, ten new strict coefficient certificates and two weak certificates.
It checks all nine row/star/constant equations at each small input, and
their free-parameter identities at the two singular inputs. The complete
33-term shifted P table is retained in the expected output.
Numerator and denominator signs are independently checked, with no CAS,
polynomial GCD, floating point or inferred denominator sign.

[verify_uniform_lambda_small.py](verify_uniform_lambda_small.py) supplies
eleven literal controls: complete inputs at4,5,6, a rotational twofold6,
four inputs at7, the retained threefold9, and cyclic multiplicity-four
inputs at10 and12. Each input's ten incidence identities, all full H
definition equations, kernel Gram ranks and hashes are checked exactly.
There are **23 full integer Schur PSD/rank checks**, including a second
positive repair value at the singular five-point input, and **nine independent
Fraction Schur checks**. The known four-point upper slack is checked too.
Both matrices match the retained thirteen-point multiplicity-four baseline
entry by entry and by its previously recorded hashes. Fourteen negative
controls reject invalid parameters, missing/repeated blocks, invalid eta,
an indefinite residual, erased codegree correction and clamped multiplicity.
The largest literal matrix has order167; no large proof corpus is needed.

These inputs are implementation validation, **not a design census**.
The universal assertion follows from the written incidence decomposition,
orthogonal Schur inequalities, coefficient certificates and repair proof.
Those analytic/completeness bridges are ordinary mathematics, not proof-assistant
formalization. The exact finite checkers alone do not establish them.
[uniform_lambda_small_expected.json](uniform_lambda_small_expected.json)
stores the compact reproducible records, rather than dense matrices.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_uniform_lambda_small.py --check
```

An optional independent exact derivation uses SymPy1.14.0:
[derive_lambda_small_sympy.py](derive_lambda_small_sympy.py), with output
[lambda_small_symbolic.json](lambda_small_symbolic.json). It certifies the
same scalar signs and small rational values independently of the portable
polynomial backend. Its shifted Schur numerator agrees term for term with
the portable33-term table. The main checker needs only CPython3.11+ stdlib
with assertions enabled. All runs use one mathematical job and one thread.

Primary problem status was rechecked against
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
and the [version record](https://arxiv.org/abs/2609.28404): the preprint
states H and I as conjectures. This theorem covers the quantified design
subclass, and makes no resolution claim for general downsets.
