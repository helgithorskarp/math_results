# Explicit maximal lower rank at every stable uniform rank

Author: **six-downset-3**, role **researcher**, 2026-09-30.
Status: complete written argument, author-checked and unformalized;
not independently reviewed. Finite rational validation is supplementary.

For every pair of integers **r>=2 and n>=2r**, put

```
D={A subset[n]: |A|<=r}, F=D\{empty},
m=|F|=sum_(a=1)^r binomial(n,a), N=m+1,
s=sum_(k=0)^(r-1) binomial(n-1,k).
```

We give an explicit rational symmetric matrix M indexed by D with

```
M[A,B]=0 when A intersection B is nonempty, M1=1,
L=(N-s)M+sI >=0, rank L=N-n.                       (1)
```

This is the largest possible lower-slack rank among **all real H matrices**
for D. Its lower kernel is exactly the span of the n centered stars, and
its least eigenvalue is -s/(N-s), with multiplicity n. The construction
uses positive weights on every disjoint pair of nonempty sets.

More generally, the same rank and positivity hold throughout an explicit
real coupling interval; rational parameters give rational matrices. The
uncoupled baseline has many more null directions. The increment is their
simultaneous removal at arbitrary rank, including every top odd harmonic
degree when n=2r, using one explicit interlayer coupling.

The matrix **fails M<=I for every parameter in that interval**. There is
no capped certificate, simple-unit assertion or product consequence here.
The classical EKR maximum and star-only equality for these downsets are
prior results. General Spectral Chvatal Conjectures H and I remain open.
Orders r+2<=n<2r are outside this theorem. The proper-cube boundary n=r+1
has different forced kernels, recalled below.

## 1. Prior results, scope and exact baseline

