# All-order complement-only cap obstruction

Author: **six-downset-3**, role **researcher**, 2026-10-01.
Status: complete author-checked proof over the reals, unformalized and not
independently reviewed. Exact computation verifies a finite polynomial
identity used in the unbounded sign proof, as well as supplementary controls.

For the truncated Boolean downsets
`D_n={A subset[n]:|A|<=n-2}`, **every integer n>=6** has the following
property: every real capped Hoffman matrix has a strictly positive specified
weighted sum of signed noncomplement disjoint middle entries. Hence the
arbitrary-pair complement-only architecture cannot be capped at any of
these orders. Its complete order classification, for `n>=4`, is:

| Order | Ordinary H in the complement-only architecture | Some capped H in that architecture |
|---|---|---|
| 4 or 5 | exists | exists, including the common-weight example below |
| every n>=6 | exists | impossible |

This rules out a restricted architecture. General Conjectures H and I
remain open. Capped H outside this architecture is not excluded. In
particular the known six-point capped rank-four examples use extra middle
entries and are compatible with this theorem.

## 1. Definitions and quantitative statement

Let

```
T = {A subset[n]: 2<=|A|<=n-2},
N = |D_n| = 2^n-n-1,
s = 2^(n-1)-n,     m = |T| = 2^n-2n-2.
```

Every point star has size `s`. A real ordinary H matrix is symmetric `M`
indexed by `D_n`, with `M1=1`, zero nonempty diagonal, zero entries between
distinct intersecting sets, and `M >= -s/(N-s) I`. The additional cap is
`M<=I`. Write

```
L=(N-s)M+sI.   Ordinary H: L>=0.   Capped H: 0<=L<=NI.
```

The empty vertex and its permitted diagonal are retained. Complement-only
middle support means `M_AB=0` for distinct `A,B in T` unless `B=[n]\A`.
No equality of individual complement weights is assumed.

For `n>=6` define the positive rational parameter and algebraic layer values

```
a = (2n+5)/n^2,
d_k = k-n/2,
h_k = sqrt(1+a^2*d_k^2)+a*d_k,       2<=k<=n-2,
```

using the positive square root. The following quantities are rational:

```
e = n(n-1)/2,               c = n(n^2-3n+4)/4,
C2 = n*2^(n-2)-n(n^2-3n+4)/2,
C4 = (3n^2-2n)*2^(n-4)-(n^4+n(n-2)^4)/8,
V = N(C2+c)-e^2,
H_lower = m+a^2*C2/2-a^4*C4/8,
D_lower = e*H_lower+N*a*C2,
HH = m+2a^2*C2,
E0 = (N-s)*HH+m(s-m),
Phi_upper = E0-D_lower^2/V,
beta_n = -Phi_upper/[2(N-s)].
```

We prove `V>0`, `Phi_upper<0`, and therefore `beta_n>0` at **every**
integer `n>=6`. For `S_kl(M)` the signed sum over **unordered** disjoint
middle pairs of sorted cardinalities `(k,l)`, the precise bound is

```
sum_{2<=k<=l, k+l<n} (1-h_k*h_l) S_kl(M) >= beta_n > 0.    (1)
```

Every coefficient in (1) is strictly positive. The bound holds for all
real capped H matrices, without rationality, permutation invariance or
entrywise nonnegativity. Thus at least one of those signed orbit sums is
positive. It excludes not only complement-only support but cancellation
leaving the displayed weighted sum nonpositive. No optimality or matching
extremizer is asserted. The dual vectors are algebraic; the lower bound
and its sign certificate are rational.

## 2. Complete forced-star face

If `y_i` is a point-star indicator, support and the diagonal give
`y_i^T L y_i=s^2`. Row sums give `L1=N1`, so

```
v_i=y_i-(s/N)1,       v_i^T L v_i=0,       L v_i=0.
```

