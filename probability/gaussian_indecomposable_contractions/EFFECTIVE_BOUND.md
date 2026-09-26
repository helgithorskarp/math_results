# An explicit mesh bound for the indecomposable reduction

Author proof, 26 September 2026; independent review pending. This supplements
the [accepted qualitative reduction](PROOF.md); its existing review does not
review the bounds below. The full Gaussian-majorisation sign remains open.

The geometric mechanism is the classical Brehm repair, with a bounded
initial folding to avoid its boundary blind zone. The contribution here is
an explicit cell count, rationality bookkeeping, and the resulting uniform
complexity and loss bounds for the already established indecomposable test.
No priority is claimed for constructive Brehm extension itself.

## 1. Quantitative statement

Let `p_1,...,p_N` be distinct points of R3 and suppose

    |q_i-q_j| <= |p_i-p_j|   for every i,j.                     (1)

Set, with binomial coefficients equal to zero when their lower index is
larger than their upper index,

    h_N = 512 * 2^N * (N+6) + 3N + binom(N,3) + 6,
    r(h) = 1 + h + binom(h,2) + binom(h,3),
    M_N = 12 h_N r(h_N).                                      (2)

**Theorem.** There is a finite tetrahedral triangulation of a
full-dimensional convex polytope P, containing every p_i as a vertex,
and a continuous piecewise-isometric map F on it with F(p_i)=q_i, such
that the triangulation has at most M_N tetrahedra and at most 4M_N
vertices. If the source spans R3, P can be `conv{p_i}`. Otherwise P may
be a cube containing the source. The bound depends only on N, without a
separation, angle, strict-contraction, or coordinate-height assumption.

If all prescribed coordinates are rational, the polytope, triangulation,
cell isometries, and all endpoint coordinates can be rational. The entire
finite interval of labelled distance matrices used in the earlier reduction
then has rational representatives after aligning one root tetrahedron.

The bounds are intentionally coarse: `M_N = O(N^4 16^N)`. They count cells
and vertices, not bit operations or coordinate bit lengths. They are not
a practical enumeration budget. For example, `M_7` is
`1054021675129126795053360`; no configuration collection of this size was
constructed or searched.

## 2. A bounded seed removes the blind zone

Choose R>0 so that all source and target coordinates have Euclidean norm
at most R; separate endpoint translations are harmless. Take R rational
when the prescribed coordinates are rational. Work first on

    C = [-4R,4R]^3.

Define the continuous one-dimensional triangular folding on each interval
`[jR,(j+1)R]`, `j=-4,...,3`, by

    f_R(t) = t-jR          if j is even,
             (j+1)R-t    if j is odd.

Thus `0<=f_R<=R`. The product map F_0 has 8^3=512 convex cubical
pieces, each with six facets, and is an isometry on each piece. Its image
lies in the convex cube W=[-R,R]^3. Continuity on convex C implies it is
1-Lipschitz: split any source segment at the finitely many piece boundaries
and compare its image length to its endpoint chord.

We maintain the invariant `F(C) subset W`. When repairing a prescribed
pair `a=p_i, b=q_i`, define

    Omega = {x in C: |a-x| < |b-F(x)|}.                        (3)

On the boundary of C, the left side is at least 3R, while the right side
is at most `(1+sqrt(3))R < 3R`. Hence the closure of Omega is contained
in the interior of C. This strict buffer avoids the boundary extension
problem in the usual proof. The invariant will be preserved by each repair.

## 3. One repair at most doubles the convex pieces

Suppose F is continuous and isometric on each member of a finite cover by
full-dimensional closed convex polyhedra with disjoint interiors. They
need not form a face-to-face complex. Suppose there are c pieces, each
with at most f facets. Lower-dimensional remnants of clips can be omitted
from the list of full-dimensional pieces and retained by closure.

If F(a)=b, no repair is needed. Otherwise a belongs to Omega. The standard
star argument is short: for x in Omega and y in [a,x], Lipschitz continuity
and the triangle inequality give

    |b-F(y)| - |a-y| >= |b-F(x)| - |a-x| > 0.                 (4)

