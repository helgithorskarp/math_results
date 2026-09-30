# Independent review: exceptional octagon bridge and exact covering threshold

**Reviewer:** six-reviewer-1. **Role:** independent mathematical reviewer.
**Date:**2026-09-30. Shared campaign signatures do not distinguish people;
this identifies the actual reviewer and method.

## Verdict and precise scope

The [target local theorem](../tammes15_octagon_exception_exclusion/PROOF.md),
graph `bafkreiduvmer774uramyquzcuq6wxznurqb7go6f5epr3lc2utkdqfyfhu`,
height7458, source457645158de222fa8eaa3981b8c171810b828e3d, is **confirmed
at the written geometric/exact-computation trust boundary**. The new
ten-case calculation, two core orientations and saturation are independently
rederived below. Its all-octagon classification uses the explicitly
credited contact-pair-closure dependency. The stated strict-improvement
corollary additionally uses the older355-case exclusion and incumbent
existence. Their proofs were inspected and native exact checkers/selftests
replayed successfully; their entire classifications were not independently
rederived by this new checker. No proof-assistant certification is claimed.

A packing is a set of distinct unit vectors in real three-dimensional
Euclidean space whose different-point dot products are at most t, where
\(1/2<t<3/5\). Eight original points A prescribe every edge of an
abstract noncrossing octagon triangulation. Five other original points B
prescribe a pentagon triangulation; its two degree-two ears each have
two prescribed contacts to A. **A/B labels are disjoint.** Additional
points and contacts are unrestricted. Neither spherical facial embedding,
symmetry, a complete contact graph, nor a triangle/quadrilateral face
decomposition is assumed. An old neighbor refers to common adjacency
using prescribed A edges.

If either ear's A pair has no old neighbor, the only realizable
thirteen-point core, up to orthogonal motion and the stated relabelings,
is the core computed below. It occurs only at the unique interval root
\(\theta\) of the following polynomial, printed in ascending coefficients:

```text
[-1,-17,-69,403,4323,10179,-24449,-171609,-279635,119709,
 843073,671593,-148047,348145,1374277,823837]
```

It cannot admit even one additional unit point at threshold theta. This
does not force every fifteen-point optimizer to contain this motif or
establish any new global Tammes-15 bound.

## The finite geometric cover and its dependencies

Every contact vertex has degree at most five: two neighbors on its tangent
circle have azimuthal separation at least
\(\arccos(t/(1+t))>\pi/3\). Six consecutive gaps cannot sum to
\(2\pi\). Reverse polygon ear removal forces the alternate unit solution
at each equilateral edge. With anchor Gram
\(H=(1-t)I+tJ\), the forced reflection is
\(a_{\rm new}=2t(a_i+a_j)/(1+t)-a_{\rm old}\). Positive definiteness
of H and point distinctness justify the choice without an embedding
assumption.

The [closure theorem](../tammes15_contact_pair_closure/PROOF.md), graph7430
`bafkreiglj3fpqibmepcmkilp6ykjz2qknysdepz3zlcrpi3hx7lry3nvmm`,
sourced0e9574dd3699f4ab6fc636f84f43070d49903f7, identifies the only
zero-old octagon/marked-pair type. Its edges are

```text
01 04 05 06 07 12 13 14 23 34 45 56 67,
```

and its pair is E=(2,7), with exactly one compatible external position
throughout the open interval. That classification covers all132
triangulations,84 degree-compatible ones in eight dihedral orbits,
including32 eligible zero-old pairs at size eight. Across sizes5..8 its
39 eligible entries split into30 empty lenses, eight blocked lenses and
the unique compatible exception. Inspection confirms that its Cauchy
and unsquared lens-sign arguments retain tangency and reject no valid
orientation. The native checker regenerates the cover by Catalan and
noncrossing-diagonal enumeration and checks every classified entry.

Every pentagon triangulation has the one dihedral type with B edges
01,02,03,04,12,23,34 and ears1,4. Its ear interchange preserves these
edges. Assign E to ear1. If ear4 also uses a zero-old pair, closure forces
the same unique position, violating distinctness. If it has two or more
old neighbors, those distinct points already fill the at-most-two unit
common-neighbor positions. An antipodal A pair has no common positive-t
contact. Thus ear4 has exactly one old neighbor. Degree accounting gives
the following exhaustive ten triples(i,j,old):

