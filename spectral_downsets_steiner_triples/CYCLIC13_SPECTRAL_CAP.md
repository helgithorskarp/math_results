# Mean-point certificates and longer Pasch closures at thirteen points

Author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary conditional proof and exact
computer-assisted base theorem; unformalized and independently unreviewed.
The lower PSD theorem, greatest ranks, Pasch stability lemma and eligible
tensor mechanism are inherited. General Spectral Chvatal H and I remain open.

## 1. The new finite theorem

Start with any **existing simple 2-(13,3,l) design admitting a point
automorphism that is one thirteen-cycle**, including every point relabeling.
For l=4,5,6 respectively, apply **any sequence of at most 2,3,4 legal Pasch
switches**. Supports may overlap; no symmetry or decomposition hypothesis
is imposed on any intermediate or final design. Legality means that the
four removed triples are present and all four added triples absent.

Every resulting triple-design downset has a rational, greatest-rank H
matrix with a simple upper endpoint. More precisely, its unchanged parent
centered slack Q_c and sparse repair E satisfy, with K_N=I-J_N/N,

```
Q_m=Q_c+eta E PSD, rank Q_m=N-13,
Q_c|_(1-perp)<B I,
Q_m|_(1-perp)<(N-delta/2)I,
NI-Q_c-delta K_N and NI-Q_m-(delta/2)K_N PSD of rank N-1,
for EVERY REAL 0<eta<=1/1352.
```

Here delta=N-B and the common caps are:

| l | complete fixed-shift bases | initial point budget gamma0 | allowed switches | final point budget gamma | N | s | B | delta | (delta-330/13)/2 |
|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| 4 | 762 | 20 | <=2 | 160/3 | 196 | 37 | 151 | 45 | 255/26 |
| 5 | 1305 | 18 | <=3 | 68 | 222 | 43 | 183 | 39 | 177/26 |
| 6 | 1305 | 18 | <=4 | 254/3 | 248 | 49 | 220 | 28 | 17/13 |

The budgets20,18,18 are the **least common nonnegative INTEGER** values
such that gamma0 K_13-Z is PSD for every design in the corresponding base
cohort. No optimal real budget, optimal cap or maximum possible switch
radius is asserted. A negative principal minor at the preceding integer
proves failure of that point bound, not failure of H or any other matrix.

The earlier [Pasch theorem](PASCH_DEFECT_STABILITY.md), graph8403, proved
<=1,1,2-switch closures using the initial absolute-row budget28 and a
scalar row cap. The present result proves the longer closures by exact
mean-point certificates and a joint comparison of the whole three-layer
Gram bounds from [graph8370](DEFECT_GRAM_CAP.md). The underlying H matrices
were already available for **all** simple triple designs from
[graph8122](UNIFORM_LAMBDA_ALL_ORDERS.md); the new content is these stronger
upper caps and capped closures. Designs, Pasch trades, integer determinants,
Sylvester's criterion and the tensor theorem are not claimed as new.
The joint comparison and complement-defect identity were already used in
[graph8260](DENSE_SCHUR_CAP.md), and are credited here.

## 2. General joint completion-defect criterion

Let U be any existing simple 2-(v,3,l) design, with integer v>=7,l>=2.
Existence, simplicity, constant pair multiplicity and the ensuing
integrality are hypotheses; they imply l<=v-2. Set

```
r=l(v-1)/2, m=v(v-1)/2, b=lv(v-1)/6, s=v+r,
N=1+v+m+b, k=(v-2)(v-3)/2, u=l(l-1)/2, K_v=I-J_v/v.
```

The downset contains empty, every point, every pair and U. Let C be the
point/pair completion matrix and

```
Z=CC^T-(r-u)I-uJ_v,  Z_xx=0,  Z*1=0.
```

Suppose gamma>=0 and **gamma K_v-Z is PSD**. Use exactly the unchanged
weights a,c,d,t,w,h from Section2 of [DEFECT_GRAM_CAP.md](DEFECT_GRAM_CAP.md).
In particular c,d,t,h>0, and w may have either sign. Define the same scalars

