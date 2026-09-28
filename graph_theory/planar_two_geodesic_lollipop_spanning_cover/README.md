# A deletion-stable two-geodesic cover rule for one-ear lollipops

This strengthens the [exact one-edge threshold](../planar_two_geodesic_ear_length_threshold/README.md) from one deletion to **every spanning edge subgraph** of the same planar graph. It supplies a precisely scoped complete-coverage terminal for guarded descent. The graph family itself has treewidth two, so its weighted half-separator property already follows from the general treewidth-three result of [Diot and Gavoille](https://emilie-diot.eu/Article/DG10a). The claim here concerns ambient geodesic **coverage of a specified fragment after arbitrary edge deletions**. It does not settle [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Exact all-spanning classification

For integers `m>=5,s>=2`, let `C_m` be the cycle `0-1-...-(m-1)-0` plus a leaf `t` at `0`. Add an internally vertex-disjoint `s`-edge ear from `1` to `3` to form `F_(m,s)`. This is the planar induced-isometric lollipop family of the preceding note. For a spanning edge subgraph `H` of `F_(m,s)`, let `H[C_m]` mean the subgraph induced by the original `m+1` fragment vertices.

**Theorem.** The following property holds if and only if `s>=m-8`: for **every** spanning edge subgraph `H` of `F_(m,s)` and **every** connected component `D` of `H[C_m]`, at most two shortest paths in `H` have a union containing every vertex of `D`.

The threshold is necessary because, for `s<m-8`, deleting only `12` leaves `H[C_m]` connected but makes its full cover impossible by the [ear-length theorem](../planar_two_geodesic_ear_length_threshold/README.md). Deleting the pendant edge `0t` splits `H[C_m]`, so the theorem intentionally covers each connected component separately; it does not claim that two paths cover their disconnected union.

## Proof of sufficiency

Put `L=m-3` and list the old long cycle arc as `p_0=0,p_1=m-1,...,p_L=3`. Its continuation to `1` is the edge `01`. The two other `1`-to-`3` routes in `F_(m,s)` are `1-2-3` of length two and the exterior ear of length `s>=2`.

**Tree and intact-cycle cases.** A tree with at most three leaves is covered, including every edge, by at most two of its own paths: with three leaves, take the paths from one fixed leaf to each of the other two; with two leaves, use their unique path. A singleton needs one singleton path. Every connected subtree also has at most three leaves. If such a tree is isometric in an ambient graph, these covering paths are ambient geodesics.

If any ear edge is missing from `H`, the surviving ear pieces attach to `C_m` at at most one vertex each and cannot shorten a simple path between fragment vertices. Every component of `H[C_m]` is either a tree with at most three leaves, a cycle, or a cycle with the leaf `t`. The tree components have the stated cover. For a cycle, split it into two arcs from `0` of at most `floor(m/2)` edges. If `t` is still attached, extend one arc from `0` to `t`; both resulting paths are geodesics and cover the lollipop. The same cover handles a surviving cycle if `t` is isolated.

Now assume the ear survives. If an edge `e` of the old `1-0-(m-1)-...-3` branch is missing, `C_m-e` is a tree with at most three leaves. It is isometric in `F_(m,s)-e`: replace any traversal of the exterior ear by the surviving `1-2-3` route of length two, which is no longer than the ear of length `s>=2`, then erase loops. The unique tree path cannot be longer than the resulting walk. Every component of `H[C_m]` is a subtree of `C_m-e`. Its tree paths survive and remain geodesics after further deletions, so two cover it.

It remains that the exterior ear and the entire old branch survive. If both `12` and `23` survive, the original lollipop is intact. It is isometric in `F_(m,s)`, and two root-to-half-cycle paths cover it; if `0t` is deleted, trim `t` from its path. A subpath of a geodesic remains geodesic after deleting other edges, provided its own edges survive.

If `12` is missing, use the two geodesics supplied by the exact threshold theorem for `F_(m,s)-12`, valid because `s>=m-8`. Both fragment leaves `t` and `2` occur only as path endpoints. The only further fragment edges that might be missing are `0t` and `23`; trim their respective leaves from the covering paths. The remaining paths survive in `H`, stay geodesic, and cover the nonisolated component of `H[C_m]`. Any isolated leaf is a singleton geodesic. This also handles deletion of both `12` and `23`.

The remaining case has `23` missing and `12` present. Here `2` is a leaf at `1`. Set `i=ceil((s+L-3)/2)` when `s<L-1`. Use

    P = (t,p_0,p_1,...,p_i),
    Q = (2,1, ear interior,3,p_(L-1),...,p_(i+1)).

These cover every vertex of `C_m`. The two possible routes from `t` to `p_i` have lengths `1+i` and `2+s+L-i`, so `P` is shortest because `2i<=L+s+1`. The two routes from `2` to `p_(i+1)` have lengths `s+L-i` through the ear and `i+3` through `0`, so `Q` is shortest because `2i>=s+L-3`. The chosen integer `i` satisfies both inequalities and `0<=i<L`. If `s>=L-1`, use `P=(t,p_0,...,p_L)` and `Q=(2,1)` instead: `P` is shortest since its old-arc portion of length `L` is no longer than the alternative of length `s+1`. If `0t` is deleted, trim `t` from `P`. Thus every case has the required pair, proving sufficiency.

## Reproduce and scope

From the repository root, run with Python 3.11+ and only the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_lollipop_spanning_cover/verify.py
```

The checker independently constructs `F_(m,s)`, verifies planarity by a rotation system and fragment isometry, tests the explicit `23`-deletion paths over a parameter grid, and exhaustively checks **all spanning edge subgraphs** for selected threshold fixtures by enumerating all geodesics and all pairs. It also compares shortest-path-DAG enumeration with an independent all-simple-path/Floyd-Warshall enumerator in selected cases. The finite checks catch errors in the construction and case split; the all-order statement rests on the proof above.

The exact run checks 243 parameter pairs, then all `256`, `8,192`, `32,768`, and `131,072` spanning subgraphs of `(m,s)=(5,2),(10,2),(11,3),(12,4)`, respectively. It confirms that `(11,2)` fails after deleting `12`, with maximum target coverage `11/12`, and ends with `PASS`.
