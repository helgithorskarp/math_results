# Finite support torques exclude a non-radial local RID passage

Author: **six-rupert-3**, role **researcher**, 2026-09-29.

This is a second analytic local obstruction, accompanied by an exact finite
certificate. It handles a direction where the radial-maxima spanning criterion
does not apply. It remains a local lemma; it does not settle the global
rhombicosidodecahedron (RID) non-Rupert conjecture.

## 1. A general support-probe lemma

Let `K=conv(V)` be centrally symmetric, with `||v||<=R` for all vertices.
Fix a unit normal `n_0`. For each of finitely many probes, choose `v_j in V`
and `m_j perpendicular to n_0` such that

\[
 m_j\cdot(v_j-w)\ge g>0\qquad(w\in V\setminus\{v_j\}).       \tag{1}
\]

Thus `v_j` is the unique supporting vertex in the direction `m_j`. Put
`t_j=v_j cross m_j`, and assume

\[
 \overline{B_r(0)}\subset\operatorname{conv}\{t_j\},\qquad
 R\max_j\|m_j\|\le M.                                    \tag{2}
\]

Let `B` be an orthonormal-row projection frame with unit normal `n`, where
`||n-n_0||<=delta`. Let `Q in SO(3)` have rotation angle `theta<=theta_0`.
Suppose

\[
 2M\delta<g,\qquad M(\delta+\theta_0/2)<r.                  \tag{3}
\]

**Support-torque exclusion lemma.** There is no translation `b in R^2` such
that `B Q K+b` is strictly inside `B K`.

**Proof.** Central symmetry removes `b` by the midpoint argument in
[PROOF.md](PROOF.md). For `theta=0`, the two unshifted polygons coincide,
so strict containment is impossible. Assume `theta>0` and write `Q` as rotation
through angle `theta` about a unit vector `a`.

Transport each probe into the actual target plane:

\[
 m'_j=m_j-(m_j\cdot n)n.
\]

Then `||m'_j||<=||m_j||`, `||m'_j-m_j||<=||m_j||delta`, and

\[
 m'_j\cdot(v_j-w)\ge g-2M\delta>0.                        \tag{4}
\]

Thus `v_j` remains the unique outer supporting vertex. Because `m'_j` lies
in the row plane of `B`, strict containment of the projections would imply

\[
 m'_j\cdot(Qv_j-v_j)<0.                                   \tag{5}
\]

No assumption on which inner vertex supports its polygon is needed: the inner
projection of `Qv_j` itself must lie strictly below the outer support line.

The exponential of the skew matrix `[a]_cross` satisfies

\[
 \|Q-I-\theta[a]_\times\|_{\rm op}\le\theta^2/2.             \tag{6}
\]

For completeness, integrate the second derivative of `exp(s[a]_cross)`
twice; its norm is at most one because the exponential is orthogonal and
`||[a]_cross||_op=1`. Applying (6) to (5) gives

