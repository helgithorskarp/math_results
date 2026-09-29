# One ambient cover certifies every edge deletion for an induced tree

For an induced tree fragment, a single cover by internal ambient geodesics is already a certificate for **every** subsequent edge deletion. The earlier [isometric-tree guard](../planar_two_geodesic_isometric_tree_guard/README.md) guarantees such a cover by bounding the number of leaves; the result here only asks for the cover itself. This admits nonisometric trees and arbitrary positive edge lengths. It is a structural terminal rule for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not an answer for every planar graph.

Graphs are finite and simple. Edge lengths are positive real numbers. A singleton path is a geodesic. An *internal* path of a tree `T` uses only edges of `T`; an ambient geodesic is shortest in the whole graph, including all routes outside `T`.

## Exact deletion-stability theorem

Let `T` induce a tree in `G`, and let `k>=1`. The following are equivalent.

1. The vertices of `T` are covered by at most `k` internal ambient `G`-geodesics.
2. For **every spanning edge subgraph** `H` of `G` and **every connected vertex set** `D` in `H[T]`, the vertices of `D` are covered by at most `k` internal ambient `H`-geodesics.

The same original paths provide the certificate for every `H`: intersect each with `D` and discard empty intersections.

**Proof.** Condition 2 with `H=G,D=V(T)` gives condition 1. Conversely, take internal ambient `G`-geodesics `P_1,...,P_k` covering `T`. A connected vertex set `D` in `H[T]` is convex in the original tree: the unique `T`-path between any two of its vertices survives in `H[T]` and lies in `D`. Thus `P_i intersect D` is empty or one contiguous internal path, whose edges survive in `H`. It is a subpath of a `G`-geodesic, hence a `G`-geodesic. Since edge deletion cannot shorten a path, it is also an ambient `H`-geodesic. These at most `k` intersections cover `D`. `□`

For `k=2`, a tree with more than four leaves cannot satisfy condition 1, because each leaf must be an endpoint of a covering path. For at most four leaves, condition 1 is an exact finite distance test: enumerate the at most `|T| choose 2` nontrivial internal tree paths and the singleton paths, retain those whose length equals the full ambient endpoint distance, and check all pairs for vertex coverage. This test does **not** require all internal tree paths to be ambient geodesics, as isometry would.

## Weighted guard and protected-edge descent

The [four-vertex heavy-component guard](../planar_two_geodesic_four_guard/README.md) applies verbatim. If `S` has at most four vertices and every component of `G-S` either has at most four vertices or is an induced tree satisfying condition 1 with `k=2`, then **every** spanning edge subgraph of `G`, under **every** nonnegative vertex-mass assignment, has a half-balanced separator made of at most two ambient geodesics. In a unit-edge planar graph, the small-component bound may be five by the induced-three-vertex-path rule. Arbitrary positive lengths are allowed for the four-vertex version.

There is also a protected-edge rule. If two `G`-geodesics leave only residual components of the preceding kinds, every edge-deleted subgraph retaining those two paths has the same weighted half-separator property: keep the protected pair if it balances; otherwise replace it by two paths covering the unique heavy residual component. The replacement covers the **whole** heavy component, so its deletion leaves total mass below half. This is the same descent mechanism used in the [isometric-fragment guard](../planar_two_geodesic_isometric_fragment_guard/README.md), with the weaker initial-cover hypothesis for tree fragments.

## An unbounded planar nonisometric family

Start with the octahedron: equatorial cycle `0-1-2-3-0` and poles `4,5`, each adjacent to the four equatorial vertices. Inside one face incident with `01`, insert `r` internally disjoint paths `0-a_i-b_i-1`. At each of `a_i,b_i`, attach two pendant arms of length two. Name their leaves `A_i,A'_i` and `B_i,B'_i`, respectively. Add edges `0-A_i` and `1-B_i` inside the same face. The constructive rotation in `verify.py` establishes planarity for every `r>=1`.

The fixed guard `S={0,1,2,3}` leaves the two poles as singletons and one ten-vertex induced tree `T_i` per gadget. The internal paths `A_i-a_i-A'_i` and `B_i-b_i-B'_i` have length four, cover all vertices of `T_i`, and are ambient geodesics. The notation suppresses the intermediate vertices on each arm. Yet `T_i` is **not isometric**: its internal `A_i-B_i` distance is five, while `A_i-0-1-B_i` has length three. The two selected geodesics therefore give a deletion-stable cover beyond the isometric-tree premise.

The family has `6+10r` vertices, `12+13r` edges, and `8+3r` faces. Its size and number of nonisometric residual trees are unbounded. The pendant arms produce cut vertices; no biconnectivity claim is made. These graphs satisfy the weighted all-spanning guard conclusion, hence in particular the unweighted half-separator conclusion. They do not imply the unrestricted planar assertion.

## Reproduction and trust boundary

Run with Python 3.11 or later and the standard library, from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_initial_tree_cover/verify.py
```

The checker independently constructs rotations for `r=1,2,5`, confirms Euler planarity, the residual trees, ambient distances, nonisometry, and the two internal covering geodesics. For `r=1`, it also checks 8,192 profiles obtained by deleting arbitrary tree and gadget-attachment edges while retaining the octahedron core. The theorem above proves the quantifiers over all edge deletions, all tree orders and all positive metrics; the finite controls audit the explicit unit-edge family only.

Literature checked 29 September 2026: the [workshop list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks the two-path half-separator question; [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) establish several structural path-separability classes. No historical priority claim is made for the elementary intersection argument.
