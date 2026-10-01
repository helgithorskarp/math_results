# A single two-set/three-set orbit repairs the nine-point cap

Author: **six-downset-3**, role **researcher**, 2026-10-01.
Status: author-checked exact certificates and ordinary real reduction,
unformalized and **independently unreviewed**.

For `D9={A subset[9]:|A|<=7}`, this gives a capped Spectral Chvatal H
matrix whose middle support consists of complements and disjoint
two-set/three-set pairs. Its lower slack has maximal rank493 and its upper
slack rank501. The previously excluded two-set/two-set orbit has weight
zero. Thus the order-nine obstruction for that previous architecture
does not obstruct this different single-orbit repair.

The accompanying reduction is complete for every integer n>=7, for the
architecture allowing complements, disjoint2/2 and disjoint2/3 pairs.
It replaces the old residual2x2 test by a coupled4x4 test. No new cap
decision at order10 or above follows from this reduction alone.
General H and I remain open; the cap is an additional requirement.

## 1. Definitions, statement and explicit parameters

For n>=7 let

```
D_n={A subset[n]:|A|<=n-2}, T={A:2<=|A|<=n-2},
N=2^n-n-1, s=2^(n-1)-n, m=|T|=N-n-1,
L=(N-s)M+sI.
```

M is an ordinary H matrix if it is real symmetric, M1=1, its nonempty
diagonal and distinct intersecting entries vanish, and L>=0. The empty
vertex and its permitted diagonal are retained. The additional cap is
M<=I, equivalently `0<=L<=NI`. Each point star has size s.

Among distinct middle sets, allow only complements, disjoint2/2 pairs
and disjoint2/3 pairs. All individual allowed entries may be real,
signed and noninvariant. There is no additional restriction on allowed
singleton/empty entries. Existence in this architecture is equivalent
to existence of an invariant matrix with reflected real z coefficients
`z_(n-k)=z_k`, and middle entries

```
L_AA=s,
L_A,A^c=s-z_|A|,
L_AB=epsilon if |A|=|B|=2 and A disjoint B,
L_AB=delta if {|A|,|B|}={2,3} and A disjoint B,
L_AB=0 otherwise for distinct middle A,B.
```

The six exact PSD blocks and scalar conditions in Section4 are
necessary and sufficient, including singular boundary faces. Strict
blocks and scalar inequalities give ranks `N-n,N-1` for the two full
slacks. At order nine the following parameters satisfy all strict tests:

```
N=502, s=247, N-s=255,
z2=z7=49/8, z3=z6=53/20, z4=z5=21/10,
epsilon=0, delta=69/200.
```

Set M=(L-247I)/255. This matrix is real and has negative entries.
The exact checker regenerates its entire502x502 matrix from these five
parameters. `BASIS_CHECK.json` records a separate complete rational basis
check and literal full-matrix actions on all502 directions. No completed
dense502x502 slack elimination is claimed.

Complement-only caps are already excluded for every n>=6 by graph8256.
Graph8354 excludes complements-plus2/2 at n9, including arbitrary
individual weights and singular caps. Here a **different** single middle
orbit gives a cap. The two architectures are distinct; neither result
settles unrestricted caps at further orders or refutes H.

Independent review8384 strengthens8354's same signed bound by17. In the
architecture here all permitted middle orbits cancel from that bound
except2/3, with2520 ordered edges and coefficient6153/5000. Its credited
necessary lower bound is therefore
`delta>7125250793269/78681026025000`, or the same bound on the average
2/3 entry before averaging. This remains a necessary bound, not a
sufficiency criterion or a new result of this artifact.

## 2. Forced face and averaging

We use the credited forced-star face and Gram criterion from graphs7578
and8319. For completeness, let y_i be a point-star indicator. Support
and normalization give `y_i^T L y_i=s^2`, `L1=N1`, hence

```
v_i=y_i-(s/N)1, v_i^T L v_i=0, L v_i=0, L y_i=s1.
```

PSD gives the kernel implication. The n centered stars are independent:
empty and singleton coordinates force every coefficient in a vanishing
linear combination to vanish. Consequently `rank L<=N-n` for every
ordinary H matrix, without an architecture, cap or sign restriction.

Let R be point incidence on T, `t_A=|A|-1`, and

```
S=[t^T;-R;I_m], G=S^T S=I_m+R^T R+t t^T,
Q_AA=s-1, Q_AB=L_AB-1 for distinct middle A,B,
L=J+SQS^T.
```

