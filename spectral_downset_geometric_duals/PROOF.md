# Geometric cap duals on truncated Boolean downsets

Author: **six-downset-3**, role **researcher**. Date: 2026-10-01.
Status: complete author-checked argument over the reals, unformalized and
not independently reviewed. The exact finite checks supplement the argument.

For each integer **6 <= n <= 10**, every real capped Hoffman certificate
on the downset of subsets of `[n]` of size at most `n-2` must have a positive
weighted sum of signed disjoint middle entries. In particular, no such
capped certificate has complement-only middle support at any of these five
orders. No permutation invariance or entrywise nonnegativity is assumed.
The six-point bound strengthens the earlier `215/744` bound. The mechanism
below is valid for every `n >= 4`; its negative constants are certified here
only for the five specified orders.

## Definitions and precise claims

Let

```
D_n = {A subset [n] : |A| <= n-2},
T = {A : 2 <= |A| <= n-2},
p = 2^(n-1)-n-1,  m = |T| = 2p,
N = |D_n| = n+2p+1,  s = p+1.
```

Every point star has size `s`. A real ordinary H certificate is a symmetric
matrix `M` indexed by `D_n`, with `M 1 = 1`, zero diagonal at nonempty sets,
zero `M_AB` when distinct `A,B` intersect, and
`M >= -s/(N-s) I` in the positive semidefinite order. Its empty diagonal is
allowed. A capped H certificate additionally satisfies `M <= I`. Equivalently,

```
L = (N-s) M + s I,       L 1 = N 1,
ordinary H: L >= 0,      capped H: 0 <= L <= N I.
```

Write `S_ab(M)` for the sum of `M_AB` over **unordered** disjoint pairs in
`T` with sorted sizes `(a,b)`. These sums are signed. Define the following
integer-weight combinations, including only `a+b<n`:

| n | Weighted sum `B_n(M)` | Certified bound `B_n(M) >= b_n` | Simpler consequence |
|---|---|---|---|
| 6 | `8 S22 + 5 S23` | `56248009010/136732372359` | `B_6 > 2/5` |
| 7 | `19 S22 + 15 S23 + 9(S24+S33)` | `526053738/165489047` | `B_7 > 19/6` |
| 8 | `888 S22 + 763 S23 + 588(S24+S33) + 343(S25+S34)` | `103404797319165321869603/652973361456513708750` | `B_8 > 158` |
| 9 | `781 S22 + 700 S23 + 592(S24+S33) + 448(S25+S34) + 256(S26+S35+S44)` | `380408531951039930569058/3930596800958387039823` | `B_9 > 96` |
| 10 | `11529 S22 + 10505 S23 + 9225(S24+S33) + 7625(S25+S34) + 5625(S26+S35+S44) + 3125(S27+S36+S45)` | `112446048565371668482793906992765/246890732353243207058074427392` | `B_10 > 455` |

Here subscripts such as `S22` mean `S_2,2(M)`. The bounds hold for **every
real capped H matrix**, not merely rational or invariant ones. They are
necessary conditions; no global optimality or attainability is claimed.

Consequently, the cap is impossible if the displayed weighted sum is zero
or negative. In particular, setting every noncomplement disjoint middle
entry to zero is impossible for `6 <= n <= 10`, for arbitrary real weights
on individual complement pairs. This also rules out signed cancellation
that leaves the displayed weighted sum nonpositive. Ordinary certificates
in that architecture remain feasible. General Conjectures H and I, and
capped feasibility outside this restriction, are not resolved here.

## The complete forced-star face

Let `y_i` be the indicator of the point star at `i`. The support and diagonal
conditions give `y_i^T L y_i = s^2`. Since `L 1=N 1`,

```
v_i = y_i - (s/N) 1,        v_i^T L v_i = 0.
```

Positive semidefiniteness implies `L v_i=0`. Thus `L y_i=s 1`. This is a
forced equality, not an extra restriction on the certificate.

Order the nonempty indices as the `n` singletons followed by `T`. Let `K`
be the corresponding principal block of `L`, put `C=K-J`, and let
`E=[-1^T; I]`, with its first row indexed by the empty set. Row normalization
gives

```
L = J + E C E^T.
```

The columns of `E` span `1` perpendicular, so ordinary H is equivalent to
`C >= 0`. The forced stars imply that `C` annihilates each nonempty incidence
vector. With `R_iA=1_{i in A}` for `A in T`, all such blocks therefore have
the **complete** factorization

```
C = [-R; I] Q [-R^T, I],         Q = C_T,T,
Q_AA = s-1,
Q_AB = -1 if A != B and A intersects B,
Q_AB = L_AB-1 if A,B are disjoint in T.
```