```text
(1,2,3) (1,6,0) (1,7,0) (2,3,1) (3,4,1)
(3,5,4) (4,5,0) (4,7,0) (5,6,0) (6,7,0).
```

Our code independently regenerates this list from the prescribed edges.
It is a complete necessary cover, not an assertion that every listed
case has a geometric realization.

## Independent reduction using a rank-four Gram determinant

Work in coefficient space with dot product \(x^THy\). Anchor
\(a_0=e_0,a_6=e_1,a_7=e_2\). Put \(r=2t/(1+t)\), then reconstruct

\[
a_5=r(a_0+a_6)-a_7,\quad a_4=r(a_0+a_5)-a_6,\quad
a_1=r(a_0+a_4)-a_5,\quad a_3=r(a_1+a_4)-a_0,\quad
a_2=r(a_1+a_3)-a_4.
\]

For B anchor \(b_0=e_0,b_3=e_1,b_4=e_2\), set
\(b_2=r(b_0+b_3)-b_4\), \(b_1=r(b_0+b_2)-b_3\). Its ear dot is
\(\kappa=t(9t^2-2t-3)/(1+t)^2\). For a ten-case second pair, its
external ear is forced by its old neighbor o to be
\(v=2t(a_i+a_j)/(1+a_i^THa_j)-a_o\). The divisor is positive; the
old contact also proves this by Cauchy. All norms/contact identities are
checked as rational functions.

Let \(w=a_2^THa_7\), \(g_2=a_2^THv\), \(g_7=a_7^THv\). Any first
ear u must have contacts t to a2,a7 and dot kappa with v. Four vectors
in three-dimensional space therefore require

\[
\det\begin{pmatrix}
1&w&g_2&t\\ w&1&g_7&t\\ g_2&g_7&1&\kappa\\
t&t&\kappa&1
\end{pmatrix}=0. \tag{1}
\]

This necessary condition includes singular first-three-vector cases:
there is no inverse or generic-rank premise in(1). It uses neither the
author's radical residual nor a squared equation.

`templates.py` computes all ten determinants by the Leibniz expansion
in SymPy's exact rational-function field. Their strict interval signs
are(-,-,-,-,-,+,-,-,undecided,+), with separately certified denominator
signs. Exact Bernstein coefficients certify strict signs on the open
interval, even when an endpoint coefficient is zero. Nine cases are
excluded. The reduced numerator for case8,(5,6,0), is exactly
\((t-1)^3P(t)\); the other factor is nonzero throughout the interval.
Exact root counts find one root of P in the full interval and in

\[
\frac{2196767}{3802339}<\theta<\frac{535329}{926590}.
\]

Exactly160 rational bisections refine this fixed sign-changing bracket.
No floating search, adaptive successful precision, or solver verdict
supplies the exclusion.

## Independent core reconstruction and both orientations

At theta the second ear v is reconstructed from a5,a6,old a0. Pivoted
exact Gaussian elimination solves the three linear equations
\(u^THa_2=u^THa_7=\theta\), \(u^THv=\kappa\). Successful quotient
inversions prove the linear system nonsingular there. Its solution has
unit norm, as checked exactly. This replaces the author's radical/sign
choice by a direct three-contact solve.

For equal-norm x,y, H-Householder reflection in x-y maps x to y:

\[
R_d(p)=p-\frac{2d^THp}{d^THd}d,\qquad d=x-y.
\]

First send b1 to u; then send the resulting b4 to v. The second
reflection preserves u because the ear Gram values agree. This gives a
proper H-isometry. Reflecting its images in the normal to the span of
u,v gives the other isometry. Two independent unit ears have precisely
these two placements in dimension three, so the list is exhaustive.

All thirteen norms and24 prescribed contacts hold for both frames. The
proper frame violates the packing threshold at six pairs, including(0,11).
The other frame passes all78 pair inequalities and has exactly24
contacts. Since theta<1, the inequalities also certify distinctness.
Thus exactly one thirteen-point Gram configuration survives.

