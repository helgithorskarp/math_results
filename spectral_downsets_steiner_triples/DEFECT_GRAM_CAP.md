# Completion-defect Gram caps and the cyclic thirteen-point cohort

Author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary criterion and exact computer-assisted
cohort corollary; unformalized and independently unreviewed. The lower PSD/rank
theorem is inherited and independently confirmed. General Spectral Chvatal
Conjectures H and I remain open.

## 1. Conditional theorem and new finite corollary

Let U be any **existing simple 2-(v,3,l) design**, with integer v>=7,l>=2.
Existence, simplicity, constant pair multiplicity and the integrality below
are hypotheses, and imply l<=v-2. Put

```
r=l(v-1)/2, m=v(v-1)/2, b=lv(v-1)/6,
s=v+r, N=1+v+m+b, k=(v-2)(v-3)/2, q=v-2-l, u=l(l-1)/2.
```

Let the downset contain empty, every point, every pair and U. Use exactly
the parent centered matrix Q_c and sparse trade E from
[the all-orders construction](UNIFORM_LAMBDA_ALL_ORDERS.md), graph8122.
For a pair p, let T(p) be its l completing points. Define the symmetric
point defect by Z_xx=0 and

```
Z_xy=|{p:x,y in T(p)}|-u, x!=y;   Z*1=0.
```

Write K_v=I-J_v/v. Suppose gamma>=0 and **gamma K_v-Z is PSD**. A sufficient
checkable hypothesis is max_x sum_y |Z_xy|<=gamma. Let c,d,t,w,h be the
unchanged weights displayed in Section2, and define

```
alphaH=(v-5)r-(v-6)u+3l^2-l,
betaH=(v-6)u+l^2(v-4)+l,
mu12=w^2(v-2)+d^2(r-u)-2wdl,
nu12=w^2+d^2u+2wdl,
mu13=h^2(r-l)-6htu+t^2 alphaH,
zcoef13=2ht+t^2(v-6),
nu13=h^2 l+6htu+t^2 betaH,
rho12=mu12+d^2 gamma,
rho13=mu13+zcoef13 gamma,
rho23=d^2(v-4)^2(2v-6)/4,
D1=s+l/3+t gamma, D2=s+c, D3=s+t(v-5).
```

These rho quantities are nonnegative under the point-defect hypothesis,
as they bound positive semidefinite cross Grams. Choose any positive
rational A12,A13,A23 with Aij^2>rhoij. The implementation chooses the
least strictly adequate positive integer. Define

```
G=[[D1,A12,A13],[A12,D2,A23],[A13,A23,D3]],
R1=D1+A12+A13, R2=D2+A12+A23, R3=D3+A13+A23,
B=max(R1,R2,R3), delta=N-B, g=mk/v^2.
```

If **delta>g**, then

```
Q_c|_(1-perpendicular) < B I,
for every real 0<eta<=1/(8v^2), Q_m=Q_c+eta E is PSD of rank N-v,
Q_m|_(1-perpendicular) < (N-delta/2)I.
```

The centered lower rank is N-v-1. With K_N=I-J_N/N, both
NI-Q_c-delta K_N and NI-Q_m-(delta/2)K_N are PSD of rank N-1,
positive definite on 1-perpendicular. Both slacks have row sums N,
nonempty diagonal s and zero distinct entries on intersections. The
repaired kernel consists of precisely the v independent centered stars.
Rational eta gives a rational H matrix M=(Q_m-sI)/(N-s) with M<=I and
a simple upper endpoint1. The conditional criterion does not assert that
every design satisfies its point bound or its scalar margin. Its failure
proves no nonexistence or failure of H.

**New finite corollary.** Every simple 2-(13,3,l) design admitting a point
automorphism that is a single13-cycle, for l=4,5,6, satisfies the criterion
with the common gamma=28. In labels where the cycle is x->x+1 modulo13,
the complete cohort has the following exact sizes and uniform caps:

| l | fixed-shift labelled designs | N | s | A12,A13,A23 | B | delta | delta-g |
|---|---:|---:|---:|---|---|---|---|
| 4 | 762 | 196 | 37 | 12,35,34 | 16720/129 | 8564/129 | 68762/1677 |
| 5 | 1305 | 222 | 43 | 12,38,34 | 3788/27 | 2206/27 | 19768/351 |
| 6 | 1305 | 248 | 49 | 12,40,34 | 9719/65 | 6401/65 | 4751/65 |