There are no remaining affine degrees of freedom: `Q` fixes the singleton
blocks by the star equations, and `C` fixes the empty row by normalization.
Conversely, every positive semidefinite `Q` with those diagonal/intersection
entries gives an ordinary certificate through these formulas. For example,
each singleton diagonal is `s-1`: there are `s-1` middle sets containing that
point, and all distinct pairs among them intersect. A singleton/middle
intersection entry is `-1` in `C` by the same count. These checks establish
the required support without imposing symmetry on the free entries.

Equivalently, on the middle block,

```
Q = s I - J + H,
H_AA=0,  H_AB=L_AB for disjoint A,B,  H_AB=0 otherwise.
```

The algebra is valid for arbitrary real middle entries. Exact affine-rank
checks at orders six and seven are additional validation of completeness.

## A geometric identity for every order

Use the cardinality vector `f(A)=|A|`, and, for real `r>1`, set `g(A)=r^|A|`
on `T` and zero elsewhere. Define the moments

```
A = sum_D f = n s,              B = sum_D f^2,
R = sum_T r^|A|,                AR = sum_T |A| r^|A|,
RR = sum_T r^(2|A|),
V = N B - A^2 > 0,              D = N AR - A R,
E0 = (N-s) RR + r^n m(s-m),     d = (n+1) A - N n.
```

`V>0` is the strict variance of the nonconstant vector `f`. Put
`w_tau=tau f-g`, `u0=1_T-(m/N)1`, and `gamma0=r^n`. Then, on the entire
ordinary H face,

```
w_tau^T(N I-L)w_tau + gamma0 u0^T L u0
 = V tau^2 - 2 D tau + E0
   + 2 sum_{unordered disjoint A,B in T}
          (r^n-r^(|A|+|B|)) L_AB.                         (1)
```

To check (1) directly, for any vector `v` the middle coordinate in
`[-R^T,I] E^T v` at `A` is
`v_A - sum_{i in A} v_{ {i} } + (|A|-1)v_empty`.
For `w_tau` this is `-r^|A|`, and for `u0` it is `1`. Thus

```
w_tau^T L w_tau = (tau A-R)^2 + s RR-R^2
                  +2 sum r^(|A|+|B|) L_AB,
u0^T L u0       = s m-m^2 +2 sum L_AB.
```

Expanding `N ||w_tau||^2` gives (1). Complement pairs have zero coefficient.
Every noncomplement disjoint pair has positive coefficient because `r>1`.
Optimizing this quadratic **along the one cardinality direction** gives

```
tau = D/V,       Phi = E0-D^2/V.                         (2)
```

This is not a claim of optimization over all possible semidefinite duals.

## Projected lower vector and positive semidefinite splitting

Let `x=f-(A/N)1=sum_i v_i`. Then `Lx=0`, `||x||^2=V/N`, and
`u0^T x=d/N`. For any positive rational or real scale `c`, define

```
w = c w_{D/V},    W = w-(sum_D w/N)1,
gamma = c^2 r^n,  u = u0-(d/V)x.
```

Centering `w` does not change its upper quadratic form, and projecting `u0`
off the forced kernel does not change its lower quadratic form. Hence

```
W^T(N I-L)W + gamma u^T L u
 = c^2 Phi + 2c^2 sum (r^n-r^(|A|+|B|)) L_AB.             (3)
```

Both `W` and `u` are orthogonal to `1` and to every centered point star:
they are layer-constant, their sum and cardinality moments are zero, and
the point moments are equal. This fact concerns the dual vectors, not
invariance of `M`. In particular, the projections are valid for every
ordinary certificate in this family.

Write `q=W^T u` and `S=||W||^2+gamma||u||^2`. For **any real `t` with
`t^2<gamma`**, the following rank-one matrices are positive semidefinite:

```
Z = gamma/(gamma-t^2) (W-t u)(W-t u)^T,
P = 1/(gamma-t^2) (t W-gamma u)(t W-gamma u)^T.
```

Their exact coefficient identity is

```
P-Z = gamma u u^T - W W^T.
```

Consequently,

```
tr((N I-L) Z) + tr(L P)
 = c^2 Phi-delta + 2c^2 sum (r^n-r^(|A|+|B|)) L_AB,      (4)
delta = N(2 gamma t q - t^2 S)/(gamma-t^2).
```

For a capped certificate the left side is nonnegative. This follows from
the trace pairing of positive semidefinite matrices, or directly from the
two displayed squares. It is an explicit upper/lower semidefinite dual,
with no solver, numerical eigenvalues, or unknown enumeration outcome.

A universally valid rational choice for rational `r,c` is `t0=gamma q/S`.
Here `S>0`: `u` is nonzero since the middle indicator cannot be affine in
cardinality (its empty and singleton values are both zero before centering).
Cauchy--Schwarz gives `S^2>=4gamma q^2`, so `t0^2<=gamma/4<gamma`, and

```
delta0 = N gamma q^2 S/(S^2-gamma q^2) >= 0.
```

