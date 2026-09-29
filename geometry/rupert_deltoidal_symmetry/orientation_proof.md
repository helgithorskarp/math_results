# Every fixed orientation has a local rotation exclusion

Author: **six-rupert-1**, role **researcher**, 2026-09-29.

Let `K` be the standard deltoidal hexecontahedron, with the exact 62-vertex
model in [verify.py](verify.py) and [proof.md](proof.md). For a nonzero
direction `u`, let `P_u` be orthogonal projection onto `u`-perpendicular.

**Theorem.** For every `u != 0` there exists `epsilon(u)>0` such that,
for every `Q in SO(3)` with rotation angle
`0 < theta <= epsilon(u)` and every planar translation `t`,

\[
       P_u(QK)+t\not\subseteq P_u(K).                       \tag{1}
\]

Thus this solid is not locally Rupert in the fixed-outer definition of
[Scott, Definition 1](https://arxiv.org/html/2208.12912#S2).
The assertion includes all directions, including boundaries between
silhouette types. The bound is allowed to depend on the fixed outer
direction. It does not exclude two independently varying orientations,
does not assert a uniform bound over directions, and does not settle
the global Rupert property. The reversed, fixed-inner local question is
also outside this theorem.

[orientation_certificate.py](orientation_certificate.py) verifies the
finite inequalities below in exact `Q(sqrt(5))` arithmetic. There are no
floating-point decisions in this verification and no external input files.

## 1. A contact-cone lemma

Suppose `K=conv(V)=-K`, and fix `u`. Choose finitely many contacts
`(v_i,n_i)` satisfying

\[
 n_i\cdot u=0,\qquad b_i=n_i\cdot v_i>0,\qquad
 n_i\cdot w\le b_i\quad(w\in V).                          \tag{2}
\]

Put `g_i=v_i cross n_i`. If zero is in the interior of
`conv{g_i}`, there is an `r>0` such that

\[
       \max_i a\cdot g_i\ge r\qquad(\|a\|=1).             \tag{3}
\]

Write a rotation of angle `theta` as `Q=exp(theta[a]_cross)` and take
`R=max_{v in V} ||v||`, `M=R max_i ||n_i||`. Integration of the second
derivative of this exponential gives

\[
 \|Q-I-\theta[a]_\times\|_{op}\le\theta^2/2.               \tag{4}
\]

For the contact supplied by (3),

\[
 n_i\cdot(Qv_i-v_i)
 \ge \theta r-M\theta^2/2>0
       \quad(0<\theta\le\min\{1,r/M\}).                  \tag{5}
\]

Its rotated vertex is outside an outer support half-plane. This proves
(1) without translation. Central symmetry removes any translation:
if `P+t subseteq S`, with `P=-P` and `S=-S` convex, then both
`p+t` and `p-t` lie in `S` for every `p in P`, and their midpoint `p`
lies in `S`. The same argument works with strict containment.

The preceding [fixed symmetry-axis certificate](proof.md#a-reusable-contact-gradient-certificate-and-local-bound)
uses this mechanism. The present work constructs contact cones for every
direction, rather than only three symmetry representatives.

For four vectors `g_0,...,g_3`, define

\[
 L_i=(-1)^i\det(g_0,...,\widehat{g_i},...,g_3).              \tag{6}
\]

The determinant cofactor identity gives `sum_i L_i g_i=0`.
If either all `L_i>0` or all `L_i<0`, the vectors span `R^3` and zero
is strictly inside their tetrahedron. Indeed, their column matrix has
rank three and its one-dimensional kernel has a vector with four
positive coordinates. Adding a row of ones gives an invertible affine
coordinate matrix. Its barycentric coordinates of zero are positive.
This establishes (3).

An explicit pointwise choice of `r` is the minimum distance from zero to
the four tetrahedron facet planes. If a facet uses `g_i,g_j,g_k`, its
normal is `h=(g_j-g_i) cross (g_k-g_i)`, and its distance is
`|h dot g_i|/||h||`. These distances are positive under the preceding
hypothesis. Equations (3)-(5) then give an explicit, possibly small
`epsilon(u)`.

## 2. Reduction to one chamber

Write `phi=(1+sqrt(5))/2`. The checker verifies that reflections in the
three planes with normals

\[
        (1,0,0),\quad(0,1,0),\quad(-\phi,-\phi^2,1)        \tag{7}
\]

all permute the 62 exact vertices of `K`. These reflections generate a
finite orthogonal group: its faithful action on the finite vertex set
embeds it into a finite permutation group, since the vertices span
`R^3`.

Every nonzero direction has an image under this group in

\[
       x\ge0,\quad y\ge0,\quad z\ge\phi x+\phi^2y.         \tag{8}
\]

To see this, choose an orbit point maximizing its `z` coordinate, and
then use the first two reflections to make `x,y>=0`. It still maximizes
`z`. If the last inequality in (8) failed, reflection in the third
plane would increase `z`, a contradiction. Equations (8) force `z>0`
for a nonzero point. Rescaling to `z=1` gives the closed triangle

\[
 A=(0,0,1),\quad B=(1/\phi,0,1),\quad C=(0,1/\phi^2,1).    \tag{9}
\]

Orthogonal vertex symmetries transport (1), even if their determinant
is negative: conjugating `Q` by such a symmetry gives another proper
rotation with the same angle, and preserves all projected containments.
Consequently it suffices to prove the theorem throughout triangle (9).

## 3. A finite polynomial certificate on the triangle

The partition planes are `n dot u=0`, where `n` ranges over cyclic
permutations and independent sign changes of

\[
 (1,1,\phi^3),\quad(\phi,2\phi,\phi^2),\quad
 (0,\phi^2,2+\phi).                                      \tag{10}
\]

There are 60 directions and 30 distinct unoriented planes. Splitting
(9) by these planes yields twelve convex polygons, with sizes
`3,4,3,3,4,3,4,3,4,3,3,3`. Taking the fan from each polygon's first
vertex gives sixteen closed triangles with fourteen distinct vertices.
The checker reconstructs every split by exact half-plane clipping,
checks area preservation, and requires exactly one certificate for
every resulting triangle. Its coverage follows from the elementary
clipping operation, not from sampled directions or aggregate counts.
No completeness assertion about three-dimensional facets is needed.

Number the exact sorted vertices `V_0,...,V_61` as in `verify.py`.
For a stored contact `(a,b,j)` set

\[
 e=V_b-V_a,\qquad n(u)=e\times u,\qquad
 g(u)=V_j\times(e\times u).                               \tag{11}
\]

Both `n(u)` and `g(u)` are linear functions of `u`. For each of the
four stored contacts on a triangle `T=(u_0,u_1,u_2)`, the checker proves
at **all three** vertices of `T` that

\[
 n(u_k)\cdot V_j>0,\qquad
 n(u_k)\cdot V_a=n(u_k)\cdot V_b=n(u_k)\cdot V_j,
\]
\[
 n(u_k)\cdot(V_j-w)\ge0\qquad(w\in V).                    \tag{12}
\]

Linearity proves (2) for every nonzero positive combination of the
three triangle vertices. This includes all of its boundary. There
are **11,904** individual support comparisons in (12).

For `u=t_0u_0+t_1u_1+t_2u_2`, each signed cofactor in (6) is a
homogeneous cubic in `t_0,t_1,t_2`. The checker obtains its ten monomial
coefficients by determinant multilinearity. For example, the coefficient
of `t_0^2 t_1` in `det(g_a(u),g_b(u),g_c(u))` is

\[
 \det(g_a(u_1),g_b(u_0),g_c(u_0))
 +\det(g_a(u_0),g_b(u_1),g_c(u_0))
 +\det(g_a(u_0),g_b(u_0),g_c(u_1)).                        \tag{13}
\]

All **640** coefficients are nonnegative, and **626** are strictly
positive. Each of the four cubics on every triangle has a positive
coefficient. Hence they are all positive when `t_0,t_1,t_2>0`.

For each open triangle edge, the checker also requires that every
cubic have a positive coefficient involving only the two coordinates
of that edge. Therefore every cubic is positive on every open edge,
including fan diagonals, partition lines, and the chamber boundary.

Finally, at thirteen of the fourteen distinct triangle vertices, at
least one incident certificate has four strictly positive pure cubic
coefficients. It therefore proves (6) directly at that vertex. The
checker determines the uncovered set **exactly** as `{A}`; it does not
discard degenerate or boundary cases.

## 4. The exceptional twofold corner and conclusion

At `A=(0,0,1)`, several extra collinear contacts are present. The old
[local_certificate.py](local_certificate.py) supplies six exact positive
combinations of the normalized gradients `(v cross n)/b`, giving the
six signed coordinate vectors with total weights less than seven.
The new checker rederives and verifies those six combinations at `A`.
Their positive cone is `R^3`; since the contact set is finite, zero is
in the interior of its convex hull. Thus the contact-cone lemma applies
at the last direction too. The previous quantitative bound of
`1/10 radians` is available at this corner.

Sections 3 and 4 cover the entire closed triangle, Section 2 covers
every direction by vertex symmetries, and Section 1 proves (1). QED.

## 5. Reproduction, context, and trust boundary

From the repository root, using Python 3.11 or later:

```sh
python3 -B geometry/rupert_deltoidal_symmetry/orientation_certificate.py --self-test
```

Its compact output is [expected_orientation.json](expected_orientation.json).
The self-tests reject a missing triangle, a reversed support normal,
a reversed cofactor sign, and a repeated contact. Every field in the
expected output records a finite hypothesis above; matching output by
itself is not a substitute for the proof.

The field implementation and exact coordinate generator are shared
with the previous contribution. The generator was independently
matched entry by entry to
[McCooey's coordinate table](https://dmccooey.com/polyhedra/DeltoidalHexecontahedron.txt).
The new checker needs no downloaded table, scientific package, solver,
or omitted large artifact. Exploratory floating-point choices of contacts
are not trusted: each stored contact, support inequality, coefficient,
wall symmetry, corner combination, and coverage boundary is rechecked.
The analytic bridges in Sections 1-3 and correctness of rational field
arithmetic are written mathematics and inspected source, not a
proof-assistant formalization.

Primary context checked on 2026-09-29:

- [Scott, 2022](https://arxiv.org/html/2208.12912): precise fixed-outer
  local definition, fixed-inner reverse definition, and polygonal-section
  sufficient conditions. The present result uses the former definition.
- [Steininger--Yurkevich, 2023](https://arxiv.org/html/2112.13754):
  projection equivalence and the central-symmetry translation reduction.
- [Steininger--Yurkevich, 2025](https://arxiv.org/html/2508.18475):
  local and global exclusion methods and the Noperthedron counterexample.
- [Fredriksson](https://arxiv.org/html/2210.00601),
  [Gosain--Grimmer](https://arxiv.org/html/2509.08190), and
  [Zeng](https://arxiv.org/html/2604.26531): current named-solid status;
  the global deltoidal question remains unresolved.

The all-direction certificate above was not found in the bounded primary
sources searched; no priority claim is made for the contact-gradient
mechanism or the result. Complementary team work by **six-rupert-3**
uses [stable unique-support probes for a varying rhombicosidodecahedron receiver](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/TORQUE_PROOF.md).
That varying-normal condition is not assumed or concluded here.

Next: replace the varying contact sets by stable support probes where
possible, and handle independently moving pairs near the twofold
directions with separate geometric inequalities. Those tasks, together
with nonlocal passage candidates, are needed for the global problem.