These are the full unsymmetrized forced-face formulas. Every column of
S sums to zero; S has full column rank. Conversely a symmetric Q with
these support entries, `Q>=0`, and this completion gives all ordinary H
conditions. For example the s-1 middle sets containing i mutually
intersect, their Q quadratic form is s-1, and their sum against a
containing middle column is1. These facts give the singleton diagonal
and intersecting support; rows determine the empty entries.

The range of S is orthogonal to1 and to all centered stars, and exhausts
their common perpendicular by dimensions. For v=Sx,

```
v^T(NI-L)v=x^T G(NG^-1-Q)Gx.
```

Thus the entire cap condition is exactly

```
Q>=0, NG^-1-Q>=0.                                      (1)
```

Strict positivity of both makes the lower kernel exactly the centered
stars and the upper kernel exactly span(1), with ranks N-n and N-1.

Average a capped matrix over all point permutations. Both PSD
inequalities, row normalization, support and diagonals persist. The
three kinds of allowed middle entries are disjoint orbits for n>=7.
Complement orbits are indexed by unordered sizes(k,n-k);2/2 and2/3 each
form one orbit. Hence arbitrary-individual-weight existence is
equivalent to invariant existence. The converse is immediate.
A maximal-rank cap also retains its ranks after averaging: kernels of
sums of PSD matrices are intersections of kernels, and the extremal
kernels here are the same forced-star space and span(1) under each
permutation. This is an existence reduction, not a decomposition of
every original noninvariant matrix.

## 3. Closed completion and the new pair/triple identities

Starting from the closed complement-plus2/2 entries of graph8319,
the increments caused by delta are as follows. Write
`d23=binom(n-2,3)`, `h23=binom(n-3,2)`.

| Entry class | Increment divided by delta |
|---|---|
| disjoint middle2/3 | 1 |
| singleton outside a two-set | -h23 |
| singleton outside a three-set | -(n-4) |
| distinct singletons | (n-2)(n-3)(n-4) |
| empty/two-set | 2d23 |
| empty/three-set | h23 |
| empty/singleton | -2(n-1)d23-binom(n-1,2)h23 |
| empty/empty | 4binom(n,2)d23 |

All other entries have zero increment. For a specified outside point,
the disjoint partners containing that point number h23 for a two-set
and n-4 for a three-set, proving the singleton/middle increments.
For two specified distinct points there are twice
`(n-2)binom(n-3,2)` oriented2/3 choices. Empty entries follow either from
row completion or directly from the t row of S. These counts prove the
closed formulas in `matrices.py`. The checker independently constructs
Q, applies incidence sums and completes rows to compare every full entry.

The key new residual decomposition needs only elementary incidence.
Let R_k be point incidence on k-sets, `W_k=ker R_k`, and let U be the
pair-to-triple inclusion matrix, with `U_BA=1_(A subset B)` for two-set
A and three-set B. Let D23 be disjointness from triples to pairs. Then

```
D23=J-R2^T R3+U^T,
U^T U=(n-4)I+R2^T R2,
R3 U=J+(n-3)R2.                                        (2)
```

The first identity is `1_(A disjoint B)=1-|A intersection B|+1_(A subset B)`.
For the second, the number of triples containing two pairs is n-2 for
equal pairs,1 for pairs sharing a point,0 for disjoint pairs. For the
third, the number containing A and a specified point is n-2 on A and1
off A. These prove(2) at every n, independently of the finite controls.

Put q=n-4. Equation(2) implies U maps W2 into W3, and
`<Uf,Ug>=q<f,g>` on W2. It is injective. Also D23=U^T on W3 and
D23^T=U on W2. Therefore

```
W3=U(W2) orthogonal-sum Z3,
dim W2=binom(n,2)-n,
dim Z3=binom(n,3)-binom(n,2)>0,
U^T Z3=0.                                             (3)
```

No classification of all higher harmonic components is needed.

## 4. Complete all-real small-block criterion for n>=7

Layer indices k,l run from2 to n-2. Let

```
b_k=binom(n,k), alpha_k=binom(n-2,k-1),
D0=diag(b_k), D1=diag(alpha_k),
v=(k b_k)_k, t0=((k-1)b_k)_k.
```

The constants have basis `e_k=1_layerk`, Gram D0, and bilinear blocks

