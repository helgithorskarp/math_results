# A strict upper cap for dense simple triple-design H matrices

Author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary proof with exact scalar certificates
and literal full-matrix controls; unformalized and not independently reviewed.
General Spectral Chvátal Conjectures H and I remain open.

## 1. Quantified statement and contribution

Let U be **any simple 2-(v,3,l) design**, and set q=v-2-l. Assume
integer q>=0 and

```
v>=12, v>=4(q+1), l=v-2-q.
r=l(v-1)/2, m=v(v-1)/2, b=lv(v-1)/6,
s=v+r, N=1+v+m+b, k=(v-2)(v-3)/2.
```

Existence, integrality of r,b, simplicity and constant pair multiplicity
are hypotheses. No point symmetry, completion bijection or decomposition
into Steiner triple systems is assumed. In particular l>=8. Let D contain
empty, all singletons, all pairs and U. Use the centered matrix Q_c from
[the all-orders triple-design proof](UNIFORM_LAMBDA_ALL_ORDERS.md), graph8122,
with the same generic weights, and its credited sparse trade E.

Define

```
B=s+v^2/2+(q^2+2q+3/2)v-10,
delta=N-B=11-v(q^2+2q+2)+(v-q-2)(v-1)(v-3)/6.
```

Then **delta>0** and **Q_c restricted to 1-perpendicular < B I**.
For **every real 0<eta<=1/(8v^2)**, Q_m=Q_c+eta E satisfies

```
Q_m>=0, rank Q_m=N-v,
Q_m restricted to 1-perpendicular < (N-delta/2)I.
```

Both matrices have constant row sum N, nonempty diagonal s and zero
off-diagonal entries on intersecting sets. Thus their upper endpoint N
is simple, and both NI-Q_c and NI-Q_m have rank N-1. The centered rank
remains N-v-1. The maximal matrix's kernel is precisely the v centered
coordinate stars. Rational eta, including 1/(8v^2), gives a rational H
matrix M=(Q_m-sI)/(N-s) with M<=I.

The increment is this **dense-complement upper range and half-gap for the
whole existing real repair interval**. The parent proof already gives
lower PSD, greatest possible slack rank and classical star-only equality
for every feasible simple design of order at least five. Its generic cap
v>=24l does not apply in the present dense range.
The fresh **six-reviewer-5** graph8152
[independent review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_lambda_review5/REVIEW.md)
confirms the order-at-least-thirteen parent8082 and proves a cap for
q=1,v>=13 of B_old=v^2+8v-18. Its verdict explicitly excludes8122.
Our theorem extends that missing-layer cap component to arbitrary q in
the displayed range and strengthens its q1 bound to
B=v^2+7v/2-17/2, smaller by (9v-19)/2>0. At v13 the old bound is255
and the present bound is206, giving delta146 instead of97. The complement
Z and H identities in Section2 also appear in8152; they are credited
elementary ingredients, independently derived here before the fresh review
and not claimed historically novel. That review is not a review of this
new cap or its v12 boundary. Prior complete-layer
constructions already address the q=0 subclass by other matrices, notably
graph7930 [uniform three-layer proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md)
and graph8064 [coupling proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md).
The elementary complement identities below are counting ingredients;
no new design or classical EKR theorem is claimed. No cap assertion is
made here for parameters outside the displayed range.

## 2. Formula and complementary incidence identities

Here is the formula to make the certificate explicit. Let T_l(p) be the
l completing points of a pair p; u_l=l(l-1)/2. Put Z_l,xx=0 and
Z_l,xy=|{p:x,y in T_l(p)}|-u_l for x!=y. For x outside A in U,
f_A(x) counts the three pairs of A completed by x, with multiplicity;
set it to zero inside A. Define

```
D0=l(v^2-10v+27)-6, a=-l/3,
c=[v^2-(l+3)v+11l/3]/[(v-2)(v-3)],
d=(v^2-v-4)/[(v-4)(v-3)],
t=(v-1)[l(v-3)-6]/D0,
w=s-(v-3)c-(r-2l)d,
h=s-(v-4)d-(r-3l)t.
```

All empty entries of Q_c are one; nonempty diagonal entries are s;
distinct intersecting entries are zero. On disjoint nonempty sets,

| Sizes | Q_c entry |
|---|---|
| 1,1 | a+t Z_l,xy |
| 1,2 | w-d*1_(union in U) |
| 1,3 | h-t f_A(x) |
| 2,2 | c |
| 2,3 | d |
| 3,3 | t |

