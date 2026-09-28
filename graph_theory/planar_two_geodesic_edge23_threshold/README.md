# Exact three-port threshold after one lollipop edge deletion

This gives an all-order **if and only if** fragment-cover rule for one edge-deletion state. It joins the [exact multiport trace closure](../planar_two_geodesic_multiport_closure_review1/REVIEW.md) with the [five-point metric obstruction](../planar_two_geodesic_two_ear_metric_obstruction/README.md). It is a local terminal for guarded descent toward [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not a settlement of that question for arbitrary planar graphs.

## Theorem

Fix an integer `m>=10`. Let `C={0,...,m}` be a vertex set in a finite simple unit-edge graph `H`. Suppose `H[C]` consists of the cycle `0-1-...-(m-1)-0` **with edge `2-3` deleted**, together with the pendant edge `0-m`. Thus `H[C]` is connected. Every edge from `C` to `H-C` must meet `C` at a port in `{1,3,5}`. Let `x=delta(1,3)` and `y=delta(1,5)` be shortest exterior route lengths, where all internal route vertices lie outside `C`, and infinity means no route. Assume

    x,y >= m-8.

**Exact threshold.** The following are equivalent:

1. The vertices of `C` lie in the union of at most two shortest paths in `H`, with endpoints allowed anywhere.
2. The vertices of `C` lie in the union of at most two shortest paths in `H`, each with both endpoints in `C`.
3. `max(x,y) >= m-6`.

No planarity assumption on `H` is needed. The third exterior route length `delta(3,5)` is arbitrary. The internal path `3-4-5` has length two, so any exterior `3`-to-`5` route (necessarily of length at least two) cannot shorten a distance between vertices of `C`.

### Positive direction: two explicit geodesics

By the reviewed multiport theorem, replace the exterior network by separate weighted routes of lengths `x,y,z=delta(3,5)`. This preserves distances between vertices of `C` and traces of `C`-endpoint geodesics. The `z` route can be ignored for distance comparisons because `3-4-5` is no longer.

If `x>=m-6`, take

    P=(m,0,1,2),
    Q=(3,4,5,...,m-1).

They cover `C`. The first is geodesic since `m` and `2` are leaves attached through `0-1`. The second has length `m-4`, and the only potentially competitive simple routes through the exterior have lengths at least `x+2` or `y+4`. Both are at least `m-4` under `x>=m-6,y>=m-8`. This also covers `x=infinity` or `y=infinity`.

Otherwise `x` is either `m-8` or `m-7`, while `y>=m-6`. Take

    P=(m,0,m-1,m-2,...,5),
    Q=(2,1, [a shortest exterior 1-to-3 route], 3,4).

The first has length `m-4`; its alternatives through the exterior have lengths at least `y+2` or `x+4`, again at least `m-4`. The second has length `x+2`. Competing routes to `4` have length at least `y+2` or `m-2`, both strictly larger because `x<=m-7<y`. Its exterior route exists since `x` is finite. Thus these two paths are geodesics. The multiport trace theorem transfers the chosen routes and covers back to `H`.

### Negative direction: five vertices in strict metric position

If `max(x,y)<m-6` under the assumed lower bounds, then `x,y` are each in `{m-8,m-7}`. Set `r=m-7` and `q=m-1`. The [weighted seven-point skeleton](../planar_two_geodesic_two_ear_metric_obstruction/README.md) gives the following exact distances on five vertices `L=(2,3,5,q,m)`:

|  | `2` | `3` | `5` | `q` | `m` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `2` | 0 | `x+1` | `y+1` | 3 | 3 |
| `3` | `x+1` | 0 | 2 | `x+2` | `x+2` |
| `5` | `y+1` | 2 | 0 | `r+1` | `y+2` |
| `q` | 3 | `x+2` | `r+1` | 0 | 2 |
| `m` | 3 | `x+2` | `y+2` | 2 | 0 |

All triangle inequalities among **distinct** vertices of `L` are strict for all four choices of `(x,y)` and every `r>=3`. Each slack is affine in `r`, has nonnegative slope, and is at least one at `r=3`. If a geodesic, even with exterior endpoints, contained three landmarks in order, its subpaths would force equality in one of these inequalities. Hence each geodesic meets at most two landmarks, and two geodesics cannot cover `C`. This proves the converse and the equivalence. `□`

The exact route-length array need not satisfy a triangle inequality, and exterior routes may overlap. Both features are handled by the multiport theorem. The displayed metric is on fragment vertices, so it also rules out paths whose endpoints lie outside the fragment.

## Sharp planar witnesses and scope

For every `m>=10`, let the ambient graph contain the full cycle plus leaf, an exterior `1`-to-`3` ear of length `m-7`, and an internally disjoint exterior `1`-to-`5` ear of the same length. Draw them as a noncrossing fan in the cycle face. Deleting `2-3` produces a planar instance with `x=y=m-7`, exactly one below the combined threshold. The five-point obstruction proves failure even for paths with arbitrary endpoints. Thus the strict inequality in condition 3 is necessary for a uniform rule under the stated one-ear lower bounds.

This theorem classifies the **specific** internal state `H[C]=C_m` minus `2-3`. It does not classify every spanning edge subgraph of a three-port lollipop. Exhaustive checks through `m=14` suggest the same inequalities suffice for all internal deletion patterns, but that broader statement is not claimed here. The local cover obstruction itself does not imply failure of a half-balanced separator in the whole planar graph.

## Reproduction and trust boundary

Run from the repository root with Python 3.11 or later and only the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_edge23_threshold/verify.py
```

Expected output:

```text
negative_affine_paths=128 min_strict_slack_r3=1 positive_affine_paths=19 finite_profiles=400 PASS
```

The symbolic checker enumerates **all** simple paths between the relevant vertices of an eight-vertex skeleton. It checks every proposed negative-case distance against every alternative as an affine inequality valid for all `r>=3`, then checks all ordered strict-triangle inequalities for all four short-route choices. For the two positive cases it checks every competing skeleton path over the full unbounded parameter cones, including both possibilities `x=m-8` and `x=m-7` in the second case. An independent Dijkstra/shortest-path-DAG calculation checks 400 weighted closure models around the threshold for `m=10,...,17`. The theorem's all-order and arbitrary-exterior scope rests on the symbolic inequalities, written path argument, and separately reviewed multiport trace theorem; the 400 finite cases are controls.

Literature status checked 28 September 2026: the [workshop problem list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still prints Problem 31 as a question. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) mentions a disproof of an unspecified Codsi conjecture about planar balanced separators but gives neither its precise statement nor a witness.
