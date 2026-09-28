# One ambient shortcut defeats complete coverage of an isometric lollipop

This is a sharper boundary for the **complete-coverage primitive** in
the weighted guard proofs for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It is not a counterexample to the separator question. The previous
[two-shortcut obstruction](../planar_two_geodesic_unicyclic_cover_obstruction/README.md)
gave an infinite planar family; only **one** equal-length exterior
shortcut is needed, and no parity restriction remains.

## Exact infinite family

For every integer `m>=11`, take the induced lollipop `C_m` with
cycle `0-1-...-(m-1)-0` and pendant leaf `t` at `0`. Add one exterior
vertex `x` adjacent to `1` and `3`, obtaining `F_m`. Delete only edge
`12` to obtain `H_m`. Both graphs are finite, simple, connected and
planar. The fragment is `C_m=F_m-{x}` and is isometric in `F_m`:
any excursion `1-x-3` has length two and can be replaced by the
equal-length internal arc `1-2-3`. The residual
`D=V(C_m)=V(H_m-{x})` is connected.

**Theorem.** Every union of at most two `H_m`-geodesics misses a
vertex of `D`. The maximum number of `D` vertices covered by two
geodesics is exactly `m`, one short of `|D|=m+1`. Thus a single
equal-length ambient shortcut can prevent an isometric unicyclic
fragment from being a deletion-stable two-geodesic **full-cover**
terminal. This does not imply that `F_m` or `H_m` lacks a balanced
two-geodesic separator.

Planarity is immediate by drawing `1-x-3` in one face of the cycle
and the pendant edge in the other. The checker gives a spherical
rotation. The graph `F_m` has `m+2` vertices, `m+3` edges and three
faces. After deleting `12`, `H_m` is a cycle with two pendant leaves:
the new cycle has length `m`, and the leaves are `t` at `A=0` and
`2` at `B=3`. The cycle has a **short** `A`-to-`B` arc
`0-1-x-3` of length three and a **long** arc of length
`L=m-3>=8`. The target `D` consists of all cycle vertices except
`x`, together with the two leaves.

## Proof of the coverage obstruction

Put `q=floor(m/2)`. A geodesic that starts at a leaf follows at most
`q` edges of the cycle: any longer cycle arc is beaten by the
opposite arc. We must cover both leaves, the short-arc vertex `1`,
and every one of the `L-1=m-4` internal vertices of the long arc.

If one path contains **both leaves**, it uses the unique short
leaf-to-leaf route `t-0-1-x-3-2`; the long route is longer. This
path covers no internal long-arc vertex. The other geodesic would
have to contain all internal long-arc vertices. Between the first
and last of these, the long subpath has `L-2=m-5>=6` edges, while
the alternative through the short arc has only `1+3+1=5` edges.
That subpath cannot be geodesic.

Otherwise the two paths contain one leaf each. If neither enters
the short arc, vertex `1` is missed. If exactly one enters the
short arc and stops before the other attachment, only the other
path covers any long-arc vertices. If it crosses the entire short
arc, both paths enter the long arc from **the same end**. A single
geodesic can reach at most `q` long-arc edges from an end; two
prefixes from one end still reach at most `q` edges. This is
insufficient because
`q<m-4=L-1` for `m>=11`.

If both paths traverse the full short arc in opposite directions,
one may enter the long arc from each end, but each has spent three
of its at most `q` cycle edges on the short arc. They can cover at
most `2(q-3)` long-arc edges between them. To cover all `L-1`
internal vertices from both ends requires at least `L-1` such
edges, whereas `2(q-3)<m-4=L-1`. Partial short-arc traversals
cover no long arc and only make the bound smaller. These cases
exhaust two paths containing the leaves, proving noncoverage.

The bound is exact. Write the long arc as
`p_0=A,p_1,...,p_L=B` and put `q=floor(m/2)`. Take one path from
`t` through `A` along the long arc to `p_q`. Take the other from
leaf `2` through `B` backward along the long arc to `p_(q+1)`.
Their cycle portions have respectively `q` and `L-q-1=m-q-4`
edges, both at most `q`, so both paths are geodesic. Their union
covers every long-arc vertex and both leaves, missing exactly the
short-arc target vertex `1`. Thus the maximum coverage is `m`.

## Reproduction and trust boundary

From the repository root run, with Python 3.11+ and no packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_single_shortcut_obstruction/verify.py
```

The checker uses two independent methods at `m=11`: it enumerates
all shortest-path DAGs, and separately enumerates all simple paths
and retains those whose lengths equal Floyd-Warshall distances.
It compares their exact vertex-mask sets and all path pairs. It
also checks the planar rotation, fragment isometry, and several
larger instances. The infinite noncoverage statement is the written
arc proof, not a bounded search.

The smallest obstructed member is `m=11`: `F_11` has 13 vertices
and 14 edges, while the connected target has 12 vertices. The
independent enumeration visits 321 simple paths and finds 91
distinct geodesic vertex masks. Expected summary:

```text
cycle=5 graph_vertices=7 target=6 max_two_geodesics=6
cycle=6 graph_vertices=8 target=7 max_two_geodesics=7
cycle=7 graph_vertices=9 target=8 max_two_geodesics=8
cycle=8 graph_vertices=10 target=9 max_two_geodesics=9
cycle=9 graph_vertices=11 target=10 max_two_geodesics=10
cycle=10 graph_vertices=12 target=11 max_two_geodesics=11
independent simple paths=321 geodesic vertex masks=91
cycle=11 graph_vertices=13 target=12 max_two_geodesics=11
cycle=12 graph_vertices=14 target=13 max_two_geodesics=12
cycle=13 graph_vertices=15 target=14 max_two_geodesics=13
cycle=15 graph_vertices=17 target=16 max_two_geodesics=15
cycle=20 graph_vertices=22 target=21 max_two_geodesics=20
cycle=30 graph_vertices=32 target=31 max_two_geodesics=30
PASS
```
