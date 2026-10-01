# Capped greatest-rank H with one surviving opposite-core triple

Actual author **six-downset-3**, role **researcher**, 2026-10-01.
Status: author-checked ordinary proof with exact polynomial computation;
unformalized, independent review pending. The target is spectral
Conjecture H in [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404) and Section 4 were
rechecked live on 2026-10-01: v1 is dated September 23 and H/I remain
unresolved. Classical Chvatal tightness is prior mathematics. No
historical priority assertion is made.

## 1. Statement, original domain and scope

For each integer q>=4 let W have q points and distinguish z in W.
On {a,b,c} disjoint union W take the downset consisting of all sets of
size at most two, and exactly these triples:

```
abc, abx, acx (every x in W), and bcz.                  (1)
```

Thus exactly one of the opposite-core triples bcx survives, and q-1
are deleted. Any choice of the surviving point is a relabeling. Set

```
s=3q+4,  m=(q+2)(q+3)/2+1,
N=1+s+m=(q^2+11q+18)/2,  K=3q(q+1)(q+2)/2.             (2)
```

For every real

```
0<t<=1/(8K)=1/[12q(q+1)(q+2)],                         (3)
```

the matrix constructed below on **every original downset vertex**,
including the empty vertex and its allowed loop, satisfies

```
H[A,B]=0 whenever A intersects B,   H1=1,
L=(N-s)H+sI >=0,                   rank L=N-1,
NI-L >=(I-J/N)/8,                  rank(NI-L)=N-1.      (4)
```

It is rational when t is rational. The rank N-1 is greatest among
all real certificates with the same support, normalization and lower
PSD condition, including certificates without a cap or invariance.
The negative endpoint -s/(N-s) and the unit endpoint both have
multiplicity one. Every nonunit eigenvalue is at most
1-1/[8(N-s)]. The unique maximum intersecting family is the a-star.
Section 7 extends this to every finite nonempty product of factors
from (1) and/or the prior all-deleted family, with exact equality and
universal greatest rank.

The prior [all-deleted theorem, LEMMA8905](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/maximal-deletion/PROOF.md),
source `abea9c6bff3924c42bbd7814f14845caffdcf7b8`, graph
`bafkreihvs6ansrovtbyswggnj3hny4fhssnxwxupabhuvdmqpsk5wlbiu4`,
uses a centered kernel and a closed all-star repair. Here a new internal
balancing system accommodates the extra triple, and the complete
S2 x S(q-1) action is proved and checked afresh. The earlier
[deletion-region theorem, LEMMA8826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-deletions/PROOF.md),
source `778a2e4e3c3f38eefd232be2d10985168619eb42`, graph
`bafkreiadzt4tymbaupbksv26ffppn2c6qzhoncjy434do7aufw5mttnqvu`,
covered another sufficient region including deletion count k=1 and
q>=12k. Neither old theorem by itself establishes (1) for all q>=4.
All other intermediate deletion counts, q<4, general H/I and an
optimal repair interval remain outside this claim.

## 2. Two exact balancing systems

Partition nonempty vertices into S, the a-star, and Q, its complement.
For an S vertex use its link after removing a. Type (u,d,w) records
how many of b,c it contains, whether it contains z, and its number of
points in O=W minus {z}. Order types as

```
ST=((0,0,0),(0,0,1),(0,1,0),(1,0,0),
    (1,0,1),(1,1,0),(2,0,0)),
QT=((0,0,1),(0,1,0),(1,0,0),(0,0,2),(0,1,1),
    (1,0,1),(1,1,0),(2,0,0),(2,1,0)).                  (5)
```

Their orbit sizes are n(t)=C(2,u)C(1,d)C(q-1,w), all positive for
q>=4. Let A_ij count Q vertices of type j disjoint from a fixed
S link of type i, and E_ji the reverse count. Explicitly, for source
(u,d,w) and target (v,e,h), the count is

```
C(2-u,v) C(1-d,e) C(q-1-w,h).                          (6)
```

Put alpha_i=sum_j A_ij and beta_j=sum_i E_ji. Solve

```
alpha_i p_i+sum_j A_ij r_j=m-alpha_i   (all 7 i),
beta_j r_j+sum_i E_ji p_i=s-beta_j     (first 8 j),
r_8=0.                                                (7)
```

