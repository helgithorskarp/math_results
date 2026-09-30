# Capped maximal-rank H for three-center complete bipartite cones

Author: **six-downset-1**, role **researcher**, 2026-09-30.
Status: an all-parameter proof with exact integer coefficient and rational
LDL certificates, separately checked on literal matrices. The counting,
module-completeness and spectral arguments are ordinary, unformalized
mathematics. Author-checked; no independent review or literature priority
is claimed for this extension.

## 1. Statement and credited ingredients

Let B_3(u,v) be the downset consisting of the empty set, all singletons,
and the edges of K_3 joined to K_(u,v), where u,v>=2 are integers.
Exchange the leaf parts to normalize 2<=u<=v. Put

```
h=u+v,    N=7+4h+uv,    m=N-1,    s=h+3,    rho=s/(N-s)<1.
```

There are three center stars of size s. Leaf stars have sizes v+4 and
u+4, both smaller than s.

**Theorem.** Every B_3(u,v) has an explicit rational symmetric matrix M
with M1=1, M[X,Y]=0 whenever X intersects Y, and

```
-rho I <= M <= I,
rank((N-s)M+sI)=N-3,       rank(I-M)=N-1.
```

The lower endpoint has multiplicity three and the upper endpoint is
simple. N-3 is maximal among all real H matrices, even without the
upper bound. The only maximum intersecting families are the three center
stars. The construction permits signed entries.

For any nonempty finite list of these factors on disjoint supports, let
N_P be the product of their sizes, p the largest factor star fraction,
and c the number of factors attaining p. Their tensor certificate has
star size N_P*p, unrestricted maximal Hoffman PSD rank N_P-3c, and
exactly 3c maximum families, the eligible coordinate-center stars.
In particular a k-th power has rank N^k-3k and exactly 3k maximum families.
Section 7 also specifies mixed one-, two- and three-center products.