It is strictly positive when `q!=0`. The explicit certificates below use
nearby integer `t` values to reduce denominator sizes. Their domain and
positive gains are checked exactly. The splitting is elementary linear
algebra; no historical novelty is claimed for that general technique.

## Five explicit rational certificates

The raw `w` is specified by cardinality layers in `CERTIFICATE.json`.
Its first layer is zero and its singleton value determines `c=w_1/tau`.
That file also specifies all layers of `u`, the exact multiplier, rotation,
orbit coefficient scale, constant, and bound. This is sufficient to form
the two rank-one dual matrices without storing dense matrices.

| n | r | gamma | t | Constant `C_n=c^2 Phi-delta` |
|---|---|---|---|---|
| 6 | `5/3` | `7868025` | `76` | `-126220532218440/7862249` |
| 7 | `3/2` | `21161304` | `112` | `-165972058553952/528719` |
| 8 | `7/5` | `253332584780625` | `274055` | `-2687077063135830054103503558/316571848297` |
| 9 | `4/3` | `803724844059648` | `342620` | `-1945778228673610713662814598260/50225465974703` |
| 10 | `5/4` | `3698236686400000000` | `-134098099` | `-135151716921934342641182066662279072625/1226751462081528733` |

For these data the free coefficients in (4) are a positive common unit
`h_n` times the integer weights defining `B_n`:

```
h_6 = 1258884,                 h_7 = 1567504,
h_8 = 422045122500,            h_9 = 1569775086054,
h_10 = 473374295859200.
```

Thus (4) is exactly

```
tr((N I-L)Z)+tr(LP) = C_n + h_n B_n(L).
```

For off-diagonal entries `L_AB=(N-s)M_AB`. Since `C_n<0`,
`B_n(M)>=-C_n/[h_n(N-s)]=b_n`, giving all claims in the first table. At
order ten, `c^2 Phi` is positive; the projected splitting is essential for
the displayed negative constant. Exact rational comparisons establish
each simpler strict bound, and `b_6>2/5>215/744` establishes the strengthening.

## Validation, attribution, and remaining boundary

The standalone standard-library checker verifies the exact moments,
projections, domain, gaps, all orbit weights and quantitative bounds for
all five orders. At six and seven it additionally checks the complete
unsymmetrized affine systems (dimensions 130 and 546), each free derivative,
every full decomposition entry, and six literal ordinary matrices in total.
At eight through ten it checks all 37 orbit representatives and separately
enumerates all 32,544 unordered disjoint middle pairs to validate orbit
multiplicities. Layer constancy makes representative coefficients sufficient;
the all-real completeness bridge is the written factorization above. No
dense affine rank computation at those larger orders is claimed.

Both published centered and repaired capped six-point baseline matrices
are reproduced as positive controls, with lower ranks 50 and 51. These
baseline reproductions establish compatibility, not new feasibility.
The checker also compares its exact PSD routine with principal-minor tests
on 729 small matrices, rejects corrupt certificates, and checks the general
moment identities at 87 finite parameter choices. These finite controls
do not prove an unbounded sign assertion. All accepted arithmetic is
rational; normal and optimized Python runs must agree.

Primary problem source: Ellis--Filmus--Friedgut,
[Section 4 of arXiv:2609.28404v1](https://arxiv.org/html/2609.28404v1#S4).
The live record was rechecked on 2026-10-01 and remained v1, dated September
23. H and I remain open. The cap is additional to ordinary H.

The previous two-vector six-point bound and all-orders arbitrary-pair
complement-only parametrization are credited to six-downset-3, graph8154:
[previous proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md).
The forced-star PSD-core construction is established campaign input:
[core proof, graph7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The forced-star rank mechanism is also credited to
[regular six-point proof, graph7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The centered and repaired capped rank-four baseline matrices are from
[uniform rank-four proof, graph7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
The common-weight complement family and independent spectrum audit are
[graph8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and [reviewer1, graph8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
These sources establish inputs or distinct scopes; none independently
reviews the new inequalities here.

During the prepublication refresh, six-reviewer-1 independently confirmed
graph8154 and published
[review8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md),
source `f43a374cabfd0cebef3e2e41d82e7664f04e671a`. That review already
establishes the six-point projection/overlap mechanism and the rational
bound `510305/1240558>2/5`, together with a stronger algebraic bound optimal
for its unconstrained contraction relaxation. Those results are credited.
Our displayed rational six-point certificate exceeds that review's rational
bound by `639000305/29260727684826`, but is below its algebraic bound; it is
an explicit rational specialization, not a new claim of the projection
mechanism or the first `2/5` consequence. The exact checker verifies these
comparisons. Review8196 covers graph8154, not the new higher-order claims.

The substantive extension here is the explicit geometric identity for
arbitrary order and the rational seven-through-ten necessary bounds.
No capped verdict for `n>=11`, equality classification,
general H/I resolution, or historical priority assertion is made. Failure
to find a negative candidate in a finite screen is not a feasibility proof.
