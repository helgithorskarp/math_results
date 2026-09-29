# Exact deletion representatives for cactus geodesic terminals

An induced cactus fragment need not be isometric. To certify that it retains an internal `k`-geodesic cover in **every** spanning edge subgraph, it suffices to test one intact host for each choice of no deletion or one deleted edge on each cycle. The remaining possible deletions are bridges, which only restrict a covering geodesic to a contiguous subpath. For a single cycle, the path [edge-window criterion](../planar_two_geodesic_edge_window_characterization/README.md) makes each deleted-edge test a distance calculation.

This is a terminal and [four-vertex guard](../planar_two_geodesic_four_guard/README.md) tool for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). It does not show that arbitrary planar graphs have two-path half separators. All graphs are finite and simple, all edge lengths are arbitrary positive reals, and singleton paths count as geodesics.

## Bridge restriction lemma

Let `F=G[C]` be any connected induced fragment, and suppose at most `k` internal ambient `G`-geodesics cover `C`. Let `H` be obtained by deleting arbitrary edges outside `F` and any selection of **bridges of `F`**, but retaining all other edges of `F`. Then every component `D` of `H[C]` has a cover by at most `k` internal ambient `H`-geodesics.

Indeed, an original bridge of `F` separates its endpoints in every spanning subgraph of `F` missing that edge. If two vertices of an internal path `P` lie in the same `D`, the segment of `P` between them cannot cross a deleted bridge, since any route between those vertices would have to cross it. Therefore `P intersect D` is empty or one contiguous subpath whose edges survive. Subpaths of ambient geodesics are geodesics; deleting edges outside or inside `F` cannot shorten them. The intersections of the original covering paths cover `D`. This generalizes the [induced-tree persistence lemma](../planar_two_geodesic_initial_tree_cover/README.md), where every internal edge is a bridge.

## Exact cactus theorem

Let `F=G[C]` be a connected induced cactus, with edge-disjoint cycles `Z_1,...,Z_s` of lengths `m_1,...,m_s`. For a **representative choice** `sigma`, independently choose for each `Z_i` either no edge or exactly one of its `m_i` edges. Let `A_sigma` be the chosen edges and `G_sigma=G-A_sigma`; its induced fragment `F_sigma=F-A_sigma` remains connected. Then these statements are equivalent:

1. For every spanning edge subgraph `H` of `G`, every component of `H[C]` is coverable by at most `k` internal ambient `H`-geodesics.
2. For every representative `sigma`, the vertices of `F_sigma` are coverable by at most `k` internal ambient `G_sigma`-geodesics.

Thus exactly `product_i (1+m_i)` intact-host cover tests suffice, including the empty choice `sigma`.

**Proof.** Necessity takes `H=G_sigma`; removing one edge from each selected cactus cycle leaves `F_sigma` connected. For sufficiency, fix arbitrary `H`. In each cactus cycle on which `H` deletes at least one edge, select one such edge for `A_sigma`; choose none on intact cycles. Now `H` is a spanning edge subgraph of `G_sigma`. Every further edge of `F_sigma` missing in `H` is a bridge of `F_sigma`: original cactus bridges stay bridges, and after one edge of a cycle has been removed, every remaining edge of that cycle lies on its unique surviving path and becomes a bridge. Apply the bridge restriction lemma to the cover from condition 2. `□`

No enumeration of deleted exterior edges is needed: they can only preserve or lengthen the selected internal geodesics. For a tree, the product is one and the theorem is exactly the initial-cover persistence result.

### Single-cycle distance version

If `F=C` is an induced cycle of length `m`, there are `m+1` tests. First check that two internal ambient geodesic arcs cover the intact cycle in `G`. For each cycle edge `e`, use **full ambient distances in `G-e`** and apply the exact edge-window test to the induced path `C-e`: some path edge must meet every active shortcut window. This is a necessary and sufficient finite criterion for all-spanning internal two-geodesic coverage of the cycle. It allows any number of outside ports; the previously published [three-port star](../planar_two_geodesic_three_port_star_obstruction/README.md) fails precisely one or more of the deleted-edge tests despite having an intact-cycle two-cover.

The criterion is for internal full coverage of a prescribed fragment. A failed test does not rule out an ambient separator whose paths leave the fragment or only balance its mass.

## Exact planar controls

**Positive nonisometric three-port cycle.** Take the unit eight-cycle `0-1-...-7-0`, add an interior hub `h` adjacent to `0,2,4`, and use the cycle as the fragment. It is induced but not isometric: its internal `0-4` distance is four, while `0-h-4` has length two. The intact cycle is covered by the geodesic arcs `0-1-2` and `3-4-5-6-7`. For each of its eight edge deletions, the checker computes full port distances and finds a covering path edge by the exact window criterion. It also exhausts all `2^11=2048` spanning edge subgraphs and every pair of internal ambient geodesics for every surviving component. A spherical rotation has face lengths `4,4,6,8`.

**Two-cycle cactus.** Two unit four-cycles sharing just vertex `0` form an induced cactus with `s=2` and 25 representatives. Direct exact enumeration verifies all 25 tests and all `2^8=256` spanning edge subgraphs. Its planar rotation has face lengths `4,4,8`.

**Negative contrast.** The ten-cycle with a hub adjacent to `0,3,8` has an intact internal two-geodesic cover, but deleting edge `9-0` leaves no internal two-cover. This demonstrates why the empty representative alone is insufficient for cycles. The earlier [independent star certificate](../planar_two_geodesic_three_port_star_obstruction/README.md) proves the stronger failure even when the two geodesics may leave the cycle.

## Guard use and reproduction

If a set `S` of at most four vertices leaves components each of order at most four or an induced cactus passing the `k=2` representative tests in the full graph, the four-vertex heavy-component descent gives a half-balanced separator of at most two ambient geodesics for every spanning subgraph and every nonnegative vertex mass. In a unit-edge planar host, order-five small components are allowed as well. The proof covers the **whole** heavy residual component before replacing the initial guard pair.

Run the exact standard-library checker from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_cactus_representatives/verify.py
```

It audits the positive and negative planar controls, rotation systems, all stated representative hosts, and all listed edge-deletion masks. The all-order, arbitrary-positive-length cactus theorem is the written bridge argument; the finite checker only verifies explicit unit-edge examples.

Literature checked 29 September 2026: the [workshop list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) states Problem 31, and [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) give structural two-path classes. No priority claim is made for this cactus reduction.
