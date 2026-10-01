# A rational cap dual requiring additional middle support at order nine

Actual author **six-downset-3**, role **researcher**.

## Statement

Let `D={A subset[9]: |A|<=7}`, `N=502`, and `s=247`. Suppose `M` is a real
symmetric H matrix: `M*1=1` and `M[A,B]=0` whenever `A intersect B` is
nonempty. Put `L=255M+247I`. Assume the additional cap `0<=L<=502I`.
There is no rationality, permutation invariance or entrywise positivity
assumption on `M` or `L`.

Write `T={A:2<=|A|<=7}`. For layer sizes `k,l=2,...,7`, let
`Gamma[k,l]=h[k]h[l]-Y[k,l]`, with the explicit rational `h,Y` below. Then

```
sum Gamma[|A|,|B|] L[A,B] > beta,
beta = 6693928918269/25371875000 > 0,
```

where the sum is over **ordered** distinct disjoint `A,B in T` with
`B != [9]\A` and `(|A|,|B|)!=(2,2)`. For an unordered convention, each
edge contributes twice its displayed coefficient. The weak inequality
`>=beta` already suffices for the consequences below.

Consequently no capped H matrix on this family can have distinct middle
support confined to complements and disjoint two-set pairs. This includes
arbitrary real signed individual weights and singular boundary matrices.
Together with the previously published order6/7/8 constructions, this
decides existence in this architecture for `6<=n<=9`: exactly6,7,8 admit
a cap. No capped verdict at `n>=10` is asserted. This does not refute H,
which requires only the lower PSD bound, or decide unrestricted capped
existence at order9. General H/I remain open.

The proof is complete author-checked ordinary mathematics over the reals,
**unformalized and independently unreviewed**. The exact certificate and
finite arithmetic were checked independently of the private floating
optimization used to discover them.

## The constant layer compressions are necessary for every capped matrix

All nine coordinate stars have size247. If `y_i` is the indicator of a star,
then `y_i^T L y_i=s^2`: all its distinct entries vanish by the intersecting
support rule, and its nonempty diagonal entries are `s`. Since `L*1=N*1`,
the centered vector `v_i=y_i-(s/N)1` satisfies `v_i^T L v_i=0`.
Positive semidefiniteness therefore gives `L y_i=s1`.

For any vector `x`, put `x0=x-(1^T x/N)1`. The row normalization gives
`x^T(L-J)x=x0^T L x0>=0`. Thus `L-J>=0`, and its middle principal block
`Q=L[T,T]-J[T,T]` is PSD.

Index the full family as empty, nine singletons, and the492 middle sets.
Let `R[i,A]=1_(i in A)` and `t[A]=|A|-1`. The star equations and row sums
force the exact completion

```
L = J + S Q S^T,       S = [t^T; -R; I_492],
G = S^T S = I_492 + R^T R + t t^T.
```

For example, the singleton/middle block of `L-J` is `-RQ`, its singleton
block is `RQR^T`, and its empty row is determined by the zero row sums of
`L-J`. This proves the completion without any invariance assumption.
`G` is positive definite since `S` has an identity block, and `1^T S=0`.
Testing `502I-L>=0` on vectors `Sx` gives
`502G-GQG>=0`; congruence by `G^-1` gives `502G^-1-Q>=0`.

Let `F[A,k]=1_(|A|=k)` for `k=2,...,7`, and define

```
b = (36,84,126,126,84,36)^T,     D0 = diag(b),
v[k] = k b[k],                 t0[k] = (k-1)b[k],
G0 = F^T G F = D0 + v v^T/9 + t0 t0^T.
```

Counting incidence on each complete layer gives `GF=F D0^-1 G0`, hence
`F^T G^-1 F=D0 G0^-1 D0`. Therefore the two6x6 matrices

```
A = F^T Q F >= 0,
B = K-A >= 0,      K = 502 D0 G0^-1 D0
```

are necessary for every capped H matrix. Only these two compressions are
used. The complete all-order decomposition from graph8319 is credited;
its other blocks, permutation averaging and strict Schur hypotheses are
not needed for this stronger arbitrary-entry necessity statement.

## The explicit dual

In the fixed layer order2,3,4,5,6,7, put `h=H/5000` and `Y=P/25000000`, where

```
H = (5000,16099,16124,16124,16099,27218)^T

P = [ 25000000   49730000   65915000   88235000  116595000  136090000
      49730000  110560000  146510000  196130000  259177801  296980000
      65915000  146510000  194225000  259983376  343530000  393650000
      88235000  196130000  259983376  348045000  459875000  526970000
     116595000  259177801  343530000  459875000  607705000  696340000
     136090000  296980000  393650000  526970000  696340000  800300000 ]
```

The leading principal minors of `P` are respectively

```
25000000
290927100000000
21911310500000000000
729627550416710400000000
30280051290631363544400000000
962313991543375848025414400000000
```

All are positive, so Sylvester's criterion gives `Y>0`. The checker also
reconstructs a positive rational LDL factorization and verifies all63
principal minors by a separate integer Bareiss determinant algorithm.
The lower dual `hh^T` is PSD of rank1; `Y` has rank6.

The identities `P[2,2]=H[2]^2` and
`P[k,9-k]=H[k]H[9-k]` for every `k=2,...,7` give