The arithmetic is a quotient Q[t]/(P); irreducibility of P is not
assumed. Exact modular identities hold at theta. Every used inverse is
an actual quotient inverse and hence nonzero at theta. A nonzero quotient
representative receives a sign only when rational Horner enclosure at
the isolated real root excludes zero; unresolved signs fail.

## Independent saturation through the dual convex hull

Let K be the convex hull of the thirteen surviving unit points. A positive
origin relation on labels0,1,4,8, found by affine Gaussian elimination,
proves that zero is strictly inside K. Rank is certified by the same
successful solve. All thirteen points are vertices: their own unit
directions expose them strictly because every other dot is at most theta<1.

For every one of the286 triples, compute its ordinary coefficient cross
normal \(c=(a_j-a_i)\times(a_k-a_i)\) and offset \(d=c^Ta_i\).
Every offset is certified nonzero, so all triples span a plane. A triple
is supporting precisely when all thirteen signs of \(c^Ta_l-d\) lie on
one side. Orient it with d>0. Its squared metric distance to zero is

\[
\rho_F^2=\frac{d^2}{c^TH^{-1}c}. \tag{2}
\]

Every three-dimensional polytope facet contains three affinely independent
vertices, so the exhaustive triple census omits none. Exactly262 triples
are nonsupporting and24 supporting. Deduplication by the entire coplanar
label set gives20 triangular facets and the single quadrilateral
(6,7,8,9), hence21 facets. Incidences give32 edges and satisfy
13-32+21=2. This also handles the four supporting triples of the
quadrilateral without a general-position assumption.

Let \(\rho=\min_F\rho_F\). Comparing all exact squared distances
identifies the **unique minimizing facet(4,5,11)** and certifies

\[
\frac{335708431733}{10^{12}}<\rho^2<
\frac{335708431734}{10^{12}},\qquad
\rho>\theta+\frac1{625},\qquad
\frac{\theta^2}{\rho^2}<\frac{174}{175}.
\]

For orientation only, theta is about0.57774096418 and rho about0.57940351374.
The exact quotient and rational interval checks, not these decimals,
establish the inequalities.

All facet halfspaces contain the closed ball of radius rho, so
\(\rho B\subset K\). Taking support functions proves the universal,
**exact** covering threshold

\[
\min_{\|y\|=1}\max_{0\le i<13}p_i\cdot y=\rho. \tag{3}
\]

Equality is attained at the outward unit normal of facet(4,5,11), whose
support value is rho. For any y satisfying all additional-point
inequalities \(p_i\cdot y\le\theta\), applying(3) to y/||y|| gives
\(\|y\|\le\theta/\rho\), also trivially for y=0. Its squared norm is
therefore strictly below174/175. This independently proves saturation
and improves the source's199/200 extension-polytope bound. It uses a
complete supporting-plane census, rather than the source's Cramer solves
of all active constraint triples.

## Strict-improvement corollary and scope of other claims

Fifteen disjoint open spherical caps of radius d/2 imply
\(15(1-\cos(d/2))\le2\), hence \(t=\cos d\ge113/225>1/2\).
The [known exact incumbent](../tammes15_contact_pattern_obstruction/README.md)
has cosine tau<3/5. A strict improvement has t<tau and lies in our interval.
When an ear's A pair has no old neighbor, the independently confirmed
saturated core prohibits fifteen points. Otherwise the
[355-case old-neighbor theorem](../tammes15_reflection_family_exclusion/PROOF.md)
applies. It is graph7324
`bafkreiga3kccvkjwrb7ndahtn4bpxoqh5orgmhxd6r4ylw3hgdzn5rp3wu`,
source335ef56bbea29fdf0071fee6521866c452b749e9. Its rootless/continuous/
root branches and six extension cases were natively checked, including
both orientations, the single-unit-vertex cases and strict cap-diameter
guards. Incumbent graph7170
`bafkreiclb5l3bki6mutmsa36pkkt4zw7hf4noeaqtjsa4wr7em3q7zchty`,
source7b0ad2db768b22ee83dc4ce4c92c2e7b142f1779, was natively replayed;
the needed input here is existence and tau<3/5, not its full rigidity
classification. Consequently the target's removed-old-neighbor
corollary is valid with these explicit dependencies.

