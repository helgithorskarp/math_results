# An all-spanning three-port lollipop guard of unbounded size

This extends the [fixed ten-cycle three-port certificate](../planar_two_geodesic_three_port_lollipop10/README.md) to lollipop fragments of **every cycle length at least twelve**. The route-length conditions are explicit and the conclusion survives arbitrary edge deletion in the ambient graph. The result supplies a conditional weighted planar half-separator class for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf); it does not establish the two-path claim for every planar graph.

## All-order terminal theorem

Let `m>=12`, and let `C={0,...,m}` induce the cycle `0-1-...-(m-1)-0` plus the pendant edge `0-m` in a finite simple unit-edge graph `G`. Suppose all edges from `C` to `G-C` meet `C` at ports in `{1,3,5}`. Let `lambda_ab` be the length of a shortest `a`-to-`b` path whose internal vertices are outside `C`, with infinity if no such path exists. Assume

    lambda_13 >= m-8,    lambda_15 >= m-8,
    lambda_35 >= m-10,   max(lambda_13,lambda_15) >= m-6.

**Theorem.** For **every spanning edge subgraph** `H` of `G` and every component `D` of `H[C]`, two ambient `H`-geodesics with both endpoints in `D` cover all vertices of `D`. No planarity hypothesis is needed for this terminal.

The combined `max` bound is sharp as a uniform condition under the three other displayed bounds: the [planar two-ear family](../planar_two_geodesic_two_ear_metric_obstruction/README.md) has both `lambda_13=lambda_15=m-7`, `lambda_35=infinity`, and after deletion of `2-3` has a fragment that no two geodesics cover, even with exterior endpoints. This says nothing by itself about the existence of a half-balanced separator in that graph.

### Proof: fixed exterior network and four templates

Fix `H`, and write `x,y,z` for its three restricted exterior route lengths. Edge deletion can only increase these lengths, so they satisfy the four bounds. The [reviewed exact multiport closure](../planar_two_geodesic_multiport_closure_review1/REVIEW.md) replaces the exterior by three weighted virtual routes and preserves all fragment-endpoint distances and fragment traces of geodesics. It suffices to construct covers in this weighted model, even for route-length arrays that no exterior network realizes.

If all edges of the short arc `1-2-3-4-5` survive in `H[C]`, then that arc supplies internal port-pair paths of lengths `2,4,2`. Since `m>=12`, the three exterior lower bounds are at least `4,4,2`. Replace any exterior excursion between ports by the corresponding short-arc path without increasing its length. Thus each component of `H[C]` is isometric in `H`. A tree component has at most three leaves and is covered by two of its paths; if the entire cycle survives, two half-cycle geodesics cover it and the optional leaf. This handles every edge-deletion state whose short arc survives.

Otherwise select a missing short-arc edge in this priority order: `3-4`, `4-5`, `1-2`, `2-3`. Keep the **same exterior edge subgraph as `H`**, but restore every internal fragment edge except the selected one, including the leaf edge. Call the resulting supergraph `J`. It has the same exterior route lengths `x,y,z`; write `q=m-1`, `t=m`. The table gives two `J`-geodesics whose fragment traces partition `C`. `[x]` denotes any shortest exterior `1`-to-`3` route. In case A, `x>=m-6`. In case B, `x` is `m-8` or `m-7` and `y>=m-6`.

| Missing edge | Case | First geodesic | Second geodesic |
| --- | --- | --- | --- |
| `1-2` | A | `t-0-1` | `2-3-4-5-...-q` |
| `1-2` | B | `2-3-[x]-1-0-t` | `4-5-...-q` |
| `2-3` | A | `t-0-1-2` | `3-4-5-...-q` |
| `2-3` | B | `t-0-q-...-5` | `2-1-[x]-3-4` |
| `3-4` | A or B | `t-0-1-2-3` | `4-5-...-q` |
| `4-5` | A or B | `t-0-1-2-3-4` | `5-6-...-q` |

Here is an exact, finite proof of geodesicity for **all** admitted integer parameters. In every `J` above, vertices on the long `5`-to-`q` arc have degree two, so suppress them to one edge of length `m-6`. The remaining weighted skeleton has eight vertices `{0,1,2,3,4,5,q,t}`, the surviving unit edges, and virtual edges `1-3`, `1-5`, `3-5` of lengths `x,y,z`. Every simple skeleton path length is affine in `r=m-7,x,y,z`.

The source checker enumerates every simple skeleton path between each displayed geodesic's endpoints. For case A it substitutes `r=5+R`, `x=r+1+X`, `y=r-1+Y`, `z=r-3+Z`, where `R,X,Y,Z>=0`. For case B it substitutes `r=5+R`, `x=r-d` with `d in {0,1}`, `y=r+1+Y`, `z=r-3+Z`, where `R,Y,Z>=0`. For every competing path, every coefficient of its length **minus** the displayed path length is nonnegative, including the constant term. The displayed path occurs in the enumerated list. These 126 exact affine comparisons prove the six pairs geodesic for all `m>=12` and all finite admitted route lengths. Infinity deletes a virtual edge and cannot shorten a surviving path. The case `2-3` also agrees with the separately proved [exact one-edge threshold](../planar_two_geodesic_edge23_threshold/README.md).