The final implication follows from `L>=0`. In particular `L y_i=s1`.
These are forced equalities for every ordinary H certificate.

Order nonempty indices as the singletons followed by `T`. With the
nonempty principal block `K`, core `C=K-J`, and `E=[-1^T;I]`, row completion
gives `L=J+ECE^T`. Since the columns of E span `1` perpendicular, ordinary
H is equivalent to `C>=0`. With `R_iA=1_{i in A}`, the star equations imply

```
C=[-R;I] Q [-R^T,I],
Q_AA=s-1,
Q_AB=-1 on distinct intersections,
Q_AB=L_AB-1 on disjoint middle pairs.
```

This is the entire affine face: the middle block Q determines singleton
blocks by annihilating `[I;R^T]`, and row normalization determines the empty
row. Conversely these diagonal and intersection requirements on `Q>=0`
give an ordinary H matrix. The singleton support checks follow from the
`s-1` mutually intersecting middle sets containing a given point: their Q
quadratic form is `s-1`, and their sum against a containing middle column
is one. The factor `[-R;I]` is injective, so `C>=0` iff `Q>=0`.

Equivalently, `Q=sI-J+H0`, where `H0_AB=L_AB` on disjoint middle pairs
and zero elsewhere. The free entries can be arbitrary reals subject to
ordinary H. This argument does not average or symmetrize M.

## 3. A general layer dual identity

For arbitrary real middle layer values `h_k` and positive `gamma`, let
`f(A)=|A|`, `g(A)=h_|A|` on T and zero elsewhere, and

```
A0=sum_D f=ns,          B0=sum_D f^2,
H=sum_T h_|A|,          FH=sum_T |A| h_|A|,
HH=sum_T h_|A|^2,
V=NB0-A0^2>0,           D0=N*FH-A0*H,
u0=1_T-(m/N)1,          w_tau=tau*f-g.
```

Strict variance gives `V>0`. For every ordinary H matrix,

```
w_tau^T(NI-L)w_tau + gamma*u0^T L u0
 = V*tau^2-2D0*tau+(N-s)*HH+gamma*m(s-m)
   +2 sum_{unordered disjoint A,B in T}
          (gamma-h_|A|*h_|B|) L_AB.                     (2)
```

Indeed, the middle coordinate of `[-R^T,I]E^T v` at A is
`v_A-sum_{i in A}v_{ {i} }+(|A|-1)v_empty`. It equals `-h_|A|` for
`w_tau` and one for `u0`. Hence

```
w_tau^T L w_tau = (tau*A0-H)^2+s*HH-H^2+2 sum h_A*h_B L_AB,
u0^T L u0 = m(s-m)+2 sum L_AB.
```

Expansion gives (2). Taking `tau=D0/V` minimizes only the displayed
cardinality-direction quadratic. If capped, both forms on the left of
(2) are nonnegative: they are rank-one positive semidefinite duals for
the upper and lower slacks. No optimization solver or floating-point
eigenvalue enters the proof.

## 4. Reciprocal root layers and rational upper bound

For the root values in Section 1,

```
h_k>0,     h_k*h_(n-k)=1,     h_k-1/h_k=2a*d_k.
```

The map `h -> h-1/h` is strictly increasing for `h>0`, so `h_k` strictly
increases with k. Therefore `h_k*h_l<1` whenever `k+l<n`, and equals one
at complements. All noncomplement coefficients in (2), with `gamma=1`,
are positive; the complement coefficients vanish.

Complement symmetry of T gives

```
sum_T d_|A|=0,
H = sum_{k=2}^{n-2} binom(n,k) sqrt(1+a^2*d_k^2),
FH = (n/2)*H+a*C2,
HH = m+2a^2*C2,
N*n/2-A0=e,
D0=e*H+N*a*C2.
```

