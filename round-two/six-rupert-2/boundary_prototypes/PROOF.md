# Exact local shadow prototypes and reflected source motions for J74

**six-rupert-2, researcher; 2026-10-01.** This is an author-checked,
unformalized intermediate proof. No independent review or historical
priority is asserted. J74's Rupert property remains unresolved.

Let `s=sqrt(5)>0`, `phi=(1+s)/2`, and let `K=conv(V)` be the unit-edge
metabigyrate rhombicosidodecahedron from the [original model](../model.py).
Its sixty original vertices have common squared radius

\[
 R^2=(11+4s)/4.
\]

For a unit vector `n`, write `P_n=I-nn^t` and `M_n=I-2nn^t` for
orthogonal projection and reflection in `n^perp`. The six unit minimum
normals, with fixed signs and indexing, are

\[
 m_0=e_x,\quad m_1=e_y,\qquad
 m_2,m_3,m_4,m_5=
 \frac{(1,\epsilon\phi,\delta\phi^2)}{2\phi},
\tag{1}
\]

where `(epsilon,delta)` is respectively `(-1,-1)`, `(-1,1)`, `(1,-1)`,
`(1,1)`. Define the projective unit-normal chord distance

\[
 d_i(n)=\min\{\|n-m_i\|,\|n+m_i\|\},\qquad \rho=1/15.
\tag{2}
\]

This proof retains proper spatial motions, arbitrary planar roll,
physical translation, and all original vertices when establishing
containment. The reduction radius is a domain of exact shadow equality;
it is **not an exclusion cap**.

## Statements

Let `W_i` consist of all original vertices whose projections lie on the
boundary of `P_(m_i)K`, and put `C_i=conv(W_i)`.

1. Each `W_i` has **28** actual original vertices: twenty preimages of the
   twelve shadow corners, and eight additional originals projecting to
   edge interiors. The full-dimensional, 28-vertex polytope `C_i`
   satisfies `M_(m_i)C_i=C_i`. This reflection is not a symmetry of the
   full body at any of the four mixed normals.
2. For **every** unit normal with `d_i(n)<=1/15`,

   \[
   P_nK=P_nC_i.
   \tag{3}
   \]

   Every one of the other 32 original projections lies strictly inside
   this shadow. All 22 proper base configurations from the original
   minimum-fit catalogue map the entire spatial boundary set of their
   source to that of their receiver. Proper marked-plane transports
   reduce the six models to **at most three** representatives
   `C_0,C_1,C_2`.
3. Suppose `Q` is proper orthogonal, `n` is the receiving unit normal,
   and `k=Q^t n` is the source normal. If `d_j(n)<=rho` and
   `d_i(k)<=rho`, then for any `lambda>0` and any `t in n^perp`,

   \[
   \lambda P_n(QK)+t\subseteq P_nK
   \quad\Longleftrightarrow\quad
   \lambda P_n(QC_i)+t\subseteq P_nC_j.
   \tag{4}
   \]

   The same equivalence holds with strict inclusion in the relative
   planar interior. Both normal premises are required for this
   two-sided reduction; it does not localize arbitrary sources.
4. Only the source premise `d_i(Q^t n)<=rho` is needed for the proper
   reflected companion

   \[
   \widetilde Q=M_n Q M_{m_i},\qquad
   P_n(\widetilde QK)=P_n(QK).
   \tag{5}
   \]

   It retains the same receiving normal, scale, translation and shadow,
   without assuming any full-body reflection symmetry. For fixed
   `n,m_i`, the map `Q -> Qtilde` is an involution, and its source normal
   remains in the same projective cap.
5. If `Q_0` is any catalogue base motion from `i` to `j`, then throughout
   `d_j(n)<=rho` both proper motions

   \[
   Q_0\quad\hbox{and}\quad M_nM_{m_j}Q_0
   \tag{6}
   \]

   give exactly the receiver shadow `P_nK`. These are explicit closed
   touching fits of unit scale and zero translation, not strict
   passages. No completeness of these moving families is claimed.

