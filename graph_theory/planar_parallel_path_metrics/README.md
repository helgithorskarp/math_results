# Half separators when parallel paths carry the metric

**Proved family exclusion for Barbados Problem 31.** Let G be a finite
simple connected planar graph with positive real edge lengths. Suppose G
contains a subgraph H that is the union of distinct internally disjoint a-b paths,
and distances between vertices of H are the same in H and G. Then every
nonnegative real mass assignment **supported on V(H)** has a half-balanced
separator equal to the union of at most two shortest paths in the original
G. In particular, when H is spanning, the conclusion holds for every
nonnegative real vertex-mass assignment.

The edge lengths on different branches, and on individual edges of one
branch, are arbitrary. A full a-b branch need not be shortest. The proof
instead covers **two entire branches together by two shortest paths**, then
uses their cyclic order in a planar embedding to select a balanced pair.
There is no bound on the number or length of the branches.

This excludes a defined class of adversarial edge metrics. It does not
settle [Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
and it does not cover a theta core with arbitrary attached trees. In
particular, this result assumes H contains **every positive-mass vertex**.
The elementary ingredients and this formulation carry no priority claim.

## A directly checkable metric hypothesis

When H is spanning, assign arbitrary positive lengths to its edges.
For every added edge uv of G, require

    length(uv) >= d_H(u,v).

This condition is necessary and sufficient for H to preserve all distances
of G: replace each added edge of a G-walk by an H-shortest path, and use
H as a subgraph for the reverse inequality. Equality is allowed, as are
ties between geodesics. Thus one need not make added edges uniformly huge.

For example, take any capped cylindrical grid, include every longitudinal
column as an a-b branch, and give all column edges arbitrary independent
positive prices. Each horizontal or diagonal edge may have any length at
least the distance of its endpoints in the column network. The theorem
gives half balance for every vertex mass, at every circumference and height
for which the simple capped grid is defined. It permits any planar chords
inside the strips, not just the displayed grid diagonals.

The earlier [capped-mesh obstruction](../planar_geodesic_mesh_obstructions/PROOF.md)
uses individually shortest columns certified by a height function. Here
long columns can be much more expensive than an alternative a-b branch;
the midpoint cover is the additional step. Face vertices with only one
cheap attachment can still have other incident edges in G. Positive mass
on those vertices falls outside the criterion; the finite control below
shows why it cannot simply be assigned to a core branch.

The [weighted reduction](../planar_two_geodesic_weighted_reduction/README.md)
justifies searching these edge metrics and supported masses for the original
unweighted question. The present result excludes this metric family;
it supplies no counterexample or unrestricted resolution.

## Proof and finite checks

[PROOF.md](PROOF.md) proves the branch cover and the all-order weighted
separator statement. Its proof, rather than bounded computation, establishes
the theorem. [verify.py](verify.py) is a standalone exact regression checker:
it builds capped annuli with unequal branch prices, validates the metric
hypothesis with Floyd distances, checks every branch-pair cover, and checks
the median construction on integer and rational masses. It also supplies
an explicit 20-vertex control where adding nine face vertices defeats
every union of two full core branches, while an actual two-geodesic half
separator still exists. That control is an obstruction to the naive
extension of this construction, **not a counterexample to Problem 31**.

From the repository root, using Python 3.11+ and only its standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_parallel_path_metrics/verify.py --check
```

The compact deterministic result is in [expected.json](expected.json).
It records 60 annular metrics, 1,280 branch-pair covers, 2,432 mass cases,
156 full branches that are not shortest, three rational-length boundary
metrics, and six rejected malformed inputs. Three additional metrics have
zero-mass vertices inserted into every face; these check the nonspanning
isometric-core version on 19 branch pairs and 304 mass assignments.
The marked-face control checks all three core-branch pairs and all 4,845
four-vertex cuts. A separate check compares all metric intervals and all
rooted triangle interval unions on the 20-vertex longitudinal metric.
No solver, graph census, external data, private discovery code, or large
certificate is required. An [independent review](../planar_parallel_path_metrics_review1/REVIEW.md)
confirms the conditional theorem and independently checks the finite controls.

## Literature and scope

[Diot and Gavoille's full paper](https://emilie-diot.eu/Article/DG10a)
distinguishes ambient, or strong, path separability from sequential
shortest paths, proves the three-path planar baseline, and treats
face-separable graphs. This note concerns two simultaneous ambient paths
and exact half balance. It is a metric restriction on planar graphs,
not an assertion about all edge metrics on this graph class.

The marked 6-by-3 control also gives a scope comparison: the checker finds
no half-balancing four-vertex set for its nine marked vertices. Its
underlying graph is a 20-vertex triangulation, so every face in any plane
embedding has three vertices; no face boundary can half-balance that mass.
Giving the longitudinal columns arbitrary prices and dominating all other
edges nevertheless satisfies the theorem here, and the checker verifies
an explicit separator for that metric. Thus the metric criterion applies
to an instance without the earlier face-separator hypothesis.

The team's [interval and facial-interval theorem](../planar_two_geodesic_interval_sweep/README.md)
has a different metric hypothesis. Equal-length branches fit its single
interval case. Unequal branch lengths need not: on the checker's
20-vertex longitudinal metric `annulus(6,3,1)`, now with mass one at
**every vertex**, every interval I(s,t) has at most 12 vertices. For every
root r and every triangle T, the union of I(r,z) over z in T has at most
17 vertices. The checker tests all vertex pairs, roots, and all 36
triangles. Since this topology is a triangulation, every face in any
embedding is a triangle. Neither support hypothesis of that theorem
therefore applies directly to this metric with all 20 masses positive,
whereas the parallel-path criterion gives an explicit half separator.
This is a comparison of the stated hypotheses, not a claim about all
possible reductions between the two results.

The [reviewed quantitative extension](../planar_two_geodesic_interval_sweep_review1/REVIEW.md)
does cover this particular example: for root 0 and face (12,16,13), the
mass outside the facial interval union is 3, while the geodesic
(0,2,3,4,1,13) removes mass 6. Its bound `(W - w(P) + E)/2` is therefore
at most W/2. The [marked-face supplement](marked_faces/README.md) records
explicit witnesses and proves a different exclusion for every positive
choice of core and pendant lengths in the original nine-leaf obstruction,
under its stated isometry condition. The marked-leaf metric family on
that original 20-vertex triangulation escapes even this error criterion.

A targeted search did not locate this particular parallel-path formulation;
that is not an originality claim.