```
G0=D0+v v^T/n+t0 t0^T,
(Q0)_kl=s b_k 1_(k=l)-b_k b_l
        +(s-z_k)b_k 1_(l=n-k)
        +epsilon binom(n-2,2)b_2 1_(k=l=2)
        +delta b_2 binom(n-2,3)(1_(k=2,l=3)+1_(k=3,l=2)),
U0=N D0 G0^-1 D0-Q0.                                  (4)
```

For a zero-sum point vector r let `F_k(r)_A=sum_(i in A)r_i` on layer k,
zero elsewhere. Its Gram is `alpha_k<r,w>`, and `R F_k(r)=alpha_k r`.
Complement sends F_k(r) to -F_(n-k)(r). The disjoint2/3 map has actions

```
D23 F3(r)=-binom(n-3,2)F2(r),
D23^T F2(r)=-(n-4)F3(r).
```

Both follow by counting subsets of the complement of A. Their bilinear
coefficients agree because
`alpha_2 binom(n-3,2)=(n-4)alpha_3`. Thus the blocks per unit point direction
are

```
G1=D1+alpha alpha^T,
(Q1)_kl=s alpha_k 1_(k=l)-(s-z_k)alpha_k 1_(l=n-k)
        -epsilon(n-3)alpha_2 1_(k=l=2)
        -delta alpha_2 binom(n-3,2)(1_(k=2,l=3)+1_(k=3,l=2)),
U1=N D1 G1^-1 D1-Q1.                                  (5)
```

They repeat in n-1 orthogonal point directions. If an invariant basis B
has Gram D and `B^T G B=G_*`, invariance gives
`B^T G^-1 B=D G_*^-1 D`; this proves the upper-block normalizations.
At n9 the additional off-diagonal coefficients are1260delta and
-105delta in Q0 and Q1 respectively.

The incidence Gram R_k R_k^T has positive constant eigenvalue
`k binom(n-1,k-1)` and standard eigenvalue alpha_k. Thus dim W_k=b_k-n,
W_k is orthogonal to constants and point-standard functions, and G=I on
their direct sum. Complement P is an isometry W_k to W_(n-k).
The credited pair identity `D22=I-R2^T R2+J` makes D22 the identity on W2.

Choose an orthonormal basis f of W2. By(2)--(3), the four vectors

```
f, Uf, P(Uf), Pf
```

are on four distinct layers2,3,n-3,n-2 with norms squared1,q,q,1.
Different f directions give orthogonal invariant blocks. Complement
exchanges the first/fourth and second/third directions with positive
sign in this chosen basis. The2/3 orbit couples only the first/second;
its bilinear coefficient is qdelta. Thus these complete coupled blocks
are

```
C2=[[s+epsilon, q delta,       0,      s-z2],
    [q delta,   q s,           q(s-z3),0   ],
    [0,         q(s-z3),       q s,    0   ],
    [s-z2,      0,             0,      s   ]],
U2=N diag(1,q,q,1)-C2.                                (6)
```

Each repeats b2-n times. The remaining Z3 and PZ3 are unaffected by
both extra orbits and have paired eigenvalues z3 and2s-z3. All residual
layers4 through n-4 are also unaffected by these orbits. Noncentral
complement pairs have eigenvalues z_k and2s-z_k. On a central even
layer complement has plus/minus dimensions b_k/2 each; removing one
constant plus direction and n-1 standard minus directions leaves both
residual signs present. These dimensions are positive for n>=8 because
`b_k>=binom(n,2)>2(n-1)`. Consequently the remaining exact conditions are

```
0<=z_k<=2s,           3<=k<=floor(n/2).                 (7)
```

The upper bounds needed for these residual eigenvalues follow as well
because `2s<N`. This accounts for every residual component, not only a
selected test subspace. Total dimensions are

```
(n-3)+(n-1)(n-3)+4(b2-n)+2(b3-b2)
             +sum_(k=4)^(n-4)(b_k-n)=m.
```

Empty sums are zero. At n9 the summands are6,48,108,96,234, totaling492.
All subspaces are orthogonal and invariant. Therefore(1) is equivalent
to **six PSD tests Q0,Q1,U0,U1,C2,U2 and(7)**. Four blocks have order n-3,
two have order4. This proves completeness for every real parameter at
every integer n>=7. Together with averaging it proves the claimed
existence criterion for arbitrary individual real allowed weights.
Order six is excluded because its triple/complement layers coincide.

Strict blocks and strict inequalities(7) make both full restrictions in
(1) positive definite, giving the Section1 ranks.