## Exact finite geometry and sharp interior clearance

The [certificate](certificate.json) records, for each signed normal in
(1), twelve cyclic corner indices and the sorted 28 boundary indices.
Indices are zero-based positions in the pinned `model.VERTICES`; an edge
index starts at the corresponding cyclic corner. The production
[checker](check.py) reads these literal indices and validates the entire
polygon against all sixty originals. It does not invoke a hull finder.

Write the projected cyclic corners as `p_e` and set

\[
 a_e=m_i\times(p_{e+1}-p_e).
\]

Every `a_e` is nonzero. Every other declared corner lies strictly in
the halfplane `a_e dot (x-p_e)>0`, and every original lies in its closed
halfplane. These checks prove that the supplied strict convex cyclic
polygon is the full projected hull. Every supporting edge is covered,
and zero support over all edges recovers exactly `W_i`. Thus omitted
vertices are not merely missing from a corner list: their projections
are in the strict interior of the complete polygon.

For each of the 32 omitted originals `v` and all twelve edges, the
checker establishes

\[
 a_e\cdot(v-p_e)>0,\qquad
 \frac{[a_e\cdot(v-p_e)]^2}{a_e\cdot a_e}
 \ \ge\ \gamma^2=\frac{3-s}{8},
 \qquad \gamma=\frac{s-1}{4}>0.
\tag{7}
\]

Since `a_e` is in `m_i^perp`, replacing `v` by `P_(m_i)v` does not
change the numerator. These are physical squared distances to the
supporting lines, with unit-normalization performed explicitly. The
uniform bound is sharp in all six views:

| Axis index | Omitted original attaining (7) | Edge index | Full-body reflection? | Original refuting full-body reflection |
| --- | --- | --- | --- | --- |
| 0 | 36 | 4 | Yes | — |
| 1 | 25 | 5 | Yes | — |
| 2 | 2 | 4 | No | 1 |
| 3 | 4 | 6 | No | 5 |
| 4 | 0 | 0 | No | 1 |
| 5 | 6 | 10 | No | 5 |

For example, a refuting index means its exact reflected original is
absent from the full sixty-vertex set. All originals lie on the common
sphere, so such a reflected point is also absent from `K`: a point on
that sphere cannot be a nontrivial convex combination of other points
on the sphere. For the smaller boundary set, the checker instead
verifies a full reflection permutation of all 28 actual originals in
every view.

The twelve-corner preimage inventory gives twenty originals; it is
essential to retain the other eight edge originals in `W_i`. Dropping
one of them leaves an omitted vertex with zero supporting-line
distance, invalidating the uniform positive clearance argument.

Each `C_i` has full affine dimension: the checker gives three
noncollinear equatorial originals and an off-plane original with
nonzero affine determinant. Every element of `W_i` is an exposed
vertex of `C_i`, since its own dot product uniquely maximizes on the
common sphere. Thus “28 vertices” describes the actual prototype hull,
not just a generating-set size.

For each original base matrix `Q_0`, the checker independently checks
orthogonality, determinant `+1`, `Q_0 m_i=+/-m_j`, and

\[
 Q_0W_i=W_j.
\tag{8}
\]

The catalogue contains two configurations from axis 0 to itself, four
from axis 1 to itself, and one for each ordered pair among axes 2–5.
This is all 22 configurations from the original proof, with 616 actual
boundary matches. Exactly twelve of the configuration tuples also
preserve the full body; no full-body symmetry is assumed for the other
ten. In particular there is a verified proper marked transport from
axis 2 to every mixed axis. Together with the identity representatives
at axes 0 and 1 this proves that at most three marked models suffice.
It does not classify all possible unmarked spatial congruences.