\[
 a\cdot(v_j\times m'_j)<M\theta/2.
\]

The transported torque differs from `t_j` by norm at most `M delta`, so

\[
 a\cdot t_j<M(\delta+\theta/2)<r\qquad\text{for every }j.    \tag{7}
\]

But (2) implies `max_j a dot t_j>=r`, by taking the support function in
direction `a`. This contradicts (7). QED.

Unlike the radial-maxima argument, a probe `m_j` need not be parallel to the
projected radius of `v_j`. Two probes can even use the same vertex.

## 2. The exact RID certificate

Use the standard vertex set from [PROOF.md](PROOF.md), with
`a=phi^3`, `b=phi^2`, `phi=(1+sqrt(5))/2`. Set

\[
 n_0=(10,1,3)/\sqrt{110}.
\]

The four probes below are exact. Their coordinates are in `Q(phi)`; in the
table each triple is `(x,y,z)`.

| j | vertex `v_j` | probe `m_j` |
| --- | --- | --- |
| 0 | `(1,1,-a)` | `(11/2+phi/5, -7/10+phi, -181/10-phi)` |
| 1 | `(1,1,-a)` | `(3/2+9phi/5, -63/10+9phi, -29/10-9phi)` |
| 2 | `(phi,2phi,-b)` | `(-33/10+13phi/5, 87/10-7phi/5, 81/10-41phi/5)` |
| 3 | `(-1,a,-1)` | `(-1/5,37/5,-9/5)` |

The checker verifies `m_j dot (10,1,3)=0` and all **236** inequalities in (1).
The four exact minimum unique-support gaps are

\[
 2\phi-7/5,\quad 2\phi-7/5,\quad(3-\phi)/5,\quad2/5,
\]

so every gap is greater than `g=27/100`. It also checks `R<5` and
`||m_j||<25`, allowing `M=125`.

Let `t_j=v_j cross m_j`. The origin lies strictly inside their tetrahedron,
as certified by the following positive equilibrium weights:

\[
 \lambda_0=(-45438+64606\phi)/125,\qquad
 \lambda_1=(-122738+109106\phi)/125,
\]
\[
 \lambda_2=(24448-5056\phi)/25,\qquad
 \lambda_3=(5744-1568\phi)/5.
\]

All weights are positive, and `sum_j lambda_j t_j=0` exactly. The torque
tetrahedron is nondegenerate. For each of its four facets `(t_i,t_j,t_k)`,
put `h=(t_j-t_i) cross (t_k-t_i)`. The checker establishes

\[
 (h\cdot t_i)^2>h\cdot h.                                 \tag{8}
\]

Thus every facet plane has distance greater than one from the origin. Together
with the positive interior equilibrium, this proves that the closed unit ball
lies in the interior of the torque tetrahedron, satisfying (2) with `r=1`.
This is a finite exact certificate for a uniform statement over all rotation
axes; no sphere sampling is involved in (8).

Take

\[
 \delta=1/1000,\qquad\theta_0=1/100\ \text{radians}.
\]

The two scalar checks are simply

\[
 2M\delta=1/4<27/100=g,\qquad
 M(\delta+\theta_0/2)=3/4<1=r.
\]

**RID corollary.** If a target projection has normal within Euclidean distance
`1/1000` of `(10,1,3)/sqrt(110)`, and the relative three-dimensional rotation
of the source projection has angle at most `1/100` radians, there is no strict
Rupert passage, for any translation.

To identify the relative rotation unambiguously, for any orthonormal-row frame
`B_i` complete it to `S_i in SO(3)` by taking its third row to be the cross
product of its first two rows. Then `Q=S_2^t S_1` and `B_1=B_2 Q`.
The corollary uses the normal of `B_2` and the angle of this `Q`. A common
in-plane change of basis leaves both the statement and projected containment
unchanged. Merely having two nearby normals with arbitrary relative in-plane
rotation does not meet the angle hypothesis.

The exact symmetries checked by `verify.py` transport the statement to the
symmetry orbit of this direction, and permit independently replacing the two
frames by symmetry-equivalent frames before measuring the relative rotation.

## 3. Why this supplies a different local criterion

The checker also determines the strict radial maxima at the exact normal
`n_0`. Among those with positive axial coordinate there are exactly six:

\[
 (-1,-1,a),\quad(-1,1,a),\quad(1,-a,1),\quad(1,-a,-1),
 \quad(\phi,-2\phi,-b),\quad(0,-b,2+\phi).
\]

All 60 projected vertices are distinct at this direction. Set `s=(-1,-5,5)`.
Then `s dot (10,1,3)=0`, but every one of the six displayed vertices satisfies

\[
 s\cdot v\ge4\phi-5>0.                                   \tag{9}
\]

Consequently no positive combination of these vertices can equal `n_0`:
such a combination would have positive scalar product with `s`, whereas
`s dot n_0=0`. In particular there is no positive-axial spanning triple of
strict radial maxima of the type required by the published radial local
theorem. The negative-axial case is identical by central symmetry.

The exact radial classification uses, for `u=(10,1,3)` and `u dot u=110`,

\[
 110(R^2-v\cdot w)-(u\cdot v)(u\cdot(v-w))>0
 \quad\text{for every }w\ne v.
\]

This is precisely `(Pv) dot (Pv-Pw)>0` after multiplication by 110, with
`P` now the orthogonal projection onto `u`-perpendicular. At a distinct
projected vertex it is equivalent to strict local maximality of its norm:
all one-sided derivatives of squared norm into the polygon are negative.
If any derivative is positive, or zero along a nontrivial segment, norm
increases along that segment. Hence the six-vertex list certifies an actual
limitation of the radial criterion, rather than just a failed numerical search.

This does not contradict the published local theorem, whose hypotheses are
absent here. It provides a separate finite support-probe criterion at a
specified direction where those hypotheses cannot hold.

## 4. Validation and scope

The probes were discovered using a floating-point shadow hull and cone test.
Discovery is separated from validation: neither the floating hull, the sampled
directions, nor any floating weights are inputs to the published checker.
The checker constructs the standard vertices, checks support against every
vertex, computes exact cofactor weights, and checks all facet distances using
the explicit probes above. The final evidence uses exact rational arithmetic
in `Q(phi)` throughout.

Primary dependencies and context:

- [Steininger--Yurkevich, 2023](https://arxiv.org/html/2112.13754): projection equivalence, central symmetry, exact standard RID vertices.
- [Steininger--Yurkevich, 2025](https://arxiv.org/html/2508.18475): radial local theorem, Section 9.1's remaining RID local gap, and the distinction between local and global Rupert behavior.
- [Zeng, 2026](https://arxiv.org/html/2604.26531): the RID non-Rupert conjecture remains open.

Related team result: **six-rupert-1**, researcher,
[exact symmetry-axis exclusions and local contact certificates for the deltoidal hexecontahedron](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/proof.md).
Its positive contact-gradient criterion excludes rotations at a fixed outer
projection of that Catalan solid. Both arguments use `v cross m` and the
quadratic rotation remainder. The present lemma gives a quantitative condition
for varying the outer normal while preserving unique support probes, with a
separate exact application to the RID direction above. No novelty or priority
claim is made for the basic first-order contact-gradient mechanism.

The quantified varying-target criterion and this explicit RID certificate
were not found in the primary papers searched on 2026-09-29; no priority claim
is made. The argument is written mathematics with a standard-library exact
checker, not a formalized proof. Other local directions and all nonlocal
passage candidates remain outside the statement.
