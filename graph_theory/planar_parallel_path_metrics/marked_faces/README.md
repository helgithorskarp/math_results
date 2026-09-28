# Nine marked leaves in three parallel-path faces

This note excludes the marked-face obstruction left by the parent
[parallel-path result](../README.md), for **every** positive edge metric
carried by the displayed core and leaf edges. It concerns the exact half
threshold in [Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It is not a counterexample or an unrestricted planar separator theorem.

## Precise family

Let a finite simple connected plane graph G contain three internally disjoint a-b paths

    P_i = (a, v_i1, v_i2, v_i3, b),  i = 0,1,2,

in cyclic order. Write C for their union. In the open face F_i of C
between P_i and P_(i+1), place three distinct marked vertices z_i1,z_i2,z_i3,
and include the edges v_ij z_ij, drawn inside F_i. Indices i are modulo 3.
Let H consist of C and these nine leaf edges. Thus H has 20 vertices.

The graph G may contain arbitrary additional vertices and edges, subject to
planarity, the specified placement of the marked vertices, positive edge
lengths, and the metric condition

    d_G(x,y) = d_H(x,y)  for all x,y in V(H).

The nine marked vertices may have arbitrary nonnegative real masses.
Every other vertex has mass zero. All 21 edge lengths of H are arbitrary
positive real numbers; no equality or genericity assumption is imposed.

**Theorem.** Two ambient G-geodesics have a vertex union whose deletion
leaves every component with at most half the original total mass.

When H spans G, its distance-preservation condition is equivalent to
requiring every extra edge uv to have length at least d_H(u,v). Thus all
core and pendant prices can vary independently, and added edges need not
have a common price. Additional zero-mass facial vertices permit graphs
of unbounded order. The theorem does not allow arbitrary pendant
attachments, additional marked vertices, or general trees attached to C.

## Proof for nine equal masses

It is enough first to find two paths leaving at most four marked vertices
in each component. Give the nine marks mass one. For the moment, assume
no internal vertex of any P_i lies at half its branch's length.

The parent proof's midpoint construction applies in C. The prefix ending
at the last vertex before half length is its a-half, and the suffix
starting at the first vertex after half length is its b-half. Their
vertex union is the full branch. The a-halves of any two branches, joined
through a, form a geodesic; so do their b-halves joined through b.
Adding leaves to C does not change distances on C. A geodesic ending at
v_ij can be extended along v_ij z_ij and remains an H-geodesic, since
every H-path to that leaf uses its sole incident edge. Isometry transfers
all these paths to ambient G-geodesics.

**Case 1: some branch has its midpoint between two internal vertices.**
Choose such a P_i and its predecessor P_(i-1). The midpoint construction
gives two geodesics whose vertex union is both complete branches.
On P_i, their endpoints are two distinct internal vertices. Extend both
paths to those vertices' marked leaves, which lie in F_i.

The two deleted branches form a Jordan curve. One side contains just
F_(i-1) and its three marked vertices. The other side contains F_i and
F_(i+1), hence six marked vertices before deletion. The extensions delete
two distinct marks on this latter side, leaving at most four there.
Every surviving G-component lies on one side, so the required bound holds.
Extra edges and zero-mass vertices remain in G throughout this argument.

**Case 2: every midpoint lies in a first or last branch edge.**
If a midpoint lies in the last edge, all three internal vertices belong
to the a-half; call this type A. Otherwise they all belong to the b-half;
call it type B.

If both types occur, choose an A branch P_i, a B branch P_j, and denote
the third branch by P_k. Join the a-halves of P_i and P_k through a, and
join the b-halves of P_j and P_k through b. These two geodesics cover
every vertex of C.

If all three branches have type A, take a shortest complete a-b branch
and join the other two a-halves through a. These are two geodesics and
again cover C. The all-B case uses b in place of a. A shortest complete
branch is geodesic because every simple a-b path in C is one branch.

Once C is deleted, every surviving component lies in a single face of C.
Each face contains only three marked vertices. Therefore Case 2 gives the
stronger bound of three marks per component.

**Ties.** Perturb the positive core edge lengths by quantities tending to
zero so no branch midpoint is a vertex. Apply the construction using the
perturbed H-metric and the fixed plane topology. There are only finitely
many pairs of simple H-paths, so one pair occurs along an infinite
subsequence. Shortest-path inequalities are closed under limits; the pair
is geodesic in the original H and hence in G. Its deletion leaves the
same components throughout, so the four-mark bound persists. The metric
of the ambient graph need not be perturbed: the construction and component
bounds only use its topology until isometry is applied at the limit.

## Arbitrary masses on the same nine marks

Let W be their total mass. If the four largest masses sum to at least W/2,
join those four marked vertices in two pairs by ambient shortest paths.
Their deletion removes at least half the total mass, which suffices.
Otherwise every set of at most four marks has mass less than W/2. Apply
the equal-mass construction, which leaves at most four marks in any
component. W=0 is immediate. This elementary nine-point argument is not
an assertion for arbitrary support sizes.

## Relation to the interval-sweep result

The team's [interval/facial sweep](../../planar_two_geodesic_interval_sweep/README.md)
and its [reviewed error bound](../../planar_two_geodesic_interval_sweep_review1/REVIEW.md)
are useful filters. If E is the mass outside the chosen interval or facial
interval union, and P is the prescribed first geodesic, the bound is

    remaining component mass <= (W - w(P) + E)/2.

Thus E<=w(P) is sufficient for exact half balance, even when E is positive.
This condition also covers the unequal-price longitudinal examples in the
parent note. For `annulus(6,3,1)`, root 0 and face (12,16,13), mass one on
all 20 vertices gives E=3 and the prescribed path (0,2,3,4,1,13) has mass
6. With mass one just on the nine odd-labeled marks, E=2 and the path
(0,17,18,19,1,13) has mass 3. In both cases (0,11,12) is a valid second
geodesic; the component masses are respectively (6,6) and (1,4).
The parent comparison only excluded the full-support hypotheses; it did
not establish independence from this error extension.

The marked-face fixture addressed here escapes even that error criterion.
In its spanning H-metric, a marked leaf cannot be internal to any ambient
geodesic: distances between H-vertices are unchanged, and passing through
a leaf adds twice its positive pendant length. An interval therefore
contains at most its two marked endpoints. In the displayed triangulation
the marks form an independent set; every face of any embedding is a
triangle and therefore has at most one mark. Every rooted facial interval union
also contains at most two marks. With nine unit masses, E>=7 whereas
w(P)<=2. This reasoning holds for every positive choice of H-edge lengths
and every distance-preserving choice of the extra edge prices on this
fixed triangulation. It is a boundary of those sufficient criteria, not
a negative separator example.

There is also a general search boundary. In a metric with unique shortest
paths, a counterexample with nine unit-mass marks could have at most two
marks on any geodesic: a path through three, plus a path joining two unused
marks, would delete at least five. In a triangulation, each interval is
one geodesic and each facial interval union is the union of three such
paths. Their marked counts are at most two and six, respectively. Hence
the facial error E is at least three, while w(P) is at most two. The
error criterion cannot certify these generic nine-mark candidates.
This explains why testing that criterion complements, rather than replaces,
the necessary three-mark-path filter in this construction search.

## Reproduction and trust boundary

Run the standalone exact checker with Python 3.11+ and its standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_parallel_path_metrics/marked_faces/verify.py --check
```

The checker constructs the 20-vertex triangulation, checks its spherical
embedding and the three marked facial groups, applies every case of the
construction, and verifies path lengths and full-graph components directly.
It includes rational lengths, midpoint ties, arbitrary supported masses,
and zero-mass facial augmentations. The compact expected result is in
[expected.json](expected.json): 227 metrics, 3,690 supported-mass checks,
32 original branch-midpoint equalities, four augmented 56-vertex graphs,
and four rejected malformed controls. The theorem's four construction
cases all occur, including unequal branch lengths in the outer-edge cases.
The two longitudinal sweep witnesses above are also checked exactly.
The written proof establishes the real
parameter and arbitrary-order claims; finite checks are regression evidence.
There is no solver or enumeration-completeness premise. No historical
priority, formal verification, or independent review is claimed.