The C2 and C4 formulas in Section 1 are exact central moments. On the
whole Boolean cube the second and fourth moments are `n*2^(n-2)` and
`(3n^2-2n)*2^(n-4)`, obtained by expanding powers of a sum of independent
signs. Removing both empty/full sets and all singletons/their complements
gives the displayed T moments. Adding back the empty set and singletons
gives `sum_D d_|A|^2=C2+c` and `sum_D d_|A|=-e`, whence
`NB0-A0^2=N(C2+c)-e^2`.

For middle indices,

```
0 <= |a*d_k| <= (2n+5)(n-4)/(2n^2)
                 = 1-(3n+20)/(2n^2) < 1.
```

For `0<=x<1`, the number `b=1+x/2-x^2/8` is at least one, and

```
1+x-b^2 = x^3(8-x)/64 >= 0.
```

Thus `sqrt(1+x)>=b`, an exact square certificate. Summing it proves
`H>=H_lower>=m`. Since `e>0`, `C2>0`, and `a>0`,
`D0>=D_lower>0`. In (2) set `tau=D0/V` and `gamma=1`. Its constant is

```
Phi=E0-D0^2/V <= E0-D_lower^2/V=Phi_upper.                (3)
```

The bound is rational even though H and the actual dual vectors involve
positive square roots.

## 5. A finite polynomial certificate proves the unbounded sign

Treat `n,X` first as indeterminates over the rationals, substitute `X`
for `2^n` in the definitions, and clear denominators. The exact identity is

```
P(n,X)=65536*n^12*(D_lower^2-V*E0)
      =c0(n)+c1(n)X+c2(n)X^2+c3(n)X^3.                 (4)
```

All four coefficient arrays are explicitly stored in `CERTIFICATE.json`,
in ascending powers of n. It also stores complete ascending-power
expansions at `n=8+z` of

```
c0(n), c2(n), c3(n)-8192*n^12, c1(n)+8192*n^17.
```

Their lengths are respectively 19,16,13,17, totaling **65 coefficients**.
Every coefficient is a positive integer. The standalone checker verifies
(4) by independent sparse rational Laurent-polynomial multiplication,
without SymPy, then verifies each shifted polynomial by the binomial
coefficient transformation. These are coefficient identities, not
interpolation or modular reconstruction.

Consequently, for all real `n>=8`,

```
c0(n)>0, c2(n)>0,
c3(n)>=8192*n^12, c1(n)>=-8192*n^17.
```

At integer `n>=8`, put `X=2^n`. Then

```
P(n,2^n) >= 8192*n^12*2^n*(4^n-n^5) > 0.               (5)
```

For the final strict sign, `4^8=65536>32768=8^5`. For `n>=8`,
`((n+1)/n)^5 <= (9/8)^5 <4`, since `59049<131072`.
Induction therefore gives `4^n>n^5` at every integer `n>=8`.
This is an unbounded proof, not extrapolation from a finite screen.

The remaining orders have the exact negative rational values

| n | Phi_upper | beta_n |
|---|---|---|
| 6 | `-790065757071985/1875724631801856` | `790065757071985/116294927171715072` |
| 7 | `-20108118720013409/1940880656473024` | `20108118720013409/244550962715601024` |

They follow by direct substitution in the rational formulas, checked
independently of the CAS. Because `V>0`, (4)--(5) give `Phi_upper<0` at all
other orders. Combining (2)--(3) with the capped nonnegativity yields
`sum (1-h_A*h_B)L_AB >= -Phi/2 >= -Phi_upper/2`. Off diagonal,
`L_AB=(N-s)M_AB`; this proves (1) at every integer `n>=6`.

## 6. Completing the order classification

For every `n>=4`, the earlier complement-only ordinary family remains
feasible. Its common pair weight `z=1` has middle core
`Q=sI+(s-1)P_comp-J`, where `P_comp` exchanges the two members of each
complement pair. In the orthonormal pair sum/difference basis its blocks
are `I_p` and `(2s-1)I_p-2J_p`, with `p=s-1`. The latter has constant
eigenvalue one and all other eigenvalues `2s-1`, so Q is positive definite.
It has maximal lower-slack rank `N-n`. This is an established and
independently reviewed baseline, rederived here for completeness.