Here g=330/13, eta_max=1/1352, and the positive strict transfer margins
are respectively34381/1677,9884/351,4751/130. These are (delta-g)/2;
the preceding column is twice that margin. The worst absolute row defect
is exactly28 in each cohort. The three centered/repaired ranks are
182/183,208/209,234/235; both upper ranks are195,221,247 respectively.

The scope is **3372 fixed-shift labelled designs**, with all point relabelings
covered by permutation congruence. It is not a count of full isomorphism
classes, and is not a claim about all thirteen-point designs. No symmetry
is required for the conditional criterion itself. The existing sparse
range v>=3l+8 (graph8313) and dense range v>=12,3v>=7q+10 (graph8260)
both exclude these three parameter pairs. Their lower H matrices were
already covered by8122. The new information is the reusable defect-Gram
criterion and the capped, greatest-rank factors in these intervening cohorts.
No design novelty, optimal cap, optimal threshold or historical priority
claim is made.

## 2. Exact new Gram mechanism

The unchanged weights, with no exceptional orders needed at v>=7, are

```
D0=l(v^2-10v+27)-6,
a=-l/3,
c=[v^2-(l+3)v+11l/3]/[(v-2)(v-3)],
d=(v^2-v-4)/[(v-4)(v-3)],
t=(v-1)[l(v-3)-6]/D0,
w=s-(v-3)c-(r-2l)d,
h=s-(v-4)d-(r-3l)t.
```

D0,c,d,t,h are positive throughout this domain; no sign assumption on w
is needed. To see this, write v=7+x, x>=0. Then
D0=l(x^2+4x+6)-6>=6, and l(v-3)-6>=2. For c, its numerator multiplied
by3 is decreasing in l and, at l=v-2, equals8v-22>0. Finally

```
h=Hnum/[(v-3)D0],
Hnum=3l^2v^2-12l^2v+9l^2+lv^3-12lv^2+11lv+36l+12v-24,
Hnum at v=7+x
=12(l-1)(6l-5)+[10l(3l-1)+12]x+3l(l+3)x^2+lx^3>0.
```

Let P,C be point/pair incidence and completion incidence, B0 be
point/present-triple incidence, and R,R_q be pair/present-triple and
pair/missing-triple incidence. H_xA counts, with multiplicity, pairs of A
completed by x, with H_xA=0 inside A. The notation B0 avoids confusion
with the scalar cap B. The parent identities, all credited to8122, are

```
PP^T=(v-2)I+J, B0 B0^T=(r-l)I+lJ,
CC^T=(r-u)I+uJ+Z, CP^T=PC^T=l(J-I),
PR=2B0, CR=B0+H, RB0^T=lP^T+C^T,
HB0^T=B0H^T=Z+3u(J-I).
```

In particular, the mixed HB0 identity is **not new here**. The credited
complete-pair identity from the preceding dense proofs is

```
RR^T+R_q R_q^T=(v-4)I+P^TP.
```

Define F=C R_q. It is the incidence of present-design completions along
the pairs of missing triples. A missing triple has no inside completion
from the present design. Thus F is nonnegative, with row sum qr and
column sum3l. The completion-defect identity used here is

```
HH^T=alphaH I+(v-6)Z+betaH J-FF^T.                 (1)
```

For a direct derivation, H=CR-B0 and

```
CRR^T C^T=(v-4)CC^T+l^2 I+l^2(v-2)J-FF^T,
CRB0^T=l^2(J-I)+CC^T.
```

Expanding HH^T gives
(v-6)CC^T+3l^2 I+l^2(v-4)J+B0B0^T-FF^T, hence(1).
The missing triples contribute a **subtracted positive semidefinite term**.
Set A=wP+dC and T=hB0+tH. The exact full point Grams are

```
AA^T=mu12 I+d^2 Z+nu12 J,                         (2)
TT^T=mu13 I+zcoef13 Z+nu13 J-t^2 FF^T.            (3)
```

All matrices have regular row and column sums and preserve the respective
sum-zero spaces. On sum-zero points, the J terms vanish, and (1)-(3),
gamma K_v-Z PSD and zcoef13>0 give

```
||A||^2<=rho12, ||T||^2<=rho13.
```

These are bounds for the **whole cross operators** on the indicated
sum-zero spaces, not sampled columns or a restriction to cyclic modes.
The same point defect controls the point diagonal and both couplings.

## 3. Exhaustive modes, strictness and repair

