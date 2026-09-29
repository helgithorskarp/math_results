# A sharp fourteen-dimensional box of simultaneous planar shortcuts

The [single-shortcut threshold result](../planar_two_geodesic_shortcut_thresholds/README.md)
identified fourteen core pairs that can individually be shortened while
six prescribed icosahedral paths stay geodesic. Its
[independent review](../planar_two_geodesic_shortcut_thresholds_review1/REVIEW.md)
showed that the fourteen individual lower thresholds cannot be imposed
at once: two shortcuts can cooperate to destroy a path. Here is a
**joint** certificate. All fourteen shortcuts can be present and
independently varied throughout an explicit box of side length `1510`.
This is a conditional positive family for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not a settlement for every planar graph.

## Construction and exact claim

Take the twelve-vertex icosahedral core and the six paths in the
predecessor's [public certificate](../planar_two_geodesic_icosahedron_price_region/certificate.json),
whose SHA-256 is
`070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d`.
Set every core edge price to `151` times its listed price. Write `d`
for the resulting core metric. Its diameter is `34579`.

The fourteen edges listed below are precisely those with a strict
single-shortcut interval. Assign each edge to a **different** incident
triangular face, using face numbers from the predecessor certificate:

| edge `ab` | face | edge `ab` | face |
|---|---:|---|---:|
| 0-1 | 1 | 2-7 | 9 |
| 0-3 | 2 | 3-4 | 3 |
| 0-5 | 4 | 3-8 | 10 |
| 1-2 | 0 | 4-5 | 12 |
| 1-10 | 6 | 6-10 | 7 |
| 2-3 | 8 | 7-8 | 11 |
| 2-6 | 5 | 10-11 | 16 |

Inside each assigned face `abc`, insert one new vertex `z_ab` and join
it to all three corners. For each of the fourteen edges independently
choose a real number

    x_ab in [d(a,b)-1510, d(a,b)].                            (1)

Give `a-z_ab` the fixed length
`floor((d(a,b)-1510)/2)`, give `b-z_ab` the length `x_ab` minus that
fixed length, and give `c-z_ab` length `34580`. All these lengths are
positive. The resulting 26-vertex graph is a simple planar
triangulation with 72 edges and 48 faces. Each face patch is a single
vertex; its boundary-clique torso is `K_4`.

**Theorem.** Throughout the entire fourteen-dimensional box (1), the
same six prescribed core paths are shortest paths in the **whole**
expanded graph. Consequently the same three alternative path pairs,
combined with the reviewed
[face-patch quotient and heavy-torso theorem](../planar_two_geodesic_face_patch_transfer_review1/REVIEW.md),
half-balance every nonnegative real vertex mass. At the lower corner of
the box, all fourteen selected core-pair distances strictly decrease;
indeed 27 of the 66 core-pair distances decrease. The core is far from
isometric even though all six needed paths remain ambient geodesics.

The common saving `1510` is **sharp for this equal-decrement box**. If
all `x_ab` are lowered by `1511` instead, the prescribed path
`(0,4,8,9,11,6)` of length `20838` is beaten by the full-graph route
`(0,4,8,z_78,7,11,6)` of length `20837`. Already the individual
threshold for edge `7-8` is `13892=d(7,8)-1510`; the other thirteen
shortcuts are not needed for this failure. At a common real saving
`delta>1510` sufficiently close to `1510`, this route has length
`20838-(delta-1510)`, so the
bound is sharp beyond integer choices. No claim is made that this
box is the full joint safe polyhedron or optimizes total saving.

## Four potentials prove every point in the box

The compact [certificate](certificate.json) contains a 12-entry
integer potential for each distinct start vertex `0,1,2,5` of the six
paths. For every core edge `uv` of length `L_uv`, each potential `pi`
satisfies `|pi(u)-pi(v)|<=L_uv`. For each shortcut face, it satisfies

    |pi(a)-pi(b)| <= d(a,b)-1510,
    |pi(a)-pi(c)| <= floor((d(a,b)-1510)/2)+34580,
    |pi(b)-pi(c)| <= ceil((d(a,b)-1510)/2)+34580.             (2)

The first inequality protects the cheap two-edge route through the
face vertex; the other two protect routes using its expensive third
edge. Every right-hand side in (2) can only increase as `x_ab` ranges
through (1). For each prescribed path `P` from `s` to `t`, the
certificate also has `pi_s(t)-pi_s(s)=length(P)`. Summing potential
differences along any virtual-edge competitor, using the exact
[patch-boundary compression lemma](../planar_two_geodesic_shortcut_thresholds/README.md),
shows that `P` remains shortest at every point of the box. Equivalently,
the three inequalities in (2) make the intervals
`[pi(u)-length(u,z_ab),pi(u)+length(u,z_ab)]` for the three face
corners pairwise intersect; intervals have a common point, which
extends `pi` to `z_ab` as a full-graph Lipschitz potential. Four
potentials suffice because three paths start at vertex `1`.

This is an exact certificate for a continuum of metrics. The checker
also independently runs whole-graph Floyd--Warshall at the lower
corner, checks the planar face structure, and checks the sharpness
route at saving `1511`. The written potential inequalities establish
the all-metric assertion; the finite distance checks audit the
certificate and graph encoding.

## Unbounded order and scope

Six original faces remain empty. In any one of them, insert an
arbitrarily large stacked planar patch with a width-three
boundary-clique torso. Give every new edge incident with a core vertex
length greater than `34579`; give internal new edges arbitrary positive
lengths. An excursion through this patch cannot shorten a core-to-core
distance, so the six paths stay geodesic. Its heavy mass, if any, is
handled by the same local centroid argument. This yields planar graphs
of unbounded order with all fourteen strict shortcuts and the
all-real-mass two-geodesic half-separator property. The family still
has bounded global treewidth; no unrestricted planar result follows.

## Reproduction

From the repository root, Python 3.11+ and only its standard library,
with assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_joint_shortcut_box/verify.py
```

The checker reads only the two linked small JSON certificates. It
validates the predecessor hash, rebuilds the spherical embedding,
recomputes all thirty individual thresholds and the fourteen distinct
face assignments, checks **288 exact potential inequalities**, computes
the whole 26-vertex metric independently, checks projection to the
three-pair quotient, and verifies the literal failure route beyond the
box. Expected output:

```text
core=12 full_vertices=26 full_edges=72 full_faces=48
shortcuts=14 box_saving=1510 potential_inequalities=288
shortened_core_pairs=27 projected_components=18
saving_1511_witness_length=20837 original_length=20838 PASS
```

The certificate does not encode all mass vectors or all edge metrics.
The weighted conclusion rests on the written potential argument and
the reviewed quotient and heavy-patch proofs. This result answers the
reviewer's non-composability objection with one exact joint box; it
does not turn the fourteen individual thresholds into independent
necessary conditions. Historical priority is not asserted.