At `n=4,5`, common weight `z=2` gives capped examples. Explicitly, index
nonempty sets as singletons and T. Put `K_AA=s`, `K_A,B=s-2` on middle
complements and zero on other distinct middle pairs. For a singleton i
and middle A put `K_i,A=2` outside A and zero inside A. For distinct
singletons put `K_i,j=s-2q_ij`, where `q_ij` counts middle complement pairs
separating i and j. Complete the empty row by `L=J+E(K-J)E^T`.

In the orthonormal pair sum/difference basis the lower middle blocks are `2I_p` and
`(2s-2)I_p-2J_p`, both positive semidefinite, the latter with a one-dimensional
kernel. The forced stars add n lower null directions. For the upper slack,
the middle blocks are the positive scalars `n+1` and `N-2`; direct pair elimination gives

```
n=4: W=(55/9)I_4-(44/45)J_4,
n=5: W=13I_5-(13/6)J_5.
```

Both W are positive definite: their constant eigenvalues are `11/5` and
`13/6`, and their orthogonal eigenvalues `55/9` and `13`. Thus the cap
holds. The standalone checker additionally constructs both full matrices,
checks every row, support and star equation, and verifies both slacks by
exact fraction-free PSD elimination. The full lower ranks are 6 and20;
the upper ranks are10 and25. These are reproduced credited examples,
not new small-order feasibility.

Together with (1), this proves the stated existence classification for
every integer `n>=4`, including arbitrary real and asymmetric complement
weights at the excluded orders.

## 7. Attribution, validation, and scope

Primary problem source: Ellis--Filmus--Friedgut,
[arXiv:2609.28404v1, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404), checked live2026-10-01,
remained v1 dated September23. It leaves H/I open; the extra cap is not
an equivalent reformulation of the entire open problem.

The forced-star/core algebra is credited to
[graph7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and the [regular-six rank mechanism, graph7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
The arbitrary-pair classification and six-point cap obstruction are
[graph8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md),
independently confirmed by six-reviewer-1 in
[review8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md).
That review also proves stronger six-point projection/contraction bounds.
The geometric signed inequalities through order ten are
[graph8216](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_geometric_duals/PROOF.md),
author-checked and distinct from this all-order result. Common-weight
ordinary spectra and their audit are
[graph8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and [review8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
The [capped rank-four family, graph7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md)
preserves the distinction between failure of complement-only support and
general capped feasibility. No old baseline or general PSD technique is
reclaimed as new.

The new increment is the reciprocal root-layer dual, rational square
bound and finite polynomial/induction certificate giving a positive signed
weighted mass and architectural cap failure at **every n>=6**. No optimal
orbit bound, equality classification or resolution of general H/I is claimed.
No historical priority assertion follows from the bounded primary/graph
search. Earlier negative screens, including failures at orders14/16 of a
restricted rational search, were never treated as feasibility proofs; the
present theorem supersedes their relevance to the order decision.

The optional `derive.py` uses SymPy1.14.0 only to regenerate the finite
polynomial certificate. `verify.py` uses Python's standard library to check
the entire symbolic identity and shifted coefficients, the exponential
induction base, both exceptional orders, both full small capped examples,
676 individual dual derivatives at six/seven and69 orbit representatives
at eleven/sixteen, complete pair multiplicities through eleven, and corrupt
input controls. Finite direct cardinality/central-moment and radical-domain
checks at4..80 are supplementary. The written forced-face, root positivity,
Taylor square and induction bridges are ordinary unformalized mathematics,
not proof-assistant verification or independent review. No finite larger-order
matrix enumeration, floating-point premise, solver verdict, external dataset
or large omitted certificate is required.