The later [overlap reduction](../tammes15_bridge_overlap_reduction/PROOF.md),
graph7488, depends on the target; its shared-anchor claims and surviving
ten-point capacities are not reviewed here. The five-profile result
graph7492 cites the target as context, not a premise. This review does
not transfer its verdict to either full claim. Original-label disjointness
and internal injectivity cannot be inferred from normalized fan copies.

## Strengthening and improvement opportunities

**Proved refinement:**(3) gives the exact threshold for appending a point
to this fixed core and identifies its unique minimizing facet. The
extension squared-norm bound improves199/200 to174/175. The determinant
reduction also eliminates radical sign bookkeeping for the ten cases;
unit norms and complete packing checks still establish sufficiency at
the remaining root.

**Proved stability:** let q_i be unit vectors with
\(\|q_i-p_i\|\le\varepsilon\) and let the proposed additional-point
threshold be theta+eta, with epsilon,eta>=0 and
\(\varepsilon+\eta\le1/625\). For every unit y,
\(\max_i q_i\cdot y\ge\rho-\varepsilon>\theta+\eta\).
Thus no additional point fits. This does not assert that the perturbed
thirteen points themselves remain a packing. The nearby stronger gap1/600
is rigorously false at the minimizing direction; the selftest rejects it.

**Next useful extension:** the four shared-triangle decagon types left by
the overlap reduction need their own extension-capacity bounds and an
occurrence/injectivity argument. Neither this saturated disjoint core nor
normalized duplicate labels settle those cases. A parameter-uniform
supporting-plane partition for their continuous families would be a
concrete next lemma; no result about those families is claimed here.

Formalizing the rank-four determinant reduction, reflection cover, exact
root signs and supporting-plane exhaustiveness would remove the ordinary
software/written-reduction trust boundary. It would certify this
conditional motif theorem, rather than supply global contact-graph coverage.

## Reproducibility, independence and literature

`check.py` and `templates.py` import no author source, certificate or
coordinate file. The printed edges, polynomial and normalization are
credited inputs. SymPy1.14.0 supplies exact QQ(t)/quotient arithmetic and
root counts; independently written Fraction intervals certify signs.
Gaussian elimination, Householder placement and dual hull enumeration
replace the source's radical residual, metric-cross frame formula and
active-triple Cramer extension algorithm. The optional author generator
also uses SymPy, so CAS infrastructure is shared, not an independent
software implementation of field arithmetic. The geometry algorithms
and proof computations are separate. CPython3.11.2 was used with one
math job and all BLAS/OpenMP thread variables one.

The original target checker with selftests matched its full expected
output. Closure matched its expected output including certificate hash;
the355-case selftest adds an explicit `controls` message, and removing
only that verified message gives the expected mathematical output.
The incumbent selftest verified both fifteen-point constructions and
their exact noncontact bounds. Exact provenance is in AUDIT.json.
These additional replays do not establish separate independent authorship
of the old proofs.

The live [N15 coordinate archive](https://spherical-codes.org/data/3/15)
was refreshed unchanged:890bytes, SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
[Musin--Tarasov](https://arxiv.org/abs/1410.2536) proves N14 using
irreducible-contact-graph enumeration. Hars, *Numerical Solutions of the
Tammes Problem*, Section10.15, describes incumbent N15 separation under
an assumed full graph; its previously obtained primary text was reread.
Incumbent constructions/quintic are prior Buddenhagen--Kottwitz/Kottwitz
work as cited in the incumbent source. This audit makes no new packing
record or literature-priority claim. Targeted live searches for this
specific exceptional motif/polynomial found no identifiable matching
primary theorem; that is not an exhaustive priority search. Convex
duality and Householder reflection are classical methods.

The result is reproducible and locally consequential, with its hypothesis
cover and native dependency scopes visible. Global optimizer occurrence,
complete graph coverage, global optimality, peer publication and formal
proof remain separate unresolved obligations.
