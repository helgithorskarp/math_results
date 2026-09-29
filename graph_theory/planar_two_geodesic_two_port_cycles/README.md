# Two-port paths and cycles need no exterior length bound

This note proves an all-spanning terminal rule for any induced path or cycle with **at most two attachment vertices**. It extends the [end-port path lemma](../planar_two_geodesic_three_port_path_gluing/README.md) to arbitrary port positions and adds cycles, with no metric condition on exterior shortcuts. An explicit biconnected planar family has nonisometric cycle residuals and treewidth at least four. These are sufficient classes for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a universal answer.

All graphs below are finite, simple, and unit-edge. A singleton counts as a shortest path. A set `C` has *at most two ports* if at most two vertices of `C` are incident with edges joining `C` to its complement. A terminal cover of `D` means at most two ambient geodesics with endpoints in `D` whose union contains `D`.

## The two-port path lemma

**Lemma.** Suppose `H[D]` is an induced path `w_0-...-w_L` and `D` has at most two ports in `H`, at arbitrary positions on this path. Then `D` has a terminal cover in `H`.

**Proof.** With at most one port, every ambient path between vertices of `D` stays in `D`: a simple path leaving through its sole port cannot return without repeating it. Thus the whole path is a geodesic.

Otherwise let the ports be `w_i,w_j`, with `i<j`, and put `k=floor((i+j)/2)`. The two internal paths `w_0-...-w_k` and `w_(k+1)-...-w_L` partition `D`. Any alternative from `w_0` to `w_k` that leaves `D` must make an excursion between the two ports. If it traverses `i` to `j`, its length is at least `i+1+j-k`, which is greater than `k` because `2k<=i+j`; if it traverses `j` to `i`, its length is at least `j+1+k-i>k`. Thus the first path is geodesic. From `w_L` to `w_(k+1)`, the analogous `j`-to-`i` excursion has length at least `(L-j)+1+(k+1-i)`, which is no less than `L-k-1` because `2k+2>=i+j`; the other excursion is longer still. Thus the second path is geodesic. An excursion may be any positive-length route through an arbitrary exterior network; no shortest-route value was assumed. `□`

If `C` induces a path with at most two ports in `G`, then after **any** edge deletion every component of `H[C]` is again an induced path with at most two ports in `H`. The lemma therefore gives a terminal cover of every such component for every spanning edge subgraph `H`.

## The two-port cycle theorem

**Theorem.** Suppose `C` induces a cycle of length at least three in `G` and has at most two ports. For **every spanning edge subgraph** `H` of `G` and every component `D` of `H[C]`, `D` has a terminal cover in `H`. There is no planarity or exterior-route-length hypothesis.

**Proof.** If an edge of the cycle is deleted, every component `D` of `H[C]` is an induced path with at most two ports. Apply the path lemma. Assume now that all cycle edges survive. With at most one port, the cycle is isometric in `H`, so two ordinary half-cycle arcs cover it by geodesics.

For two distinct ports `a,b`, write the two internally disjoint `a`-to-`b` cycle arcs as `A_0=a,A_1,...,A_p=b` and `B_0=a,B_1,...,B_q=b`, where `p,q>=1`. Put `i=floor((p-1)/2)` and `j=floor((q-1)/2)`. Let `P_a` run from `A_i` to `B_j` through `a`, and let `P_b` run from `A_(i+1)` to `B_(j+1)` through `b`. These internal paths are disjoint and partition the cycle vertices.

Each endpoint of `P_a` is at least as close along its own arc to `a` as to `b`: `i<=p-i` and `j<=q-j`. A simple competing path between its endpoints goes through `a`, through `b`, or uses one exterior `a`-to-`b` excursion. The path through `a` is `P_a`; the path through `b` cannot be shorter, and an exterior excursion adds positive length while replacing one endpoint's shorter route to `a` by its no-shorter route to `b`. Hence `P_a` is an ambient `H`-geodesic. Likewise `p-i-1<=i+1` and `q-j-1<=j+1`, so both endpoints of `P_b` are at least as close to `b` as to `a`; the same comparison proves `P_b` geodesic. This covers the surviving cycle and finishes all deletion cases. `□`

The theorem says that *each component* of `H[C]` is coverable by its own pair; it does not say one common pair simultaneously covers every component after deletion. This is exactly the terminal property used by the [four-vertex heavy-component guard](../planar_two_geodesic_four_guard/README.md).

## Weighted guard consequence

Let `S` have at most four vertices in a finite simple planar graph `G`. If every component of `G-S` either has order at most five or is an induced path/cycle with at most two ports in `G`, then every spanning edge subgraph `H` and every nonnegative real vertex weighting has a half-balanced separator that is the union of at most two `H`-geodesics. Cover the guard vertices inside a unique heavy component by two geodesics; if a heavy residual remains, cover its containing `H[C]` component by the terminal theorem. A planar residual of at most five vertices uses the reviewed pairing/induced-three-vertex-path rule. This is the same [guard descent](../planar_two_geodesic_four_guard/README.md) used for other terminal types.

## A biconnected planar family with a nonisometric cycle

For each `m>=8`, let `C_m` be an induced `m`-cycle and choose ports `v_0` and `v_k`, where `k=floor(m/2)>=4`. Add vertices `a,b` and the path `v_0-a-b-v_k`. Glue an octahedron along the edge `ab`, adding its other four vertices. There are no other edges. Draw the cycle as a convex oval, place the three-edge route outside it, and draw the octahedron on the other side of `ab`; this is planar. Both the cycle-plus-route and the octahedron are biconnected and meet along `ab`, so their union is biconnected.

With guard `S={a,b}`, the residual components are exactly the whole cycle and the four remaining octahedron vertices. The two-port cycle theorem and the small-component guard prove the **weighted all-spanning half-separator property**. The graph has `m+6` vertices and `m+14` edges. Its octahedron subgraph has minimum degree four, implying treewidth at least four because treewidth-three graphs are three-degenerate. The two ports have cycle distance `k>=4` but an exterior route of length three through `a,b`; thus the induced cycle is nonisometric in the whole graph. This family demonstrates the metric gain over an isometric-cycle-only guard for this fixed residual decomposition. It may belong to other previously known separator classes; no historical priority is claimed.

## Reproduction and trust boundary

Run from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_port_cycles/verify.py
```

The standard-library checker enumerates all pairs of cycle ports, all cycle-edge masks, and capped exterior route lengths for cycle orders four through nine; it independently enumerates anchored ambient shortest-path traces and finds a two-path cover of **every** residual component. It then checks rational straight-line drawings, biconnectivity, guard residuals, the octahedron, and the exterior distance for family orders `8,9,16,32,100`. Expected totals are `384,1600,5760,18816,57344,165888` finite cycle profiles, followed by five family lines and `PASS`. The finite checks support the proof but do not establish its unbounded quantifiers. Those follow from the midpoint arguments above. No exhaustive census of planar graphs is claimed.

Literature checked 29 September 2026: the [workshop problem list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still prints Problem 31 as a question. The [schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) refers to a disproof of an unspecified Codsi conjecture without a formal statement or witness linking it to this problem.