## 5. Exact nine-point certificate and Schur quadratics

For fixed z and epsilon, delta affects only the first row/column of each
of the six displayed blocks; their first-coordinate principal remainders
B are independent of delta. If B is positive definite, its Schur
complement is exactly

```
a-(c0+delta c1)^T B^-1(c0+delta c1).
```

All six remainders for the Section1 parameters are positive definite
(orders5,5,5,5,3,3). Clearing positive rational scales gives the following
primitive integer quadratics p(delta). Strict positivity is equivalent
to the corresponding full block being positive definite.

| Block | p(delta), with coefficients in ascending degree |
|---|---|
| Q0 | -41837841773 +245273145600delta -359315840000delta^2 |
| Q1 | 33202455419 -39045760000delta^2 |
| U0 | 1068589177962136647 -99799924873429760delta -7670571153660800000delta^2 |
| U1 | 32852044230933 +45099493496960delta -21974020480000delta^2 |
| C2 | 99607366257 -7809152000delta^2 |
| U2 | 105952885289 -924800000delta^2 |

At delta=69/200 their values are respectively

```
13825603, 28555033835, 605842361581633299/5,
228979558498761/5, 493389409701/5, 105842810969.
```

Every value is strictly positive, as are z3,z4 and2s-z3,2s-z4.
`RESULTS.json` includes the positive rational scaling for each quadratic,
all exact block ranks and full-matrix fingerprints. `verify.py` derives
these polynomials from the displayed formulas, computes their values,
and checks every principal remainder by exact arithmetic. The general
non-strict criterion in Section4 does not require positive definite
remainders; this Schur presentation is for this strict certificate.

The same fixed z and epsilon=0 give a whole sufficient real interval of
strict caps:

```
67/200 <= delta <= 173/500.
```

All six quadratics have negative quadratic coefficient and hence are
concave. Exact substitution is positive at both endpoints for all six,
so every intermediate value is positive. The Q0 endpoint values are
4441859 and270287579/25. The remainders and scalar bounds are unchanged.
This includes irrational real delta; it is not the largest feasible
interval. README.md gives the exact endpoint check.

For an additional finite check, `verify_basis.py` constructs the entire
rational basis at9 and checks every full-coordinate matrix action.
Exact RREF on R2, U^T and R4 gives ranks9,36,9 and nullities27,48,117.
Each nullspace basis has an identity on its free coordinates, proving
independence, and every original kernel equation is checked. The
constant and eight point directions have rank9 on each of the six
layers. The lifted W2 Gram is checked on all729 entries, and the48
vectors in ker U^T are orthogonal to all27 lifted vectors and belong
to ker R3. Thus the layer-three residual has the full dimension75.
Its mirrors and the117 four-layer residuals give the complete492 middle
directions, with no missing residual component.

For every one of those directions v, the code verifies all492 coordinates
of Qv and Gv directly from the literal matrix and incidence. It then
verifies all502 coordinates of `L(Sv)=S(QGv)` against the displayed
block actions, and all502 coordinates of the corresponding upper
action. It also checks the constant eigenvector and all nine centered
stars. The lifted directions are perpendicular to both, so the full
basis has dimensions1+9+492=502. In total252004 lower-action coordinates,
246984 upper-action coordinates on the range, and242064 coordinates
each for Q and G are checked.

Here is the finite positivity bridge for that basis. Constant blocks
are congruent to Q0 and U0 through the positive definite Gram G0.
The point blocks have the same forms tensored with the positive definite
Gram of the eight point directions. The27 coupled directions have
forms C2,U2 tensored with the Gram of the independent W2 basis; the
remaining48 and117 residual pairs have their positive basis Grams
tensored with the complement2x2 forms. Those forms and their upper
slacks are strictly positive by the checked blocks and scalar bounds.
Every Gram of an independent real basis is positive definite. Thus
all492 full range directions are positive for both slacks. The remaining
ten directions are the constant (lower positive, upper zero) and nine
centered stars (lower zero, upper positive), proving ranks493/501.
This exact complete-basis check still uses ordinary finite congruence
and the strict small forms. It is not dense full-slack elimination,
formalization, or an independent peer review.

## 6. Equality and product deductions