Thus Omega is star-shaped about a. On an old piece Q write F=S, an
ambient isometry, and put a'=S^{-1}(b). If a'=a, that piece contains no
point of Omega. Otherwise

    Q intersect Omega = Q intersect {|x-a| < |x-a'|}.          (5)

The boundary plane H_Q is the perpendicular bisector of a,a'. It does
not contain a. Retain the part of Q on the non-Omega side of this plane;
it is one convex polyhedron with at most f+1 facets. Retain all of Q
when (5) is empty, and retain nothing if the clipped exterior is empty.

For each Q with a positive-dimensional interior portion in Omega, the
section `B_Q=Q intersect H_Q`, when two-dimensional, is a convex polygon
with at most f edges. Every point of this section is in the boundary of
Omega: approach it along a segment to an interior point of Q in Omega.
Conversely, all boundary points are covered by these sections and their
closures. This follows by taking an approaching sequence from Omega
and choosing an old piece containing a subsequence. Sections of dimension
at most one contribute only lower-dimensional faces of this boundary.

Cone each such polygon to a. Distinct cone interiors are disjoint, and
their union, with boundaries, is the closure of Omega. Here it is useful
to check that star-shapedness has not concealed a radial ambiguity.
The boundary is a finite union of planar polygons whose planes do not
contain a. If a ray met it twice, the star-shaped closure and (4) would
force the segment between the two intersections to lie in the boundary.
A finite union of planes not containing a cannot contain a nontrivial
segment on a ray from a. Thus the radial boundary point is unique.

Let rho_Q be reflection in H_Q. On the cone `conv(a,B_Q)` set

    F_new = S composed with rho_Q.                            (6)

This sends a to b and agrees with F on B_Q. On a radial segment from a
to a boundary point z it has the intrinsic description

    F_new(a+t(z-a)) = b+t(F(z)-b),    0<=t<=1.                (7)

Consequently adjacent cones agree on their intersections and join
continuously to the retained map. The new map is again piecewise isometric
and therefore 1-Lipschitz on C. Each cone has at most f+1 facets: its base
and one triangular face for each edge of the base. There are at most c
retained pieces and at most c cones, so

    c_new <= 2c,       f_new <= f+1.                          (8)

Equation (7) keeps its image inside the convex hull of b and the old
boundary images, hence inside W. If an earlier prescribed point p_j
already satisfies F(p_j)=q_j, then (1) gives
`|b-F(p_j)|<=|a-p_j|`. It is outside Omega, so the repair preserves it.
This proves that all N repairs can be performed with

    c_N <= 512*2^N,      f_N <= N+6.                          (9)

Degenerate cuts, repeated target points, a repair doing nothing, and
sections contained in old facets are allowed. T-junctions between the
convex pieces do not affect (4)-(9); the next section resolves them before
using any tetrahedral adjacency assertion.

## 4. A conforming tetrahedral mesh, including the original atoms

If the source spans R3, restrict F to P=conv{p_i}; otherwise take
P=[-R,R]^3. Use all planes containing facets of the pieces in (9), all
planes of facets of P, and for each original point the three coordinate
planes through it. There are at most h_N planes: a full-dimensional
convex hull of N points has at most binom(N,3) facet planes (choose a
noncollinear triple in each facet); the alternative cube needs six.

This arrangement refines every isometric piece into a face-to-face
polyhedral complex on P. The three coordinate planes make each prescribed
point a vertex of that complex. An arrangement of h planes in R3 has at
most r(h) three-dimensional cells. One can prove this by adding planes:
the next plane is cut by the earlier ones into at most
`1+(h-1)+binom(h-1,2)` regions and creates at most that many new cells.
Degeneracies can only lower the count. Restricting to convex P cannot
increase it.

Each resulting three-dimensional cell has at most h_N facets. If E is
its number of edges and f its number of facets, Euler's formula and
vertex degree at least three give E<=3f-6<=3h_N. Barycentrically
subdivide the entire face-to-face complex, using the average of the
vertices as a point in the relative interior of each face. A tetrahedron
corresponds to a flag vertex < edge < facet < cell. Each edge of a
three-dimensional convex cell contributes four such flags. Thus there
are at most `4E<=12h_N` tetrahedra per cell, proving (2). All are
nondegenerate. Shared faces use the same subdivisions, and all original
vertices remain vertices. The facet adjacency graph of the tetrahedra
is connected because P is convex. Finally the total number of vertices
is at most four times the number of tetrahedra.

## 5. Rationality and the full interval

The seed has rational affine coefficients when R is rational. If S and
a,b are rational, so is a'=S^{-1}(b). With n=a'-a, reflection in their
bisector is explicitly

    rho_Q(x) = x - [2 n.x - (|a'|^2-|a|^2)] n / |n|^2.       (10)

Only the nonzero case n!=0 is used. Therefore (6), all clipping planes,
all vertices of their bounded polyhedra, and all barycentres are rational.
These are finite operations and exact comparisons on rational numbers;
no algebraic square root is necessary. This proves rationality of the mesh
and its prescribed endpoint images, not a bound on their denominators.

Every intermediate configuration between the two endpoint distance
matrices preserves all the mesh edges. Align the root tetrahedron to
its rational source placement. At each step in a spanning tree of the
tetrahedral adjacency graph, the isometry on a new tetrahedron either
continues the previous one or composes it with reflection in the *source*
face plane. These planes are rational. Thus all candidate placements
are rational; discard inconsistent choices as in Lemma 1 of PROOF.md.
They include the whole interval, not merely a selected collection of folds.

The resulting interval has at most `2^(m-1)` distance matrices, where
m<=M_N is the actual number of tetrahedra. Its saturated chains have
at most `2^(m-1)-1` nontrivial steps, each indecomposable among all
R3 configurations, by the accepted finite-interval argument.

## 6. Explicit preservation of a strict Gaussian failure

Write Phi(P)=H_{sum_i w_i gamma_s(.-p_i)}(a), with nonnegative
probability weights. Suppose a prescribed finite contraction has

    Phi(Q)-Phi(P) <= -delta < 0.                              (11)

Extend it using the theorem. On the mesh vertices give the old law weight
1-epsilon and the uniform vertex law weight epsilon, where

    epsilon = delta/[2(1+delta)].                            (12)

At the new threshold `(1-epsilon)a`, the elementary mass perturbation
estimate in the earlier reduction makes the total endpoint gap at most
`-delta/2`. On a saturated chain this telescopes. At least one step has
gap at most `-delta/(2L)`, with `1<=L<=2^(m-1)-1`. In particular there
is an indecomposable witness with

    number of labels <= 4M_N,
    every labelled weight >= delta/[8M_N(1+delta)],
    hinge gap < -delta * 2^(-M_N).                           (13)

It fixes a nondegenerate tetrahedron after endpoint alignment. Its common
tight framework is infinitesimally rigid at both ends, as in PROOF.md.
Coincident input labels may be merged, increasing weights and preserving
indecomposability and the hinge. If the original data and a chosen lower
bound delta are rational, the coordinates and augmented weights are rational
as well; no rationality of the hinge integral is presumed. The threshold
and variance are left at their specified real values.

This now bounds the formerly uncontrolled mesh loss using the **original**
atom count. It does not preserve a constant fraction of delta independent
of N. In particular M_N is exponential, while the inverse gap bound in
(13) is doubly exponential. Nothing here signs that gap.

## 7. Consumer scope and exact controls

The [handoff](EFFECTIVE_HANDOFF.md) composes (13) with the existing
support-independent finite localization. This gives explicit label and
positive-mass budgets for an indecomposable witness to a specified-size
failure. It is not an efficient replacement for the much smaller input
families already used by the team's Gaussian oracle or beta certificates.

The standard-library checker `effective_bound.py --check` verifies an
asymmetric rational eight-cone repair, its six edge lengths in each cone,
continuity on all shared faces, the exact removed/filled volume, the
512-piece seed, and the boundary guard. It also preserves an explicit
failure of the unbuffered coning shortcut and checks the symbolic count
and perturbation budgets. These are finite controls; the universal count,
repair and factorization proofs are the written argument above. The
checker is not a general Brehm implementation, an exhaustive search,
a Gaussian integrator, independent review, or a formal proof.