Put L=Q_c-J_N. Its empty row is zero. Regularity separates the full
constant-layer space from the sum-zero point, pair and present-triple
spaces. On the latter spaces the six exact blocks are

```
L11=(s+l/3)I+tZ,
L22=(s+c)I-cP^TP,
L33=(s-t)I+tR^TR-tB0^TB0,
L12=-wP-dC, L13=-hB0-tH,
L23=d(R-P^TB0)=d(I-P^TP/2)R.
```

The first two diagonal upper bounds are D1,D2. For the third let Pi
project pair space onto ker P. On sum-zero triples z, PRz=2B0z and
PP^T=(v-2)I on sum-zero points give the orthogonal decomposition

```
Rz=Pi Rz+2P^TB0z/(v-2),
||Rz||^2-||B0z||^2
=||Pi Rz||^2+[4/(v-2)-1]||B0z||^2 <=(v-4)||z||^2.
```

The coefficient is nonpositive at v>=7, and the complete-pair identity
gives ||Pi R||<=sqrt(v-4). Thus L33<=D3 I. That identity also gives
||R||<=sqrt(2v-6) on sum-zero triples. On sum-zero pairs, P^TP has
eigenvalues0,v-2, so ||I-P^TP/2||=(v-4)/2. Consequently
||L23||^2<=rho23. This composition estimate is inherited from the preceding
dense analysis and its independent reviews. Equations(2),(3) bound the
other two cross blocks without separately adding their component norms.

All three cross norms are strictly below the chosen Aij. For a vector
in the three sum-zero layers put its component norms into z. If at least
two components are nonzero, one strict cross comparison gives
x^TLx<z^TGz<=B||x||^2. The last inequality follows from the symmetric
absolute-row bound, since G has positive entries. With only one nonzero
component, Di<Ri<=B supplies strictness. This proves L<B I on every
nonconstant mode; it makes no strict diagonal assumption.

The inherited full constant-layer form, including empty, is PSD of rank1
with its only positive eigenvalue alpha0=l(v+7)/6+1. Its nullspace contains
the global constant. The exact gap
s-alpha0=v-1+l(v-5)/3>0 and B>s show alpha0<B. These two invariant spaces
exhaust1-perpendicular, where J_N vanishes. Thus Q_c|_(1-perp)<B I.

The independently confirmed lower theorem8122 gives centered rank N-v-1
and repaired PSD rank N-v throughout the real interval
0<eta<=1/(8v^2). The unchanged trade kills constants and stars and has
||E||<=4mk. Hence eta||E||<=g/2<delta/2 and

```
Q_m|_(1-perp)<(B+g/2)I<(N-delta/2)I.
```

The full upper rank claims follow. The lower ranks and kernels are inherited,
not inferred from the small principal checks below. The density identity
N-2s=(v-1)[(v-2)/2+l(v-6)/6]>0 permits the existing tensor mechanism:
for finitely many such factors on disjoint supports, put
N_*=product N_j, p=max(s_j/N_j), r_*=sum_(j:s_j/N_j=p)v_j.
The resulting product slack has greatest possible rank N_*-r_* and kernel
exactly the greatest-density centered coordinate stars; maximum intersecting
families are exactly these stars. This follows from the credited tensor
theorem7578 and capped-factor criterion7627. Mixed products may include
previously capped factors only in their separately proved ranges, with their
proved repair choices. Classical strict EKR for the base designs is inherited.

## 4. Complete finite coverage and reproducibility

For a fixed shift on thirteen labels, every triple orbit has length13:
an orbit stabilizer in the prime-order group is either trivial or the
whole group, and a three-set cannot be fixed by a transitive thirteen-cycle.
The286 triples partition into22 such orbits. Simplicity and shift invariance
therefore identify each possible family with a unique subset of22 orbits.
The78 pairs partition into six orbits, indexed by distances1,...,6. Each
triple orbit has a six-coordinate pair-degree signature with nonnegative
integer entries summing to3. A selected subset is a 2-(13,3,l) design
exactly when the sum of signatures equals(l,l,l,l,l,l).

[cyclic13_gram.py](cyclic13_gram.py) splits the22 orbits into two halves.
Its2048 subsets per half and exact signature matching cover all2^22
invariant simple families. It generates unique designs; no multiplier
or full-isomorphism quotient is used. Independently,
[verify_defect_gram.py](verify_defect_gram.py) constructs the orbits from
tuples instead of bit masks and evaluates the coefficient of
x1^l...x6^l in product_o(1+x^signature(o)), by a truncated integer DP.
Truncation is complete since every exponent is nonnegative. The resulting
counts762,1305,1305 agree with the unique generated valid-design counts.
Cardinality equality with a valid subset proves coverage independently.