```
alphaH=(v-5)r-(v-6)u+3l^2-l,
mu12=w^2(v-2)+d^2(r-u)-2wdl,
mu13=h^2(r-l)-6htu+t^2 alphaH,
zcoef13=2ht+t^2(v-6)>0,
rho12=mu12+d^2 gamma,
rho13=mu13+zcoef13 gamma,
rho23=d^2(v-4)^2(2v-6)/4,
D1=s+l/3+t gamma, D2=s+c, D3=s+t(v-5).
```

Choose positive rational A12,A13,A23 with Aij^2>rhoij and put

```
G=[[D1,A12,A13],[A12,D2,A23],[A13,A23,D3]].
```

**Joint criterion.** Any rational B satisfying

```
B I_3-G PSD,      delta=N-B>g=mk/v^2
```

gives all the centered/repaired upper and lower conclusions of the
parent criterion, with that B and delta, throughout
0<eta<=1/(8v^2). This includes the old B=max_i sum_j G_ij criterion.
It is sufficient only: failure of any comparison has no nonexistence
interpretation. [cyclic13_spectral.py](cyclic13_spectral.py) checks the
initial full point form, all trade legality, and the joint3-by-3 form,
then calls the unchanged parent matrix constructors.

**Proof.** We retain the exhaustive block and mode reductions of graph8370.
For clarity, P is point/pair incidence, B0 point/present-triple incidence,
R pair/present-triple incidence, R_q pair/missing-triple incidence and
H=CR-B0. The complete cross Grams, including the discarded constant terms,
are

```
(wP+dC)(wP+dC)^T=mu12 I+d^2 Z+nu12 J,
(hB0+tH)(hB0+tH)^T
   =mu13 I+zcoef13 Z+nu13 J-t^2(C R_q)(C R_q)^T.
```

Their derivation and nu12,nu13 are in the parent proof. On sum-zero
points the J terms vanish and the missing-triple Gram is subtracted PSD.
Thus the entire point/pair and point/triple cross norms are bounded by
sqrt(rho12),sqrt(rho13). The parent complete-pair decomposition bounds
the entire pair/triple cross norm by sqrt(rho23), and bounds the three
diagonal operators by D1,D2,D3. These are whole-operator bounds, not
samples or a restriction to cyclic eigenspaces.

For a vector in the three sum-zero layers, let z_i be its component
norms. If at least two components are nonzero, the strict Aij bounds give

```
x^T(Q_c-J_N)x < z^T G z <= B ||x||^2.
```

For a single component, D_i<B also holds. Indeed B I_3-G PSD implies
B-D_i>=0, and equality would make the2-by-2 principal minor involving
any other layer equal to -Aij^2<0, impossible. This supplies strictness
even when the comparison is singular. Also B>D1>s. The full constant-layer
restriction, including empty, has just one positive eigenvalue
alpha0=l(v+7)/6+1<s, with all other eigenvalues zero, by the parent proof.
The constants and three sum-zero spaces exhaust the constant complement.
Consequently Q_c|_(1-perp)<B I. No point mode has been omitted.

To recover the old row bound, write B I_3-G as the Laplacian with positive
edge weights Aij plus diag(B-sum_j G_ij). Both summands are PSD when B
is the maximum row sum. Thus this joint criterion includes that case;
its use with the exact completion-defect Grams is the refinement here.

The inherited lower theorem gives rank Q_c=N-v-1 and rank Q_m=N-v with
kernel exactly the v independent centered stars. The unchanged trade
has E*1=0 and ||E||<=4mk. Hence, for every real eta in the entire interval,

```
eta||E||<=mk/(2v^2)=g/2<delta/2,
Q_m|_(1-perp)<(B+g/2)I<(N-delta/2)I.
```

Both upper buffered forms are therefore PSD of rank N-1. They kill the
global constant and are positive definite on its complement. All row,
support and lower rank statements are inherited; small principal forms
are not being used to infer whole-slack PSD. This proves the joint criterion.

## 3. Complete exact base point certificates

For the fixed shift x->x+1 modulo13, all286 triples have orbits of length13,
because a prime-order transitive group cannot stabilize a three-set.
There are22 triple orbits and six pair-distance orbits. Each simple
invariant family corresponds uniquely to a subset of22 triple orbits;
it is a design precisely when all six pair-degree sums equal l.
The complete MITM generator and independent tuple-orbit coefficient DP
from graph8370 are reproduced, with762,1305,1305 candidates for l=4,5,6.
Coverage follows from unique valid candidates and equal independent exact
counts, not from a numerical sample.

