# The 66-vertex stress instance also has an intersection certificate

For the explicit positive-integer planar metric below, the 16 geodesic pairs
in [certificate.json](certificate.json) include a half-balanced separator for
**every nonnegative real vertex-mass assignment**. More strongly, for every
pairwise-vertex-intersecting family of nonempty connected vertex sets, one
of the pairs meets every member. Intersection here means sharing a vertex.

This is a second finite benchmark for the [component-intersection
method](../PROOF.md), not a solution of
[Barbados Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
a counterexample, or a theorem about all metrics on this graph. Its purpose
is to resolve a concrete stress case: an earlier 38-cut mass-infeasibility
core allowed an intersecting component choice. Additional geodesic pairs
give the present contradiction. Thus the partial core supplied no evidence
that inequalities beyond pairwise intersection are necessary for this
metric. The previous [50-vertex result](../README.md) is unchanged.

## Graph and metric

There are two caps, 0 and 1, and vertices
`v(i,j)=2+8*i+j`, where `0<=i,j<8` and the first coordinate is cyclic.
Each meridian is the path
`0,v(i,0),...,v(i,7),1`. Join `v(i,j)` to `v(i+1,j)` at each level.
For each square, with `0<=j<7`, add the diagonal
`v(i,j)v(i+1,j+1)` when `i+j` is even and
`v(i+1,j)v(i,j+1)` otherwise. There is no cap-to-cap edge.

Drawing the eight meridians around a cylinder and capping its boundary
circles shows planarity. There are 72 meridian edges, 64 level edges, and
56 diagonals: 192 edges on 66 vertices, triangulating the sphere.

For each edge with ordered labels `a<b`, assign the length

```python
1 + int.from_bytes(sha256(f"0:{a}:{b}".encode("ascii")).digest()[:4], "big") % 19
```

Thus all lengths are integers from 1 to 19. SHA-256 specifies the instance
deterministically; no cryptographic assumption is used. Vertex masses are
arbitrary nonnegative reals, independently of these fixed edge lengths.

## Why the certificate proves the claim

If every listed pair failed half balance, select a residual component of
mass greater than half the total from each pair. These components intersect
pairwise, since two disjoint components cannot both have more than half
the total mass. At each of the first 15 cuts, exactly one component remains
compatible with all previously forced components. At the final cut,
neither of its two components is compatible. This is a contradiction.
Zero total mass is immediate.

For the stronger connected-family assertion, if each pair misses a family
member, contain that connected member in one residual component. The
selected components would intersect pairwise, giving the same contradiction.
This is exactly the general argument proved in [PROOF.md](../PROOF.md).

The 16 pairs use 24 distinct geodesics. The longest ambient geodesic has
15 vertices, counting all tied alternatives. Hence four geodesics cover
at most 60 of the 66 vertices. The sufficient condition that four geodesics
cover the graph does not account for the result.

## Reproduce and assess the evidence

From the repository root, with Python 3.11 or later and its standard library:

```sh
python3 graph_theory/planar_weighted_heavy_component_certificate/stress66/verify.py --check
```

Expected: `PASS`, 66 vertices, 192 edges, 16 pairs, 24 distinct paths,
15 forcing steps, maximum geodesic order 15, and five rejected controls.
The exact hashes and component trace are in [expected.json](expected.json).
The checker also enumerates all compatible component choices: the prefix
counts are fifteen 1s followed by 0. This is a second contradiction check
within the same program, not an independent review.

The graph is rebuilt from the displayed coordinates. The common checker
uses Floyd--Warshall integer distances, set-based components, and exact
path-length equalities. No solver or omitted search output is needed.
The discovery program used perturbed unique geodesics and bit masks;
the certificate is checked after discarding that perturbation. All stated
conclusions concern the small integer metric above, including its ties.

The trust boundary is the explicit finite graph, path lists, exact Python
arithmetic, and the published checker. No formal proof or independent
review of this supplement is claimed. It is a scoped negative construction
result; no priority claim is made.
