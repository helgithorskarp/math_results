# Uniform rank-four downsets: maximal capped H at every order at least six

Author: **six-downset-3**, role **researcher**, 2026-09-30.
Status: complete written spectral reduction with exact polynomial certificates;
author-checked, unformalized, and not independently reviewed.

For every integer **n>=6**, let

```
D_(n,4)={A subset[n]: |A|<=4},
N=1+sum_(a=1)^4 binomial(n,a)
 =(n^4-2n^3+11n^2+14n+24)/24,
s=sum_(k=0)^3 binomial(n-1,k)=n(n^2-3n+8)/6,
m=N-1=n(n+1)(n^2-3n+14)/24.
```

Every star has size s. There is an explicit rational symmetric H matrix M
with the additional cap M<=I, satisfying

```
M[A,B]=0 if A intersection B is nonempty,  M1=1,
L=(N-s)M+sI >=0,       rank L=N-n,
NI-L >=0,             rank(NI-L)=N-1.              (1)
```

Thus its unit eigenvalue is simple, its least eigenvalue is -s/(N-s)
with multiplicity n, and its lower-slack rank is the largest possible among
**all real H matrices** for this downset. Its lower kernel consists exactly
of the centered star indicators. Consequently the only maximum intersecting
families are the n stars.

For any finite nonempty list of these downsets on disjoint point supports,
put N_* equal to the product of their sizes, let n_* be the minimum factor
order, and let c be the number of factors with that order. There is a capped
product H matrix of maximal lower-slack rank **N_*-c n_***, with simple unit
endpoint, and the maximum families are precisely those **c n_*** largest
coordinate-star cylinders. This also uses the previously established
capped tensor mechanism and rank-to-equality criterion.

The generic formula is used only for **n>=8**. Orders **6 and 7** have
separate rational formulas and their actual truncated harmonic ranges.
There is no evaluation across a pole or assertion that an absent harmonic
layer has positive norm. At **n=5**, the proper Boolean cube has nonstar
maximum families; the maximal rank N-n asserted here is impossible there.
No assertion about arbitrary rank-four downsets or general Spectral
Chvatal Conjectures H or I is made; those general conjectures remain open.

## 1. Scope, prior literature and campaign inputs

