# Which geometric endpoint does the restricted weight theorem actually give?

This annex connects the global criterion to a precise Kneser--Poulsen
endpoint and completely classifies the finite logarithmic weight profiles
in the two coefficient cones of the team's square-cone orbit theorem.
The classification shows that this particular extraction yields radius
patterns already covered by coordinate-preserving relabelling. It is a
scope result and a concrete obligation for extending that theorem, not a
negative Gaussian hinge or a new Kneser--Poulsen class.

Status: author proof, with exact finite coefficient checks and independent
mathematical review pending. The positive orbit theorem is credited to its
[original source](../gaussian_majorisation_square_cone_orbits/PROOF.md).
The variable-radius limit is already the mechanism of Aishwarya--Li,
[Theorem 5.1](https://arxiv.org/html/2609.07041v2); it is not claimed as new.

## 1. A single logarithmic weight path and its exact defect scale

Fix finitely many centres `x_i,y_i` in `R^3`, with `y_i=T(x_i)` for a
contraction, and positive functions `q_i(s)` such that

\[
\lim_{s\downarrow0}2s\log q_i(s)=r_i^2\ge0.
\]

Set `Z_s=sum_i q_i(s)`, `mu_s=sum_i q_i(s) delta_(x_i)/Z_s`,
`nu_s=sum_i q_i(s) delta_(y_i)/Z_s`, `C_s=(2 pi s)^(-3/2)`, and
`a_s=C_s/Z_s`. Write `f_s=mu_s*gamma_s`, `g_s=nu_s*gamma_s` and
`H_p(a)=integral(p-a)_+`. Then

\[
\boxed{\quad
\lim_{s\downarrow0}\frac{H_{g_s}(a_s)-H_{f_s}(a_s)}{a_s}
=\left|\bigcup_i B(x_i,r_i)\right|
 -\left|\bigcup_i B(y_i,r_i)\right|.\quad}              \tag{G1}
\]

Indeed, equal masses give

\[
\frac{H_{g_s}(a_s)-H_{f_s}(a_s)}{a_s}
=\int\min\left\{\sum_iq_i(s)e^{-|z-x_i|^2/(2s)},1\right\}dz
 -\int\min\left\{\sum_iq_i(s)e^{-|z-y_i|^2/(2s)},1\right\}dz.
                                                               \tag{G2}
\]

Except on the finitely many boundary spheres, each integrand tends to the
indicator of its ball union. Zero radii cause only null singleton sets.
To justify dominated convergence, choose `M>max r_i^2`. For all sufficiently
small `s<=s_0`, every `q_i(s)<=exp(M/(2s))`. Outside
`d(z,{x_i})<=sqrt(M)`, the first integrand is at most
`n exp((M-d(z,{x_i})^2)/(2s_0))`; inside use one. This is integrable.
The same argument applies to the target. This proves (G1), including
subexponential prefactors and weights varying with `s`.

Consequently the hinge comparison along **this one path at this one
threshold per variance** suffices for the corresponding union-volume
inequality. Theorem 5.1's all-law/all-variance premise is a convenient
sufficient hypothesis; its proof does not make that premise necessary
for an individual radius assignment.

The global criterion in [PROOF.md](PROOF.md) supplies a useful precise
normalization. For the varying pair let
`Delta_s=sup_a(H_(f_s)(a)-H_(g_s)(a))_+`. Then

\[
\left(\left|\bigcup_i B(y_i,r_i)\right|
 -\left|\bigcup_i B(x_i,r_i)\right|\right)_+
\le\liminf_{s\downarrow0}\frac{\Delta_s}{a_s}.           \tag{G3}
\]

In particular `liminf Delta_s/a_s=0` suffices. By the global theorem,
`Delta_s` is also the minimum failure probability of the five-dimensional
endpoint density-value coupling. Thus (G3) states exactly the scale at
which an approximate coupling would have a geometric consequence.
An absolute estimate `Delta_s -> 0` alone does not imply this condition:
when some radius is positive, `a_s` is exponentially small in `1/s`.
No extra tail sign premise or general stability impossibility is asserted.

## 2. The two fixed coefficient cones

Use zero-based directional indices, following the orbit packet:

\[
\begin{split}
A&=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),\\
B&=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)).
\end{split}
\]