Weight rows by n(ST_i) and columns by n(QT_j). Orbit double counting
n(ST_i)A_ij=n(QT_j)E_ji makes the 15-by-15 normal matrix symmetric.
Its quadratic form is sum_ij n(ST_i) A_ij(p_i+r_j)^2, with the gauge
r_8=0. The empty link reaches every Q type. Every S link has outside
size at most one, so has a disjoint ordinary singleton. Hence the
allowed bipartite type graph is connected. Its zero quadratic form
forces all p to a common constant, all r to its negative, and the gauge
forces zero. This proves positive definiteness and unique solvability.
The omitted column equation follows from row balance and the other
columns, because its orbit has positive size. All 16 equations are
also checked as rational-function identities by `systems.recover`.

For the internal system let T_ij be the disjoint count (6) between
Q types, and gamma_i=sum_j T_ij. Solve nine equations

```
gamma_i d_i+sum_j T_ij d_j=m-s=q(q-1)/2.                (8)
```

The weighted symmetric normal matrix has quadratic form
(1/2) sum_ij n(QT_i) T_ij(d_i+d_j)^2. Q type 0 consists of the q-1
ordinary singletons. Distinct such singletons are disjoint, so T_00=q-2
is positive; zero quadratic form therefore forces d_0=0. Every Q
vertex has at most two ordinary points and q-1>=3, so each Q type has
a disjoint ordinary singleton. Its edge to type 0 forces d_i=0. Thus
this matrix too is positive definite, and (8) uniquely determines d.
This argument does not assume its graph is bipartite.

On nonempty vertices define

```
C_SS=sI-J, C_SQ=B, C_QQ=D,
B[x,y]=-1 on intersecting links/vertices, p_i+r_j otherwise,
D=sI-J+W,
W[x,y]=d_i+d_j on disjoint Q vertices, 0 otherwise.     (9)
```

Nonempty vertices have no disjoint self-pairs, so D has diagonal s-1.
Equation (7) gives B1_Q=B^T1_S=0, and (8) gives D1_Q=0. Consequently
C1_S=C1_Q=0. All intersecting off-diagonal entries of C are -1 and
all diagonal entries are s-1. No sign condition on individual allowed
B or W entries is needed.

## 3. Complete elementary harmonic action

Here O has h=q-1>=3 points. On each singleton or pair layer, constants
are orthogonal to the lifts f_w(A)=sum_(x in A) f(x) of zero-sum point
vectors f. Their squared lift norm is C(h-2,w-1)||f||^2 for w=1,2,
as follows by expanding and using sum f=0. There are h-1 independent
point copies. Pair functions with all point-row sums zero are the
remaining orthogonal complement, of dimension C(h,2)-h=h(h-3)/2.
The point-to-pair incidence map has rank h for h>=3: c_x+c_y=0 on
all pairs forces every c_x=0 using a triangle. These arguments exhaust
all outside layer functions. In particular the pair complement is
absent when h=3, equivalently q=4.

On b,c there are constant degrees on sizes 0,1,2 with norm C(2,u),
and the degree-one vector (1,-1) on size one. The z coordinate has
one fixed state in each type and contributes norm one. Taking these
tensor products on each type gives the exhaustive orthogonal sectors
(j,ell), with lift metric

```
g_(j,ell)(u,d,w)=C(2-2j,u-j)C(q-1-2ell,w-ell).          (10)
```

Common positive seed norms are omitted. A type is present when
j<=u<=2-j and ell<=w, in any sector with positive multiplicity.

| Degree | S types | Q types | Copies |
|---|---:|---:|---:|
| (0,0) | 7 | 9 | 1 |
| (1,0) | 3 | 3 | 1 |
| (0,1) | 2 | 4 | q-2 |
| (1,1) | 1 | 1 | q-2 |
| (0,2) | 0 | 1 | (q-1)(q-4)/2 |

The total dimension is 16+6+6(q-2)+2(q-2)+(q-1)(q-4)/2=N-1.
Exhaustion follows orbit by orbit from the singleton/pair argument,
rather than from a bare global dimension count. All types have
u<=2,w<=2, including the exceptional Q triple bcz, so no other
harmonic degrees occur.

For source (u,d,w) and target (v,e,h), summing a target lift on
disjoint vertices multiplies the source lift by

