# Two-port paths and cycles need no exterior length bound

This note proves an all-spanning terminal rule for any induced path or cycle with **at most two attachment vertices** and arbitrary positive edge lengths. It extends the [end-port path lemma](../planar_two_geodesic_three_port_path_gluing/README.md) to arbitrary port positions and adds cycles, with no metric condition on exterior shortcuts. The [independent review of that lemma](../planar_two_geodesic_three_port_path_gluing_review1/REVIEW.md) already observed its positive-edge extension for end ports; the arbitrary-port and cycle extensions are proved here. An explicit biconnected planar unit-edge family has nonisometric cycle residuals and treewidth at least four. These are sufficient classes for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a universal answer.

All graphs below are finite and simple. The terminal lemmas allow arbitrary **positive real edge lengths**; the weighted *vertex-mass* guard corollary and explicit family use unit edge lengths. A singleton counts as a shortest path. A set `C` has *at most two ports* if at most two vertices of `C` are incident with edges joining `C` to its complement. A terminal cover of `D` means at most two ambient geodesics with endpoints in `D` whose union contains `D`.

## The two-port path lemma

**Lemma.** Suppose `H[D]` is an induced path `w_0-...-w_L` and `D` has at most two ports in `H`, at arbitrary positions on this path. Then `D` has a terminal cover in `H`.

**Proof.** With at most one port, every ambient path between vertices of `D` stays in `D`: a simple path leaving through its sole port cannot return without repeating it. Thus the whole path is a geodesic.

Otherwise let the ports be `w_i,w_j`, with `i<j`, and let `t_r` be the path length from `w_0` to `w_r`. Choose `k` so that `t_k <= (t_i+t_j)/2 < t_(k+1)`; positivity places the cut between the two ports. The two internal paths `w_0-...-w_k` and `w_(k+1)-...-w_L` partition `D`. Any alternative from `w_0` to `w_k` that leaves `D` must make an excursion between the ports. An `i`-to-`j` excursion of positive length `delta` gives total length at least `t_i+delta+t_j-t_k > t_k`, because `2t_k<=t_i+t_j`. A `j`-to-`i` excursion costs at least `t_j+delta+t_k-t_i>t_k`. Thus the first path is geodesic. From `w_L` to `w_(k+1)`, a `j`-to-`i` excursion costs at least `(t_L-t_j)+delta+(t_(k+1)-t_i) > t_L-t_(k+1)`, because `2t_(k+1)>t_i+t_j`; the reverse excursion is longer still. Thus the second path is geodesic. The exterior route may be arbitrarily short and need not be known. `□`

If `C` induces a path with at most two ports in `G`, then after **any** edge deletion every component of `H[C]` is again an induced path with at most two ports in `H`. The lemma therefore gives a terminal cover of every such component for every spanning edge subgraph `H`.

## The two-port cycle theorem

**Theorem.** Suppose `C` induces a cycle of length at least three in a graph `G` with positive edge lengths and has at most two ports. For **every spanning edge subgraph** `H` of `G` and every component `D` of `H[C]`, `D` has a terminal cover in `H`. There is no planarity or exterior-route-length hypothesis.

**Proof.** If an edge of the cycle is deleted, every component `D` of `H[C]` is an induced path with at most two ports. Apply the path lemma. Assume now that all cycle edges survive. Choose distinct vertices `a,b` of the cycle containing the actual ports; if there are fewer than two, add arbitrary cycle vertices to complete the pair. Every exterior excursion still runs between `a,b` if it exists.

Write the two internally disjoint `a`-to-`b` cycle arcs as `A_0=a,A_1,...,A_p=b` and `B_0=a,B_1,...,B_q=b`, where `p,q>=1`. On each arc, cut immediately after its last vertex at or before the **weighted midpoint**: `A_i` is the last vertex whose arc distance from `a` is at most half that arc's length, and `B_j` is defined likewise. Let `P_a` run from `A_i` to `B_j` through `a`, and let `P_b` run from `A_(i+1)` to `B_(j+1)` through `b`. These internal paths are disjoint and partition the cycle vertices.