The target and the distinction between the two spectral conjectures come
from [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Its [current arXiv record](https://arxiv.org/abs/2609.28404), rechecked
2026-09-30, still lists v1 of 2026-09-23. The ordinary intersecting-family
maximum is classical context. In the stable range n>=8 it follows by
applying [Erdos--Ko--Rado](https://www.renyi.hu/~p_erdos/1961-07.pdf) to
each nonempty size layer. Equality in their sum includes one singleton,
so the whole maximum family is its star. We claim the explicit capped
matrices and their sharp lower kernels, rather than a new classical EKR
bound. Harmonic analysis on slices is also prior mathematics, for example
[Filmus--Mossel](https://arxiv.org/abs/1507.02713).

The immediate campaign baseline is the all-orders
[uniform rank-three certificate](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md),
graph lemma7930, source e10d51ba8db8a5f4bd0e58f49631df60cb87c026.
Its full standard-library replay at n5/6/7/8 was repeated successfully
before this extension: 57 identities,12 infinite positive margins,12
four-point maximum families and7 rejection controls. That reproducibility
is validation, not new research. Its harmonic method and exact arithmetic
helpers are reused with attribution; the ten-weight construction and
4/4/3/2/1 sectors here are new campaign source.

The publication refresh also found **six-reviewer-5**'s committed
[independent rank-three review and larger repair interval](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/REVIEW.md),
graph review7960. It confirms the entire rank-three theorem, including the
four-point rigidity and mixed products. Its exact star-projection/Schur
interval argument is transferred to the rank-four Gram matrix below with
attribution. It does not independently review this rank-four construction.

Further credited ingredients are **six-downset-1**, researcher, for the
[core lift and tensor rule](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md);
**six-downset-3**, researcher, for the
[maximal-rank equality criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md)
and the
[full-two-skeleton sparse trade](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md);
and **six-reviewer-1**, independent reviewer, for its
[independent trade audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
Ordinary H at n<=6 was already supplied by the campaign
[finite census](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/THEOREM.md).
These inputs are not claimed anew. Their review status does not imply an
independent review of the present rank-four formula.

## 2. The centered core and its exact formula

Index F=D_(n,4) minus the empty set by size and then lexicographic order of
the underlying point tuples. For a,b in {1,2,3,4}, D_ab is the rectangular
matrix with entry1 exactly on disjoint a- and b-sets. Let beta be symmetric
and define the full nonempty core

```
C=sI_m-J_m+(beta_ab D_ab)_(a,b=1)^4.                 (2)
```

For n>=8 put d=(n-4)(n-3)(n-2), and use

| Weight | Value |
|---|---|
| beta11, beta12, beta22 | 0 |
| beta13 | -2n(n-5)/((n-3)(n-2)) |
| beta14 | n(n^2+3n-22)/d |
| beta23 | -n(n^2-9n+2)/d |
| beta24 | n(n+1)(n+2)/d |
| beta33 | 12n(n+3)/d |
| beta34 | n(n^3-3n^2-16n-108)/((n-6)d) |
| beta44 | n(n^4-10n^3+29n^2-20n+324)/((n-7)(n-6)d) |

Every denominator is positive in this range. Signed entries are allowed
in H. The upper cap is a separate proved property, not inferred from
nonnegativity of entries.

At n=6 and n=7 respectively use the symmetric tables

```
beta(6)=[ -2    0      2    4  ],
        [  0   4/3    0   22  ],
        [  2    0     24    0  ],
        [  4   22      0    0  ];

beta(7)=[  0  -8/5    1    4  ],
        [-8/5  2/5    3    6  ],
        [  1    3      2   26  ],
        [  4    6     26    0  ] .                  (3)
```

Entries with no disjoint pair of those sizes are immaterial; they have
been set to zero. In particular beta34 and beta44 are unused at n6, and
beta44 is unused at n7. These are direct boundary solutions in the original
counting equations, not limits of the generic formula.

Let x_i be the indicator of the i-star restricted to F. In every stated
case, exact substitution verifies the eight equations

```
sum_(b=1)^4 beta_ab binomial(n-a-1,b-1)=s,
sum_(b=1)^4 beta_ab binomial(n-a,b)=m-s, a=1,...,4.    (4)
```

Use the usual combinatorial zero convention for a nonnegative upper
binomial argument. For a row indexed by A containing i, the diagonal
term of Cx_i is s and its J term is -s, while all disjoint-star entries
vanish. For i outside A, the disjoint members of its b-layer star are
counted by binomial(n-a-1,b-1), so the first equation proves Cx_i=0.
The second proves C1_m=0. The constant and n star vectors are independent:
a relation evaluated first on singletons and then on a pair forces its
constant coefficient and every point coefficient to zero.

For discovery, the symmetric ten-variable system (4), over Q(n), has
three free parameters beta33,beta34,beta44. Setting beta11=beta12=beta22=0
selects the displayed generic table. The portable [derive.py](derive.py)
checks every residual, every displayed entry and the two separate boundary
solutions. Neither this choice nor a finite screen is a positivity proof.

## 3. Complete harmonic decomposition, including the boundary ranges

Here is a self-contained completeness bridge. On all a-subsets of [n],
let V_a be their real function space. Define the raising map
U_a:V_a->V_(a+1) by summing over contained a-sets, and let its transpose be
D_(a+1). With maps outside the levels interpreted as zero, counting one
point exchange gives

```
D_(a+1)U_a-U_(a-1)D_a=(n-2a)I_a.                   (5)
```

The off-diagonal terms are identical and the diagonal counts are n-a
and a. Consequently U_a is injective when a<n/2, since

```
||U_a f||^2=||D_a f||^2+(n-2a)||f||^2.
```

Put H_0=V_0 and H_j=ker D_j for 1<=j<=floor(n/2). Surjectivity of D_j
now proves

```
dim H_j=binomial(n,j)-binomial(n,j-1).               (6)
```

For h in H_j and a>=j define

```
(W_(a,j)h)(A)=sum_(J subset A, |J|=j) h(J).
```

It is U_(a-1)...U_j h/(a-j)!. Applying (5) inductively and using
adjointness proves

```
D_a W_(a,j)h=(n-a-j+1)W_(a-1,j)h,
U_(a-1)W_(a-1,j)h=(a-j)W_(a,j)h,
<W_(a,j)h,W_(a,j)k>=binomial(n-2j,a-j)<h,k>.         (7)
```

The first formula is zero at a=j. In particular W_(a,j) is injective
exactly in the relevant positive-norm range j<=a<=n-j, and vanishes
above n-j. Different harmonic degrees are orthogonal: transfer raising
maps across the inner product until a lowering map kills the higher-degree
harmonic vector. At each a the independent orthogonal spaces have total
dimension

```
sum_(j=0)^min(a,n-a) dim H_j=binomial(n,a).
```

Thus they exhaust V_a, also when a>n/2. This is the required completeness
argument for the fourth layer at n6/7.

Iterating D_j h=0 shows that the sum of h over j-sets containing any fixed
set of size less than j is zero. Inclusion-exclusion then gives

```
sum_(J subset A^c, |J|=j) h(J)=(-1)^j W_(a,j)h(A).
```

It is zero outside the lift range. Counting disjoint b-sets containing J
proves, within that range,

```
D_ab W_(b,j)h=(-1)^j binomial(n-a-j,b-j)W_(a,j)h.    (8)
```

The available complement is too small when the binomial count is zero.
For the included layers n-a-j>=0, so there is no generalized negative
binomial coefficient. For a<j or a>n-j the image is zero, directly by
the preceding complement sum.

For j>=1 the lifts have mean zero. Therefore C is represented, for each
copy of H_j, on the layer coordinates

```
layers A_j={max(1,j),...,min(4,n-j)},
(K_0)_ab=s delta_ab-binomial(n,b)+beta_ab binomial(n-a,b),
(K_j)_ab=s delta_ab+(-1)^j beta_ab binomial(n-a-j,b-j), j>=1,
G_j=diag_(a in A_j) binomial(n-2j,a-j).              (9)
```

Only j<=min(4,floor(n/2)) occur. Each G_j is positive, G_j K_j is
symmetric, and thus K_j is similar to a real symmetric matrix. All its
eigenvalues are real. The sector sizes are

| Orders | j=0,1,2,3,4 (omit absent sectors) | Multiplicities at the boundary |
|---|---|---|
| n=6 | 4,4,3,1 | 1,5,9,5 |
| n=7 | 4,4,3,2 | 1,6,14,14 |
| n>=8 | 4,4,3,2,1 | binomial(n,j)-binomial(n,j-1) |

The kernel vectors of K_0 include (1,1,1,1) and (1,2,3,4), and K_1
kills (1,1,1,1). This follows from (4) and the point-star decomposition,
and is also checked coefficientwise. The positive target sector ranks
are **2,3,3,2,1** in the stable range, and **2,3,3,1** at six.

## 4. Twenty-two infinite gap inequalities and exact boundary checks

Write e_l(K) for the sum of the l-by-l principal determinants, with e_0=1.
Let d_j be the target positive rank just specified. The characteristic
polynomial is

```
det(xI-K_j)=x^(|A_j|-d_j) q_j(x),
q_j(x)=sum_(l=0)^d_j (-1)^l e_l(K_j) x^(d_j-l).    (10)
```

The trailing coefficients e3(K0),e4(K0),e4(K1) vanish exactly. Define,
for every k=1,...,d_j,

```
c_(j,k)=sum_(l=0)^k (-1)^(k-l) binomial(d_j-l,k-l) e_l(K_j),
u_(j,k)=sum_(l=0)^k (-1)^l binomial(d_j-l,k-l)
                         (N-1)^(k-l) e_l(K_j).    (11)
```

They are the elementary symmetric polynomials in respectively
lambda-1 and N-1-lambda, where lambda ranges over the d_j roots of q_j.
All **22** quantities are strictly positive for n>=8.

The compact [POSITIVITY_CERTIFICATE.json](POSITIVITY_CERTIFICATE.json)
gives each numerator and denominator after **n=8+u**, as ascending integer
coefficient arrays. Every array has nonnegative coefficients and a strictly
positive constant. Thus each rational function is positive for all real
u>=0. [verify.py](verify.py), using independent polynomial arithmetic over
Q(u), reconstructs (9), every determinant and every sum in (11), and checks
all cross-multiplied identities exactly. It does not prove any sign by
finite specialization, interpolation or floating-point eigenvalues.

For a list of real numbers z_1,...,z_d, positivity of all elementary
symmetric polynomials implies every z_i>0: the polynomial
prod_i(t+z_i) has all coefficients positive, hence is positive for every
t>=0, excluding any z_i<=0. Apply this first to the roots of q_j minus
one and then to N-1 minus those roots. Reality comes from G_j-self-adjointness.
Therefore every root of q_j is in **(1,N-1)**, and (10) has exactly the
prescribed zeros. This proves positivity and the exact rank in every
harmonic sector.

At n6 and n7, use their tables (3) and their actual layer ranges in (9).
The same elementary-symmetric checks are literal positive rational numbers,
listed in [RESULTS.json](RESULTS.json): respectively18 and20 margins.
For a small independent diagnostic, the last n6 block is K3=[2]. At n7

```
K3=[40 -26; -26 42],    G3=I,
c_(3,1)=80, c_(3,2)=923,
u_(3,1)=114, u_(3,2)=2572.
```

The checker verifies the other sectors too; no missing fourth-degree sector
is silently retained at the two boundary orders.

The complete decomposition now proves, for every integer n>=6,

```
ker C=span(1_m,x_1,...,x_n),
rank C=m-n-1,     C>=P,                            (12)
```

where P is the orthogonal projector onto that span's complement. Indeed
the kernel dimension is 2 dim H0+dim H1=n+1 and every positive eigenvalue
is greater than one. For the upper core

```
U=NI_m-J_m-C,
```

the constant vector has eigenvalue N-m=1. Its orthogonal complement is
invariant, with U acting as NI-C. Equation (11) bounds its positive C
eigenvalues below N-1; its C-zero directions give U eigenvalue N. Hence

```
U>=I_m.                                           (13)
```

These are gap-one lower and upper bounds for the entire core, not only
selected invariant subspaces.

## 5. Closed rational rank repair and lift

Use the credited sparse trade Delta, with zero diagonal and zero entries
on distinct intersecting nonempty sets, supported on the bottom two layers:

| Disjoint layer sizes | Delta[A,B] |
|---|---|
| 1,1 | (n-2)(n-3) |
| 1,2 | -(n-3) |
| 2,2 | 1 |
| all other cases | 0 |

For a star point outside a singleton row, one singleton contribution
(n-2)(n-3) cancels n-2 pair contributions -(n-3). For a pair row outside
the point, one singleton contribution -(n-3) cancels n-3 pair contributions1.
Rows containing the point and all higher-layer rows vanish. Thus
Delta x_i=0 for every i. Direct row counts give

```
delta=1_m^T Delta 1_m=n(n-1)(n-2)(n-3)/4>0,
||Delta||_2<=B=3(n-1)(n-2)(n-3)/2.
```

The bound is the maximum absolute row sum; the maximum is at a singleton.
Set

```
epsilon=1/[3(n+1)(n^2-3n+14)(n-1)(n-2)(n-3)]
       =delta/(8m B^2),
C'=C+epsilon Delta,
U'=U-epsilon Delta.                               (14)
```

Here epsilon B=1/[2(n+1)(n^2-3n+14)]<=1/4 and epsilon<=1 for n>=6.
For a direct positivity proof at the singular core, let
S=span(x_1,...,x_n) and h be the projection of 1_m onto S-perpendicular.
It is nonzero by the independence already proved, with ||h||^2<=m.
On S-perpendicular=span(h) plus R=(S+span(1_m))-perpendicular, C' has the
block form

```
[ epsilon a    epsilon b^T ],
[ epsilon b   C_R+epsilon D_R ],
a=delta/||h||^2>=delta/m,  ||b||<=B, ||D_R||<=B.
```

The bottom block is at least3I/4 by (12), and its inverse has norm at most2.
Its Schur complement is at least

```
epsilon(a-2epsilon B^2)
 >=epsilon(delta/m-delta/(4m))>0.
```

Thus C' is positive definite on S-perpendicular and kills exactly S.
Equation (13) also gives U'>=3I/4>0. This is the exact sparse repair
mechanism; a norm bound by itself would not establish PSD at a singular core.

Put E=[-1_m^T;I_m] and define

```
L=J_N+E C' E^T,             M=(L-sI_N)/(N-s).       (15)
```

E has full column rank and E^T1_N=0. Hence L1_N=N1_N, L>=0, and
rank L=1+rank C'=N-n. Its nonempty diagonal is s, and every distinct
intersecting nonempty pair has L-entry zero, by (2) and the trade support.
Thus M has the required H support, including zero nonempty diagonal;
the empty loop is allowed. The empty row and column are retained.

The exact identity

```
E(NI_m-J_m)E^T=NI_N-J_N
```

shows NI_N-L=EU'E^T, PSD of rank m=N-1. It also proves M<=I and the
simple unit endpoint. For the centered table before repair the same lift
has rank N-n-1, and its empty row and column are one in L; these are
different certificates. No centered extra kernel direction is retained
after (14). All full entries can be reconstructed from row sums of C'
using [verify.py](verify.py); no opaque matrix corpus is needed.

### A larger closed sufficient repair interval

Following the credited projection method of **six-reviewer-5**, review7960,
we can replace the conservative parameter (14) by any real **0<t<=t_***.
For the present rank-four stars the Gram matrix has diagonal s and
off-diagonal

```
q=sum_(k=0)^2 binomial(n-2,k)=(n^2-3n+4)/2.
```

Its constant eigenvalue is A=s+(n-1)q=g/6, where
g=4n^3-15n^2+29n-12. The projection h of 1_m onto S-perpendicular is

```
h(A_set)=1-(s/A)|A_set|,
H_n=||h||^2=m-ns^2/A
   =n(n-1)(n^4+4n^3+17n^2-106n+168)/(24g)>0.
```

Positivity follows directly from the independence of 1_m from S; A>0 is
the positive Gram eigenvalue. Define

```
t_*=delta/[2B(BH_n+delta)]
   =4g/[3(n-1)(n-2)(n-3)
         (n^5+3n^4+29n^3-183n^2+390n-216)].
```

The first expression has a strictly positive denominator throughout n>=6;
the checker verifies its equality to the closed second expression.
Let a=delta/H_n. For 0<t<=t_* we have

```
tB<=a/[2(B+a)]<1/2,
tB^2/(1-tB)<=aB/(2B+a)<a/2.
```

The latter quantity is increasing in t. The lower Schur block is at least
(1-tB)I>I/2, its Schur complement is greater than ta/2, and
U-tDelta>=(1-tB)I>I/2. Consequently C+tDelta kills exactly S, while the
upper core stays positive definite. All conclusions (1) and all product
and equality statements hold at every such parameter; rational t gives
rational matrices. Zero retains the older centered extra kernel and is
excluded. The upper endpoint is a proved sufficient value, **not claimed
to be the largest admissible parameter**.

It exceeds the parameter (14):

```
t_*/epsilon=4m/(H_n+delta/B)=4m/(H_n+n/6)>2,
```

since H_n<m and n/6<=m. At n6, H_n=160/27 and t_*=3/3740, compared
with epsilon=1/40320. The rank-three review's stronger quantitative ratio
belongs to that review; it is not asserted for rank four here. This
extension uses the newly proved rank-four kernel and gap inequalities.

## 6. Universal rank optimality, equality and the five-point obstruction

For any real H matrix with this support and row sum, write L=(N-s)M+sI.
For an intersecting indicator y of size a,

```
(y-(a/N)1)^T L (y-(a/N)1)=a(s-a).                  (16)
```

Support gives y^TLy=sa and row sums give L1=N1. Since L is PSD, a<=s.
At equality the centered indicator belongs to ker L. The n centered star
indicators are independent: evaluating a relation at the empty vertex
gives a zero coefficient sum, and singleton evaluations then give every
coefficient zero. Thus every H matrix has rank L<=N-n; (15) attains this.

For our maximal-rank matrix, any maximum centered indicator is a linear
combination of centered stars. At the empty coordinate the coefficients
sum to one; at singleton coordinates each coefficient is zero or one.
Exactly one coefficient is one, so the family is that star. This is the
credited rank-to-equality criterion applied to a new capped certificate.

At n5 the family of all three- and four-sets has size15=s and is
intersecting, since any two have total size greater than five. It is maximum:
the30 nonempty proper subsets form15 disjoint complementary pairs, from
each of which an intersecting family takes at most one set. It contains
no singleton and so is not a star. Its centered indicator is outside the
five centered-star span by the same empty/singleton argument. Every H
matrix there therefore has at least six kernel directions; rank N-n=26
is impossible. The familiar complement-pair partition already supplies H
on the proper cube; we do not claim its existence anew or infer the
precise optimal rank from this weaker obstruction. This explains the sharp
lower threshold six for the present maximal-rank star-kernel assertion.

## 7. Finite products and all equality cases

For factor j, let p_j=s_j/N_j and rho_j=p_j/(1-p_j). Our factors satisfy

```
N_j-2s_j=binomial(n_j-1,4)>0,
spec M_j subset[-rho_j,1],  0<rho_j<1,
mult(-rho_j)=n_j,          mult(1)=1.
```

The tensor M_*=tensor_j M_j has the product support on sets with disjoint
coordinate supports and row sum one. Every negative product eigenvalue
has magnitude at most max rho_j. To attain that maximum it must have
**exactly one** negative factor at its lower endpoint in a tied factor,
and all other factors at one. Extra negative factors have magnitude<1;
any nonunit positive factor also has magnitude<1 by the simple upper
endpoint and cap. Thus the lowest tensor endpoint has multiplicity
sum_(j:p_j=max p) n_j, with simple upper endpoint one. Set
s_*=N_* max p_j, an integer because it is a largest coordinate-star size.
Then (N_*-s_*)M_*+s_*I is PSD with that kernel dimension.

For completeness the densities decrease strictly with n in the stated
range. Put f(n)=n^4-2n^3+11n^2+14n+24 and p_n=4n(n^2-3n+8)/f(n).
Exact polynomial arithmetic gives

```
p_n-p_(n+1)=4(n-1)(n-2)(n-3)(n^3+3n^2+14n+24)
             /[f(n)f(n+1)]>0, n>=6.               (17)
```

The denominators are positive since
f(n)=n(n+1)(n^2-3n+14)+24, and n^2-3n+14>0 in this range.
The checker verifies (17) over Q(u) with n=6+u. Hence the tied factors
are exactly the c factors with minimum order n_*.

Their c n_* centered coordinate-star cylinders are independent by the
global empty and singleton coordinates and exhaust the tensor lower
kernel. Equation (16) for the full product forces any maximum indicator
into their span. Empty/singleton evaluation again selects exactly one
cylinder. This proves maximal lower rank N_*-c n_* and all stated equality
cases. More general mixtures with existing capped maximal star-kernel
factors use the same density-tie criterion; no extension to factors with
nonstar endpoint kernels is silently assumed.

## 8. Reproduction, coverage and trust boundary

[verify.py](verify.py) uses only CPython3.11+ and its standard library. Its
Q(u) arithmetic uses rational polynomial Euclidean gcd and coefficient
cross multiplication. Principal determinants are expanded independently
by permutations, while the optional CAS uses exact domain Gaussian
elimination. The written harmonic completeness and Schur repair arguments
remain unformalized; the checker does not replace them.

The full replay checks98 identities,22 infinite positive margins, and
entire dense rational matrices at n6/7/8. It checks actual downward closure,
stars, support, row sums, both full PSD slacks and exact ranks, and direct
gap-one inequalities C-P>=0 and U-I>=0 using the exact kernel Gram
projector. It checks every vector in complete harmonic bases, every lift
norm, every disjointness action and core action, and cross-degree
orthogonality. The lifted basis sizes56,98,162 exhaust all nonempty vertices;
the action counts are224,392,648. The repaired full ranks are51,92,155.
It checks the exact star projection norm and all compressed lower/upper
slacks at t_* at each finite order, including a strict upper-core buffer
above one half. These three projection/endpoint identities use n=6+u;
the22 coefficient margin checks use n=8+u with separate6/7 branches.
These finite validations check the implementation; they do not establish
the infinite coverage by extrapolation.

Seven deliberately damaged controls are rejected, including a changed
positive polynomial coefficient, a zero denominator constant, a wrong
six-point star weight, the omitted generic2/3-layer weight, evaluation at
the six/seven poles, and a wrong supported diagonal. Checks use explicit
exceptions and remain active under python -O.

From the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O spectral_downset_uniform_four/verify.py \
  --check spectral_downset_uniform_four/RESULTS.json
```

Expected compact output:

```json
{"ok":true,"symbolic_identities":98,"positive_margins":22,"finite_orders":[6,7,8],"full_lower_ranks":[51,92,155],"negative_controls":7}
```

The final dense replay took62.5seconds and37,072KiB peak child RSS on
CPython3.11.2, with one research job and all native threads one; no resource
escalation was used. Runtime varies with hardware. The compact
[RESULTS.json](RESULTS.json) includes coefficient margins and hashes of
the regenerated centered cores and repaired full matrices, without those
large matrices themselves. [SHA256SUMS](SHA256SUMS) covers the source and
compact evidence.

For optional CAS regeneration, install **SymPy1.14.0** with its normal
dependency **mpmath1.3.0**, then use one-thread settings and

```bash
python3 -B -O spectral_downset_uniform_four/derive.py \
  --check spectral_downset_uniform_four/POSITIVITY_CERTIFICATE.json
```

It solves (4) over Q(n), verifies every formula and boundary residual,
and regenerates all22 coefficient arrays exactly. No numerical optimizer,
floating-point SDP, modular reconstruction or proof by interpolation enters
the published certificate. Author checking and source publication do not
constitute independent peer review or formalization.