The new finite checker proves (7)–(8), all boundary inventories and all
reflection permutations. The [original geometry proof](../PROOF.md)
supplies the named-body identification, the fact that (1) are exactly
the minimum axes, and the completeness of the base-fit catalogue.
Those original global arguments are not rerun by this small checker.
[DEPENDENCIES.json](DEPENDENCIES.json) pins the five original inputs by
SHA256 to verified source commit
`c038d0689b522a1be2b8ba5aa53d230df0b72181`.

## Uniform support trimming

Here is the continuous bridge from finite clearance to a whole normal
cap. Fix one `m=m_i`, let `E=m^perp`, `P=P_m`, and `C=C_i`.
By the complete edge description and (7), every omitted original
satisfies

\[
 Pv+\gamma B_E\subseteq PC=PK,
\tag{9}
\]

where `B_E` is the closed unit disk. Consequently, for every unit
`a in E`, with support function `h`,

\[
 h_{PC}(a)-a\cdot Pv\ge\gamma.
\tag{10}
\]

Let `L:R^3 -> E` be any linear map with operator norm
`||L-P||<=rho`. Every original has norm `R`; hence each scalar support
evaluation changes by at most `R rho`. Taking the maximum over the
prototype vertices gives

\[
 \begin{aligned}
 h_{LC}(a)-a\cdot Lv
 &\ge h_{PC}(a)-a\cdot Pv-2R\rho\\
 &\ge\gamma-2R\rho>0.
 \end{aligned}
\tag{11}
\]

The last strict inequality is certified without approximation:

\[
 \gamma^2-4R^2\rho^2
   =\frac{587-257s}{1800}>0,
 \qquad 587^2-5\,257^2=14324>0.
\tag{12}
\]

Both squared quantities are positive and `587,257>0`, so the integer
comparison establishes the positive sign. Equation (11) in every
unit planar direction puts each omitted `Lv` strictly inside `LC`
(indeed a disk of radius `gamma-2R rho` around it is contained).
Therefore

\[
 LK=LC
\tag{13}
\]

for every such linear map, including the closed boundary of the
operator-norm domain. This proves a continuum statement rather than
an enumeration of orientations.

## Exact unit-normal transport

Choose the sign of `m` so that a unit `n` satisfying (2) has
`||n-m||<=rho`. The boundary set and prototype are unchanged by this
choice of sign. Write `n=u+zm`, with `u in E` and `z=n dot m>0`.
Let `H_n` be the shortest proper rotation sending `n` to `m`, with
identity action on the orthogonal complement of their span. Set
`T_n=P_m H_n`. For `u!=0`, the rotation matrix on the ordered plane
`(u/||u||,m)` is

\[
 \begin{pmatrix}z&-\|u\|\\\|u\|&z\end{pmatrix}.
\]

The case `u=0` is the identity. It follows exactly that

\[
 T_n|_E=I_E-\frac{uu^t}{1+z},\qquad T_nm=-u,
 \qquad H_nP_n=T_n.
\tag{14}
\]

The only nonzero row of `T_n-P_m` on this two-dimensional plane is
`(z-1,-||u||)`, so

\[
 \|T_n-P_m\|_{\rm op}
   =\sqrt{(1-z)^2+\|u\|^2}
   =\sqrt{2(1-z)}=\|n-m\|\le\rho.
\tag{15}
\]

Apply (13), and undo the proper isometry `H_n` on the image plane.
This gives (3), including strict interior for all omitted originals.
No receiving roll bound is needed: orthogonal planar changes of frame
preserve the equality and the distance statements.

For proper `Q` and `k=Q^t n`, the exact identity
`P_n Q=Q P_k` transfers (3) in the source plane. Together with (3) in
the receiver plane, it replaces both shadows in a containment by
identical sets, proving (4) with unchanged scale and translation.
Relative planar interior is unchanged as well.

## Reflection without a full-body symmetry premise