The source sites are `(0,A,-B)` and the target sites `(0,A,B)`.
Let `K_A,K_B` be exactly the nonnegative coefficient cones in Section 6
of the original orbit proof, using its retained orders on 48 signed
coordinate permutations. Each cone requires all coefficients of each
retained polynomial difference to be nonnegative. Its definition is
finite and homogeneous; multiplying a weight vector by a positive scalar
does not affect membership.

The complete order matrices are in the original
[CERTIFICATE.json](../gaussian_majorisation_square_cone_orbits/CERTIFICATE.json),
SHA256 `06b7a995ad6594448faecd9559c0e9e443d36c4a7a21afc3bd4c73e52168dc7a`.
The following eleven inequalities are among the retained coefficients:

\[
\begin{array}{ll}
K_A:&q_1\le q_0,\quad q_1\le q_2,\quad q_0\le q_3,
\quad q_2\le q_3,\\
&q_3\le2q_0+3q_1,\quad q_3\le2q_2+3q_1;\\[2pt]
K_B:&q_1\le q_0,\quad q_0\le q_2,\quad q_2\le q_3,
\quad q_2\le q_0+q_1,\quad q_3\le q_2+2q_1.
\end{array}                                                   \tag{G4}
\]

For an independently locatable certificate, the rows below give the
lower and upper group labels, the coefficient position `(U,V,W)`, and
the primitive coefficient form `d`. The actual coefficient is the last
column's positive integer times `d.q`. Group labels and monomial order
are exactly those of the original packet.

| Cone | Lower | Upper | Position | `d` | Multiplier |
|---|---:|---:|---|---|---:|
| A | 18 | 4 | (2,0,0) | (1,-1,0,0) | 1 |
| A | 18 | 0 | (2,0,0) | (0,-1,1,0) | 1 |
| A | 4 | 16 | (2,0,0) | (-1,0,0,1) | 1 |
| A | 0 | 16 | (1,0,2) | (0,0,-1,1) | 3 |
| A | 40 | 7 | (0,1,0) | (2,3,0,-1) | 1 |
| A | 40 | 3 | (0,1,0) | (0,3,2,-1) | 1 |
| B | 2 | 6 | (0,0,3) | (1,-1,0,0) | 4 |
| B | 4 | 20 | (1,0,0) | (-1,0,1,0) | 2 |
| B | 0 | 4 | (0,0,3) | (0,0,-1,1) | 4 |
| B | 0 | 43 | (0,3,0) | (1,1,-1,0) | 4 |
| B | 28 | 3 | (0,1,0) | (0,2,1,-1) | 2 |

The exact checker rebuilds these coefficients from the signed coordinate
permutations and binomial expansions, and verifies that every listed
comparison belongs to the retained order.

Four cone membership checks provide the converse needed below:

\[
\begin{split}
v_A=(1,0,1,2),\quad&w_A=(1,1,1,2)\ \in K_A,\\
v_B=(1,0,1,1),\quad&w_B=(1,1,1,1)\ \in K_B.             \tag{G5}
\end{split}
\]

Membership here means **every** retained coefficient inequality, not only
the eleven selected in (G4). The checker exhausts all coefficient positions
for all 875 A comparisons and 871 B comparisons, including their zero
coefficients and diagonal comparisons. These exact finite checks are a
premise for sufficiency. The original orbit comparison itself remains a
credited theorem input, not something re-reviewed by this annex.

## 3. Exact classification of all finite logarithmic profiles

**Theorem.** For either `C=A` or `C=B`, suppose
`q(s) in K_C intersect (0,infinity)^4`, and every limit
`lambda_i=lim_(s->0) 2s log q_i(s)` is finite. Then

\[
\boxed{\lambda_0=\lambda_2=\lambda_3\ge\lambda_1.}      \tag{G6}
\]

Conversely every finite vector with (G6) is achieved by an explicit path
in that cone, for every `s>0`. The same necessity holds along any sequence
of variances tending to zero for which the four limits exist.

**Proof.** For `K_A`, (G4) gives

\[
\max(q_0,q_2)\le q_3\le5\min(q_0,q_2),
\qquad q_1\le\min(q_0,q_2).
\]

Hence the three indicated coordinates have uniformly bounded positive
ratios, while the remaining one cannot have a larger logarithmic rate.
For `K_B`, (G4) gives