The new [cohort checker](verify_cyclic13_spectral.py) rebuilds every pair
degree and every link intersection from literal tuple triples. It compares
all569868 point entries to the completion constructor, and verifies
literal symmetry, zero row sums and circulant structure. There are
335,575,575 different ordered first rows. For each row it uses only the
point permutations x->kx modulo13, k=1,...,12; it verifies all169 entries
of the chosen congruence for each design. Symmetry makes k and13-k
equivalent. There are59,98,98 resulting **point-row** classes, not design
isomorphism classes. No triple-design symmetry is presumed from this
point congruence.

For integer gamma define the integer full point form

```
M(gamma)=13(gamma K_13-Z)=13 gamma I-gamma J-13 Z.
```

For every class representative the checker deletes row and column0 and
computes all12 leading principal determinants using exact integer Bareiss
arithmetic with checked divisions. Every determinant is strictly positive
at the claimed budget. Sylvester's criterion makes the12-by-12 restriction
positive definite. Since M*1=0, for any x the vector y=x-x_0*1 has y_0=0
and x^T M x=y^T M y. Thus the **full** point form is PSD of rank12, with
kernel precisely the point constant. This closes the reduction from the
principal certificate to the full point hypothesis.

The l5 and l6 classes share the same98 point forms. This is the credited
complement identity Z_l=Z_(11-l) from graph8260, not a new identity. The
checker also verifies the entire1305-element complement-mask bijection
and all point entries implied by the common circulant rows. Altogether
there are157 distinct positive12-by-12 forms and1884 positive integer
leading minors. The author's distinct positive-content Schur algorithm
also checks255 full13-by-13 forms, one per class in each cohort. It is not
the determinant algorithm used for the independent positive certificates.

Sharpness among common integer budgets is witnessed by the following
**negative principal determinants of M(gamma0-1)**. Points are zero-based;
the complete first rows and orbit masks are in the compact expected file.

| l | orbit mask | trial integer | principal points | determinant |
|---|---:|---:|---|---:|
| 4 | 23768 | 19 | 1,...,8 | -82756145440215468 |
| 5 | 40920 | 17 | 1,...,8 | -10262329952840524 |
| 6 | 988913 | 17 | 1,...,11 | -125845303518730284769852 |

A PSD matrix has nonnegative principal determinants, so each preceding
integer fails. Decreasing gamma subtracts a PSD multiple of K_13 and
cannot restore positivity. Together with the complete positive coverage,
this proves the least-common-integer claim. It does not identify the
greatest real eigenvalue, and imposes no obstruction to other H matrices.

## 4. Every permitted Pasch sequence

The ordinary stability lemma of graph8403 gives

```
-(50/3) K_13 <= Delta Z <= (50/3) K_13
```

for every legal Pasch switch. Its explicit rational certificate has
determinant4/9 and Young margin2/75. It applies to arbitrary existing
simple designs, with no cyclic assumption, and to overlapping supports.
Starting from Section3 and summing these Loewner bounds proves

```
(gamma0+50h/3) K_13-Z_h PSD
```

for **every** legal h-step sequence. Any shorter sequence satisfies the
same hypothesis at the corresponding maximum budget by adding a PSD
multiple of K_13. Completeness of a closure enumeration is unnecessary;
no closure count is claimed.

At the maximum budgets the exact joint matrices are:

```
l4: G=[[5275/43,15,44],[15,6244/165,34],[44,34,2135/43]], B=151,
l5: G=[[4198/27,16,51],[16,1444/33,34],[51,34,1513/27]], B=183,
l6: G=[[12459/65,18,59],[18,2732/55,34],[59,34,4049/65]], B=220.
```

All three leading principal minors of B I_3-G are positive:

| l | first minor | second minor | third minor |
|---|---|---|---|
| 4 | 1218/43 | 7048301/2365 | 326309834/61017 |
| 5 | 743/27 | 3185989/891 | 108695693/24057 |
| 6 | 1841/65 | 16088188/3575 | 2753237688/232375 |

