# An exact edge-window criterion for deletion-stable path covers

This note sharpens the [common-point metric-window theorem](../planar_two_geodesic_common_shortcut_window/README.md). A path edge can meet two disjoint shortcut windows. That edge still divides the path into two ambient geodesics, and the criterion below is **necessary and sufficient** for this to work after every edge deletion. It is a path-terminal tool for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a solution for arbitrary planar graphs.

All graphs are finite and simple, with arbitrary positive edge lengths. An internal path uses only edges of the specified induced path; a singleton is a geodesic. A *spanning edge subgraph* retains all vertices and an arbitrary subset of the edges.

## Exact characterization

Let `C=v_0-...-v_l` be an induced path of `G`, with `l>=1`. Write `t_i` for cumulative path length, so `0=t_0<...<t_l`. A **port** is a vertex of `C` incident with an edge to `G-C`. For each port pair `i<j`, put `delta_ij=d_G(v_i,v_j)`. It is **active** if `delta_ij<t_j-t_i`, and its closed window is

    J_ij=[(t_i+t_j-delta_ij)/2, (t_i+t_j+delta_ij)/2].

Use full ambient distances: shortest routes may use several exterior excursions. Then the following are equivalent.

1. For every spanning edge subgraph `H` of `G` and every component `D` of `H[C]`, the vertices of `D` can be partitioned into at most two internal ambient `H`-geodesics.
2. `C` can be covered by at most two internal ambient `G`-geodesics.
3. Some path edge `v_k v_(k+1)` meets every active window: `t_k<=U_ij` and `t_(k+1)>=L_ij` for all active pairs, where `J_ij=[L_ij,U_ij]`.

The empty active set makes condition 3 vacuous. For a singleton `C`, condition 1 is automatic. The finite distance test for condition 3 is

    exists k in {0,...,l-1}:
        2*t_k <= min_active(t_i+t_j+delta_ij),
        2*t_(k+1) >= max_active(t_i+t_j-delta_ij).

The criterion uses at most `|B| choose 2` full-graph port distances and a scan of the path edges. No planarity hypothesis is needed.

### Endpoint test

For an intact induced path interval `D=v_a-...-v_b` in any positive-edge graph `F`, define active pairs and windows using the ports of `D` and the **full** distances in `F`. Then for `a<=k<b`:

* The internal prefix `v_a-...-v_k` is an ambient geodesic exactly when `t_k<=U_ij` for every active pair of `D`.
* The internal suffix `v_(k+1)-...-v_b` is an ambient geodesic exactly when `t_(k+1)>=L_ij` for every active pair of `D`.

To prove the prefix statement, any simple competing route that leaves `D` first exits at port `p` and last returns at a different port `q`. Its middle length is at least `d_F(p,q)`, even if it enters `D` in between. The pieces before first exit and after last return are the unique internal paths. Reverse-order excursions `p>q` cannot improve the prefix, and neither can a nonactive forward pair. For active `p<q`, the walk that follows `D` from `a` to `p`, takes a shortest `p-q` route, and follows `D` from `q` to `k` is shorter than the internal prefix exactly when `t_k>U_pq`. This equivalence also covers `q<=k` and `p>k`: in the former case `U_pq<t_q<=t_k`, and in the latter `t_k<t_p<U_pq`. A shorter walk contains a shorter simple route, so it witnesses failure even if its pieces overlap. The suffix statement follows by reversing the path. Positivity ensures an active window lies strictly between its two port coordinates.

### Equivalence proof

Condition 1 implies 2 by taking `H=G`. An internal path is an interval of `C`. If two such geodesics cover `C`, truncate any overlap to obtain a geodesic prefix `v_0-...-v_k` and geodesic suffix `v_(k+1)-...-v_l`. The endpoint test gives condition 3. If one geodesic covers all of `C`, any edge works.

Now assume condition 3 and fix an arbitrary spanning `H`. A component `D` of `H[C]` is an interval of `C`. Every active pair in `D` for `H` is also active in `G`, since deleting edges only increases its distance. Its `H`-window contains the corresponding `G`-window. If the selected edge `v_kv_(k+1)` survives inside `D`, it meets every `H`-active window of `D`; the endpoint test makes its two sides ambient `H`-geodesics. If the selected edge does not lie in `D`, both endpoints of every port pair in `D` lie strictly on the same side of that edge. Any active `G`-window lies strictly between its port coordinates and thus cannot meet the selected edge. Hence `D` has no active pair even in `G`, so it is itself an ambient `H`-geodesic. This proves condition 1.

Thus an all-deletion statement reduces exactly to checking the intact host. The common-point condition from the earlier note implies condition 3, but the converse fails.

## A planar unit-edge strict example

Take the nine-vertex path `0-1-...-8` and two exterior two-edge ears `0-x-5` and `2-y-8`. Draw the ears on opposite sides of the path, giving a planar graph; the path remains induced. Its ports are `0,2,5,8`. Direct distance calculation gives precisely these active pairs:

| Pair | Ambient distance | Window |
| --- | ---: | --- |
| `(0,5)` | 2 | `[3/2,7/2]` |
| `(0,8)` | 4 | `[2,6]` |
| `(2,8)` | 2 | `[4,6]` |

The windows have **empty point intersection** because `7/2<4`, but all meet the edge `[t_3,t_4]=[3,4]`. The two internal geodesics are `0-1-2-3` and `4-5-6-7-8`; the characterization protects every component after every edge deletion. This example has 11 vertices and 12 edges.

For contrast, on the path `0-...-9` add disjoint exterior two-edge ears `0-x-3` and `6-y-9`. The active windows around the two distant ears have no common path edge. The exact criterion proves that this path cannot be covered by two internal ambient geodesics even before deletion. This is a *terminal* failure, not a counterexample to the global planar separator question.

## Guard consequence and reproduction

The two internal geodesics are endpoint-anchored, so the [four-vertex heavy-component guard](../planar_two_geodesic_four_guard/README.md) applies. If some set `S` of at most four vertices leaves components each either of order at most four or an induced path satisfying condition 3 in the full host, every spanning edge subgraph under every nonnegative vertex weighting has a half-balanced separator made of at most two ambient geodesics. This allows arbitrary positive edge lengths and does not require planarity. In a unit-edge planar graph, the small-component allowance rises to five by the induced-three-vertex-path rule. This remains a sufficient class, not a universal theorem for Problem 31.

Run the exact standard-library checker from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_edge_window_characterization/verify.py
```

It independently computes all-pairs ambient distances, all internal geodesic intervals and every pair of those intervals. It checks every one of the `2^12=4096` spanning edge subgraphs of the strict example and checks the distant-ear terminal failure. The proof above establishes the arbitrary-order, arbitrary-positive-length quantifiers; the finite program audits only the examples.

Literature checked 29 September 2026: the [workshop list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still states Problem 31 as a question. [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) prove two-path half separators for several structural planar classes, not this universal assertion. No historical priority claim is made for this criterion.
