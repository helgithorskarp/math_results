# A third port defeats deletion-stable path and cycle coverage

The [two-port path/cycle terminal](../planar_two_geodesic_two_port_cycles/README.md) has a sharp boundary in its **number of attachment vertices**. A biconnected planar unit-edge graph with an induced cycle and three outside ports has a spanning edge subgraph whose cycle component cannot be covered by two ambient geodesics, **even if their endpoints may lie outside the cycle**. The obstruction extends to cycles of every length at least ten. This concerns full coverage of a prescribed residual fragment; it is not a counterexample to the half-separator question in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Eleven-vertex witness

Let `G_10` consist of the induced cycle `0-1-...-9-0` and one new vertex `h` adjacent exactly to `0,3,8`. Draw the cycle convexly and `h` inside; its three spokes do not cross. The graph is biconnected: after deleting any cycle vertex, the remaining cycle path and `h` stay connected through at least two spokes; after deleting `h`, the cycle remains. The only outside ports of the cycle are `0,3,8`.

Delete the cycle edge `9-0`, obtaining `H_10`. Its induced fragment on `C={0,...,9}` is the **connected path** `0-1-...-9`. Yet no union of at most two shortest paths of `H_10` covers `C`. Endpoints of those paths are unrestricted and may equal `h`.

Here is a compact exact certificate. Write the intersection of a geodesic with `C` as a ten-bit mask, with bit `i` representing vertex `i`. Enumerating all `H_10` geodesics over **all endpoint pairs**, including `h`, gives 67 paths and 57 distinct masks. The inclusion-maximal masks are exactly

```text
007 039 07e 0f0 18c 1c3 303 30c 318 3e0    (hexadecimal)
```

The bitwise OR of any two of these ten masks has at most nine set bits, whereas the full fragment is `3ff`. Every other geodesic mask is contained in one of the listed masks. Therefore no pair of ambient geodesics covers the ten fragment vertices. [`verify.py`](verify.py) recomputes every shortest path from breadth-first distances and checks the full mask set, maximal list, and pairwise maximum. An independent [`audit.py`](audit.py) uses Floyd–Warshall distances and enumerates all bounded simple paths; it obtains the same certificate. The table is not a guessed list of candidate paths.

## Unbounded biconnected planar family

For every `m>=10`, form `G_m` from the induced `m`-cycle `0-1-...-(m-1)-0` by adjoining a hub `h` to exactly the same three ports `0,3,8`. The convex-cycle drawing proves planarity, and the same deletion argument proves biconnectivity. Let `H_m=G_m-(m-1)0`. Then `H_m[C]` is the path `0-1-...-(m-1)`.

The subgraph of `H_m` induced by `{0,...,9,h}` is exactly `H_10`. The additional vertices `10,...,m-1` form a pendant path attached to vertex `9`. This shows the small witness propagates to every `m`:

1. The old subgraph `H_10` is isometric in `H_m`, since a simple route between old vertices cannot enter and leave a pendant path through `9`.
2. Any `H_m`-geodesic meets the old subgraph in an interval; trim away its possible pendant end. The remaining path is an `H_10`-geodesic, or it meets the old subgraph only at vertex `9`.
3. If two `H_m`-geodesics covered all vertices of `C`, their trimmed old portions would cover `0,...,9`, contradicting the exact witness certificate.

Thus **every** `G_m` has one cycle-edge deletion for which its sole cycle-fragment component lacks a two-geodesic cover. The conclusion is stronger than failure of the anchored-terminal rule because exterior endpoints were already allowed in the 11-vertex calculation. It does not assert that two paths cannot give a half-balanced separator of `G_m` or `H_m`.

## Reproduction and scope

Run from the repository root with Python 3.11 or later:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_three_port_star_obstruction/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_three_port_star_obstruction/audit.py
```

The standard-library checker uses exact rational coordinates to verify noncrossing straight-line drawings and biconnectivity at `m=10,11,12,20,50`. It enumerates every shortest path and every pair of its fragment traces after the specified deletion at `m=10,11,12,13`; all four have maximum coverage `m-1`. The independent audit verifies a planar rotation system with face lengths `4,5,7,10`, then independently enumerates all simple paths against Floyd–Warshall distances and confirms `67` geodesics, `57` traces, the ten maximal masks, and pairwise maximum `9`. The all-order family claim rests on the pendant-path trimming proof, not on the finite checks. No generated graph dump or binary is needed.

Literature checked 29 September 2026: the [workshop list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still states Problem 31 as a question; the [schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) names an unspecified Codsi-conjecture disproof without a formal witness. This terminal obstruction does not identify that announcement with Problem 31 and makes no priority claim.