Fix a source axis `m_i` and put `M=M_(m_i)`. If `d_i(k)<=rho`, then
`d_i(Mk)<=rho` also: `M` interchanges the two signed base normals and
preserves Euclidean distances. Using projection-reflection covariance,
(3) twice, and the finite prototype symmetry, we obtain

\[
 \begin{aligned}
 P_k(MK)&=M P_{Mk}K
        =M P_{Mk}C_i\\
        &=P_k(MC_i)=P_kC_i=P_kK.
 \end{aligned}
\tag{16}
\]

This argument is valid at the four mixed normals where `MK != K`.
The discarded originals remain behind the prototype's support in
both required source directions.

Since both factors `M_n` and `M` have determinant `-1`, the matrix
`Qtilde=M_n Q M` is proper. Using `P_n M_n=P_n` and (16),

\[
 P_n\widetilde QK=P_n QMK
   =Q P_kMK=Q P_kK=P_nQK.
\tag{17}
\]

Its source normal is

\[
 \widetilde k=\widetilde Q^t n=-M k,
 \qquad d_i(\widetilde k)=d_i(k).
\tag{18}
\]

Applying the same map twice gives `Q` because both reflections square
to the identity. This proves (5). The receiver need not lie in any
minimum-axis cap, and all planar rolls, scales and translations are
retained. An improper reflection alone is not being substituted for
a physical proper motion.

For a base `Q_0` from `i` to `j`, (8) and `Q_0m_i=+/-m_j` imply
that `d_i(Q_0^t n)=d_j(n)` and `Q_0C_i=C_j`. Thus (3) yields

\[
 P_nQ_0K=P_nQ_0C_i=P_nC_j=P_nK.
\tag{19}
\]

Finally `Q_0M_(m_i)=M_(m_j)Q_0`, so its companion in (5) is exactly
the second motion in (6). At a signed base normal this companion
coincides with `Q_0`; away from it, (6) supplies two exact reference
families for the equal-tilt and reflected-tilt branches. Equations
(17)–(19) prove shadow equality, not a larger or strictly contained
copy.

## Scope, prior work and next frontier

The [weighted-contact result](../tangent_contacts/PROOF.md) constrains
C1 translated fit paths through these same 22 base configurations;
it identifies equal or opposite normal velocities and rules out a
scale gain through quadratic order. The present result supplies exact
reference fits throughout a quantified neighborhood and an exact
source involution. It does not strengthen that necessary condition
into a local impossibility theorem.

The proper normal-transport mechanism is also used in the
[RID receiving-cap proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_brightness_twofold_caps/PROOF.md).
Translated reflected-source pairing and bilinear matching are prior
mechanisms in the
[J77 mirror-cap proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md).
Those different-body theorems and their numerical constants are not
inputs here. The additional step for asymmetric J74 is the verified
28-original trimming identity (3), which permits the reflection
locally despite its failure as a full-body symmetry. The earlier
independent audit of the original J74 geometry does not audit this
new extension.

Bounded primary status checks on 2026-10-01:
[Gosain–Grimmer, Table 4](https://arxiv.org/html/2509.08190) leaves
J72, J73, J74, J75 and J77 without passages, while
[Zeng](https://arxiv.org/html/2604.26531) reports 87 of 92 Johnson
solids known Rupert. The
[Noperthedron result](https://arxiv.org/abs/2508.18475) treats a
different body. These checks do not establish an exhaustive priority
survey, and the rhombicosidodecahedron seed is a conjectural
obstruction, not an established non-Rupert theorem.

The construction frontier is now a translated fitting problem between
three compact, reflection-symmetric prototypes, when both relevant
normal caps apply. A useful next step is to compare all exact polygon
supports against the two reference families and derive higher-order
or bilinear constraints that decide a neighborhood, or find a strict
unit-scale margin and certify it on the original J74 body. Failure of
a floating-point search would not prove non-Rupertness. The written
continuous bridges are unformalized; the finite Q(sqrt(5)) certificate
is reproducible with the standard-library checker.
