# A common metric window gives deletion-stable path covers with many ports

This note gives a checkable sufficient condition for an induced path with **any number of outside attachment vertices** to retain a two-geodesic cover after every edge deletion. The condition localizes all genuine ambient shortcuts around one cut of the path. It extends the unconditional [two-port terminal](../planar_two_geodesic_two_port_cycles/README.md), while the [three-port star obstruction](../planar_two_geodesic_three_port_star_obstruction/README.md) shows why a condition is needed for more ports. The result is a terminal and guard tool for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a universal resolution.

All graphs are finite and simple. Edge lengths are arbitrary positive reals unless a corollary explicitly says unit edges. Singleton paths count as geodesics.

## Metric focus criterion

Let `C={v_0,...,v_l}` induce a path in `G`. Write `t_i` for the total path length from `v_0` to `v_i`, so `0=t_0<...<t_l=T`. Let `B` be the set of vertices of `C` incident with an edge to `G-C`. For each pair of ports `v_i,v_j` with `i<j`, write `delta_ij=d_G(v_i,v_j)`. The pair is **active** when `delta_ij<t_j-t_i`; it then defines a closed metric window

    J_ij=[(t_i+t_j-delta_ij)/2, (t_i+t_j+delta_ij)/2].

The distances here are the **full ambient distances in `G`**, not just lengths of paths whose internal vertices avoid `C`. A route may chain two outside excursions through a third port, and full distances capture it.

**Theorem.** If all active windows `J_ij` have a common point, then for **every spanning edge subgraph** `H` of `G` and **every component** `D` of `H[C]`, the vertices of `D` can be partitioned into at most two internal paths that are ambient `H`-geodesics. The intersection condition is vacuous when there are no active pairs. No planarity assumption is needed.

Equivalently, with `A` the active port pairs, the finite test is

    max_(i,j in A) (t_i+t_j-delta_ij)
        <= min_(i,j in A) (t_i+t_j+delta_ij).

This requires only shortest-path distances between boundary ports and the path's own cumulative lengths. For at most two ports, there is at most one active pair, so the condition always holds and recovers the two-port path theorem.

### Proof

Fix `H` and a component `D` of `H[C]`. It is a surviving interval of the path. A simple ambient route between vertices of `D` that leaves `D` must first exit at one port `p` of `D` and last re-enter at a **different** port `q` of `D`. The portion between these two events has length at least `d_G(p,q)`, even if it passes through other ports or makes several exterior excursions. Edge deletion cannot reduce this lower bound. Before its first exit and after its last return, the route follows the unique internal path in `D`.

If no pair of ports in `D` is active in `G`, the internal path between any two vertices of `D` is shortest: replace the middle portion's lower bound `d_G(p,q)` by the equal internal port distance. Thus `D` itself is a geodesic.

Otherwise choose a point `x` common to all active windows of `G`. An active window lies strictly between its two port coordinates, so `x` lies inside `D`. Cut `D` at an edge `v_k v_(k+1)` containing `x`, giving its left and right vertex intervals. We show that each interval is an ambient geodesic.

Consider a route from the left end of `D` to `v_k`. If its first exit port `p` lies to the right of its last return port `q`, the detour is longer than staying on the path. For `p<q`, a nonactive pair cannot shorten the route because `d_G(p,q)=t_q-t_p`. If `p<q` is active, then `x` lies in `J_pq`, and so `t_k<=x<=(t_p+t_q+d_G(p,q))/2`. A detour through `p,q` has length at least its internal prefix plus `d_G(p,q)` plus the internal suffix. When the two ports straddle `v_k`, the displayed inequality says this is at least the internal route; when both lie to the right, it is longer; and both cannot lie to the left because the upper end of `J_pq` lies strictly before `q`. Hence the left interval is an `H`-geodesic.

The right interval is symmetric. Here `t_(k+1)>=x>=(t_p+t_q-d_G(p,q))/2` prevents a right-to-left active excursion from shortening its internal route. The two paths partition `D`, and this reasoning applies independently in every `H`. `□`

The criterion is sufficient; disjoint windows do not alone prove a terminal failure. The [three-port obstruction](../planar_two_geodesic_three_port_star_obstruction/README.md) supplies an actual failure with disjoint windows, certified by all shortest paths.

## Guard consequences

The proof gives **internal**, endpoint-anchored geodesics, so it plugs directly into the [four-vertex heavy-component guard](../planar_two_geodesic_four_guard/README.md).

* In any positive-edge graph, if some `S` has at most four vertices and every component of `G-S` either has at most four vertices or is a path satisfying the metric focus criterion in the full `G`, then every spanning `H` and every nonnegative vertex-mass assignment has a half-balanced separator formed by at most two `H`-geodesics. A component of order at most four is covered by pairing its vertices; no planarity or unit-edge assumption is needed.
* In a **unit-edge planar** graph the small-component bound may be raised to five, by the induced-three-vertex-path rule in the reviewed guard theorem. The same all-spanning, weighted half-balance conclusion follows.

These are positive sufficient classes. The criterion concerns each specified residual path and does not assert that every planar graph has such a guard.

## Two active shortcuts and arbitrarily many ports

For a concrete three-port example, take the unit-edge path `0-1-...-9`, and attach internally disjoint exterior ears of lengths three from `0` to `4` and five from `0` to `8`. The ambient port distances are `d(0,4)=3`, `d(0,8)=5`, and `d(4,8)=4`. The two active windows are `[1/2,7/2]` and `[3/2,13/2]`, with intersection `[3/2,7/2]`. Thus **both** exterior routes genuinely shorten port distances, yet every component of every edge-deleted path admits the two internal geodesics supplied by the theorem.

There are planar examples with an unbounded number of active ports. For each `m>=4`, take the unit-edge path `0-1-...-(m-1)` and, for every `j=3,...,m-1`, add an internally vertex-disjoint exterior ear of length `j-1` from `0` to `j`. Draw the ears as subdivisions of noncrossing fan chords sharing `0`. The path has `m-2` ports. Its only active port pairs are `(0,j)`, with ambient distance `j-1` and window `[1/2,j-1/2]`; pairs among `3,...,m-1` retain their internal distance. Every active window contains `[1/2,5/2]`, so the terminal theorem applies for every `m`. This example concerns full coverage of the induced path fragment; the ears themselves are not asserted to form a four-guard decomposition.

## Reproduction and trust boundary

From the repository root, with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_common_shortcut_window/verify.py
```

The standard-library checker computes full ambient distances and exact rational windows. It audits all `2048` path-edge and ear-survival profiles of the three-port example, and all `4096` such profiles of the six-port `m=8` fan; broken ear fragments are pendant and have the same path metric as deleting the ear. It also checks the claimed active-pair distances and windows for fan sizes `8,16,32`. Expected final line: `PASS`. These finite controls do not replace the all-order and arbitrary-positive-length proof above. No universal planar separator claim is made.

Literature checked 29 September 2026: the [workshop problem list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still prints Problem 31 as a question. The [schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) names an unspecified Codsi-conjecture disproof without a statement or witness tying it to Problem 31.