\[
q_0\le q_2\le2q_0,\qquad q_2\le q_3\le4q_0,
\qquad q_1\le q_0.
\]

Taking `2s log` proves (G6) in both cases.

For the converse set `L=lambda_0=lambda_2=lambda_3`, `l=lambda_1<=L`
and `epsilon_s=exp((l-L)/(2s)) in (0,1]`. The paths

\[
q_A(s)=e^{L/(2s)}(1,\epsilon_s,1,2),\qquad
q_B(s)=e^{L/(2s)}(1,\epsilon_s,1,1)                     \tag{G7}
\]

have exactly the desired rates. Each parenthesized vector is
`(1-epsilon_s)v_C+epsilon_s w_C`, which belongs to `K_C` by (G5) and
convexity. All coordinates are positive. QED.

For squared-radius profiles, the obtainable assignments are therefore

\[
r_{A,0}=r_{A,2}=r_{A,3}=R_A\ge r_{A,1},\qquad
r_{B,0}=r_{B,2}=r_{B,3}=R_B\ge r_{B,1}.                \tag{G8}
\]

The two cluster scales and the origin radius are independent. This is a
classification of this fixed certificate's finite logarithmic profiles,
not of every weight vector having true Gaussian majorisation. A failed
profile in (G6) supplies no negative Gaussian hinge.

The classification also applies separately at each member of any finite
collection of complete ray shells in the original radial-law theorem.
The mass assigned to a shell multiplies all four of its coefficients;
homogeneity preserves cone membership. Whenever the four effective
logarithmic radii at that shell have finite limits, (G8) follows there.
No assertion about nonuniform limits of continuously many shells is
needed for this statement.

## 4. Every extracted radius pattern already has a relabelling proof

In fact only the equality `r_(A,0)=r_(A,2)` is needed for the following
existing-method argument; all other radii may be arbitrary. It works on
any finite collections of nonnegative radial shells, with that equality
required at each A shell.

Let `S(x,y,z)=(-x,y,z)`. Define an alternate endpoint contraction `R` by

\[
R(0)=0,\qquad R(rA_i)=rS A_i,\qquad
R(-tB_j)=tB_j\quad(r,t\ge0).                          \tag{G9}
\]

Within either cluster distances are preserved. Across clusters,

\[
|rA_i+tB_j|^2-|rS A_i-tB_j|^2
=4rt[1+(A_i)_y(B_j)_y]\ge0,                            \tag{G10}
\]

because `(A_i)_y` belongs to `{0,1,-1}` and `(B_j)_y` to `{1,-1}`.
Thus `R` is a contraction of the entire ray domain. The origin is
consistent with both pieces. Moreover the globally rotated map `S R`
preserves the first coordinate at every input point.

This is the earlier [coordinate-preserving/paired-rank-five
mechanism](../gaussian_majorisation_rank_abel/PROOF.md). For clarity its
Gaussian proof can be obtained directly from the primary planar theorem:
write input points as `(x,u)` and their `S R` images as `(x,V(u))`.
Cancelling the fixed first-coordinate difference in the contraction
inequality proves that `V` is a well-defined planar contraction on the
projected support. At each first-coordinate observation, weighting the
input by its one-dimensional Gaussian kernel gives a finite measure on
that plane. The two-dimensional majorisation theorem applies after
normalizing its mass. Integrating those hinge inequalities in the first
coordinate proves the full three-dimensional comparison for **every**
input law and variance. Theorem 5.1 then gives the union-volume comparison
for `R` with all individual radii.

The map `S` interchanges `A_0,A_2` and fixes `A_1,A_3`. Thus the
radius-decorated target union of `R` agrees exactly with that of the
original map `T` whenever the two interchanged radii are equal, shell by
shell. Both have the same B target balls and origin ball. This proves
the desired volume comparison for every pattern (G8) by an already
available method. No matching of probability weights is required for
this equality of ball unions.

This does not invalidate the new orbit theorem. Its central Gaussian
weights have unequal opposite masses, and its all-variance weighted
conclusion goes beyond this simple relabelling. The loss of distinction
occurs specifically in the logarithmic radius limit: constant factors
such as the `2` in (G7) disappear when multiplied by `2s` after a logarithm.

## 5. The resulting positive obligation