Every one of the3372 actual designs then has all78 pair degrees checked
directly. For each point x construct its set of link pairs; the codegree
in Z_xy is exactly the intersection size of the two link sets. The checker
examines all569868 defect entries, including526032 off-diagonal link
intersections, checks Z1=0 and literal cyclic symmetry, and certifies every
absolute row sum<=28. Its cohort transcript SHA256 is
`44b4eabd4e7c54bb771fc95fe27fa3e659ff23f834aaf604c6598b88592940f2`.
The compact [cohort output](defect_gram_expected.json) records the complete
counts, defect histograms, common scalar caps, and exact positive square
margins. No census or matrix dump is needed as input. Any point relabeling
transports the matrix and all inequalities by permutation congruence.

[verify_defect_gram_literal.py](verify_defect_gram_literal.py) independently
reconstructs three first worst-row fixtures, orbit masks23768,40920,106488
in multiplicities4,5,6. It checks support, row/star equations, every one
of the six full Q_c-J blocks with J terms retained, the complete constant
space, all parent incidence/complement identities, all entries of(1)-(3),
the full RB0^T identity and both small Gram upper bounds. It checks nine
13-by-13 Fraction PSD forms, three3-by-3 comparison forms, and twelve
supplementary14-by-14 principal forms, plus kernel Gram ranks and hashes.
It verifies the **full-entry** upper transfer identity and its positive
norm margin for eta=1/1352. Fifteen rejection controls detect damaged
designs, defects, blocks, outside multiplicities, intervals and false PSD
forms. [Literal output](defect_gram_literal_expected.json) distinguishes
ranks supplied by the written proof from directly eliminated small forms.
**Zero full196/222/248-dimensional dense slack eliminations are run.**

An optional independent [SymPy derivation](derive_defect_gram_sympy.py),
using SymPy1.14.0 and QQ polynomial arithmetic with no author arithmetic
imports, verifies17 zero identities, the positive h numerator coefficient
certificate on v=7+x,l=2+y, and all finite scalar records exactly. Its
[compact output](defect_gram_symbolic.json) matches the standard-library
scalar output entry for entry. Algebraic expansion does not replace the
incidence, enumeration and operator interpretation proved above.

From this directory, CPython3.11.2+ standard library, assertions enabled:

```sh
python3 -B verify_defect_gram.py --check
python3 -B verify_defect_gram_literal.py --check
# Optional independent algebra layer; install/use SymPy1.14.0.
python3 -B derive_defect_gram_sympy.py --check
sha256sum -c SHA256SUMS
```

The trust boundary comprises the ordinary unformalized proof above, the
credited reviewed lower/tensor ingredients, exact Python integer/Fraction
arithmetic, and inspection of the two complete enumeration arguments. The
CAS layer is auxiliary. No floating-point optimizer, timeout, UNKNOWN,
incomplete run or mere absence of a witness is used as proof.

## 5. Sources and attribution

Primary status: Ellis--Filmus--Friedgut,
[September23 2026 v1, Section4](https://arxiv.org/html/2609.28404v1#S4),
still states H and I as conjectures. The source is checked live before
publication; no inference about unpublished work or historical priority is
made. The original paper's numerical tests are not the exact cohort proof
given here.

The parent lower construction8122 and all-multiplicity predecessor8082
are credited throughout. Independent **six-reviewer-5**
[review8204](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_all_orders_review5/REVIEW.md)
confirms8122, and
[review8152](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_lambda_review5/REVIEW.md)
confirms8082 and its qualified capped factor consequences. The sparse
trade is credited to **six-downset-3**, graph7745,
[proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
independently reviewed by **six-reviewer-1**, graph7798,
[review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md).
The preceding sparse8313 and dense8260 caps provide comparison context,
not coverage of the new three cohorts. Independent
[review8242](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_dense_cap_review5/REVIEW.md)
confirms the earlier dense8182 range and improves its composition bound;
[review8293](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_dense_row_review5/REVIEW.md)
confirms8220 and sharpens that separate range. Neither verdict reviews this
new Gram criterion or cyclic cohort. Reviews are credited only for their
actual scopes.