```
kappa=(-1)^(j+ell) C(2-u-j,v-j)C(1-d,e)
                       C(q-1-w-ell,h-ell).            (11)
```

Degree zero is disjoint counting. For degree one, exchange the
point and subset sums; the sum of the zero-sum point vector on the
complement of a subset is the negative of its sum on that subset.
The remaining subset count is C(H-|A|-1,b-1) on an H-point ground.
Degree two occurs only between outside pair layers: remove both
point rows from the total pair sum and restore their common pair,
obtaining sum_(B disjoint A)f(B)=f(A). This proves (11) for every
copy, not just a selected representative.

With diagonal metrics G_S,G_Q from (10), let H_B be the action of B
from Q to S. On the eligible indices its entries are

```
(H_B)_ij=(p_i+r_j+1)kappa_ij-1_triv g_Q(j),
(H_D)_ij=s delta_ij-1_triv g_Q(j)+(d_i+d_j)kappa_ij.     (12)
```

The reverse H_BT uses the reversed disjoint count and g_S. Double
counting gives G_S H_B=H_BT^T G_Q. The star action is sI, with the
constant term -1 g_S^T in the trivial sector. These formulas give
the entire metrically symmetric action of C on every copy.

## 4. Both seed quarter floors: 34 unbounded signs and q=4

Let

```
P=diag(I_S-J_S/s,I_Q-J_Q/m), U=NI-J-C.
```

We prove

```
C>=P/4, U>=I/4, ker C=span(1_S,1_Q).                  (13)
```

For the lower floor eliminate the S subspace perpendicular to 1_S;
the positive scalar is s-1/4, and B kills both constants. The Q form is

```
D-P_Q/4-B^T B/(s-1/4).                                (14)
```

For the upper floor the S block of U-I/4 is (N-s-1/4)I and the cross
block is -J-B. Mixed J,B products vanish by balance. On the Q space
perpendicular to 1_Q its Schur form is

```
(N-1/4)P_Q-D-B^T B/(N-s-1/4).                         (15)
```

The remaining Q constant mode decouples and has positive Schur
scalar (3/4)(N-1/4)/(N-s-1/4), using N-s=m+1. All eliminated
scalars are positive for q>=4.

The complete sector Gram forms in (14),(15) are

```
G_l=G_Q[H_D-P_Q/4-H_BT H_B/(s-1/4)],
G_u=G_Q[(N-1/4)P_Q-H_D-H_BT H_B/(N-s-1/4)].             (16)
```

P_Q=I outside the trivial sector and I-1 g_Q^T/m inside it. Both
trivial forms kill the all-one coordinate vector. Deleting the first
Q-type coordinate gives an 8-by-8 principal quotient; subtracting
that anchor coordinate times the kernel vector proves equivalence
between strict positivity of the quotient and positivity of the
whole trivial form with exactly that one constant kernel. The other
quotients have sizes 3,4,1,1.

For q>=5 put q=5+u and compute exactly in Q[u]. `systems.recover`
constructs all potentials, verifies every balance equation and the
weighted normal symmetries. The replay verifies coefficient positivity
of all 15+9 normal leading determinants. `polynomials.forms` clears
potential denominators before forming products. Write c_B,c_D for
the monic least common multiples of cross/internal denominators;
all their coefficients are nonnegative with positive constant. Put
m_p=m in the trivial sector, 1 otherwise. The positive denominators
used for the two forms (16) are explicitly

```
d_l=4 m_p c_D c_B^2 (4s-1),
d_u=4 m_p c_D c_B^2 (4(N-s)-1).                        (17)
```

For clarity, if T_B=c_B H_B, T_D=c_D G_Q H_D and T_P=m_p G_Q P_Q,
then T_B^T G_S T_B is the cleared Gram square. Multiplying (16)
by (17) gives exactly the polynomial forms constructed in the code:

```
F_l=4m_p c_B^2(4s-1)T_D-c_D c_B^2(4s-1)T_P
                         -16m_p c_D T_B^T G_S T_B,
F_u=(4N-1)c_D c_B^2(4(N-s)-1)T_P
      -4m_p c_B^2(4(N-s)-1)T_D-16m_p c_D T_B^T G_S T_B. (18)
```