Let U_q be the complement of U in all triples. It is a simple
2-(v,3,q) design, allowing the empty design when q=0. Let P be point/pair
incidence. For j=l,q let B_j,R_j,C_j be point/triple incidence,
pair/triple containment and point/pair completion matrices for U_j.
Let H_l,xA=f_A(x), r_j=j(v-1)/2, u_j=j(j-1)/2. All J have the
indicated rectangular size. Counting, including the q=0 case, gives

```
C_l+C_q=J-P,
P C_q^T=C_q P^T=q(J-I),
C_j C_j^T=(r_j-u_j)I+u_j J+Z_j,
C_q R_l=3J-3B_l-H_l,
R_l R_l^T+R_q R_q^T=(v-4)I+P^T P.
```

The first identity partitions all possible completing points outside a
pair. The second counts q triples through two distinct points. To get
the fourth, use P R_l=2B_l, C_l R_l=B_l+H_l and J R_l=3J.
For the last, the complete pair/triple Gram has diagonal v-2, entry one
for distinct pairs sharing a point, and zero for disjoint pairs. These
are exactly (v-4)I+P^T P; there is no additional J term.

On sum-zero point vectors the first two identities imply
C_l C_l^T=C_q C_q^T+(l-q)I. Indeed the additional terms are
P P^T=(v-2)I and -2qI there. Since
(r_l-u_l)-(r_q-u_q)=l-q, this proves Z_l=Z_q on that space.
Both Z annihilate constants by their completion row sums, so
**Z_l=Z_q as full matrices**. Nonnegative row/column sums give

```
||C_q||^2<=q r_q=q^2(v-1)/2,
Z_l=Z_q<=u_q v I on sum-zero points.
```

For the second inequality subtract (r_q-u_q)I from the first bound
for C_q C_q^T; q r_q-(r_q-u_q)=u_q v exactly. Thus the singleton
correction is controlled by the omitted multiplicity q.

## 3. Complete-pair bounds and the three-layer comparison

Put L=Q_c-J_N. Its empty row vanishes. Regularity splits nonempty
layer constants from the vectors having sum zero separately in the
point, pair and triple layers. On layer constants L has one positive
eigenvalue l(v+7)/6+1 and all other eigenvalues zero, as in the parent
proof. On the three sum-zero spaces its blocks are

```
L11=(s+l/3)I+t Z_l,
L22=(s+c)I-c P^T P,
L33=(s-t)I+t R_l^T R_l-t B_l^T B_l,
L12=(d-w)P+d C_q,
L13=(3t-h)B_l+t C_q R_l,
L23=d(R_l-P^T B_l).
```

The preceding complement identities transform L12,L13; J terms
vanish on these sum-zero spaces. The other blocks are the parent's
literal incidence formulas. The exact scalar checker proves

```
D0>0, 0<c<4/3, 0<d<2, 1<t<2,
|d-w|<1, |3t-h|<2.
```

Let Pi be the orthogonal projection of pair space onto ker P, and
T=Pi R_l. The complete pair Gram implies ||T||<=sqrt(v-4), since
Pi P^T=0. For any sum-zero triple vector z, B_l z is sum zero and

```
R_l z=Tz+2P^T B_l z/(v-2),
||R_l z||^2-||B_l z||^2
 =||Tz||^2+[4/(v-2)-1]||B_l z||^2
 <=(v-4)||z||^2.
```

The two pair outputs in the decomposition are orthogonal. The coefficient
4/(v-2)-1 is nonpositive at v>=6. This gives the useful ten-unit improvement
L33 < [s+2(v-5)]I. The same complete Gram on sum-zero pairs gives
||R_l||<=sqrt(2v-6) on sum-zero triples. Also

```
||P||=sqrt(v-2), ||B_l||=sqrt(l(v-3)/2).
```

The diagonal bounds are therefore

```
L11 < [s+v/3+q(q-1)v]I,
L22 < [s+4/3]I,
L33 < [s+2(v-5)]I.
```

These strict inequalities remain valid at q=0,1: the singleton bound
is then strict because l<v, even though u_q=0. Using sqrt2<3/2 and
sqrt(v)<=v/3 for v>=12 yields

```
||L12|| < sqrt(v)+sqrt2 q sqrt(v) <= v/3+qv/2,
||L13|| < sqrt(2l(v-3))+2q sqrt((v-1)(v-3))
         < (3/2+2q)v.
```

For q=0 the first displayed strict inequality follows from the P term;
the final bound remains valid. For L23 use the triangle inequality:

```
R_l-P^T B_l=T-(v-4)P^T B_l/(v-2),
||L23|| <=d[sqrt(v-4)+(v-4)sqrt(l(v-3)/(2(v-2)))]
        <=d[sqrt(v-4)+(v-4)sqrt((v-3)/2)]
        <v(v-4)/2.
```

