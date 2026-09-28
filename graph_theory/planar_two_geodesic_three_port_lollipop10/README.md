# A three-port lollipop guard with an exact finite certificate

This is a computer-assisted, all-order sufficient condition for a component to be covered by two shortest paths in **every spanning edge subgraph**. It is relevant to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), but does not settle the unrestricted planar question. All graphs are finite, simple, and have unit edges; a singleton is a path.

## The terminal theorem

Let `C={0,...,10}` induce a ten-cycle `0-1-...-9-0` with one pendant edge `0-10` in an arbitrary graph `G`. Suppose every edge from `C` to `G-C` meets `C` at a port in `{1,3,5}`. For ports `a,b`, write `lambda_ab` for the length of a shortest `a`-to-`b` path whose internal vertices are all outside `C`, with value infinity if no such route exists.

**Theorem (three-port lollipop guard).** If `lambda_15 >= 4`, then for every spanning edge subgraph `H` of `G` and every component `D` of `H[C]`, there are at most two shortest paths **in `H`**, each with both endpoints in `D`, whose union contains `D`. No planarity assumption is needed.

The other restricted routes have lengths at least two automatically: `C` is induced, so there is no direct edge joining two ports. Note that `lambda_15 >= 4` is only a sufficient condition; the failure control below makes the uniform threshold sharp but does not classify each individual host with a route of length three.

### Proof and finite reduction

Fix `H`. Put `F'=H[C]` and let `delta_ab` be its shortest exterior route lengths. Edge deletion cannot decrease route lengths, so `delta_13,delta_35 >= 2` and `delta_15 >= 4`. The [exact multiport closure theorem](../planar_two_geodesic_multiport_closure/README.md) replaces the exterior network by three separate virtual port-to-port paths of lengths `delta_ab`, preserving **all** `C`-endpoint distances and their `C`-trace families. The arrays need not satisfy a triangle inequality. Consequently it is enough to cover each component of `F'` in every such weighted closure model; checking even nonrealizable arrays is safe for sufficiency.

A component `D` of `F'` has at most 11 vertices. If it has at most four vertices, pair its vertices and choose ambient geodesics. If it has five, `F'[D]` is connected and noncomplete, since the lollipop has no clique of order five. It has an induced three-vertex path. That path is ambient shortest: its endpoints are nonadjacent in `H`, and its length is two. A second geodesic joins the two remaining vertices. Thus only components of order at least six require computation. There can be at most one such component in an 11-vertex fragment.

For endpoints in a connected `D`, an internal `F'[D]` path has at most ten edges. A virtual route of length at least eleven cannot occur in any geodesic between these endpoints. Replace each such route by infinity. This **all-order cutoff** leaves exactly `10 * 8 * 10 = 800` length triples: `delta_13,delta_35` in `{2,...,10,infinity}` and `delta_15` in `{4,...,10,infinity}`. There are `2^11=2048` choices of `F'`; exactly 402 have a component of order at least six.

The exhaustive checker tests all `800 * 402 = 321600` remaining states. It computes exact weighted distances, traverses every shortest-path directed acyclic graph from each endpoint in `D`, records every trace on `D`, and checks whether two traces cover `D`. Every state passes. The earlier reductions turn this finite exhaustive result into the stated theorem for graphs of arbitrary order. `□`

The trusted boundary is explicit: the all-order statement uses the written cutoff and the separately proved multiport trace theorem; `exhaustive.cpp` certifies the 321,600 finite closure states. A second implementation using Dijkstra independently checks all fragment masks at four profiles and ten selected masks at every profile. Neither finite program by itself proves the unrestricted two-path planar separator conjecture.

## Sharp control and a planar application

The lower bound four is sharp as a **uniform sufficient bound**. Start from `C`, attach disjoint exterior ears `1-x-3` and `1-y-z-5`, and delete the internal edge `2-3` while retaining every other fragment edge. This is a planar 14-vertex host with exterior lengths `(lambda_13,lambda_15,lambda_35)=(2,3,infinity)`. Its fragment remains connected, but the largest union of two `C`-endpoint geodesics meets only 10 of its 11 vertices. Both implementations detect this failure. It is a failure of the local anchored-cover property, **not** a counterexample to Problem 31.

The theorem plugs into the [reviewed four-vertex heavy-residual argument](../planar_two_geodesic_four_guard_review1/REVIEW.md). If a planar graph has a fixed `S` of at most four vertices and every component of `G-S` either has order at most five or is an induced three-port lollipop of this form with `lambda_15 >= 4`, then **every spanning edge subgraph** and every nonnegative real vertex-mass assignment has a half-balanced separator formed by at most two of its geodesics. Indeed, cover the vertices of `S` in the unique heavy component by two geodesics. If a heavy component remains, it lies in a component of `G-S`; cover its containing component of `H[C]` by the terminal theorem (or the at-most-five rule), and replace the guard paths. Every surviving component then has mass less than half the original total. This is a conditional positive class, not a reduction for every planar graph.

For a concrete application, take an octahedron on vertices `0,...,5`, with equator `0-1-2-3-0` and poles `4,5` adjacent to the equator. Subdivide edge `1-4` by vertex `6`. Add the lollipop on vertices `7,...,17` (local vertex `i` is global `7+i`) in the face bounded by `0,1,6,4`, and add attachment edges `0-8`, `1-10`, `6-12`. This is a planar 18-vertex, 27-edge graph; the rotation system in `reference.py` has 11 faces. The guard `S={0,1,2,6}` leaves the 11-vertex lollipop and the three-vertex component `{3,4,5}`. The exterior route lengths between its ports are `(3,4,3)`, so the weighted all-spanning corollary applies. Contracting subdivision edge `1-6` recovers the octahedron as a minor, hence this example has treewidth at least four. This graph also admits a different guard to which the earlier five-vertex-fragment theorem applies; its purpose here is to give an explicit three-port realization, not to separate the positive classes.

## Reproduction

From the repository root, using a C++20 compiler and Python 3.11 or later with only the standard library:

```sh
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror graph_theory/planar_two_geodesic_three_port_lollipop10/exhaustive.cpp -o /tmp/three_port_lollipop10
/tmp/three_port_lollipop10
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_three_port_lollipop10/reference.py
```

Exact output with GCC 12.2.0 on the audit host:

```text
profiles=800 fragment_masks=2048 relevant_fragment_masks=402 checked_large_components=321600 short_route_control=FAILS_COVER PASS
full_masks=8192 selected_masks=10 profiles=800 selected_states=8000 negative_max_cover=10/11 example_faces=11 PASS
```

The optimized exhaustive run took about 1.3 seconds and 11 MB peak resident memory on that host. The full grid also passed an AddressSanitizer/UndefinedBehaviorSanitizer build with `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`. Runtime and memory are observations, not inputs to the certificate. No generated data or binaries are needed.

Literature status checked 28 September 2026: the [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) announces a disproof of a Codsi conjecture on balanced separators in planar graphs, but does not specify its exact statement or a witness. Its relationship to Problem 31 cannot be inferred from the schedule alone.