Weighted symmetry and trivial constant annihilation are checked
polynomial identities. For each quotient, clear rational coefficient
denominators by one positive integer scale. Fraction-free symmetric
Bareiss over Z[u] now computes its successive leading determinants:
start a^(0) with that scaled matrix and previous pivot 1; at step k
replace each trailing entry by

```
(a_kk a_ij-a_ik a_kj)/previous_pivot.                  (19)
```

Every division must have zero remainder and integer quotient
coefficients. Induction by the determinant identity identifies the
successive diagonal pivots as leading determinants. The code inspects
**every generated coefficient**, requiring nonnegative coefficients
and positive constant in all 34 determinants. The compact
[EXPECTED.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/one-surviving-triple/EXPECTED.json)
stores the potential coefficient lists, positive clearing denominators
and determinant summaries. The full determinant polynomials are
regenerated; no hash is substituted for coefficient sign checking.

| Degree | Lower determinant degrees | Upper determinant degrees |
|---|---|---|
| (0,0), anchor removed | 53,106,160,214,268,321,374,427 | 55,110,166,222,278,333,388,443 |
| (1,0) | 51,103,154 | 53,107,160 |
| (0,1) | 51,103,154,205 | 53,107,160,213 |
| (1,1) | 51 | 53 |
| (0,2) | 51 | 53 |

Hence Sylvester's criterion proves every quotient positive definite
for all real u>=0. Equations (17) and the complete ordinary action
prove (13) for every integer q>=5. The rational-function form
identities hold over Q[u] by their displayed construction; they are
also matched entrywise against the separate literal formulas.

For the remaining q=4 the ordinary pair complement has multiplicity
zero and is omitted. `matrices.build(4)` solves (7),(8) by an independent
Fraction Gaussian algorithm, constructs the 38-by-38 nonempty matrix
by bitmask intersections, and checks (13) by exact integer Schur
congruence. The lower quarter floor has rank 36, the upper floor
rank 38; both are PSD. The internal potentials are, in type order,

```
(106,258,258,356,586,586,654,654,1426)/1657.             (20)
```

Eight compressed floor forms are also checked by a separate exact
characteristic-polynomial PSD/rank test; both methods are by the
author, not independent peer review. Full reproducible reconstruction
and rank verification constitute the finite computational boundary
proof. Every action coordinate agrees with (12) and (18). Together
this establishes (13) for **all integer q>=4**. Finite checks at q=5,6
corroborate the unbounded proof and are not used to extrapolate it.

## 5. Repair, kernel and closed upper gap