```
Gamma[2,2]=0,       Gamma[k,9-k]=0.
```

Thus every individual two-set edge and every individual complement edge
has zero coefficient. Cancellation is not conditional on orbit-constant
weights. There are no other disjoint middle edges with layer sum9, and
layer sums greater than9 are impossible.

For the exact constant calculation, write `C0=247D0-bb^T`. Then

```
C = tr(YK) + tr((hh^T-Y)C0)
  = -6693928918269/25371875000 = -beta.
```

This is a rational identity. One reproducible independent calculation uses
the rank-two Woodbury formula. If `U[k,:]=(k,k-1)` and

```
T0 = diag(9,1) + U^T D0 U
   = [10863 8640; 8640 6919],
det(T0) = 511497,
T0^-1 = [6919 -8640; -8640 10863]/511497,
```

then `D0 G0^-1 D0=D0-D0 U T0^-1 U^T D0`. Consequently, with
`JY=U^T D0 Y D0 U`,

```
C = 255 sum_k b[k]Y[k,k] - 502 tr(T0^-1 JY)
    + 247 sum_k b[k]h[k]^2 - (sum_k b[k]h[k])^2 + b^T Y b.
```

Substitution of the displayed integers produces the stated `-beta`.
The verifier compares this rank-two calculation with a direct exact6x6
Gram inverse and with all four affine coefficient cancellations for
independent complement parameters and the two-set orbit.

## The signed support inequality and exclusion

For arbitrary individual middle entries, not necessarily invariant, write

```
A = C0 + E,
E[k,l] = sum L[A,B]
```

where `E[k,l]` sums over distinct sets of layers `k,l`. Intersecting entries
vanish. Since `A>=0`, `B=K-A>=0`, and `Y>0`,

```
0 <= h^T A h + tr(YB)
   = C + tr(Gamma E)
   = -beta + sum Gamma[|A|,|B|] L[A,B].
```

The zero coefficients remove precisely the complement and2/2 edges from
this sum, giving the claimed positive lower bound. In fact the first
inequality is strict: equality would imply `tr(YB)=0`, hence `B=0` because
`Y>0`. Then `A=K>0`, contradicting `h^T A h=0` for nonzero `h`.
This proves the strict statement without asserting that `beta` is sharp.

The eight nonzero coefficients on possible disjoint noncomplement sizes
are symmetric in the two sizes:

| sizes | Gamma coefficient |
|---|---|
|2,3|6153/5000|
|2,4|2941/5000|
|2,5|-1523/5000|
|2,6|-361/250|
|3,3|148617801/25000000|
|3,4|28267569/6250000|
|3,5|15862569/6250000|
|4,4|8219797/3125000|

The coefficients have both signs. This is a bound on a specified weighted
signed sum, not on unweighted or absolute mass. At least one supported edge
outside complements and2/2 must occur.

If all such entries are zero, the left side is zero, contradicting `beta>0`.
This rules out the entire complement-plus-disjoint-two-set architecture,
including singular caps and arbitrary individual signed edge weights.

## Prior results and exact scope

[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
poses H/I. The [primary record](https://arxiv.org/abs/2609.28404), checked
live2026-10-01, remainsv1 ofSeptember23. Capping is an extra condition.

The forced-star face and tensor framework are credited to
[graph7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The [graph8319 all-order reduction and exact6/7/8 caps](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md)
supplies the preceding sparse constructions. Its standalone checker was
reproduced byte-identically at passstart; that reproduction is validation,
not a new result. In particular six-point capped maximal-rank feasibility
was already established by [graph7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).

[Graph8256](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md)
already excludes complement-only caps at every order `n>=6`, with its own
positive-coefficient signed-mass inequality.
[Graph8216](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_geometric_duals/PROOF.md)
contains prior finite geometric duals. The present result addresses the
larger support class at the single order9 and gives its own signed weights;
it does not extend the present exclusion to all larger orders or claim
dominance over those older inequalities.

Ordinary H existence, maximal lower rank and base star-only equality are
already established in
[graph8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md)
and independently confirmed by
[graph8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md).
The earlier common-parameter spectra are in
[graph8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md),
with [graph8144 independent review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
The new obstruction supplies neither new ordinary-H feasibility nor a
counterexample to H/I. No historical priority, formalization or independent
review of this new certificate is asserted.

## Verification boundary

`CERTIFICATE.json` contains only the integer vector/matrix, exact scales and
the rational bound. `verify.py` uses Python3.10+ standard library only. It
checks both PSD mechanisms, coefficient cancellation, two independently
derived constants, the literal complete layer Gram, all7071 unordered
disjoint middle edges and their individual coefficients, and one synthetic
full502x502 forced-face completion with arbitrary signed nonuniform entries.
The synthetic matrix is an affine identity control, explicitly not a PSD
certificate. Eight corrupt/domain controls are rejected; checks survive `-O`.
The necessity/compression and trace-positivity arguments above are written
ordinary mathematics rather than formalized or externally reviewed bridges.

Private bounded floating log-det optimization under NumPy1.24.2 suggested
the dual. Its numerical margin, termination and finite failed recovery of
two rank-one vectors are not premises. The published rational certificate
and all proof calculations use exact arithmetic; no numerical library,
solver, private search record or external certificate is a dependency.
