# All pendant attachments on the marked twenty-vertex cylinder

**Computer-assisted theorem.** On the explicit planar triangulation T
below, choose one of the four neighbors of each of nine marked vertices
as its parent. Let H consist of these nine parent edges and the three
specified pole-to-pole branches. For every such choice, every positive
real edge metric on H, every distance-preserving assignment of lengths
to the other edges of T, and every nonnegative vertex mass supported on
the nine marks, two ambient geodesics half-balance the mass.

There are 4^9 = 262,144 parent assignments. The theorem closes the entire
pendant-attachment metric family on this topology, including mixed
attachments to either boundary branch or to a pole. It does not cover
arbitrary metrics on T, mass on its other vertices, other marked
topologies, or [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
in general. No counterexample is claimed.

## The explicit graph and metric hypothesis

Write v(i,j)=2+3(i mod 6)+j for 0<=j<=2, with poles 0 and 1. Include
the horizontal edges v(i,j)v(i+1,j), the vertical edges v(i,j)v(i,j+1),
and the cap edges 0v(i,0) and 1v(i,2). For each square with corners

    A=v(i,j), B=v(i+1,j), C=v(i+1,j+1), D=v(i,j+1),

include diagonal AC when i+j is even and BD otherwise. This defines
the 20-vertex, 54-edge triangulation T. The exact edges and 36 oriented
triangular faces are also supplied in [certificate.json](certificate.json).

The three core branches, numbered 0,1,2, are

    (0,2,6,10,1), (0,8,12,16,1), (0,14,18,4,1).

Their interiors are disjoint. The remaining nine vertices form an
independent set S. Their possible parents are exactly:

| Mark | Four possible parents |
| --- | --- |
| 5 | 0,2,6,8 |
| 9 | 6,8,10,12 |
| 13 | 1,10,12,16 |
| 11 | 0,8,12,14 |
| 15 | 12,14,16,18 |
| 19 | 1,4,16,18 |
| 17 | 0,2,14,18 |
| 3 | 2,4,6,18 |
| 7 | 1,4,6,10 |

H has the 12 core edges and one chosen parent edge per mark. Its marks
are leaves. The hypothesis on T's lengths is d_T(x,y)=d_H(x,y) for all
20 vertices. Equivalently, each non-H edge xy has length at least
d_H(x,y). Indeed, replacing each extra edge by an H-shortest path proves
sufficiency, and an extra edge shorter than d_H would contradict
necessity. These lengths need not be equal or strictly greater than
d_H. All 21 H-edge lengths vary independently over the positive reals.

## Universal geodesic templates

First give every mark mass one and assume each branch midpoint lies
strictly inside an edge. Number its four edges 0,1,2,3 from pole 0.
Let k_i specify this edge on branch i. Its prefix through vertex k_i
is its 0-half, and its suffix starting at vertex k_i+1 is its 1-half.
Let s be any shortest complete pole-to-pole branch. There are exactly
4^3 times 3 = 192 choices of (k_0,k_1,k_2,s).

The following seven paths are geodesics in H:

* the shortest complete branch s;
* the 0-halves of each pair of distinct branches, joined through 0;
* the 1-halves of each pair of distinct branches, joined through 1.

For completeness, if two coordinates x_i,x_j measured from 0 are at
most half their respective branch lengths L_i,L_j, their route through
0 has length x_i+x_j. The competing route through 1 differs by
(L_i-2x_i)+(L_j-2x_j)>=0. A route using the third branch has one of
these nonnegative summands plus that branch's positive length.
These exhaust the simple routes in the three-branch core. This also
proves the assertion at pole 1. The shortest complete branch is
geodesic because every simple core path between the poles is a branch.
Pendant leaves do not shorten any core route. This is the midpoint
mechanism of the [parent theorem](../README.md).

Every contiguous subpath of one of these generators is therefore
geodesic. An endpoint may be extended to a mark precisely when that
mark chose it as parent. Such an extension remains geodesic because
the mark is an H-leaf. Extending both ends is allowed if the resulting
path is simple. Isometry makes every resulting H-path an ambient
T-geodesic. The use of subpaths and overlapping paths matters: there
is no requirement that the two paths cover two entire core branches.

For example, in region (1,3,3), the paths

    (16,12,8,0,14,18,4) and (6,10,1)

are joined 0-halves and a 1-half. Together they delete all core
vertices except 2. The only marks that can remain connected through 2
are its three marked neighbors 3,5,17, so every residual component has
at most three marks. This works independently of all parent assignments
and of which complete branch is shortest.

## The finite certificate

The certificate provides pairs of extended generator subpaths in every
one of the 192 cases. Each pair specifies zero, one, or two required
parent choices, obtained directly from its marked endpoints. The
checker establishes three facts about every case:

1. Each listed path has the asserted generator-subpath form, with
   compatible parent requirements and no repeated vertex.
2. Deleting its pair from the **full graph T**, retaining every edge
   outside H, leaves at most four marks in each component.
3. The listed parent requirements cover all 4^9 assignments.

The compact certificate contains 305 pairs. There are 174 cases with
an unconditional pair. The remaining 18 cases are covered by 121 pairs
requiring one parent choice and 10 requiring two. All labels and all
cases are checked; no symmetry quotient or graph census is assumed.

The search used bitsets of parent assignments to find these pairs.
The standalone verifier imports no search code: it checks paths by
contiguous-sequence membership, components by set searches, and parent
coverage by recursively splitting each variable into its four values.
An empty conjunction covers all remaining choices. This counts the
entire assignment space with only 311 distinct recursion states
summed across the 192 cases. Thus the certificate proves the required
uniform nine-mark assertion for every generic positive metric, not
only for sampled lengths. Completeness of the search that selected
the certificate is irrelevant; completeness of the verified coverage
is the premise.

## Midpoint ties, masses, and zero-mass extensions

For arbitrary positive real H-lengths, choose positive perturbations
tending to them that move all branch midpoints away from vertices.
Each perturbed metric has a certified pair. Finitely many simple
path pairs are possible, so one occurs along an infinite subsequence.
Shortest-path inequalities are closed under limits. Its two paths
are geodesic in the original H, and the same deletion in T still
leaves at most four marks per component. Transfer to the original T
uses its original isometry condition; no perturbed ambient metric
is assumed.

Now let the marks have arbitrary nonnegative masses of total W. If
the four largest sum to at least W/2, two shortest paths pairing these
four vertices remove at least half the mass. Otherwise every set of
at most four marks has mass below W/2, and the uniform certificate
works. The case W=0 is immediate. This is the nine-point mass
dichotomy used in the [same-side attachment theorem](../marked_faces/README.md).

The result also permits any finite simple plane supergraph G of this
embedded triangulation T, with all new vertices of mass zero and
d_G(x,y)=d_H(x,y) on V(T). Every component outside T lies inside one
triangular face. Its surviving neighbors in T form a clique and
already lie in one T-component after deletion. Adding these vertices
therefore cannot merge different residual T-components. Isometry
transfers the same path pair to G. This supplies graphs of unbounded
order; it does not allow arbitrary rearrangements of the marked faces.

## Scope, verification, and provenance

This is an exact computer-assisted exclusion of a family of proposed
obstructions. It extends the allowed parent patterns beyond the
same-side theorem on this fixed triangulation. That earlier theorem
allows more general facial topology, so neither statement should be
silently substituted for the other's hypotheses.

For T itself, the interval/facial sweep and its error criterion do
not already certify these metrics with nine equal masses. A positive
H-leaf cannot lie internally on an ambient geodesic, even with ties.
Every geodesic interval contains at most its two marked endpoints.
Every T-face is a triangle containing one mark, so a rooted union of
its three intervals contains at most two marks. Its outside mass is
at least seven, while the first path has mass at most two; the
reviewed sufficient condition E<=w(P) fails. This comparison is for
T's spanning H-metric, not for endpoints at arbitrary added vertices.

Reproduce from the repository root with Python 3.11+ and its standard
library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_parallel_path_metrics/all_attachments/verify.py --check
```

The output in [expected.json](expected.json) reports `PASS`, 192 cases,
262,144 parent assignments, and 305 templates. It also includes 196
exact metric regressions, 12 original midpoint equalities, and five
rejected malformed controls. The metric regressions use an independent
Floyd--Warshall distance calculation, including extra edges at exactly
their H-distances. They corroborate the proof; they do not establish
its real-parameter quantifier.

Certificate SHA-256:

    d0a4cf859caee94ef7453aa3d7105035f0ff79c2c553796420e1084b8c581694

The trust boundary is the written geometric and mass reductions plus
the finite certificate checker. There is no solver, external
enumeration, historical-priority claim, formal proof, or independent
researcher review. The same researcher wrote the search and the
separate checker. The ambient weighted setting is discussed by
[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a); the known
two-path 2/3 result is not used as an exact-half theorem here.