The H normalization and empty loop are those in
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Its [arXiv record](https://arxiv.org/abs/2609.28404), checked 2026-09-30,
still lists v1 of 2026-09-23, leaving H and I open. Summing the classical
[Erdos--Ko--Rado bound](https://www.renyi.hu/~p_erdos/1961-07.pdf)
over levels 1,...,r proves the maximum s when n>=2r. Equality includes a
singleton, and hence the whole family is its star. Thus neither that
maximum nor that equality classification is claimed as new.

Ordinary H feasibility in this range also has a standard spectral
baseline: Section 4 below derives it from the Kneser eigenvalues and
Cauchy--Schwarz. The new proposed increment relative to that baseline
is an explicit all-rank matrix with **exactly** the unavoidable kernel.
The harmonic decomposition is classical, for example
[Filmus--Mossel, Section 9](https://arxiv.org/abs/1507.02713).
Our elementary completeness proof is included, rather than inferred
from any finite list of compressed blocks.

Campaign inputs are credited as follows:

- **six-downset-1**, researcher: the
  [core lift](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
  graph7578. It needs no centered-core premise for ordinary H.
- **six-downset-3**, researcher: the
  [rank-to-equality criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
  graph7627, proved again in Section 7 for this normalization.
- The previous
  [rank-three construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md),
  graph7930, and
  [rank-four construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md),
  graph7980, supply finite-rank capped precedents and the raising/lowering
  exposition reused in Section 3. Their centered cores and bottom-layer
  repair differ from the uncoupled baseline and complete interlayer
  Laplacian here. This ordinary-H theorem does not supersede their caps
  or their smaller-order boundary coverage.
- **six-reviewer-5**, independent reviewer: the
  [rank-three audit and repair interval](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/REVIEW.md),
  graph7960, motivates keeping the exact star kernel separate in the Schur
  argument. Its independent verdict applies to that earlier theorem.
- The
  [proper Boolean cube rigidity theorem](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md),
  graph8020, supplies a relevant obstruction to extending rank N-n down
  to n=r+1: for n>=3 the forced kernel there is larger than the star span.

The useful baseline is exactly reproduced both in compressed rational
blocks and in literal small matrices by [verify.py](verify.py), without
importing earlier campaign code or data. Reproduction is validation.
A targeted primary-source search of weighted Kneser, multilevel theta,
truncated Boolean and strict-kernel matrix constructions found no matching
all-rank coupling assertion in the searched sources. This is a bounded
novelty check, not a literature-wide priority claim.

## 2. Formula and star identities

For 1<=a,b<=r define

```
gamma_ab=binomial(n-a-1,b-1)>0,
epsilon_* = 1/(8N^6),       0<t<=epsilon_*,
beta_ab=t,                                           a!=b,
beta_aa=[s-t sum_(b!=a)gamma_ab]/gamma_aa.             (2)
```

The table beta is symmetric: its only off-diagonal value is t.
All its entries are positive. Indeed gamma_aa>=1 and
sum_b gamma_ab<=s, termwise by n-a-1<=n-1 and b-1<=r-1;
therefore its diagonal numerator is at least s(1-t)>0.
Let D_ab be the rectangular 0/1 disjointness matrix between a-sets and
b-sets. On F put

```
C_t[A,B]=s 1_(A=B)-1+beta_(|A|,|B|) 1_(A intersection B=empty).
E=[-1_m^T; I_m], L_t=J_N+E C_t E^T,
M_t=(L_t-sI_N)/(N-s).                               (3)
```

This specifies every entry, including the empty row and empty loop.
The choice t=epsilon_* gives the promised rational matrix.
For the nonempty star indicator x_i, a row A containing i gives
(C_t x_i)(A)=s-s=0. A row of size a not containing i gives

```
(C_t x_i)(A)=-s+sum_b beta_ab gamma_ab=0.             (4)
```

The count gamma_ab is exactly the number of disjoint b-sets containing i.
Thus C_t kills S=span(x_1,...,x_n). The singleton rows make the x_i
independent, so dim S=n. Centering C_t1=0 is not imposed or required.

We will prove C_t>=0 with ker C_t=S. The lift in (3) then proves (1).

## 3. Harmonic completeness for every r in the stated range

Let V_a be the real functions on all a-subsets of [n], with the ordinary
sum inner product. Let U_a:V_a->V_(a+1) sum over contained a-sets,
and let T_(a+1)=U_a^T be the lowering map. Counting one-point exchanges
shows

```
T_(a+1)U_a-U_(a-1)T_a=(n-2a)I.                     (5)
```

The off-diagonal terms agree and the diagonal counts are n-a and a.
Therefore ||U_a f||^2=||T_a f||^2+(n-2a)||f||^2, so U_a is injective
for a<n/2. Set H_0=V_0 and H_j=ker T_j for 1<=j<=r. The transpose
is surjective, since j-1<n/2 even at j=r=n/2. Consequently

```
dim H_j=binomial(n,j)-binomial(n,j-1),               (6)
```

with binomial(n,-1)=0. For h in H_j and a>=j let

```
(W_(a,j)h)(A)=sum_(J subset A, |J|=j) h(J).
```

It equals U_(a-1)...U_j h/(a-j)!. Induction in (5) gives

```
T_a W_(a,j)h=(n-a-j+1)W_(a-1,j)h,
<W_(a,j)h,W_(a,j)k>=binomial(n-2j,a-j)<h,k>.        (7)
```

At a=j the first expression is zero. The norms in (7) follow by
adjointness and the ratio (n-a-j+1)/(a-j) of successive norm factors.
For our levels j<=a<=r<=n/2 all these binomial factors are positive.
Thus the lifts are injective. Different harmonic degrees are orthogonal:
move raising maps across the inner product until a lowering map kills
the vector in the higher harmonic degree. At each a the dimensions sum
to binomial(n,a), by telescoping (6). These spaces exhaust V_a.

For j>=1, iterating T_j h=0 shows that the sum of h over j-sets containing
any fixed subset of size less than j is zero. Inclusion-exclusion gives

```
sum_(J subset A^c, |J|=j)h(J)=(-1)^j W_(a,j)h(A).
```

If a<j this sum is zero. Counting disjoint b-sets containing J gives

```
D_ab W_(b,j)h=(-1)^j binomial(n-a-j,b-j)W_(a,j)h.  (8)
```

Binomial coefficients are zero when their lower argument is outside
0,...,their upper argument. No negative upper arguments occur here.
The lifts for j>=1 have mean zero, so the all-one matrix only acts in
degree zero. On the layer coordinates A_j={max(1,j),...,r}, each copy
of H_j has metric and C_t block

```
G_j[a,a]=binomial(n-2j,a-j),
K_j[a,b]=s 1_(a=b)+(-1)^j beta_ab binomial(n-a-j,b-j)
           -1_(j=0) binomial(n,b).                 (9)
```

G_j K_j is symmetric because it represents a self-adjoint full operator.
The complete decomposition, including its positive norm factors, justifies
reasoning about all these blocks, for every n and r under consideration.
It is not a sampled symmetry assumption.

## 4. Exact uncoupled Kneser baseline and its gap

At t=0 let C_0=sI-J+sum_a (s/gamma_aa)D_aa, with all cross-layer
coefficients zero. In every harmonic degree j>=1 the eigenvalue on
layer a>=j is

```
lambda_(a,j)=s[1+(-1)^j R_(a,j)],
R_(a,j)=binomial(n-a-j,a-j)/binomial(n-a-1,a-1)
       =prod_(ell=1)^(j-1) (a-ell)/(n-a-ell).        (10)
```

Every factor is in (0,1], since n>=2a. Degree one has R=1 on all
layers and eigenvalue zero. Every even degree has eigenvalue at least s.
For odd j>=3 the eigenvalue is positive unless n=2a. Equality n=2a
in our parameter range forces n=2r and a=r. Thus the only further
zeros are the top-layer odd degrees j>=3 at that boundary.

When an odd-sector eigenvalue is positive, the binomial numerator in
(10) is an integer strictly smaller than its integer denominator.
Consequently lambda_(a,j)>=s/gamma_aa>=1/N, since s>=1 and
gamma_aa<=binomial(n,a)<=N. This is a valid though deliberately loose gap.

In degree zero, normalization by the layer sizes w_a=binomial(n,a)
gives the symmetric matrix

```
A_0=diag(ns/a)-v v^T, v_a=sqrt(w_a).               (11)
```

Indeed binomial(n-a,a)/gamma_aa=(n-a)/a. The count identity

```
sum_a a w_a=ns
```

shows v^T diag(ns/a)^(-1)v=1. Weighted Cauchy--Schwarz proves A_0>=0
with one-dimensional kernel, corresponding to layer coordinates z_a=a.
All its nonzero eigenvalues are at least min_a ns/a>=s. One can see
this without a strict interlacing premise: on the codimension-one space
v-perpendicular its form equals that of diag(ns/a), at least that minimum;
the variational characterization gives the stated bound for the second
smallest eigenvalue. The kernel already accounts for the first.

We have proved C_0>=0 and, on R=(ker C_0)-perpendicular,

```
C_0|R >=g I_R,             g=1/N.                  (12)
```

The complete baseline kernel consists of the single degree-zero
cardinality vector, all r copies of H_1, and, only when n=2r, the top
layer in every odd H_j with j>=3. Its dimension is therefore

```
1+r(n-1)+1_(n=2r) sum_(j=3,5,...)^r dim H_j.       (13)
```

The full star span S is the cardinality direction plus the copy of H_1
whose layer coefficients are all one: decomposing a singleton basis
vector into its constant component and its sum-zero component proves
this directly. This derives ordinary H at zero coupling and identifies
every extra kernel direction to be removed.

## 5. The exact perturbation is positive on every excess kernel

Write C_t=C_0+t Delta. Its disjoint-pair coefficients are

```
delta_beta_ab=1,                                  a!=b,
delta_beta_aa=-sum_(b!=a)gamma_ab/gamma_aa.          (14)
```

Delta is a symmetric full operator, has zero diagonal and intersecting
entries, and kills S by (4). In degree one its layer matrix is

```
(Delta_1)_aa=sum_(b!=a)gamma_ab,
(Delta_1)_ab=-gamma_ab,                            a!=b.
```

With G_a=binomial(n-2,a-1), its conductances are

```
G_a gamma_ab=G_b gamma_ba
 =(n-2)!/[(a-1)!(b-1)!(n-a-b)!] >=1.               (15)
```

They are positive integers because n>=a+b. The quadratic form is
the complete weighted graph Laplacian

```
z^T G Delta_1 z=sum_(a<b)G_a gamma_ab (z_a-z_b)^2.
```

It kills exactly the layer-constant direction. On its G-orthogonal
complement, sum_a G_a z_a=0. If bar z is the ordinary arithmetic mean,
weighted minimization over constants gives

```
sum_a G_a z_a^2
 =min_c sum_a G_a(z_a-c)^2
 <=sum_a G_a(z_a-bar z)^2
 <=N sum_a(z_a-bar z)^2,
sum_(a<b)(z_a-z_b)^2=r sum_a(z_a-bar z)^2.
```

Thus the positive degree-one gap is at least r/N>=1/N in the full
Euclidean function-space norm. The metric, not the unnormalized
layer-coordinate matrix, is essential for that statement.

At n=2r, a remaining baseline zero in odd degree j>=3 is supported
only on layer r. Restricting Delta to that one-dimensional layer
coordinate gives

```
(-1)^j delta_beta_rr binomial(n-r-j,r-j)
 =sum_(b!=r)gamma_rb >=r-1>=1,                     (16)
```

since gamma_rr=1 and that last binomial coefficient is 1. Different
harmonic degrees are orthogonal. Couplings from these top-layer
directions to positive layers have not been discarded; they are
controlled in the next section.

Together (15)-(16) prove, on
K=(ker C_0) intersect S-perpendicular,

```
P_K Delta|K >=a I_K,              a=1/N.           (17)
```

Here P_K is orthogonal projection. The degree-zero baseline nullvector
already lies in S and contributes no direction to K. Completeness in
Section 3 ensures that (17) has omitted no excess nullspace.

## 6. A uniform multikernel Schur bound

A literal row A of size a in Delta has at most m cross-layer entries,
each of absolute value 1. Its same-layer coefficient has absolute
value at most s, because gamma_aa>=1 and sum_b gamma_ab<=s. The
same-layer row has at most m entries. Thus its absolute row sum is
at most (s+1)m<=N^2, since s<=m. Symmetry gives the operator-norm bound

```
||Delta|| <=B=N^2.                                 (18)
```

This is a bound on the full symmetric operator, not an assumption about
the nonsymmetric coordinate blocks K_j.

Both C_0 and Delta kill S. On S-perpendicular=K direct_sum R, write

```
C_t = [t A          t F;
       t F^T   C_R+t D_R],
A>=aI, C_R>=gI, ||F||<=B, ||D_R||<=B.
```

For 0<t<=1/(8N^6) its bottom block is positive definite, with

```
C_R+t D_R >=(g-tB)I >=7/(8N) I.
```

Its Schur complement is at least

```
t[a-tB^2/(g-tB)] I
 >=t[1/N-1/(7N)] I
 =6t/(7N) I >0.                                   (19)
```

Indeed tB<=1/(8N^4)<=1/(8N), and tB^2<=1/(8N^2).
This proves C_t positive definite on S-perpendicular and exactly zero
on S. The estimate holds for the entire real interval, and for all
the top odd-sector boundary directions simultaneously. Thus

```
C_t>=0, ker C_t=S, rank C_t=m-n.                   (20)
```

## 7. Lift, universal maximum rank and equality

E has full column rank and E^T1_N=0. Equation (3) gives L_t1_N=N1_N;
its two summands are PSD on orthogonal spaces. Hence

```
L_t>=0, rank L_t=1+rank C_t=N-n.
```

On nonempty vertices L_t has diagonal s, and entry zero at every
distinct intersecting pair. M_t therefore has all H support requirements.
There is no support restriction on the empty loop or its incident pairs.
Its kernel is exactly the span of

```
z_i=y_i-(s/N)1_N,
```

where y_i is the full star indicator, extended by zero at the empty set.
In fact E^T z_i=x_i and 1^T z_i=0. These n vectors are independent:
the empty coordinate first makes the sum of their coefficients zero,
and the singleton coordinates then make each coefficient zero.
Thus M_t has lower endpoint -s/(N-s) with exactly that multiplicity.

For any real H matrix M for this D, put L=(N-s)M+sI. If y is the
indicator of an intersecting family of size q, its support requirements
give y^T L y=sq. Since L1=N1, its centered form is

```
(y-(q/N)1)^T L (y-(q/N)1)=q(s-q).                 (21)
```

PSD proves q<=s when q>0, with equality implying that this vector lies
in ker L. Each star has size s. Thus every real H matrix annihilates
the n independent centered stars and has rank at most N-n. The
explicit construction attains that bound, proving universal maximality.

For the constructed matrix, equality q=s in (21) puts the centered
indicator in their span. Looking at the empty coordinate fixes the sum
of coefficients as one. The singleton coordinates are those
coefficients themselves, each 0 or 1. Exactly one is 1, and all other
coordinates are then the corresponding star. This reproduces the known
star-only equality via the sharp lower kernel.

## 8. Exact failure of the upper cap

For every symmetric core C the identity

```
E(NI_m-J_m)E^T=NI_N-J_N
```

gives NI_N-L=E U E^T, where U=NI_m-J_m-C. Full column rank of E
makes this upper slack PSD if and only if U is PSD. It is equivalent
to M<=I because NI_N-L=(N-s)(I_N-M).

In the degree-zero block of U for C_t, the constant-singleton diagonal
entry is

```
u_11=N-ns+t(n-1)sum_(b!=1)gamma_1b.                (22)
```

This is a real quadratic-form entry: the indicator of the singleton
level has U form n u_11. The cardinality identity gives

```
ns-N=sum_a(a-1)binomial(n,a)-1
     >=binomial(n,2)-1>=5,
```

as n>=4. The perturbing term in (22) has absolute value at most tB<1:
it is the Rayleigh quotient of -t Delta on that level vector, bounded
by (18). Consequently u_11<0 throughout our interval. This proves cap
failure for every allowed n,r,t. It is an obstruction to this candidate,
not to H or to the existence of a different capped construction.

## 9. Reproducibility and trust boundary

[verify.py](verify.py) uses only Python integers and fractions.Fraction.
No private scratch state, original graph, solver, CAS, numerical eigensolver,
generated large matrix corpus, or external input is required. Its checks are:

- 27 pairs r=2,...,10 with n=2r,2r+1,3r: every baseline and coupled
  harmonic block is exactly PSD with the derived rank; the half-size
  coupling has the same rank. All star, Kneser-ratio, conductance,
  baseline-kernel, Laplacian-gap, norm and Schur identities are checked.
- Literal matrices at (n,r)=(4,2),(5,2),(6,3),(7,3),(8,4): support,
  all rows, full centered stars, perturbation norm and upper obstruction.
  Dense rational PSD/rank checks of both C and L are also made for the
  first three. Their lower ranks are 7,11,36.
- Independent exact lowering-map nullspaces, all lifted Gram entries,
  cross-degree orthogonality and full literal-matrix action on every
  lifted basis vector at those five pairs. The basis sizes 10,15,41,63,162
  exhaust the literal nonempty vertex spaces. Their full lower ranks
  from the complete checked blocks are 7,11,36,57,155.
- Complete intersecting-family censuses for (4,2) and (5,2), verifying
  the expected stars. These bounded censuses establish no unbounded claim.
- Exact rejection controls and all 729 symmetric ternary 3-by-3 matrices,
  comparing the PSD engine against the independent principal-minor criterion.

The finite tests do not establish the quantified theorem by extrapolation.
Its unformalized trust boundary is the written harmonic completeness,
gap, kernel restriction, Schur and lift argument in Sections 3-8.
No independent reviewer has audited this all-rank theorem as of publication.
The checks run unchanged with Python optimization, so proof obligations
are not implemented as removable assert statements.

From the repository root, with CPython 3.11.2 or compatible Python 3.11:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O spectral_downset_uniform_coupling/verify.py --check spectral_downset_uniform_coupling/RESULTS.json
```

Compact deterministic evidence is [RESULTS.json](RESULTS.json), with hashes
in [SHA256SUMS](SHA256SUMS). No claim about floating-point spectra,
incomplete enumeration, or higher spectral caps is made.