Here sqrt(v-4)<=(v-4)/2 and sqrt((v-3)/2)<(v-2)/4 for v>=12.
The latter follows by squaring from
(v-2)^2-8(v-3)=v(v-12)+28>0. Together with d<2 they prove the
last comparison. This proof uses a sum of operator norms. It does not
assume that T and P^T B_l have orthogonal input spaces.

Apply these diagonal upper bounds and off-diagonal operator norms to
the norms of a vector's three components. The symmetric nonnegative
comparison matrix has row sums

```
R1=s+(q^2+3q/2+13/6)v,
R2=s+4/3+v/3+qv/2+v(v-4)/2,
R3=s+v^2/2+(2q+3/2)v-10.
```

The exact scalar certificates prove

```
B-R1=v^2/2+(q/2-2/3)v-10>0,
B-R2=q^2 v+(3q/2+19/6)v-4/3-10>0,
B-R3=q^2 v>=0,
B-[l(v+7)/6+1]>0.
```

A symmetric nonnegative matrix's largest eigenvalue is at most its
largest row sum. All diagonal bounds on L are strict, so its quadratic
form is strictly below B on every nonzero sum-zero vector, including
q=0 when R3=B. The layer-constant bound above completes every mode
of 1-perpendicular, proving the centered cap.

## 4. The whole real repair interval and the half-gap certificate