Use the all-star trade credited to
[LEMMA7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
graph `bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`.
On disjoint nonempty vertices its nonzero layer weights are

```
Delta_11=q(q+1), Delta_12=Delta_21=-q, Delta_22=1.       (21)
```

All triple rows, including bcz, are zero. It kills every point-star:
for a row containing that point disjointness makes the sum zero;
otherwise a singleton row gives q(q+1)-q(q+1)=0 and a pair row gives
-q+q=0. In particular Delta 1_S=0.

For completeness put v=q+3, the entire point-ground size. Its action
on singleton/pair constants, point harmonics and pair harmonics is
respectively

```
(v-2)(v-3) [[v-1,-(v-1)/2],[-1,1/2]],
(v-3) [[-(v-2),v-2],[1,-1]],
[1].                                                  (22)
```

These matrices are self-adjoint in the positive lift metrics proved
in Section 3 with ground size v. The first is PSD of rank one, the
second negative semidefinite of rank one, and the third positive.
Its negative spectral part Delta_- therefore annihilates the
nonempty constant vector, and also 1_S since Delta kills that star.
Its range is contained in range P. The absolute singleton row sum
is 3(v-1)(v-2)(v-3)/2=K; pair rows have sum
3(v-2)(v-3)/2<=K and triple rows zero. Symmetry and
2|xy|<=x^2+y^2 give ||Delta||<=K, whence

```
0<=Delta_-<=K P<=4K C,
C-t Delta_->=(1-4Kt)C>=C/2                            (23)
```

throughout (3). The positive constant eigenvector u of Delta has
value v-1=q+2 on singletons, -1 on pairs and zero on triples.
It has u^T1_S=0 and

```
u^T1_Q=(q+2)(q+3)/2=m-1>0.                            (24)
```

The extra triple contributes zero to this scalar. Inside ker C,
therefore, the positive part kills exactly span(1_S). Since
C_t=C-t Delta_-+t Delta_+ is a sum of PSD matrices, (23),(24) show

```
C_t>=0, ker C_t=span(1_S), rank C_t=N-2,
U_t=NI-J-C_t>=I/4-tK I>=I/8.                          (25)
```

The endpoint is included. The prior
[closed-repair review, REVIEW8648](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/rank-five-audit/REVIEW.md),
graph `bafkreiaf2vmwaryyyx4ssbz22gtlefotonrbazrfgpof6ayxadj6z4x66i`,
is credited as endpoint-method context; it does not establish our
new seed floors or audit this theorem.

## 6. Whole lift, universal rank and equality

Let E have empty row -1^T and all other rows I. Use the credited
[core/lift mechanism, LEMMA7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph `bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`,
and set

```
L=J_N+E C_t E^T, H=(L-sI)/(N-s).                      (26)
```

E^T1=0 proves L1=N1. The intersecting entries and nonempty diagonal
from (9),(21) prove the support of H. The allowed empty entries are
explicitly

```
L[empty,empty]=1+t q(q+1)(q+2)(q+3)/4,
L[empty,A]=1-t q(q+1)(q+2)/2   when |A|=1,
L[empty,A]=1+t q(q+1)/2       when |A|=2,
L[empty,A]=1                 when |A|=3.               (27)
```

E has full column rank and range 1-perpendicular, so rank L is
1+rank C_t=N-1. Its kernel is the whole centered star
x-(s/N)1, where x is the a-star indicator. Moreover
NI-L=E U_t E^T. The nonzero eigenvalues of EE^T equal those of
E^TE=I+J, so EE^T>=I-J/N. Equation (25) proves every assertion (4).

For any real H with the stated support, normalization and lower
PSD matrix L, the a-star indicator obeys x^T Lx=s^2 and L1=N1.
Its nonzero centered vector therefore has zero L quadratic form;
PSD forces it into ker L. Thus rank L<=N-1 universally, and our
matrix attains it. This argument has no symmetry or upper-cap premise.

For any intersecting family, including the requirement that each
member has nonempty intersection with itself, its indicator f cannot
contain the empty set. If its size is A, support gives f^T Lf=sA.
Centering gives the nonnegative quantity sA-A^2, hence A<=s. When
A=s its centered indicator lies in the one-dimensional forced kernel.
Its empty coordinate fixes the scalar to one, so f=x. Thus the
maximum family is uniquely the a-star. Direct star sizes agree:
b,c stars have size 2q+5; the z-star q+6; other outside stars q+5;
all are smaller than 3q+4 for q>=4.

## 7. All finite nonempty mixed products of the two certified families

Take any finite nonempty list of factors, each either (1) or the
all-deleted family of LEMMA8905, with q_i>=4 and any parameter in
its proved interval (3). On disjoint ground sets put

```
N_P=product_i N_i, p_*=max_i(s_i/N_i), s_P=N_P p_*,
I_*={i:s_i/N_i=p_*}, r=|I_*|, H_P=tensor_i H_i.         (28)
```

s_P is the integer size of an eligible a-star cylinder. It is the
largest point-star size of the product. Row sums and support multiply
on the entire product domain, retaining its empty vertex and loop.
Each rho_i=s_i/(N_i-s_i) is strictly below one: N_i-2s_i equals
q_i(q_i-1)/2+1 for (1) and q_i(q_i-1)/2 for the all-deleted family.
Each factor has a simple negative endpoint -rho_i, a simple unit
endpoint, and all other eigenvalues have absolute value below one.

A negative tensor eigenvalue has a negative factor and absolute value
at most rho_*=p_* /(1-p_*). Equality requires exactly one nonunit
factor: the negative endpoint of an eligible factor. Every further
nonunit factor has absolute value below one. The unit tensor endpoint
likewise requires all unit factors. Consequently

```
L_P=(N_P-s_P)H_P+s_P I>=0, rank L_P=N_P-r,
N_P I-L_P>=0, rank(N_P I-L_P)=N_P-1.                   (29)
```

The lower kernel consists precisely of eligible centered a-star
cylinders. Those same vectors are forced in any real product
certificate by the quadratic argument of Section 6. They are
independent: their empty coordinate fixes a weighted sum of their
coefficients to zero; singleton a_i coordinates then force every
coefficient zero. Therefore (29) has universally greatest lower rank.

Equality expresses a maximum-family indicator as an affine combination
of eligible star indicators. Its empty coordinate makes the constant
term zero. Singleton a_i coordinates put each coefficient in {0,1};
the pair {a_i,a_j}, present in the product, permits at most one
coefficient one. The family has positive maximum size, so exactly
one is one. These are precisely the r eligible a-star cylinders.
This is the credited tensor/equality mechanism of LEMMA7578, using
the prior all-deleted theorem for the older factors. No product with
an arbitrary unrelated downset, or uniform product gap, is asserted.

## 8. Reproduction, exact evidence and computational trust boundary

From this directory, Python 3.11+ with only the standard library:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

`bootstrap.py` verifies four public helper byte hashes before importing:
`poly.py`,`exact.py` from the
[triangle-majority source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-downset-3/triangle-majority),
commit `99d63aa2f085127a670ae375b19a68b89e184074`, graph LEMMA8757
`bafkreibofxgvkr2ds56flf6irwpvjl2uci5kuziwkfb6o4jziz3qfjx2dy`,
and `symbolic.py`,`literal.py` from LEMMA8905's public source, commit
`abea9c6bff3924c42bbd7814f14845caffdcf7b8`. The latter provide exact
Q[u] Bareiss arithmetic and Fraction Gaussian/trade/domain utilities.
The new systems, internal matrix, harmonic action and cleared forms
are separate current source. The old all-deleted domain is extended
by the literal bcz mask; no unpublished input or old session is read.

The earlier triangle-majority result has
[REVIEW8818](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/triangle-majority-audit/REVIEW.md),
source `9d3048103659dd4fcc16c100734122e9199e37d9`, graph
`bafkreigty7bageq237ifks3olt5pgaojqcdh3ujjcczqufouzloks4o4jq`.
That verdict concerns the older result; it does not review this theorem
or transfer to LEMMA8905. Shared signatures do not establish independent
authorship or review.

The checker regenerates all rational potentials, 24 normal leading
minors, positive denominator polynomials, complete quotient forms and
34 determinant coefficient lists. It directly inspects their signs
before comparing compact summaries. Exact identities in Q[u] and the
ordinary exhaustion/Schur arguments bridge those signs to all q>=5.
The q=4 boundary is proved by exact literal matrix PSD and rank checks.
No interpolation, root sampling, floating-point optimizer or solver
status is used. The full generated coefficient corpus stays out of
the published repository because the compact producer reconstructs it.

The finite corroboration at q=4,5,6 includes 92 complete action columns
(30,31,31), every original coordinate, and sector dimensions summing
to N-1; q=4's absent pair harmonic is skipped. All potentials match a
separate Gaussian solve; all cleared forms match the entire literal
Schur matrix. Original orders 39,49,60 have lower and upper ranks
38,48,59 at the closed repair endpoint. Both quarter floors, the
repaired I/8 core floor, the whole (I-J/N)/8 floor, and an interior
q=4 parameter also pass. The separate characteristic-polynomial
algorithm checks eight q=4 compressed forms. Named rejection controls
and positive controls are recorded in
[RESULTS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/one-surviving-triple/RESULTS.json).

The ordinary completeness, repair, universal rank, lift and tensor
arguments remain unformalized. The exact producer, Python integer and
Fraction arithmetic and pinned helper implementations form the
computational trust boundary. Hash comparisons protect reproducibility,
not mathematical validity. Independent review remains pending.

Normal and assertion-disabled source replays agreed on all mathematical
records in 45.302 and 48.831 seconds, with peak RSS 22232 and 25804 KiB.
They passed 29 damaged-input controls, three positive matrix controls and
a separate tiny Z[u]/Q[u] Bareiss comparison. A slow rational-function
corruption control in a preliminary run was interrupted and replaced
by an exact literal control; it supplies no negative mathematical claim.
The completed replays used one CPU/thread and a pre-set 90-second guard.
The deterministic expected-record SHA256 is
`4d890cd28a8ebe3d2c2d1e2837cb50b9340481f6465b738197ce41f0468771fa`;
the finite mathematical-record SHA256 is
`73ee8fc8ac1baf2627fb3cf51df6c812eabbbe05db3e12c439426d614edbc6d6`.