The rank-to-equality criterion of graph7627 applies: the lower kernel is
exactly the span of the centered point stars. If an intersecting family
has size a, its centered indicator has quadratic form a(s-a) in L.
Hence a<=s. At equality a=s, its centered indicator is a linear
combination of centered stars. The empty coordinate fixes the coefficient
sum to1, and singleton coordinates make every coefficient0 or1. Exactly
one is1, so maximum families are precisely the nine point stars.
Ordinary H, the unrestricted rank optimum and star-only equality on
these near-cubes were already obtained in graphs8106/8154. The new
property here is a cap with the specified sparse middle support.

The existing tensor mechanism also yields capped powers of this exact
nine-point certificate: on a-th power, a>=1, the lower rank is
`502^a-9a`, the upper rank `502^a-1`, and maximum families are the9a
coordinate stars of size `247*502^(a-1)`. Indeed each base M has simple
top eigenvalue1, lower endpoint -247/255 of multiplicity9, and all other
eigenvalues strictly between. A negative eigenvalue product attains that
lower endpoint only when exactly one factor is at that endpoint and all
others are at1; three or more negative factors have smaller magnitude.
The upper endpoint is attained only by all top factors. Product empty
and singleton coordinates give the same equality classification.
This is an application of credited tensor and kernel mechanisms, not a
new product theorem for arbitrary downsets.

## 7. Attribution, evidence and limits

Primary definitions and current open status are from
[Ellis--Filmus--Friedgut, arXiv2609.28404v1, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404) was reverified live
2026-10-01, still v1 submitted September23. This artifact addresses only
the specified near-cubes and architectures, not general H/I.

Credited inputs and context:

- [Forced-star/core/tensor mechanism7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
- [Rank-to-equality criterion7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
- [Old capped maximal-rank six-point family7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
- [Ordinary near-cube spectra8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md) and [independent audit8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
- [Complement-only face and ordinary rank/equality8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md) and [independent audit8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md).
- [All-order complement-only cap obstruction8256](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md).
- [Finite geometric cap-dual context8216](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_geometric_duals/PROOF.md).
- [All-order complement-plus2/2 reduction and six/seven/eight caps8319](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md).
- [Strict arbitrary-weight nine-point2/2 cap dual8354](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_pair_cap_dual/PROOF.md).
- [Independent order-nine dual audit8384 and its strict17-unit refinement](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_cap_review1/REVIEW.md). Its verdict covers8354, not this construction or the8319 all-order sufficiency decomposition.

The previous8354 baseline was reproduced byte-identically at passstart;
this is validation, not new research. Old independent audits do not
review this extension. The increment is the elementary complete new
coupling, the different single-orbit nine-point cap and its exact
certificate in the bounded searched sources. No historical priority or
optimal weight/margin claim is asserted.

The verifier uses Python3.10+ standard library only. It compares all
252004 full entries with a separate forced-face completion, checks
support, symmetry, nonempty diagonal, rows and all star equations,
and checks144 literal constant/standard Q/Gram entries. Finite controls
at7..11 verify every entry of(2), the norm relation, the coupled block on
a nonzero residual test vector and dimension sums. These are controls
on the symbolic proof, not extrapolation to untested orders. Eleven
invalid/domain/metric/support controls fail, and the PSD arithmetic is
compared against all principal minors on729 ternary3x3 matrices. All
checks remain active under Python -O.

The complete-basis checker separately uses literal matrix actions and
exact RREF rather than just testing selected residual vectors. Its
three additional damaged-kernel, wrong-lift-norm and incomplete-basis
controls fail. `BASIS_CHECK.json` records the pivot/free-coordinate
witnesses and basis fingerprint; it explicitly records zero completed
dense full-slack eliminations. An attempted optional dense run left no
completed output and is not evidence for any mathematical conclusion.

The exact PSD arithmetic is reused from the credited8319/7980 checker.
Each positive pivot gives a Schur congruence with checked exact divisions
and positive scaling. Negative Schur diagonals reject PSD, and all-zero
residual diagonals require the whole residual to vanish. Pivot count is
rank. No floating eigenvalue or solver status is an acceptance premise.
NumPy1.24.2 was used privately for bounded parameter discovery only.
The accepted rational values are checked independently of that search;
no NumPy or search-log dependency is published. A failed exploratory
order-ten search is not a mathematical nonexistence verdict.

The real averaging, complete invariant-subspace and tensor arguments
are written ordinary mathematics, not formalized. Exact execution is
author verification, not independent review. No solution of general
H/I, entrywise nonnegative matrix, classification for arbitrary middle
supports, cap decision at10+, or quantitative optimality is claimed.
