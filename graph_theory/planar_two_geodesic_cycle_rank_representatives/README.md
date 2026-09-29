# Connected deletion representatives certify every fragment edge deletion

For a connected induced fragment, only edge-deleted hosts in which the fragment **remains connected** need direct geodesic-cover tests. If further deletion disconnects the fragment, those deleted edges are bridges of an already tested host, and each covering geodesic restricts to a geodesic in every surviving component. The number of direct tests is bounded by the fragment's **cycle rank**, rather than by every possible edge subset of the full host.

This generalizes the [induced-tree persistence theorem](../planar_two_geodesic_initial_tree_cover/README.md) and the exact [cactus representatives](../planar_two_geodesic_cactus_representatives/README.md). It is a finite terminal rule for the [four-vertex guard](../planar_two_geodesic_four_guard/README.md) in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a universal planar separator result. Graphs are finite and simple, with arbitrary positive edge lengths; a singleton is a geodesic.

## Exact connected-representative theorem

Let `F=G[C]` be any connected induced subgraph with `n=|C|` vertices, `m=|E(F)|` edges and cycle rank `beta=m-n+1`. A **connected deletion representative** is a subset `A` of `E(F)` such that `F-A` remains connected. Write `G_A=G-A`; all exterior edges remain at this test stage.

For any `k>=1`, the following are equivalent.

1. For **every spanning edge subgraph** `H` of `G`, every component of `H[C]` is coverable by at most `k` internal ambient `H`-geodesics.
2. For **every connected deletion representative** `A`, all vertices of `F-A` are coverable by at most `k` internal ambient `G_A`-geodesics.

Each representative has `|A|<=beta`, so there are at most

    sum_(j=0)^beta binomial(m,j)

direct tests. The set `A=empty` must be included. This is a bound on the number of connected internal deletion states, not a claim that finding their geodesic covers is polynomial time for arbitrary `k` or growing `beta`.

### Proof

Condition 1 applied to `H=G_A` gives condition 2, since `F-A` is connected. Conversely fix any spanning `H` and let `D=E(F)-E(H)` be its missing fragment edges. Choose an inclusion-maximal subset `A` of `D` such that `F-A` remains connected; such a set exists because `A=empty` is allowed. Every remaining missing edge `e` in `D-A` is a **bridge of `F-A`**: otherwise `A union {e}` would still leave a connected fragment. By condition 2, `F-A` has an internal ambient `G_A`-geodesic `k`-cover. The [bridge restriction lemma](../planar_two_geodesic_cactus_representatives/README.md) restricts those paths to geodesic covers of every component after the bridge deletions. Further exterior deletions from `G_A` to `H` can only increase distances, so these retained paths remain ambient `H`-geodesics. This proves condition 1. The edge bound follows because a connected graph on `n` vertices retains at least `n-1` edges. `□`

The argument needs no planarity or cactus structure. It also makes no claim that **one** intact cover persists if a cyclic internal edge is deleted: the [three-port star obstruction](../planar_two_geodesic_three_port_star_obstruction/README.md) shows that this can fail. For an induced tree, `beta=0` and the sole test is its intact cover. In a cactus, a connected deletion set contains at most one edge from each cycle and no bridges, yielding exactly `product_i(1+m_i)` representatives as in the previous theorem.

For `k=2`, an individual representative can be tested exactly by enumerating all simple internal paths of `F-A`, retaining those whose length equals the **full ambient** distance between their endpoints in `G_A`, and checking every pair for vertex coverage. The test is exact for finite graphs and may be expensive; it cannot be replaced by intrinsic distances of the fragment when exterior shortcuts exist.

## Weighted guard consequence

If some `S` of at most four vertices leaves components each of order at most four or a connected induced fragment passing the `k=2` representative test, every spanning edge subgraph of `G` has a half-balanced separator consisting of at most two ambient geodesics for **every** nonnegative vertex weighting. In a unit-edge planar graph, components of order five are allowed by the established induced-three-vertex-path rule. Cover a heavy residual by the terminal cover of its containing `H[C]` component, then use the established four-vertex heavy-component descent. This is a sufficient guard class and does not prove the unrestricted two-path conjecture.

## Non-cactus and logical controls

Take three internally disjoint three-edge paths between vertices `0` and `1`:

    0-2-3-1,  0-4-5-1,  0-6-7-1.

Their union is a planar theta graph with eight vertices, nine edges and cycle rank two. It is not a cactus: each edge belongs to two simple cycles. Its spherical rotation has three faces of length six. Exactly **37** of the `2^9` internal deletion sets leave it connected; every one has an internal ambient two-geodesic cover. The checker also exhausts all **512** edge subgraphs and their connected components. This control confirms a genuine extension of the cactus representative scheme to overlapping cycles, but is not a new global planar half-separator claim.

All connected representatives matter. In `K_5`, every maximal connected deletion representative leaves a spanning tree, and each such five-vertex tree is coverable by two geodesics in its own host. Yet the intact `K_5` has no two-geodesic vertex cover: each geodesic contains at most two vertices. The checker counts all 125 spanning-tree representatives. This nonplanar example isolates why testing only maximal deletion sets would be invalid; it has no bearing on whether planar graphs always admit half separators.

## Reproduction and trust boundary

Run from the repository root with Python 3.11 or later and the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_cycle_rank_representatives/verify.py
```

The checker constructs the theta rotation, recomputes full ambient shortest paths and every pair of internal geodesics for its 37 connected representatives and all 512 edge masks, and checks the stated `K_5` boundary. The arbitrary-order, arbitrary-positive-length theorem follows from the written maximal-connected-subset and bridge arguments. The finite controls do not establish a universal planar separator.

Literature checked 29 September 2026: the [workshop list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) states Problem 31, while [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) give structural two-path classes. No historical priority claim is made for the connected-representative reduction.