### Proof: descent to every internal edge subgraph

Let `F=H[C]`, a subgraph of the tree `J[C]`. A surviving subpath of a `J`-geodesic is an `H`-geodesic: its length was already shortest in `J`, and deleting edges cannot create a shorter path. We show that each component of `F` is covered by at most two such surviving subpaths.

For the `3-4` and `4-5` templates, and case A of `1-2` and `2-3`, the two displayed geodesics are disjoint **internal** paths partitioning `C`. Exactly one tree edge joins the two paths. A component of any subforest `F` meets each path in a contiguous interval, so trim each displayed geodesic to that interval. The resulting at most two paths survive, have endpoints in the component, and cover it. Deleting the pendant edge merely isolates `t` or trims an endpoint.

For case B of `2-3`, the first geodesic is the internal path `t-0-q-...-5`. The second has two fragment pieces, `{2,1}` and `{3,4}`, joined by the exterior route `[x]`. The priority order ensures the internal edges `1-2`, `3-4`, and `4-5` survive in `F`. If a component meets both pieces, its unique tree connector includes the whole internal path from `0` to `5`; the full second path and the appropriate first-path subpath survive. If it meets at most one piece, trim the second path to that piece and the first path to its interval in the component. Again two geodesics cover it.

For case B of `1-2`, the exterior path has fragment pieces `{2,3}` and `{1,0,t}`, while the other path is `4-5-...-q`. If `0-1` survives, the same tree-connector argument gives surviving subpaths. If `0-1` is deleted, vertex `1` is isolated in `F` and every other component lies on the path `U=2-3-4-5-...-q-0-t`. Restore any missing edges of `U` while keeping `0-1` and `1-2` absent and retaining the final exterior network. The only possible exterior shortcuts between vertices of `U` join its ports `3` and `5`; each has length at least the internal `3-4-5` route of length two, including a route that visits vertex `1` outside `U`. Thus `U` is isometric in this supergraph, and every surviving component is a geodesic subpath of `U`. Vertex `1` is a singleton geodesic. This exhausts the possible internal deletions and proves the theorem. `□`

## Weighted planar consequence

Suppose a finite simple planar graph has a set `S` of at most four vertices such that every component of `G-S` either has order at most five or is a fragment meeting this theorem's hypotheses (with its own cycle length `m>=12`). Then **every spanning edge subgraph** and **every nonnegative real vertex-mass assignment** has a half-balanced separator equal to the union of at most two ambient geodesics. Cover the guard vertices in the unique heavy component by two geodesics. If a heavy residual remains, it lies in one component of `G-S`; cover its containing component of `H[C]` by the terminal theorem, or use the at-most-five induced-path rule. Replacing the guard paths removes the whole heavy residual, leaving less than half the total mass outside the new separator. This is the [reviewed four-vertex guard descent](../planar_two_geodesic_four_guard_review1/REVIEW.md) with an unbounded three-port terminal, not a universal planar separator theorem.

## Reproduction and trust boundary

From the repository root, using Python 3.11+ and a C++20 compiler:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_all_spanning_three_port_guard/symbolic.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_all_spanning_three_port_guard/trim_audit.py
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror graph_theory/planar_two_geodesic_all_spanning_three_port_guard/closure_exhaustive.cpp -o /tmp/three_port_closure_exhaustive
/tmp/three_port_closure_exhaustive 12
```

Expected output:

```text
template_cases=24 affine_path_comparisons=126 PASS
m 12 template_states 14848 special_states 512 PASS
m 13 template_states 29696 special_states 1024 PASS
m 14 template_states 59392 special_states 2048 PASS
m 15 template_states 118784 special_states 4096 PASS
m=12 relevant=1831 profiles=1152 states=2140416 PASS
```

The trim audit checks every one of the `2^(m+1)` internal edge masks for `m=12,...,15` in both parameter cases. It verifies the priority templates, path partitions, surviving subpaths, and the special `0-1`-deletion path `U`. The independent C++ checker enumerates **every** component of order at least six for every internal edge mask and every capped length profile at `m=12`; components of order at most five have the elementary pairing/induced-three-vertex-path cover. For larger exact controls, `/tmp/three_port_closure_exhaustive 13` and `14` respectively report `m=13 relevant=3878 profiles=1152 states=4573440 PASS` and `m=14 relevant=8182 profiles=1152 states=9734400 PASS`. The cap replaces lengths at least `m+1` by infinity because two vertices of a connected fragment component have an internal path of at most `m` edges.

The all-order claim rests on the written isometry/descent argument, the separately reviewed multiport theorem, and the finite **symbolic** comparison that proves every template geodesic over unbounded parameter ranges. The mask and capped-profile runs are independent controls, not a bounded substitute for the proof. No generated data or binaries are published.

Literature status checked 28 September 2026: the [workshop problem list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still prints Problem 31 as a question. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) announces a disproof of an unspecified Codsi conjecture about planar balanced separators but does not specify its statement or witness.