To obtain a new unequal-radius consequence through weight paths on these
ray supports, an extension must allow logarithmic profiles outside the
old radius-rematching conditions, or use a different analytic endpoint.
For example, breaking both opposite-radius equalities in the A cluster
is necessary to escape its two coordinate-reflection variants. Other
possible rematchings must still be checked. The current fixed cones force
`r_(A,0)=r_(A,2)` and therefore cannot meet even that requirement.

This is a finite, checkable target for a broader functional certificate:
support prescribed exponential contrasts for small variance, not merely
increase a bounded neighbourhood of probability weights at fixed variance.
An extension with (G3) can also use approximate endpoint couplings if it
achieves the specified normalized scale. None of these missing positive
claims is assumed here. The full Gaussian conjecture remains open.

### Relationship to the latest spatial extensions

The prepublication refresh found two further positive source packets.
The [spatial-cloud stability theorem](../gaussian_majorisation_open_stability/PROOF.md)
provides one neighborhood on each compact positive variance interval.
That quantifier alone does not provide the small-variance path required
by (G1). The [paired-layer completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md)
does provide a single constrained spatial neighborhood at all variances,
but its permitted weight ball has a uniform positive lower bound on
every normalized atom weight. Along paths staying in that ball, all
ratios `q_i(s)/q_j(s)` are bounded above and below independently of `s`.
Thus every finite logarithmic squared-radius profile has all radii equal.

That equal-radius volume comparison already has a simple rematching.
For the paired layers `X=(0,A,-B)`, `Y=(0,A,B)`, write
`B={(b_j,1)}` with its transverse set invariant under `b -> -b`.
The coordinate-preserving contraction

\[
F(u_1,u_2,z)=(u_1,u_2,|z|)
\]

fixes the origin and the A layer, and maps the negative B layer onto the
positive B layer as an unlabelled set. Equal radii are preserved by this
permutation, so the earlier coordinate-preserving theorem and primary
Theorem 5.1 already give its volume inequality. The same explanation
works for radii matched in each opposite B pair. Unequal Gaussian masses
need not be preserved, so the new spatial Gaussian theorem retains its
stated additional content. Both advances therefore fit the global
criterion while leaving the exponential-weight obligation above intact.
They are cited at their author-proof status, not independently reviewed
or used as premises for (G4)--(G10).

### Subsequent positive extension with a new certificate

The later [ordered-weight theorem](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md)
uses different finite orders. It permits arbitrary weight contrasts with
four ordered coordinates in each cluster, including strictly different
logarithmic rates on every shell. This meets the positive extension
obligation above on those exact rays. Its finite-orbit argument proves
ordered-radius unions for every locally finite invariant measure, and
an all-distinct exposed-ball fixture escapes the old endpoint rematching.
No intersection or unrestricted-weight theorem is asserted there.

The fixed-cone classification (G4)--(G10), its checker and the source
certificate used here remain unchanged. This annex classifies those
specific old cones; it was not an impossibility statement for other
orbit certificates. See [the current handoff](DEPENDENCIES.md) for the
new class, its pending-review status and its geometric scope comparisons.

## Reproduction and trust boundary

From this directory, with CPython 3.11 or later and no packages, run

```sh
python3 geometric_limit_audit.py --check
python3 -O geometric_limit_audit.py --check
sha256sum -c SHA256SUMS
```

Both checker invocations return:

```text
GEOMETRIC_PROFILE_CLASSIFICATION_PASS 97cccdd40fc962b778df43ed06468a19d2d3cb61cdb6a32017260e07b15f1ee1
```

The small [GEOMETRIC_CERTIFICATE.json](GEOMETRIC_CERTIFICATE.json) locates
the eleven inequalities and records the four sufficient endpoint vectors.
The [checker](geometric_limit_audit.py) rebuilds all needed integer
polynomials, verifies every cone inequality for those vectors, and checks
the rematching geometry, normalization and invalid controls. It reads the
original order certificate at its relative repository path and rejects a
hash mismatch. That credited input and the original orbit theorem are
explicit dependencies. No raw coefficient dump, numerical Gaussian
quadrature, solver, or asymptotic sampling enters the proof.

The Gaussian and volume limits, ratio argument and planar transfer are
written analytic proofs. The finite checks are author computation, not
independent mathematical review or proof-assistant formalization. This
annex adds no claimed new volume class or priority claim for the primary
transfer theorem.
