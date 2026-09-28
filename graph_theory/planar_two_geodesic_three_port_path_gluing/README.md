# Gluing a three-port lollipop to long two-port paths

This note gives a reusable terminal rule and an explicit unbounded planar family for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). The family has finite exterior routes at all three lollipop ports, arbitrarily long residual paths that are not isometric, and treewidth at least four. Every spanning edge subgraph admits a two-geodesic half separator for every nonnegative vertex weighting. These are sufficient conditions for this family, not a resolution of the universal problem.

Graphs are finite, simple, and unit-edge. A singleton is a geodesic. A *terminal cover* of a component `D` of `H[C]` consists of at most two geodesics in the ambient spanning edge subgraph `H`, with endpoints in `D`, whose union contains `D`.

## A deletion-stable two-port path terminal

**Lemma.** Let `C={v_0,...,v_ell}` induce exactly the path `v_0-...-v_ell` in a graph `G`. Suppose every edge between `C` and `G-C` is incident with `v_0` or `v_ell`. For every spanning edge subgraph `H` of `G`, each component of `H[C]` has a terminal cover. There is no condition on the length of an exterior route between the two ports.

**Proof.** If some path edge is absent, each component of `H[C]` is an interval containing at most one port. A simple ambient path joining two vertices of that interval cannot leave it: its only possible exit and re-entry through `C` would repeat its sole port. Thus the interval itself is an `H`-geodesic. This also handles singleton components.

Otherwise the entire induced path survives. Put `k=floor(ell/2)`. The two disjoint intervals `v_0-...-v_k` and `v_{k+1}-...-v_ell` cover `C` (omit an empty interval when `ell=0`). A route from `v_0` to a vertex `v_i` with `i<=k` that leaves `C` must re-enter at `v_ell`; it has length at least `1+ell-i>i`. Hence the first interval is geodesic. The same argument from `v_ell` proves the second is geodesic, since its length is at most `floor(ell/2)`. `□`

The lemma covers paths that are **not isometric** in `G`: a very short outside route may shorten distances between opposite ends of the path. It survives arbitrary edge deletion because a broken path component has at most one attachment port.

## Hybrid four-vertex guard

Let `S` be at most four vertices in a finite simple planar graph. Suppose every component of `G-S` is one of the following:

1. of order at most five;
2. an induced path with all outside edges incident to its two endpoints;
3. a cycle-plus-leaf fragment satisfying the [all-order three-port lollipop theorem](../planar_two_geodesic_all_spanning_three_port_guard/README.md), with its restricted exterior route lengths measured in the full graph `G`.

Then **every spanning edge subgraph** `H` and **every nonnegative real vertex-mass assignment** has a half-balanced separator equal to the union of at most two `H`-geodesics.

For completeness, here is the [four-vertex guard descent](../planar_two_geodesic_four_guard/README.md) in this setting. If no component has more than half the total mass, use the empty separator. Otherwise let `K` be the unique heavy component. Pair the at most four vertices of `S∩K` and join each pair by an `H`-geodesic, using singleton paths when needed. If the resulting deletion is not balanced, its heavy component lies inside one original component `C` of `G-S` and inside one component `E` of `H[C]`. Cover `E` by two ambient geodesics using the applicable terminal theorem; for a planar component of order at most five, pair its vertices or use an induced three-vertex path and pair the rest. Deleting these geodesics removes the heavy component's entire mass and leaves less than half the original total mass. The paths can be chosen afresh in every `H`, so no edge must be protected. `□`

## An explicit planar family with three active ports

For each `m>=12`, put `L=m-8`. Start with the induced lollipop `C_m`: the cycle `0-1-...-(m-1)-0` and leaf edge `0-m`. Add four guard vertices `a,b,c,d`. Attach ports `1,3,5` to `a,b,c`, respectively, by one edge each. Add internally disjoint paths of length `L` on the four pairs `ab,bc,ca,db`, and add the edge `ad`. Finally glue an octahedron along the existing edge `ad`: its six vertices are `a,d,q,x,y,p`, with outer triangle `a,d,q`, inner triangle `x,y,p`, and cross edges `ay,ap,dx,dp,qx,qy`. There are no other vertices or edges.

The three `a,b,c` paths form a large outer triangle. Draw `C_m` inside it with ports `1,3,5` in the corresponding cyclic order, and draw their three attachment edges without crossings. Draw `d` and the path `db` outside side `ab`, and the octahedron outside side `ad`. This is a planar drawing for every `m`. The rational straight-line drawing in [`verify.py`](verify.py) independently checks crossings for sample values.

Take `S={a,b,c,d}`. The components of `G_m-S` are exactly `C_m`, the four interiors of the length-`L` paths, and the four remaining octahedron vertices. Each path interior is a two-port path terminal; the octahedron residual has order four. In the graph with `C_m` removed, the distances among `a,b,c` are all `L`: each has a direct length-`L` side, while the detour through `d` from `a` to `b` has length `L+1`, and the octahedron connects to the rest only through `a,d`. Thus all three restricted exterior distances between ports `1,3,5` equal `L+2=m-6`. The [three-port theorem](../planar_two_geodesic_all_spanning_three_port_guard/README.md) applies, and the hybrid guard proves the weighted, all-spanning two-geodesic half-separator conclusion.

The graph has `5m-27` vertices and `5m-16` edges. Its octahedron subgraph has minimum degree four, so `G_m` has treewidth at least four: every graph of treewidth at most three is three-degenerate. The path interior on `ab` has `L-1` vertices. For `m>=17`, its two ends are distance `L-2>6` along that path but have an ambient route of length six through `a-1-2-3-b`. Thus this residual path is not isometric; the two-port path lemma supplies the missing all-spanning cover.

This treewidth comparison rules out only the [Diot–Gavoille treewidth-three theorem](https://emilie-diot.eu/Article/DG10a) as an explanation of this particular family. It does not assert that the family lies outside all other known sufficient classes.

## Reproduction and scope

From the repository root, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_three_port_path_gluing/verify.py
```

The standard-library exact checker constructs `m=12,13,16,32,100`, tests every pair of drawn segments for crossings using rational arithmetic, checks vertex and edge counts, the six guard residual components, the octahedron, and the three restricted exterior distances. Its final line is `PASS`. These finite audits check the explicit construction; the all-order conclusion follows from the written planar drawing, path lemma, reviewed guard descent, and prior three-port theorem. The checker does not enumerate all edge subgraphs or vertex weights.

Literature checked 28 September 2026: the [workshop problem list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still prints Problem 31 as a question. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) mentions a disproof of an unspecified Codsi conjecture but gives neither a formal statement nor a witness identifying it with Problem 31.