The positive delta-g margins are twice the last column of Section1.
The checker independently validates all12 comparisons at every shorter
integer path length as well, with36 positive rational leading minors.
The old row criterion fails at each new maximum radius with these budgets;
that is a limitation of the old estimate only. The joint criterion proves
the full upper bound and repair interval asserted in Section1.

The three centered ranks are182,208,234 and repaired ranks183,209,235.
The upper buffered ranks are195,221,247. For rational eta the H matrix is
M_H=(Q_m-sI)/(N-s), with M_H<=I and simple upper endpoint1. Empty is
retained as a vertex with an allowed loop. At eta=1/1352 its slack entry
Q_m(empty,empty)=217/52. All these lower ranks and constructions are
credited to graph8122/8082; independently confirmed lower theorem8204
and parent construction8152 do not review the present upper refinement.

The capped factors also meet the unchanged tensor hypotheses: the density
identity N-2s=(v-1)[(v-2)/2+l(v-6)/6]>0 still holds. For finite factors
on disjoint supports put N_*=product N_j, p=max_j s_j/N_j, and
r_*=sum_(j:s_j/N_j=p)v_j. The credited graph7578/7627 mechanism gives a
product slack of greatest rank N_*-r_* and kernel exactly the greatest-density
centered coordinate stars, with the inherited star-only equality conclusion.
Other factors may be mixed in only within their own proved ranges and repair
choices. This is an inherited, qualified application, not a new product theorem.

## 5. Literal witnesses and reproduction

[verify_cyclic13_spectral_literal.py](verify_cyclic13_spectral_literal.py)
checks three exact paths from the masks in Section3, with2,3,4 legal moves
respectively. It compares every initial and subsequent defect entry with
literal tuple link intersections; each switch satisfies the complete C
update and rank-six identity. It checks42 full small Fraction PSD forms:
three initial point forms,27 step norm/accumulation forms, nine final
point/cross-Gram forms, and three joint comparison forms. It also checks
three complete layer-constant forms, all six full blocks, all incidence and
complement identities, the full sparse-repair transfer,12 supplementary
14-by-14 principal forms, and16 rejection controls.

Consecutive support intersections are4, then4/4, then5/5/5 in the three
paths. Each path has no repeated design state. All13 sorted point-defect
rows of each final design differ, an isomorphism invariant which excludes
any thirteen-cycle automorphism: such a cycle would make points transitive
and force identical row multisets. These are three literal noncyclic
witnesses, not a closure census or an isomorphism count.

CPython3.11.2, standard library only, assertions enabled. Run each command
sequentially with one native thread; do not use python -O.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B spectral_downsets_steiner_triples/verify_cyclic13_spectral.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B spectral_downsets_steiner_triples/verify_cyclic13_spectral_literal.py --check
```

Compact expected results are
[cyclic13_spectral_expected.json](cyclic13_spectral_expected.json) and
[cyclic13_spectral_literal_expected.json](cyclic13_spectral_literal_expected.json).
They contain counts, witnesses, rational margins, matrix hashes and
transcript hashes, not the full pattern or closure corpus. The157-form
positive-minor transcript hashes to
`a16ad9515a1d21453a3c97246c63f7b32c5b53e05fce6215923ef5b2ad82c753`.
Complete input/point transcripts at l4/5/6 are respectively
`7d4166105a2274bd99f03edd6ab5654eaa81c5f1fe914aea46ccafab715e73c7`,
`92d052eb5054fa3d7291dd1f327ba6a8d78aa9ab5e88452904ab5af3f38ba23b`,
`7ce547effa69b53578d6f3fe3efedfee3975ce49e5da653595a568caeeaded5a`.
The source manifest records exact file hashes. Zero whole196/222/248-dimensional
dense slack eliminations are run; the full upper and lower proofs supply
those claims. Prior failed or paused costly eliminations remain outside
this proof and are not treated as nonexistence.

The external trust boundary is exact source execution, independent finite
count completeness and the ordinary unformalized incidence, mode, point
congruence and stability bridges. No floating-point or solver output is a
premise. These checks are author checks, not independent peer review.
The primary target remains Ellis--Filmus--Friedgut,
[Section4 of arXiv2609.28404v1](https://arxiv.org/html/2609.28404v1#S4),
September23,2026; H and I remain explicitly open. This is a structural
capped-factor extension, not a claimed resolution or historical priority.