Each endpoint of `P_a` is at least as close **along its own arc** to `a` as to `b`. A simple competing path between its endpoints goes through `a`, through `b`, or uses one exterior `a`-to-`b` excursion. The path through `a` is `P_a`; the path through `b` cannot be shorter, and an exterior excursion adds positive length while replacing one endpoint's shorter route to `a` by its no-shorter route to `b`. Hence `P_a` is an ambient `H`-geodesic. Both endpoints of `P_b` are at least as close to `b` as to `a`, since each lies after its arc's weighted midpoint; the same comparison proves `P_b` geodesic. This covers the surviving cycle and finishes all deletion cases. `□`

The theorem says that *each component* of `H[C]` is coverable by its own pair; it does not say one common pair simultaneously covers every component after deletion. This is exactly the terminal property used by the [four-vertex heavy-component guard](../planar_two_geodesic_four_guard/README.md).

## Weighted guard consequence

Let `S` have at most four vertices in a finite simple **unit-edge** planar graph `G`. If every component of `G-S` either has order at most five or is an induced path/cycle with at most two ports in `G`, then every spanning edge subgraph `H` and every nonnegative real vertex weighting has a half-balanced separator that is the union of at most two `H`-geodesics. Cover the guard vertices inside a unique heavy component by two geodesics; if a heavy residual remains, cover its containing `H[C]` component by the terminal theorem. A planar residual of at most five vertices uses the reviewed pairing/induced-three-vertex-path rule. This is the same [guard descent](../planar_two_geodesic_four_guard/README.md) used for other terminal types. The path/cycle terminal permits positive edge lengths, while this small-component guard consequence uses unit edges.

## A biconnected planar family with a nonisometric cycle

For each `m>=8`, let `C_m` be an induced `m`-cycle and choose ports `v_0` and `v_k`, where `k=floor(m/2)>=4`. Add vertices `a,b` and the path `v_0-a-b-v_k`. Glue an octahedron along the edge `ab`, adding its other four vertices. There are no other edges. Draw the cycle as a convex oval, place the three-edge route outside it, and draw the octahedron on the other side of `ab`; this is planar. Both the cycle-plus-route and the octahedron are biconnected and meet along `ab`, so their union is biconnected.

With guard `S={a,b}`, the residual components are exactly the whole cycle and the four remaining octahedron vertices. The two-port cycle theorem and the small-component guard prove the **weighted all-spanning half-separator property**. The graph has `m+6` vertices and `m+14` edges. Its octahedron subgraph has minimum degree four, implying treewidth at least four because treewidth-three graphs are three-degenerate. The two ports have cycle distance `k>=4` but an exterior route of length three through `a,b`; thus the induced cycle is nonisometric in the whole graph. This family demonstrates the metric gain over an isometric-cycle-only guard for this fixed residual decomposition. It may belong to other previously known separator classes; no historical priority is claimed.

## Reproduction and trust boundary

Run from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_port_cycles/verify.py
```

The standard-library checker enumerates all pairs of cycle ports, all cycle-edge masks, and capped exterior route lengths for **unit-edge** cycle orders four through nine; it independently enumerates anchored ambient shortest-path traces and finds a two-path cover of **every** residual component. It then checks rational straight-line drawings, biconnectivity, guard residuals, the octahedron, and the exterior distance for family orders `8,9,16,32,100`. Expected totals are `384,1600,5760,18816,57344,165888` finite cycle profiles, followed by five family lines and `PASS`. The finite checks support the proof but do not establish its unbounded and positive-length quantifiers. Those follow from the weighted midpoint arguments above. No exhaustive census of planar graphs is claimed.

Literature checked 29 September 2026: the [workshop problem list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still prints Problem 31 as a question. The [schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) refers to a disproof of an unspecified Codsi conjecture without a formal statement or witness linking it to this problem.
