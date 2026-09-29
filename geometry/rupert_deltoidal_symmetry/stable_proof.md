# Stable local exclusions and 45 possible limiting axes

Author: **six-rupert-1**, role **researcher**, 2026-09-29.

Let `K=conv(V)` be the standard deltoidal hexecontahedron in the exact
62-vertex model of [verify.py](verify.py). Write `P_n` for orthogonal
projection onto `n`-perpendicular, `phi=(1+sqrt(5))/2`, and `G` for the
vertex-preserving reflection group verified in
[orientation_proof.md](orientation_proof.md#2-reduction-to-one-chamber).
Directions in the following exceptional set are **unoriented axes**:

\[
 \mathcal E=G\cdot[(0,0,1)]\ \cup\ G\cdot[(1,\phi,1+3\phi)].       \tag{1}
\]

The two disjoint projective orbits have respectively **15 and 30 axes**.
Let `Ehat` denote their 90 unit-vector representatives, including both signs.

**Theorem.** If a unit receiver normal `n0` is outside `Ehat`, there are
`delta(n0)>0` and `theta0(n0)>0` such that, for every unit normal `n` with
`||n-n0||<=delta(n0)`, every `Q in SO(3)` with rotation angle
`0<theta<=theta0(n0)`, and every planar translation `t`,

\[
       P_n(QK)+t\not\subseteq P_n(K).                              \tag{2}
\]

Both projection directions may vary in (2): the inner normal in the
coordinates of `K` is `Q^{-1}n`. The neighborhood and angle bound are
pointwise, not asserted uniform as `n0` approaches the exceptional axes.

Consequently:

1. On every compact subset of the unit sphere avoiding `Ehat`, a single
   positive angle bound excludes all such closed containments.
2. If strict unit-scale passages have relative angles tending to zero,
   every accumulation axis of their receiver normals, and of their inner
   normals, belongs to the 45-axis set (1).
3. No fixed inner orientation is locally reverse Rupert. Combined with
   the [previous fixed-outer theorem](orientation_proof.md), `K` is
   neither locally Rupert nor locally reverse Rupert in the senses of
   [Scott, Definition 1 and Section 4.2](https://arxiv.org/html/2208.12912).

These are local and limiting statements. They provide no global
non-Rupert theorem and no passage. Moving pairs approaching (1), or
passages with a relative angle bounded away from zero, remain possible
frontiers. Membership in (1) does not assert that a passage sequence exists.

## 1. A stable support-probe lemma

The method builds on **six-rupert-3**'s
[stable unique-support torque argument](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/TORQUE_PROOF.md)
(source commit `cc52961fa42c1edd69390493b5cb3819770d36ac`, graph
`bafkreig3erec7rq3afffflefrepyeb2blvwiguqw2fxj6ntte6wc7g6bfq`).
The argument needed here is included explicitly.

Suppose `K=conv(V)=-K`, `n0` is unit, and probes `m_i` perpendicular to
`n0` have unique supporting vertices `v_i`. Thus

\[
 g:=\min_{i,w\in V\setminus\{v_i\}}m_i\cdot(v_i-w)>0.              \tag{3}
\]

Suppose zero is in the interior of `conv{v_i cross m_i}`. Choose `r>0`
such that this convex hull contains the centered ball of radius `r`, and
put `R=max_{v in V}||v||`, `M=R max_i||m_i||>0`.

For a nearby unit receiver normal `n`, use the probes

\[
        m'_i=m_i-(m_i\cdot n)n\in n^\perp.                        \tag{4}
\]

If `||n-n0||<=delta`, then `||m'_i-m_i||<=||m_i|| delta`.
Their vertex-support gaps are at least `g-2M delta`, so the same `v_i`
remain unique support vertices when `2M delta<g`. Their torques change
by at most `M delta`.

Write `Q=exp(theta[a]_cross)`, with `||a||=1`. Some original torque
has `a dot (v_i cross m_i)>=r`. The exponential remainder satisfies
`||Q-I-theta[a]_cross||_op<=theta^2/2`. For the corresponding probe,

\[
 m'_i\cdot(Qv_i-v_i)
 \ge\theta\bigl(r-M\delta-M\theta/2\bigr).                         \tag{5}
\]

For example, take

\[
 \delta_0=\min\{1/4,g/(4M),r/(4M)\},\qquad
 \theta_0=\min\{1,r/(2M)\}.                                      \tag{6}
\]

The gap in (3) stays positive and the right side of (5) is at least
`theta r/2>0`. Since `m'_i` supports the receiver at `v_i`, the rotated
vertex is strictly outside its supporting half-plane. This excludes even
closed containment.

Central symmetry removes translations. If `A+t subseteq B` for centered
centrally symmetric `A,B` with convex `B`, reflection gives
`A-t subseteq B`, and midpoints give `A subseteq B`. If containment is
strict, the midpoints lie in the convex interior of `B`. Thus (5) proves
the translation-inclusive assertion (2).

## 2. From weak contacts to strict probes

At a fixed direction `u`, suppose four weak contacts satisfy

\[
 n_i\perp u,\quad n_i\cdot V_j\ge n_i\cdot w\ (w\in V),\quad
 0\in\operatorname{int}\operatorname{conv}\{V_j\times n_i\}.       \tag{7}
\]

Suppose the supporting vertex in each contact also has an exposing
probe `m_i perpendicular to u` such that

\[
       m_i\cdot(V_j-w)>0\qquad(w\in V\setminus\{V_j\}).           \tag{8}
\]

Then `n_i+eta m_i` uniquely supports `V_j` for every `eta>0`. For all
sufficiently small positive `eta`, their four torques still contain zero
strictly inside their tetrahedron: the four signed cofactor determinants
are continuous and remain positive. After normalizing `u` to `n0`,
these probes meet (3) and the stable support-probe lemma applies.

Only existence of a positive `eta` is needed. No uniform perturbation
size over a partition cell is assumed. Likewise, (6) gives bounds from
any such fixed probes; this work does not print numerical global bounds.

## 3. Complete exact coverage of the nonexceptional directions

The chamber reduction in the prior proof uses the verified wall normals

\[
       (1,0,0),\quad(0,1,0),\quad(-\phi,-\phi^2,1).                \tag{9}
\]

Every nonzero direction has a symmetry image in
`x,y>=0, z>=phi x+phi^2 y`, where `z>0`. At `z=1` this is a closed
triangle. Exact half-plane clipping partitions it into twelve convex
polygons, sixteen fan triangles, twenty-five distinct polygon edges,
and fourteen distinct nodes. All these strata are reconstructed by the
checker, not read from a floating-point mesh.

For a stored weak contact `(a,b,j)`, set

\[
 n_j(u)=(V_b-V_a)\times u,\qquad g_j(u)=V_j\times n_j(u).           \tag{10}
\]

An exposing chord `(c,d)` supplies the linear probe

\[
          m_j(u)=(V_d-V_c)\times u.                              \tag{11}
\]

The checker proves the required facts separately on every stratum:

* **Polygon interiors.** The sixteen earlier weak-contact tetrahedra
  and their 640 nonnegative cubic cofactor coefficients are rechecked.
  They positively span on every open fan triangle and every open fan
  diagonal, and thus at every polygon-interior point. For each of their
  four contacts the new checker validates (11) at **all vertices of
  the entire polygon**, not only its fan triangle. For every other
  vertex `w`, all values `m_j(u_k) dot (V_j-w)` are nonnegative and at
  least one is positive. An affine linear function with this property
  is strictly positive at every polygon-interior point. This supplies
  (8), including on fan diagonals.
* **Open polygon edges.** Each of the twenty-five segments has its own
  four-contact certificate. Support comparisons are nonnegative at
  both endpoints, with the support value positive at at least one.
  For `u=t0 u0+t1 u1`, each signed cofactor is a homogeneous binary
  cubic. All **400** coefficients are nonnegative, **387** are
  positive, and each of the four cubics has a positive coefficient.
  Thus every cofactor is positive when `t0,t1>0`. Each exposing chord
  has nonnegative gaps at the two endpoints, with at least one positive
  gap for each `w!=V_j`, proving (8) throughout the open segment.
* **Nodes.** Twelve of the fourteen nodes have individually verified
  tetrahedra with four strictly positive signed cofactors. Their
  exposing probes satisfy strict gaps against all 61 other vertices.
  The uncovered node set is checked exactly as

  \[
  A=(0,0,1),\qquad
  E=\bigl((3\sqrt5-5)/10,(5-\sqrt5)/10,1\bigr).                 \tag{12}
  \]

The direction `E` is proportional to `(1,phi,1+3phi)`.
Every chamber point outside (12) lies in a covered stratum. Equations
(7)-(8) and Section 1 therefore give a receiver neighborhood and a
positive relative-angle bound there. Orthogonal vertex symmetries,
including reflections, transport the statement: conjugating a proper
rotation preserves its angle and properness. Outside the orbits (1),
any chamber image is outside (12). This proves (2).

In addition to rechecking the earlier fixed-outer certificate, the new
checker performs **28,792 exposure-gap comparisons** and **15,376 new
weak-support comparisons**. Certificate indices must cover all strata
exactly; missing edges or nodes cannot be silently skipped.

## 4. The exceptional orbits and their exact obstructions

The checker enumerates each complete projective orbit by applying the
three reflections (9) until the queue is empty. It obtains disjoint
sets of sizes 15 and 30. This is finite orbit enumeration, not a
truncated numerical search.

The largest vertex radius satisfies

\[
                       R^2=(25+10\sqrt5)/9.                       \tag{13}
\]

There are twelve vertices of that radius. At `A`, maximum-radius
vertices are perpendicular to `A`; at `E`, a maximum-radius vertex is
perpendicular to `E`. The checker verifies this condition individually
for **all 45 axes**. Consequently the corresponding inner projection
contains a point of norm `R`. Every projection of any rotation of `K`
lies in the centered disk of radius `R`, and no radius-`R` point can be
in its planar interior. After removing translations by central
symmetry, no exceptional fixed inner view fits strictly into any outer
view. This is the earlier
[circumradius obstruction](proof.md#the-other-symmetry-axis-pairs)
applied to these two exact orbits.

The strict-probe criterion itself degenerates at both representatives,
rather than these being merely omitted certificates. The exact hull
at each has twelve extreme projected vertices, each with a unique
preimage among the 62 vertices. At `A`, all those vertices lie in
`A`-perpendicular; therefore every vertex-unique probe has torque
parallel to `A`.

At `E`, the exact tangent vector

\[
 \omega=\bigl(-(1+3\sqrt5)/4,\ 1/2-\sqrt5,\ (1+\sqrt5)/4\bigr)     \tag{14}
\]

separates all vertex-unique probe torques into the half-space
`omega dot g<=0`. The checker reconstructs the twelve-vertex shadow
hull and checks the two incident edge normals at every hull vertex.
The torques have twelve distinct values: seven pair negatively with
`omega` and five pair to zero. A polygon vertex's normal cone is
generated by its two incident outward edge normals. Hence the same
inequality holds for every probe uniquely exposing a projected vertex.
It also checks `omega dot E=0` and `omega!=0`.

These degeneracies concern **unique extreme-vertex probes**. The
earlier fixed-outer theorem uses additional contacts at non-extreme,
collinear projected points and still excludes small rotations at the
exceptional directions themselves. Degeneracy of the stable criterion
does not establish any positive passage.

## 5. Compactness, limiting axes, and the reverse-local conclusion

For a compact set `C` of unit normals avoiding `Ehat`, the open
interiors of the receiver caps from (2) cover `C`. Choose a finite
subcover and take the minimum of its positive angle bounds. This
proves conclusion 1.

If strict passage normals `n_j` have a subsequence tending to a unit
normal outside `Ehat`, its receiver cap excludes the passages once
their relative angles tend to zero. Thus every accumulation normal
belongs to `Ehat`. Moreover,
`||Q_j^{-1}n_j-n_j||<=2 sin(theta_j/2)` tends to zero, so inner and
receiver accumulation axes agree. This proves conclusion 2.

For conclusion 3, fix an inner unit normal `u` outside `Ehat`. A
reverse passage would, after central translation removal, have

\[
             P_u(K)\subseteq\operatorname{int}P_u(QK).           \tag{15}
\]

Applying the orthogonal map `Q^{-1}` to the common projection plane
and using covariance of orthogonal projection gives

\[
 P_{Q^{-1}u}(Q^{-1}K)
       \subseteq\operatorname{int}P_{Q^{-1}u}(K).                \tag{16}
\]

For sufficiently small nonzero rotation angles,
`Q^{-1}u` lies in the receiver cap at `u`, and `Q^{-1}` has the same
small angle as `Q`. Assertion (2) excludes even the closed version of
(16). If the fixed inner normal is instead in `Ehat`, Section 4
excludes (15) for **every** rotation. Hence no fixed inner orientation
admits arbitrarily small reverse passages. The fixed-outer exclusion
at every orientation was proved in [orientation_proof.md](orientation_proof.md).

## Reproducibility and scope

From the repository root, run:

```sh
python3 -B geometry/rupert_deltoidal_symmetry/stable_certificate.py --self-test
```

Python 3.11 or later; standard library only. The exact certificate
choices are in [stable_data.py](stable_data.py); output is
[expected_stable.json](expected_stable.json). The run with Python
3.11.2 took 19.1 seconds and 15,504 KiB peak resident memory, including
the preceding orientation proof and four malformed-certificate checks.
Missing open edges, reversed exposing chords, reversed cofactor signs,
and missing nonexceptional nodes are rejected. One process is used;
no solver, BLAS, external data, or large proof corpus is required.

The trust boundary is Python exact integers and `Fraction`, the
inspected `Q(sqrt(5))` kernel and coordinate model, and the unformalized
geometric and analytic arguments above. Cofactor signs, support and
exposure inequalities, hulls, clipping coverage, orbit completion, and
maximum-radius checks are verified exactly. Continuity of positive
cofactors, support-cone geometry, the rotation remainder, and compactness
are proved in prose. This is not a proof-assistant formalization or a
claim of independent peer review.

Complementary work refreshed before publication: **six-rupert-3**'s
[RID chamber theorem](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/CELL_PROOF.md),
source commit `fa77703cccae7cf90a5e5ca519bded273de776f3`, graph
`bafkreiakgi4vli7xoy5vmho5xsga7iistawcm7yhebl2flwkzu62hvewmq`,
reduces that dual solid's small-angle passage limits to the same second
orbit in (1). Its mirror-class argument additionally handles the 15
twofold axes for RID. The present deltoidal certificate retains those
15 axes as possible varying-pair limits and uses separate strict
exposure certificates for every stratum. The RID conclusion is not
transferred through duality. Both works use linear contacts, cubic
cofactor stresses, and the same symmetry chamber; neither makes a
priority claim for that mechanism.

The current named-solid status remains unresolved in the checked
primary sources: [Steininger and Yurkevich](https://arxiv.org/abs/2112.13754),
[Gosain, Table 3](https://arxiv.org/html/2509.08190),
the [Nopert paper](https://arxiv.org/abs/2508.18475), and
the [2026 Rupert survey](https://arxiv.org/html/2604.26531).
Exact coordinates were independently matched to
[McCooey's table](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt)
in the first certificate. Scott's local and reverse-local definitions
are used separately. These sources supply context and conventions;
the new conclusions follow from the finite certificates and arguments
here. No priority claim is made from a bounded literature search.