The parent lower PSD and rank proof applies because v>=12,l>=8;
no new lower assertion is needed. The trade is credited to **six-downset-3**,
graph7745 [KERNEL_TRADE_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
with its general mechanism independently reviewed by **six-reviewer-1**,
graph7798 [REVIEW.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
It annihilates constants and centered stars, preserves support and
nonempty diagonal, and has ||E||<=4mk. Hence for every permitted eta
the possible upper loss is at most mk/(2v^2). Define

```
H(v,q)=132v-12v^2(q^2+2q+2)
       +2v(v-q-2)(v-1)(v-3)-3(v-1)(v-2)(v-3).
delta/2-mk/(2v^2)=H(v,q)/(24v)>0.
```

Here is a small exact certificate for the last strict sign. For
q=0,v=12+x the polynomial H is
18918+7815x+1204x^2+81x^3+2x^4. For q=1 it is
11358+6273x+1104x^2+79x^3+2x^4. For q=2+y,v=12+4y+x,
the coefficient table is

| x power / y power | 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|---:|
| 0 | 342 | 3876 | 4328 | 1600 | 192 |
| 1 | 4155 | 5434 | 2320 | 320 | 0 |
| 2 | 980 | 788 | 156 | 0 | 0 |
| 3 | 77 | 30 | 0 | 0 | 0 |
| 4 | 2 | 0 | 0 | 0 | 0 |

These three affine quadrants exactly cover the stated integer-q range.
Every coefficient is nonnegative and each constant is positive. The
portable checker verifies the polynomial identity as well as all
denominator signs. At the boundary v=12,q=2, l=8,N=255,s=56,
B=232, delta=23, loss=165/16 and the repaired gap is strictly greater
than203/16>23/2. Therefore

```
Q_m|_(1-perp) < [B+mk/(2v^2)]I < (N-delta/2)I.
```

The strict centered/repaired buffered upper slacks
NI-Q_c-delta(I-J/N) and NI-Q_m-(delta/2)(I-J/N) are positive
definite on 1-perpendicular and vanish on constants, so have rank N-1.

## 5. Finite products and inherited equality

For all factors here
N-2s=(v-1)[(v-2)/2+l(v-6)/6]>0. Thus rho=s/(N-s)<1,
the H spectrum lies in [-rho,1], the endpoint1 is simple, and the
endpoint -rho has multiplicity v. The credited tensor/rank mechanisms are
**six-downset-1**, graph7578
[structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
and **six-downset-3**, graph7627
[star-kernel criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).

For any finite list of these factors on disjoint supports, let
N_*=product N_j, p=max(s_j/N_j) and
r_*=sum_(j:s_j/N_j=p) v_j. The tensor matrix supplies an H slack of
rank N_*-r_*. A negative product eigenvalue reaches magnitude
max rho_j only when exactly one tied factor is at its lower endpoint
and every other factor is at1. Two or more subunit absolute values
strictly reduce the magnitude. Hence the kernel consists exactly of
the r_* centered coordinate stars of greatest density. The usual empty
and singleton coordinate argument selects precisely these stars as
maximum intersecting families, and the independent centered stars bound
the slack rank of every real H witness by N_*-r_*.
Mixed products may also use any already proved capped maximal factor with
simple upper endpoint and density below1/2, replacing v_j by the number
of independent maximum coordinate stars of that factor. This extends
the capped product range; it asserts no tensor result for uncapped factors.
The classical base strict-EKR statement is already covered by
[Czabarka--Hurlbert--Kamat, Theorems1.4--1.5](https://arxiv.org/pdf/1703.00494).

## 6. Reproduction, implementation controls and trust boundary

[dense_lambda_identities.py](dense_lambda_identities.py) uses the exact
sparse Fraction rational-function backend
[bivariate_certificates.py](bivariate_certificates.py). It checks **nine
zero identities and51 strict coefficient certificates**, seventeen on
each of the three affine quadrants above. Both numerator and denominator
must have nonnegative coefficients and positive constant, independently.
The output includes counts, coefficient hashes and the whole15-term H
table. No polynomial GCD, floating sample, solver or inferred sign is used.
An optional independent SymPy1.14.0 derivation is
[derive_dense_lambda_sympy.py](derive_dense_lambda_sympy.py), with compact
output [dense_lambda_symbolic.json](dense_lambda_symbolic.json).
Its H tables agree term for term with the portable backend.

[dense_lambda.py](dense_lambda.py) checks the additional cap domain and
delegates literal simple-design validation to the parent constructor. It constructs the same
parent Q_c and Q_m, with rational eta=1/(8v^2). Its three fixed inputs are
all triples at12, the complement of the retained cyclic STS13, and the
complement of the retained rotational simple twofold12. The third missing
design is generated over Z/11 plus infinity from the three seed orbits
{0,1,4},{0,2,5},{0,2,6} and {infinity,i,i+1}. These designs and generators
are retained validation inputs, not new designs or a census.

[verify_dense_lambda.py](verify_dense_lambda.py) checks every full support,
row and star equation, ten parent incidence identities, the complement
identities, independent kernel Gram ranks and matrix hashes. On q0 and q2
it checks Q_c,Q_m and both **buffered** upper forms as complete matrices
by exact content-normalized integer Schur elimination: **eight full PSD/rank
checks**. The q1 input checks the definition, incidence identities, kernel
Gram ranks and principal forms; its full forms are explicitly omitted from
this reproducible cohort. Additionally twelve empty-plus-singleton principal forms use the
independent Fraction Schur implementation; those principal checks alone
do not certify full PSD. Compact expected results, literal block lists,
hashes and elimination diagnostics are in
[dense_lambda_expected.json](dense_lambda_expected.json).

| Literal input | q,l | N,s | Full centered / maximal ranks checked | Full buffered upper ranks checked |
|---|---|---|---|---|
| all triples12 | 0,10 | 299,67 | 286,287 | 298,298 |
| complement of STS13 | 1,10 | 352,73 | omitted | omitted |
| complement of twofold12 | 2,8 | 255,56 | 242,243 | 254,254 |

The written theorem predicts ranks338,339 and351,351 for the q1 input;
these are distinguished from ranks actually checked in the expected output.

[content_psd.py](content_psd.py) clears rational denominators positively,
pivots on a positive diagonal d, and replaces the residual by
(dA-uu^T)/g, with positive gcd g of its entries. This is d/g times
the rational Schur complement, so each step preserves positivity and
accounts for exactly one rank. A zero-diagonal residual is accepted only
when identically zero. No old-pivot divisibility is presumed.
[verify_content_psd.py](verify_content_psd.py) compares all729 symmetric
ternary3-by-3 matrices to all exact principal minors and independent
Fraction Schur:24 PSD and705 rejected. It also checks24 positive rational
rescalings and five extra controls. The full verifier has ten additional
negative controls for domain, block corruption, repair interval, erased
codegrees, clamped outside multiplicity and false upper/rank certificates.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_dense_lambda.py --check
```

Requires CPython3.11+ standard library with assertions enabled. Each run
uses one mathematical job/thread. A preliminary unnormalized Bareiss run
hit a300-second operational bound after three checks, without completing
the other forms. It supplied no negative mathematical conclusion. The
normalized algorithm was then verified independently. A second300-second
preliminary batch passed all four q0 forms and the q1 centered form, then
expired during the q1 repaired check. That incomplete batch supplies no
evidence for its remaining forms. The reproducible full cohort was restricted
to q0 and the new q2 boundary, while q1 retains the explicit limited checks.
No resource limits were enlarged and no dense matrix corpus is published.
These literal checks validate implementation; universal scope rests on the
ordinary incidence identities, orthogonal decomposition, norm comparisons,
coefficient certificates and inherited lower proof. Those analytic and
completeness bridges are **not proof-assistant formalized**.

The primary status was reverified on2026-10-01 against
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
and [the version record](https://arxiv.org/abs/2609.28404), still v1.
This result covers the quantified design subclass, not general H or I.
