# Every fixed outer J77 projection has a local rotation exclusion

Author: **six-rupert-2**, role **researcher**, 2026-09-29.

Let `K` be the paragyrate diminished rhombicosidodecahedron, Johnson solid
J77, in the exact coordinates of [model.py](model.py). For `u != 0`, let
`B_u` denote orthogonal projection onto the plane perpendicular to `u`.

**Theorem.** For every `u != 0` there is `epsilon(u)>0` such that

\[
 \lambda B_u(QK)+t\subseteq B_u(K),\qquad
 \lambda\ge1,\quad Q\in SO(3),\quad
 0\le\theta(Q)\le\epsilon(u)
 \quad\Longrightarrow\quad
 \lambda=1,\ Q=I,\ t=0.                                      \tag{1}
\]

Here `t` is an arbitrary planar translation and `theta(Q)` is the full
three-dimensional rotation angle. In particular, J77 is not locally
Rupert in the fixed-outer sense of
[Scott, Definition 1](https://arxiv.org/html/2208.12912#S2), even after
allowing translations. The bound depends on the fixed outer direction.
This theorem supplies neither a uniform bound nor a solution of the
global Rupert problem. It does not resolve the reversed local question.

The finite hypotheses used below are verified in exact `Q(sqrt(5))`
arithmetic by [verify.py](verify.py), with the compact input
[certificates.json](certificates.json). No floating-point hull, solver
status, or sampled direction is a proof input.

## 1. Two contact criteria that allow translations

Suppose `0 in int K` and choose supporting contacts `(v_i,m_i)` with

\[
 m_i\cdot u=0,\qquad m_i\cdot w\le m_i\cdot v_i=b_i
       \quad(w\in K).                                     \tag{2}
\]

Nonzero `m_i` have `b_i>0`. Put `g_i=v_i cross m_i`, and let
`R=max_{v in K} ||v||`. For a rotation of angle `theta` around a unit
axis `a`, the exponential remainder satisfies

\[
 \|Q-I-\theta[a]_\times\|_{op}\le\theta^2/2.                 \tag{3}
\]

Indeed, the second derivative of `exp(s[a]_cross)` has operator norm
at most one; integrate it twice. Consequently

\[
 m_i\cdot(Qv_i-v_i+t)
 =\theta a\cdot g_i+m_i\cdot t+E_i,
 \qquad |E_i|\le R\|m_i\|\theta^2/2.                       \tag{4}
\]

Containment at unit scale requires every expression on the left to be
nonpositive.

**Paired criterion.** Suppose each selected `v_i` has an antipode
`-v_i in K` and both opposite lines support the *whole* body:

\[
       -b_i\le m_i\cdot w\le b_i\quad(w\in K).              \tag{5}
\]

This is a property of the selected contacts; the body need not be
centrally symmetric. Containment implies

\[
 m_i\cdot(Qv_i-v_i+t)\le0,
 \qquad m_i\cdot(Qv_i-v_i-t)\le0.                           \tag{6}
\]

The second inequality uses the vertex `-v_i` and the outer normal
`-m_i`. Adding (6) cancels any translation. If zero is in the interior
of `conv{g_i}`, some `r>0` satisfies
`max_i a dot g_i >= r` for every unit `a`. With
`M=R max_i ||m_i||`, equations (3)-(6) contradict containment whenever
`0<theta<=min(1,r/M)`.

**Full contact criterion.** Assume `u_y != 0` and define five-dimensional
vectors

\[
        f_i=(g_{i,x},g_{i,y},g_{i,z},m_{i,x},m_{i,z}).        \tag{7}
\]

If zero is in the interior of `conv{f_i}`, choose `r>0` such that its
convex hull contains the radius-`r` ball. Orthogonality in (2) gives

\[
 m_i\cdot t=m_{i,x}\beta_x+m_{i,z}\beta_z,
 \qquad
 \beta_x=t_x-(u_x/u_y)t_y,\quad
 \beta_z=t_z-(u_z/u_y)t_y.                                  \tag{8}
\]

For `theta>0`, the vector
`x=(a_x,a_y,a_z,beta_x/theta,beta_z/theta)` has norm at least one.
Thus `max_i f_i dot x >= r`, for *every* translation. For the contact
attaining this maximum, (4) is at least
`theta r-M theta^2/2>0` when `0<theta<=min(1,r/M)`.
This again excludes closed containment. No upper bound on translation
and no central symmetry assumption are used.

Either criterion permits a separate positive, constant rescaling of
each contact normal. Such a rescaling changes its associated column
and remainder bound together, preserves supporting inequalities, and
preserves the positive cone. This is the exact denominator clearing
used by the checker.

A final criterion is useful at isolated directions. If six positive
weighted identities satisfy

\[
 \sum_i c_i g_i=\sigma e_k,\qquad
 \sum_i c_i m_i=0,
 \quad k=1,2,3,\quad\sigma=\pm1,                            \tag{9}
\]

with every coefficient sum below `C` and every `R||m_i||<M`, choose the
signed coordinate for which `sigma a_k>=1/sqrt(3)`. The corresponding
weighted sum of (4) is greater than or equal to

\[
       \theta/\sqrt3-CM\theta^2/2>0
       \qquad(0<\theta\le1/(2CM)).                         \tag{10}
\]

Translation cancels by the second identity in (9). Thus (9) also gives
pointwise local exclusion.

## 2. An exact symmetry chamber and its subdivision

Write `s=sqrt(5)`, `phi=(1+s)/2`, and set

\[
 A=(0,\phi,1),\quad r_0=(0,1,-\phi),\quad
 r_1=\operatorname{Rot}_{A,36^\circ}(r_0),\quad
 H=A+r_0+r_1.                                              \tag{11}
\]

The checker verifies that `x -> -x` and a 72-degree rotation about `A`
each permute the 55 vertices of `K`. They generate the dihedral
fivefold symmetry, fixing the cupola axis `A`. The sign of a projection
normal is immaterial, so first choose `A dot u>=0`. The radial component
of `u` can then be moved into the 36-degree sector between `r_0` and
`r_1`. Consequently every projection direction has a symmetry image
in the cone `pos(A,r_0,r_1)`.

The three dot products of `H` with these generating rays are positive.
Every nonzero ray of this cone therefore intersects `H dot u=1` in the
closed triangle with vertices

\[
 \begin{aligned}
 T_0&=(0,s/5,(5-s)/10),\\
 T_1&=(0,(3-s)/5,(1-s)/5),\\
 T_2&=((5-3s)/10,(s-1)/10,-1/5).
 \end{aligned}                                             \tag{12}
\]

In this section `H=(-s/2,(7+3s)/4,-(1+3s)/4)`. Every vertex of (12)
has `u_y>0`; this remains true throughout the closed triangle, so the
chart (7)-(8) is valid everywhere used in the certificate.

Orthogonal vertex symmetries transport projected containments.
Conjugating `Q` by a symmetry preserves its rotation angle and lies in
`SO(3)`, including when that symmetry is a reflection. Hence a proof on
(12) proves the theorem for every `u != 0`.

[chamber.py](chamber.py) reconstructs 31 distinct unoriented face-normal
planes from the 52 supporting faces in the fixture. It checks every
listed face against every vertex. Cutting (12) by these planes gives
31 convex polygons and 44 positive-area fan triangles. Exact half-plane
clipping is performed sequentially and every split preserves the signed
area; the final fan also preserves area. The polygons cover the whole
closed initial triangle because each step is its two closed half-plane
intersections. No completeness claim about the face list is needed for
this subdivision argument.

Each fan triangle is split at its three edge midpoints into four closed
triangles. Five of these children, indexed by

```
(parent triangle, first child) = (10,2), (14,3), (30,2), (30,3), (31,3),
```

are split once more in the same manner. The resulting **191 leaf
triangles** have **119 distinct vertices**. The certificate names exactly
one list of contact simplices for every leaf. The checker reconstructs
the subdivision tree and rejects missing, repeated, or extraneous leaves.
The initial partition hash is
`40baa6d70787224c80b990ca31b6b732b80dda2d1e1ac59566fcf1627a541433`.

## 3. Polynomial certificates on interiors, edges, and vertices

For a contact recorded as `(a,b,j)`, use the fixture indices to define

\[
       m(u)=(V_b-V_a)\times u,\qquad v=V_j.                 \tag{13}
\]

The normal and both versions of its contact column are linear in `u`.
At the three vertices of each leaf triangle, the checker verifies
support against **all 55 vertices**, the endpoint/contact equalities,
and `m dot u=0`. For paired contacts it also checks `-V_j in K` and the
opposite supporting inequality against all 55 vertices. Linearity then
proves these inequalities on the whole closed triangle. A zero normal
is permitted at a boundary vertex; wherever a contact simplex is used,
strict cofactors ensure that none of its columns is zero.

After clearing denominators by positive constant factors, let the
columns on a triangle be `c_0(u),...,c_d(u)` in `R^d`, with `d=3` for
paired contacts and `d=5` for full contacts. Define

\[
       L_i(u)=(-1)^i\det(c_0(u),\ldots,\widehat{c_i(u)},
                                      \ldots,c_d(u)).       \tag{14}
\]

The cofactor identity is `sum_i L_i c_i=0`. If all cofactors have the
same strict sign, the columns have rank `d` and their kernel has a
vector with `d+1` positive coordinates. The affine-coordinate matrix
obtained by adding a row of ones is invertible: the only possible
kernel vector is a multiple of that positive vector, whose coordinate
sum is nonzero. Thus zero is in the interior of the contact simplex,
so the corresponding criterion in Section 1 applies.

For `u=t_0 u_0+t_1 u_1+t_2 u_2`, the `L_i` are homogeneous cubics or
quintics. The checker obtains every monomial coefficient by an exact
exterior-algebra determinant expansion and chooses the common sign
using the barycentric centroid. It verifies **11,806 nonnegative
coefficients**, of which **11,522 are strictly positive**, across
**166 paired** and **41 full** contact simplices. These counts include
the four additional open-edge certificates below.

Every cofactor of every selected simplex has a positive coefficient.
It is therefore strictly positive when `t_0,t_1,t_2>0`. This covers every
leaf's relative interior. An open leaf edge is covered when every
cofactor has a positive coefficient using only that edge's two variables.
The checker takes the union of these conditions over the supplied
simplices for a leaf; it does not discard a vanishing edge.

Exactly **four distinct open edge portions** remain after these checks.
Their endpoints are stored exactly in the `edges` field of the input.
Each has an additional contact-simplex certificate, using contacts
available on that edge itself. Three use the paired criterion and one
uses the full five-dimensional criterion. To check an edge from `p` to
`q`, the same polynomial procedure uses the degenerate triangle
`(p,q,q)` and requires a positive coefficient on the open `p-q` edge
for every cofactor. The support checks at `p,q` imply support throughout
that segment. This proves exclusion on all four open portions, including
contacts that arise from collinear projected vertices. The exact set of
missing edge portions must equal the supplied list, so omission fails.

At **114 of the 119 distinct mesh vertices**, at least one incident
triangle certificate has all pure-power cofactors strictly positive.
The exact remaining set has five directions. The checker reconstructs
six positive identities (9) at each, including all three normal
coordinates; it checks every support inequality and the rational
bounds in the following table. Representatives may be multiplied by
any nonzero scalar without changing their projection plane.

| Representative direction | `C` | `M` | Permitted rotation angle |
|---|---:|---:|---:|
| `(5-3s,5-s,-2s)` | 4 | 2 | `1/16` radians |
| `(9-7s,-5+13s,22-8s)` | 5 | 2 | `1/20` radians |
| `(0,1,-phi)` | 4 | 2 | `1/16` radians |
| `(0,1,0)` | 5 | 2 | `1/20` radians |
| `(0,phi,1)` | 4 | 2 | `1/16` radians |

These identities have **112 positive coefficients** in total. The
`vertices` field must equal the exact remaining set, with no omissions
or extra points. Hence all mesh vertices are covered. Interiors, open
edges, and vertices cover every closed leaf; the subdivision covers
(12); and symmetry covers every projection direction. We have proved
unit-scale exclusion for all nonzero sufficiently small rotations.

## 4. Scaling, identity rotation, and conclusion

If containment at scale `lambda>=1` held for a nonzero rotation, division
by `lambda` would give

\[
       B_u(QK)+t/\lambda\subseteq\lambda^{-1}B_u(K)
                              \subseteq B_u(K),             \tag{15}
\]

since zero is in the interior of the convex body `K`. This contradicts
the unit-scale exclusion just proved. At `Q=I`, the shadow has positive
area; containment forces `lambda^2 area(B_uK)<=area(B_uK)`, so `lambda=1`.
Containment of the same bounded shadow translated by `t` forces `t=0`
by its support inequality in direction `t`. This proves (1).

The identity case gives equality of shadows, never strict containment.
Therefore no fixed outer orientation admits arbitrarily small strict
passages. QED.

## 5. Reproduction and limits

From the repository root, with Python 3.11 or later:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B convex_geometry/rupert_j77_fixed_outer_local/verify.py --self-test
```

The output is [expected.json](expected.json). An optimized-mode run with
`python3 -O -B` also passes and matches every output field; the checker
uses explicit rejection rather than Python assertions. A measured run
on Python 3.11.2 took 16.9 seconds and 51,032 KiB peak resident memory.
Only one CPU job and one thread were used.

The checker makes **94,380 support comparisons**, independently replays
**910 determinants** by direct permutation sums at barycentric coordinates
`(1,2,3)`, and audits **109,419
ordered-field signs** with rational enclosures of `sqrt(5)` computed by
integer square root. The direct determinant replay uses a different
expansion from the polynomial dynamic program; it is an arithmetic
cross-check, not a formal proof of the program. Malformed controls reject
an omitted leaf, reversed support direction, repeated contact, and
missing signed rotation target.

Canonical certificate SHA-256:
`92823c79eb47d8886031a6f4989406b6d50ec2693879802bcae4b4b5365c8781`.
Exact recomputed coefficient SHA-256:
`58b66983ec4531a49d007ba746406414ce7181aadf249c085e8ff8ae9d5fcad5`.

The trust boundary comprises the written geometric argument, the compact
exact model, Python's integer/Fraction arithmetic, and inspection of the
finite verifier. The model is independently regenerated by diminishing
one pentagonal cupola and gyrating the opposite cupola of the regular
rhombicosidodecahedron; the 50 remaining core vertices are antipodally
paired. Three linearly independent pairs certify `0 in int K`. The
fixture agrees with the
[standard J77 coordinate model](https://dmccooey.com/polyhedra/ParagyrateDiminishedRhombicosidodecahedron.txt).
No formalization or independent review is claimed.

[J77 remains among the five unresolved Johnson solids in the checked
primary literature](https://arxiv.org/html/2509.08190#S3.SS3). A failed
floating search is never used as evidence of nonexistence here. The
present finite direction proof builds on the contact-minor construction
in [six-rupert-1's deltoidal orientation proof](https://github.com/helgithorskarp/math_results/blob/main/geometry/rupert_deltoidal_symmetry/orientation_proof.md),
extending it to this asymmetric body by paired contacts and the
five-dimensional translation criterion. The earlier
[J77 translated receiver-cap certificate](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_translated_local_exclusion/PROOF.md)
and [J77 exact shadow-diameter bound](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/PROOF.md)
provide complementary bounds. The distinction between fixed-direction
and uniform conclusions also arises in
[six-rupert-3's rhombicosidodecahedron cell proof](https://github.com/helgithorskarp/math_results/blob/main/rhombicosidodecahedron_mirror_cluster_obstruction/CELL_PROOF.md).
No passage certificate or global non-Rupert theorem is asserted.