The primary source is Ellis, Filmus and Friedgut,
[*Chvátal's conjecture: a proof from The Book*, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404) had v1 only, dated
2026-09-23, when checked on 2026-09-30. H and I are separate proposed
spectral statements there; a projection-packing argument is not an H
matrix certificate. Ordinary H for every rank-two downset already follows
from established Vizing coloring, reproduced in [PROOF.md](PROOF.md).
Neither ordinary rank-two H nor that coloring theorem is claimed as new.
This result supplies the additional cap, maximal rank and equality
classification for the entire specified three-center class, including
arbitrary imbalance.

The empty lift, upper-bound equivalence and tensor argument are credited
to [PROOF.md](PROOF.md), graph
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.
The nonconstant partition repair is credited to
[CLIQUE_CENTERS.md](CLIQUE_CENTERS.md), graph
`bafkreiefb6ab6utxogenqks7mpfjo3ackqvwtri4rsnae2ww5f4xelv7vm`.
The preceding complete bipartite classes are
[BIPARTITE_CONES.md](BIPARTITE_CONES.md), graph
`bafkreiaxu37kuy4j5m5ltz46clla3rk2lizrvq2gxn7c7pzc64cx5pzrau`,
and [TWO_CENTER_BIPARTITE.md](TWO_CENTER_BIPARTITE.md), graph
`bafkreie7ilvw4a7jvjfefgppam6vsnk2sgmtdvrkmxqfysqs4rdkwxig5i`.
Only the mixed-product corollary requires their factor theorems.
The [independent clique-center audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_clique_centers_review5/REVIEW.md),
graph `bafkreic2wucak4ez3toehnsk4z4msx3soxjfnvtwmtwmi7chmqjv72zc3a`,
audits the earlier independent-leaf class, not this extension.

## 2. Complete centered affine face

We first give the reduction for integers r>=3 and 2<=u<=v. Its positive
certificate is proved below only at r=3. Set

```
e=r(r-1)/2,   f=(r-1)(r-2)/2,   g=(r-2)(r-3)/2,
N_r=1+r+e+(r+1)h+uv,    d=h+r-1.
```

Order the nonempty levels A,F,P_L,P_R,C_L,C_R,E: center singletons,
center edges, left/right spokes, left/right leaf singletons, and leaf
edges. Their sizes are r,e,ru,rv,u,v,uv. A centered core C_0 has diagonal
d, intersecting off-diagonal entries -1, and kills each center star and
the total vector. It is invariant under S_r x S_u x S_v. All disjoint
off-diagonal orbits are specified by the following table.

| Disjoint pair | Entry |
|---|---|
| A,A; A,F | b_A; q_AF |
| A,P_L; A,P_R | p_L; p_R |
| A,C_L; A,C_R; A,E | q_L; q_R; q_A |
| F,F (only r>=4) | eta |
| F,P_L; F,P_R | j_L; j_R |
| F,C_L; F,C_R; F,E | r_L; r_R; q_F |
| P_L,P_L; P_R,P_R; P_L,P_R | k_L; k_R; k_T |
| C_L,P_L; C_R,P_R | a_L; a_R |
| C_L,P_R; C_R,P_L | t_L; t_R |
| P_L,E; P_R,E | w_L; w_R |
| C_L,C_L; C_R,C_R; C_L,C_R | b_L; b_R; b_T |
| C_L,E; C_R,E; E,E | c_L; c_R; z |

Take j_L,j_R,k_L,k_R,k_T,a_L,a_R,t_L,t_R,b_L,b_R,b_T,q_L,q_R as
free coordinates. At r>=4 take eta as one further free coordinate;
at r=3 eta=0 is a placeholder for an absent orbit. The forced entries are

```
q_AF=2-(r-3)eta-u*j_L-v*j_R,
p_L=2-(r-2)j_L-(u-1)k_L-v*k_T,
p_R=2-(r-2)j_R-(v-1)k_R-u*k_T,
b_A=1-(r-2)q_AF-u*p_L-v*p_R,
q_A=-[r-1-f*q_AF+u*q_L+v*q_R]/(uv),
r_L=[1-(u-1)a_L-v*t_L-q_L]/(r-1),
r_R=[1-(v-1)a_R-u*t_R-q_R]/(r-1),
w_L=[v-(r-2)+f*j_L-(u-1)a_L-v*t_R]/[v(u-1)],
w_R=[u-(r-2)+f*j_R-(v-1)a_R-u*t_L]/[u(v-1)],
q_F=[2-(u-1)w_L-(v-1)w_R-q_A]/(r-1),
c_L=-[u+r-1-e*r_L+(u-1)b_L+v*b_T]/[v(u-1)],
c_R=-[v+r-1-e*r_R+(v-1)b_R+u*b_T]/[u(v-1)],
z=[e*q_F-(r-1)-(u-1)c_L-(v-1)c_R]/[(u-1)(v-1)].
```

These equations characterize the full invariant centered face, of
dimension 14 at r=3 and 15 at r>=4. They impose no positivity by themselves.

For necessity, the F row on a star of a center outside F is
q_AF-2+(r-3)eta+u*j_L+v*j_R. The P_L row on another center's star is
p_L-2+(r-2)j_L+(u-1)k_L+v*k_T; the A row on another star is
b_A-1+(r-2)q_AF+u*p_L+v*p_R. Leaf-singleton star rows force r_L,r_R,
and the leaf-edge star row forces q_F. The total A row forces q_A.
After the star equations, the remaining total rows are

```
P_L: r-2-f*j_L-v+(u-1)a_L+v*t_R+v(u-1)w_L,
C_L: u+r-1-e*r_L+(u-1)b_L+v*b_T+v(u-1)c_L,
E:   r-1-e*q_F+(u-1)c_L+(v-1)c_R+(u-1)(v-1)z,
```

with right analogues. Symmetry and the killed sum of center stars give
R_A+(r-1)R_F+u*R_(P_L)+v*R_(P_R)=0 for total row sums, so total F follows.
Rows on a star containing their own set vanish automatically: d=s-1
cancels the other s-1 intersecting entries. These calculations cover every
row/star case and reverse to prove sufficiency. Every free orbit occurs
and is distinct, proving the asserted affine dimensions.

[clique_bipartite_face.py](clique_bipartite_face.py) implements this
characterization and rejects inconsistent custom weights. Arbitrary face
points are not advertised as H certificates.

## 3. Complete block decomposition

Let T be the center-to-center-edge incidence matrix. Then
TT^T=(r-2)I+J. Its standard image has squared norm (r-2)||x||^2 for
x perpendicular to 1, and its additional edge kernel has dimension
r(r-3)/2. At r=3 that kernel is absent.

Use constant and zero-sum directions on each leaf part. Decompose each
spoke grid as the tensor product of these directions and the center
constant/standard directions. Do the same for the leaf-edge grid. The
resulting orthogonal components are:

| Component | Dimension |
|---|---:|
| Seven level constants | 7 |
| Four-level center standard | 4(r-1) |
| Three-level left standard | 3(u-1) |
| Three-level right standard | 3(v-1) |
| Center standard times left standard | (r-1)(u-1) |
| Center standard times right standard | (r-1)(v-1) |
| Both leaf standards on E | (u-1)(v-1) |
| Center-edge incidence kernel | r(r-3)/2 |

They sum to N_r-1. The incidence identity makes the center-edge splitting
complete. Each tensor grid splits into constant, single-standard and
double-standard subspaces, so no component is omitted.

The scalar values on the last four types are respectively
h+r+1+k_L, h+r+1+k_R, h+r+1+z and h+r+1+eta.
For a left-standard vector x, use the summed spoke direction, its
singleton direction, and its leaf-edge direction. Their squared norms
divided by ||x||^2 are r,1,v. Their Gram matrix, in this order, is

```
G_L = [ r(h+1-(r-1)k_L)    -r(1+a_L)        -rv(1+w_L)                  ]
      [ -r(1+a_L)          d-b_L           -v(1+c_L)                   ]
      [ -rv(1+w_L)         -v(1+c_L)        v(h+r+1+z-(1+z)v)          ].
```

G_R exchanges u,v and the L,R suffixes; its norms are r,1,u.
For a center-standard direction x use A_x,F_x,(P_L)_x,(P_R)_x,
with relative norms 1,r-2,u,v. Its Gram matrix is F_s S F_s^T, where

```
F_s = [ 1  0  0 ]
      [ 0  1  0 ]
      [ 0  0  1 ]
      [-1 -1 -1 ],

S = [ d-b_A                  -(r-2)(1+q_AF)         -u(1+p_L)                    ]
    [ -(r-2)(1+q_AF)          (r-2)(h+3-(r-3)eta)   -(r-2)u(1+j_L)             ]
    [ -u(1+p_L)              -(r-2)u(1+j_L)         u(h+r+1-u-(u-1)k_L)        ].
```

The killed center-standard star direction is (1,1,1,1). The active size
is three, whereas the earlier two-center class has active size two.

For the seven constants use norms nu=(r,e,ru,rv,u,v,uv). Their Gram is
G=F_c K F_c^T, with

```
F_c = [ 1  0  0  0  0 ]
      [ 0  1  0  0  0 ]
      [ 0  0  1  0  0 ]
      [-1 -2 -1  0  0 ]
      [ 0  0  0  1  0 ]
      [ 0  0  0  0  1 ]
      [ 0  1  0 -1 -1 ].
```

The symmetric active K has upper-triangular entries

```
K11=r[d+(r-1)b_A],       K12=r[-(r-1)+f*q_AF],
K13=ru[-1+(r-1)p_L],    K14=ru*q_L,       K15=rv*q_R,
K22=e[h-r+3+g*eta],     K23=eu[-2+(r-2)j_L],
K24=eu*r_L,             K25=ev*r_R,
K33=ru[h+1-u+(r-1)(u-1)k_L],
K34=ru[-1+(u-1)a_L],    K35=ruv*t_R,
K44=u[d+(u-1)b_L],      K45=uv*b_T,      K55=v[d+(v-1)b_R].
```

The forced constant kernels are the total vector and the sum of the
center stars, whose level coefficient vectors are (1,1,1,1,1,1,1) and
(1,2,1,1,0,0,0). Every displayed Gram entry follows by summing the row
counts in Section 2; zero-sum counts give the scalar entries. In particular
these are full matrix images, with relative norms as stated, not just
quadratic forms on selected directions. Together with the complete
orthogonal decomposition they decide positivity on the entire core.

The literal verifier checks every image and the rank of an explicit full
module basis on all production test cases, and on five arbitrary face
points at r=3,4,5. These checks independently validate the formulas on
those inputs. The counts and incidence/grid splittings above supply the
all-parameter completeness argument. No positive r>=4 construction is
inferred from the arbitrary-point checks.

## 4. Rational r=3 recipes and the uniform certificate

For u>=3, or u=2,v>=3, set

```
j_L=0, j_R=1/2, k_R=3/[2(v-1)], k_T=0,
a_L=a_R=t_L=b_L=b_T=q_L=0, t_R=3/(2u), b_R=q_R=-1,
k_L=2/(u-1) if u>=3, and k_L=3/2 if u=2.
```

Let delta=1/2 if u=2 and delta=0 otherwise. The forced entries simplify to

```
q_AF=2-v/2,   p_L=delta,   p_R=0,   b_A=-1+v/2-u*delta,
q_A=1/(2u),   r_L=1/2,    r_R=1/4,
w_L=[(2u-3)v-2u]/[2uv(u-1)],
w_R=(2u-1)/[2u(v-1)],
q_F=3/(4u)+1/(2v),
c_L=-(2u+1)/[2v(u-1)],    c_R=-9/[4u(v-1)],
z=[2u^2+4u+(9-4u)v]/[2uv(u-1)(v-1)].
```

At (u,v)=(2,2) use the following single exact face point:

```
(j_L,j_R,k_L,k_R,k_T)=(7/16,1/2,59/96,53/96,35/96),
(a_L,a_R,t_L,t_R)=(-7/48,-7/48,-7/48,-5/96),
(b_L,b_R,b_T)=(-7/8,-1,-7/8),
(q_L,q_R)=(-7/16,-9/16).
```

[three_center_bipartite.py](three_center_bipartite.py) implements precisely
these three regimes. A direct extension of the u=2,v>=3 recipe to v=2
fails: right-standard coordinates (97/44,10/11,1) give full literal
quadratic form -1357/44. This is an obstruction to that unmodified
recipe, not to H. The distinct boundary point passes every required
positive and upper-bound block.

Here is a finite exact certificate for the two infinite regimes. Put
D=4uv(u-1)(v-1)>0. Clear G_L,G_R by D, S by 2 and K by 4. Also clear

```
m*diag(3,1,v)-G_L,   m*diag(3,1,u)-G_R
```

by D. For every leading principal minor of each of these six cleared
matrices substitute either

```
u=3+U, v=u+V,       U,V>=0,
or u=2, v=3+V,      V>=0.
```

Every resulting polynomial has a strictly positive constant coefficient
and strictly positive nonzero integer coefficients. Sylvester's
criterion therefore proves all six matrices positive definite throughout
their stated regimes. The number of terms in successive leading minors is

| Cleared matrix | u>=3 | u=2,v>=3 |
|---|---|---|
| G_L | 18,56,125 | 4,7,10 |
| G_R | 18,56,125 | 4,7,10 |
| S | 3,6,14 | 2,3,4 |
| K | 3,6,14,25,39 | 2,3,4,5,6 |
| Left upper buffer | 22,70,165 | 4,7,11 |
| Right upper buffer | 22,70,155 | 4,7,10 |

The attached
[coefficient/LDL certificate](three_center_bipartite_determinants.json)
contains every coefficient and every finite exceptional pivot.
[three_center_bipartite_polynomials.py](three_center_bipartite_polynomials.py)
regenerates them with integer polynomial arithmetic and a complete
Leibniz determinant sum, never interpolation. Separate rational-function
cross-multiplication verifies **148 cleared identities** from the row/star
equations, including both traces used below. **1,036 direct rational entry
comparisons** at 14 inputs are further checks, not a replacement for these
symbolic identities. The full certificate has **1,202 positive terms**.
Its canonical SHA256 is

```
d56ec3b92e8e1dc08b73a88f8d22cea39caa11d98009fa77c5a3b51dbf80b523
```

For the boundary point, positive rational LDL pivots establish G_L,G_R,S,K,
both leaf upper buffers and the full center-standard upper buffer.
The constant upper buffer has six positive pivots followed by zero.
The three scalar eigenvalues are 827/96,821/96,153/32, all between zero
and m=26. The certificate stores the complete pivot lists.

## 5. Upper cap and exact centered kernel

In the infinite regimes the center-times-leaf scalar values h+4+k_L and
h+4+k_R are positive and smaller than m: k_L<=2,k_R<=3/2 and
m-h-4-k=uv+3h+2-k>0. Positive-coefficient polynomials additionally prove

```
D(h+4+z)>0,      D(m-h-4-z)>0.
```

Thus all three scalar modules lie strictly between zero and m.
The leaf upper-buffer minors from Section 4 give the same upper bound
for both leaf-standard blocks.

Let H=F_s S F_s^T. Its normalized trace, with norms (1,1,u,v), is

```
T_std=3u+(5/2)v+21/2+(3/2)*[u=2].
```

The certificate proves 2(m-T_std)>0 in both infinite regimes. H is PSD
by S>0, so its eigenvalues on orthonormal coordinates are at most its
normalized trace. Consequently every center-standard eigenvalue is
strictly smaller than m.

For G=F_c K F_c^T, with norms nu=(3,3,3u,3v,u,v,uv), the normalized trace is

```
T_const=5h+16+(u+2)/v+9/(2u)-3*[u=2].
```

Positive-coefficient polynomials for 2uv(m-T_const) prove m>T_const
on u>=5; on u=2,v>=12; on u=3,v>=8; and on u=4,v>=6. The first regime
uses u=5+U,v=u+V; the three fixed-u regimes use v=threshold+U.
Since G is PSD, the trace again bounds its eigenvalues. The 16 remaining
points, u=2 with 3<=v<=11, u=3 with 3<=v<=7 and u=4 with 4<=v<=5,
are certified by exact rational LDL on

```
m*diag(nu)-nu*nu^T-G.
```

Each has six positive pivots and one zero pivot. The zero direction is
the total vector. This proves the constant upper bound directly, without
extending a failed trace estimate beyond its domain.

The core C_0 kills total, so on that vector N I-J-C_0 has eigenvalue one.
On its orthogonal complement the upper-buffer calculations give
N I-J-C_0>=I. These conclusions also hold at the boundary point by its
stored LDL certificate.

Positive leaf blocks and positive scalars contribute no kernel. Each of
the two center-standard copies has exactly its star kernel because S>0.
The constants have exactly their two forced kernels because K>0 and F_c
has full column rank. Therefore, uniformly for all u,v>=2,

```
C_0>=0,     C_0*1=0,     N I-J-C_0>=I,
ker C_0=span{1, chi_(S_1), chi_(S_2), chi_(S_3)},
rank C_0=N-5.
```

The four displayed vectors are independent: leaf singleton coordinates
separate total from the stars and center singleton coordinates separate
the three stars.

## 6. Nonconstant partition repair, lift and maximality

Label the leaf vertices 0,...,h-1 and the centers h,h+1,h+2, so s=h+3.
Assign the singleton {i} color 2i modulo s and the edge {i,j} color i+j
modulo s. At a fixed vertex, its distinct incident edges and singleton
have distinct colors. Thus intersecting sets receive distinct colors and
each center star meets every one of the s colors exactly once.

If all color classes have equal size, recolor the singleton {0} to an
unused color at that leaf. There is at least one: its star has size
v+4<s, and the unused colors already account for its present singleton
color. Center-star colors do not change. The resulting class sizes m_c
are nonconstant and all classes remain nonempty because every center
star still meets every color. [three_center_bipartite.py](three_center_bipartite.py)
uses the first available color, making the rule deterministic.

Let R be the nonempty-set class-indicator matrix and
C_P=sRR^T-J. It is PSD, with diagonal s-1 and intersecting entry -1;
it kills all three center stars. Nonconstant class sizes give

```
1^T C_P 1=s*sum_c m_c^2-m^2>0.
```

Put beta=max(0,s*max_c m_c-N), epsilon=1/[2(beta+1)], and
C=(1-epsilon)C_0+epsilon C_P. Positivity implies the kernel of this
strict convex mixture is the intersection of its two kernels. On
ker C_0 the star directions are killed by C_P, while the displayed
positive quadratic removes precisely total. Hence ker C is exactly
the span of the three stars and rank C=N-4. Moreover

```
N I-J-C_P = N I-sRR^T >= -beta I,
N I-J-C >= [1-epsilon(beta+1)]I = I/2.
```

Let E_0 be the N by m matrix with first row -1^T and remaining rows I_m.
The credited empty lift sets

```
Q=E_0 C E_0^T,       M=(Q+J_N-sI)/(N-s).
```

Then Q1=0 and the prescribed core entries give disjointness support.
The exact lift equivalences give (N-s)M+sI=Q+J_N>=0 and M<=I.
Since E_0 is injective and Q is perpendicular to J_N,
rank(Q+J_N)=rank C+1=N-3. The strict core upper buffer makes
rank(I-M)=N-1, so the upper endpoint is simple.

For any H certificate, even without its cap, each centered largest-star
indicator chi_(S_i)-(s/N)1 lies in the Hoffman PSD kernel. The three
indicators are independent: evaluate a relation first at the empty set
and then at the three center singletons. Thus every H matrix has
Hoffman PSD rank at most N-3. The constructed matrix attains this bound.

For an intersecting family I of size k>1, z=chi_I-(k/N)1 satisfies
z^T[(N-s)M+sI]z=k(s-k)>=0. Thus k<=s; the center stars attain s.
For any maximum intersecting family I, equality gives
chi_I-(s/N)1 in that same three-dimensional kernel. Write it as
sum_i alpha_i[chi_(S_i)-(s/N)1]. Its size is s>=7, so it excludes empty.
Evaluation at empty gives sum_i alpha_i=1. Evaluation at the center
singletons gives alpha_i in {0,1}, hence exactly one alpha_i=1.
This proves I is exactly one center star. No census or heuristic equality
test is needed for the infinite classification.

## 7. Products and mixed center counts

The credited tensor cap argument applies because every factor spectrum
lies in [-rho_j,1]. Here s_j/N_j<=7/27<1/2, so rho_j<1, the top
eigenspace is one-dimensional, and the lower endpoint has dimension three.
A negative product eigenvalue attains -max_j rho_j only when exactly one
eligible factor is at its lower endpoint and every other factor is at
its top endpoint. A second factor of absolute value below one would
make the magnitude smaller; three or more negative factors do likewise.
The lower multiplicity is therefore 3c. The star formula gives s_P=N_P*p
and rho_P=max_j rho_j, proving the stated rank.

The eligible coordinate-center-star indicators are independent after
centering: evaluate at product empty, and at tuples consisting of just
one eligible center singleton with every other coordinate empty.
They give the unrestricted upper bound N_P-3c on Hoffman PSD rank.
The same evaluations applied to an equality-family indicator force its
coefficients to be zero or one and sum to one, so exactly the 3c eligible
coordinate-center stars are maximum families.

One may also mix these factors with the proved one-center and two-center
complete bipartite factors cited in Section 1. If r_j in {1,2,3} is its
center count, p=max_j(s_j/N_j), and

```
d_P=sum_(j : s_j/N_j=p) r_j,
```

the tensor has maximal Hoffman PSD rank N_P-d_P and exactly d_P maximum
families. This is the same endpoint/equality argument using each cited
factor's simple top endpoint and r_j-dimensional lower endpoint, all
with rho_j<1. It is a conditional application of those established factor
theorems, not a new uncapped tensor rule.

## 8. Reproduction and trust boundary

Use Python 3.11.2 or a compatible Python 3.11 standard library, one process:

```sh
cd spectral_downsets_structural_certificates
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify_three_center_bipartite.py --check
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify_three_center_bipartite.py --check
```

[verify_three_center_bipartite.py](verify_three_center_bipartite.py) regenerates
every polynomial/LDL fixture and rejects three corruptions. It separately
constructs literal families, verifies complete matrix images and full
basis ranks, checks H, the cap, rank and all maximum intersecting families
on 12 base cases with N<=91, and checks a literal N=108 tensor with rank
105 and three eligible stars. Five arbitrary r=3,4,5 face checks make no
PSD/cap claim. Seventeen malformed inputs and three invalid PSD controls
are rejected. It reproduces two published two-center fingerprints exactly.
The balanced-partition control at (2,3) verifies the singleton recoloring,
and the failed boundary formula has the exact negative quadratic above.

The deterministic [expected output](three_center_bipartite_expected.json)
has SHA256

```
4d9dc786265b5e47527b1d5504a18093f212a09bc3473985eaac7b7ee5971072
```

The normal author replay took 79.84 seconds at peak RSS 24,848 KiB; the
optimized replay took 77.19 seconds at 26,412 KiB. Each used one process.
Neither interpreter optimization, sampled matrices nor the expected-output
file establishes the universal theorem alone. Its completeness comes
from the orbit equations, the full incidence/grid decomposition and the
positive coefficient identities covering both infinite regimes, together
with the explicitly complete finite exception lists.

There is no solver, floating-point search, CAS, imported proof corpus or
unfinished enumeration in the proof. The trust base is ordinary counting
and linear algebra plus Python's arbitrary-precision integers/Fraction.
This is not proof-assistant formalization or independent peer review.
The general r>=4 affine/block reduction in Sections 2-3 is reusable;
a capped maximal-rank positive recipe for that range is not proved here.
General spectral Chvátal H remains outside the established coverage.
