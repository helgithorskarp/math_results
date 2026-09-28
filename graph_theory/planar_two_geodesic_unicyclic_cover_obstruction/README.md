# An isometric one-leaf cycle is not a deletion-stable two-geodesic fragment

This note concerns the **complete-coverage primitive** behind the
weighted guard rules for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It gives no counterexample to that planar separator problem. All edges
have unit length and all graphs are finite and simple.

The reviewed [isometric path-and-cycle guard](../planar_two_geodesic_isometric_fragment_guard/README.md)
and the [few-leaf isometric-tree guard](../planar_two_geodesic_isometric_tree_guard/README.md)
work because *every* connected residual after arbitrary edge deletion
can be covered in full by two ambient geodesics. The following family
shows that this step fails even for an isometric unicyclic graph with
only one leaf. The shortcut vertices lie outside the fragment, so
their effect is invisible to the fragment's intrinsic path cover.

## The planar family

Fix `h>=3` and put `m=2h+3`. Let `C` have vertices
`0,1,...,m-1,t`, where `0-1-...-(m-1)-0` is an `m`-cycle and `t`
is a leaf adjacent to `0`. Obtain `F_h` by adding two vertices `x,y`
and four edges `0x,2x,1y,3y`. Let `H_h=F_h-12`, deleting only the
cycle edge `12`.

**Theorem.** Both `F_h` and `H_h` are connected simple planar graphs;
`C` is induced and isometric in `F_h`; and `D=V(C)` is connected in
`H_h[C]`. In fact `C` is the component of `F_h-{x,y}`, and `D` is
the component of `H_h-{x,y}`. Yet the union of any two shortest paths in `H_h` misses at
least one vertex of `D`. The maximum number of `D` vertices covered
by two `H_h`-geodesics is exactly `m`, one short of all `m+1` vertices.

Planarity has a direct drawing: draw `0-x-2` inside the cycle and
`1-y-3` outside it, with the pendant edge at `0` in a remaining outer
wedge. These subdivided chords lie on opposite sides, so they do not
cross. Deleting `12` preserves planarity. The construction has
`m+3` vertices and `m+5` edges, hence four faces in the displayed
embedding. The checker also audits an explicit spherical rotation.

The two external two-edge routes `0-x-2` and `1-y-3` have the same
length as the corresponding two-edge arcs in `C`. Replace every
excursion through `x` or `y` in an `F_h` walk between vertices of
`C` by its equal-length arc in `C`. Thus no pair of `C` vertices gets
closer in `F_h`, proving isometry. Removing `12` leaves the long
cycle arc and the tail connected inside `H_h[C]`.

## Why complete coverage fails for every `h>=3`

In `H_h`, label the long `0`-to-`3` branch

    p_0=0, p_1=m-1, p_2=m-2, ..., p_(2h)=3.

It has length `2h`. The other two `0`-to-`3` branches are
`0-1-y-3` and `0-x-2-3`, each of length three. The pendant vertex
`t` is adjacent to `p_0`.

First, the only geodesics containing **both** `1` and `2` are
`1-0-x-2` and `1-y-3-2`, up to reversal. These are the only
length-three `1`-to-`2` routes. Neither can be extended at an end
while remaining geodesic: for example, extending the first through
`y-1` gives a length-four `y`-to-`2` subpath versus `y-3-2` of
length two; extending it through `2-3` gives a length-four
`1`-to-`3` subpath versus `1-y-3` of length two. The other route is
symmetric. These paths contain neither `t` nor any internal long-branch
vertex.

Suppose two geodesics cover `D`, and call one containing `t` by `P`.
If `P` contains neither `1` nor `2`, the other path must contain both
and hence covers no internal long-branch vertex. But a `t`-geodesic
cannot contain *all* `p_1,...,p_(2h-1)`: reaching `p_(2h-1)` from
`t` along the whole long branch costs `2h>=6`, while the route
through either short branch costs five; entering at `p_(2h)=3`
and then reaching `p_1` costs `2h+3`, versus the direct distance two.
Thus `P` contains exactly one
of `1,2` and the other path `Q` contains the other.

A geodesic from `t` containing `1` must begin `t-0-1`; one containing
`2` must begin `t-0-x-2`. Any later internal long-branch vertex is
reached through `3`, because the path cannot revisit `0`. If `P`
reaches `p_i` this way, its prefix has length `1+3+(2h-i)`, whereas
the direct `t-0-p_1-...-p_i` route has length `1+i`. Therefore
`2i>=2h+3`, so `i>=h+2`. In particular, `P` covers none of
`p_1,...,p_(h+1)`.

Hence `Q` must contain the other special vertex `s` in `{1,2}` and
the *entire* consecutive long-branch segment
`p_1,...,p_(h+1)`. A simple path can attach `s` to that segment
either through the `0` end or through the `3` end. In both cases it
has a shorter alternative between `s` and the far endpoint:

| `s` | via `0` to `p_(h+1)` | via `3` to `p_(h+1)` | via `3` to `p_1` | via `0` to `p_1` |
| --- | ---: | ---: | ---: | ---: |
| `1` | `h+2` | `h+1` | `2h+1` | `2` |
| `2` | `h+3` | `h` | `2h` | `3` |

An attachment through `0` is too long by the first two columns; an
attachment through `3` is too long by the last two. This contradicts
geodesicity of `Q` and proves no pair covers `D`.

The bound is exact. One geodesic runs from `p_h` along the long
branch to `0` and then to `1`. The other runs from `t` through
`0-x-2-3` and backward along the long branch to `p_(h+2)`.
Both are shortest (the possible route around the other side is one
edge longer), and their union covers every vertex of `D` except
`p_(h+1)`.

## Exact finite audit and scope

The smallest member of this two-shortcut family is `h=3`, with
`m=9`, `12` vertices, and `14` edges in `F_3`. The independent
[standard-library checker](verify.py) checks the explicit rotation,
all pairwise distances needed for isometry, and *every* shortest path
and path pair in `H_3` by two different enumerations: breadth-first
shortest-path DAGs and all simple paths filtered using Floyd-Warshall
distances. It also checks several larger odd members and neighboring
even cycle lengths. The universal statement is the proof above; the
finite audit catches indexing and boundary errors.

Run from the repository root with Python 3.11 or later:

```sh
PYTHONDWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_unicyclic_cover_obstruction/verify.py
```

Expected summary:

```text
cycle=7 graph_vertices=10 target=8 max_two_geodesics=8
cycle=8 graph_vertices=11 target=9 max_two_geodesics=9
independent simple paths=452 geodesic vertex masks=85
cycle=9 graph_vertices=12 target=10 max_two_geodesics=9
cycle=10 graph_vertices=13 target=11 max_two_geodesics=11
cycle=11 graph_vertices=14 target=12 max_two_geodesics=11
cycle=12 graph_vertices=15 target=13 max_two_geodesics=13
cycle=13 graph_vertices=16 target=14 max_two_geodesics=13
cycle=15 graph_vertices=18 target=16 max_two_geodesics=15
cycle=19 graph_vertices=22 target=20 max_two_geodesics=19
PASS
```

This refutes a **direct extension of the full-coverage guard
primitive** to all isometric unicyclic one-leaf fragments. It does
not show that `F_h` or `H_h` lacks a balanced two-geodesic separator;
indeed the checker finds one for uniform mass in the smallest member.
No weighted all-spanning theorem is refuted by this example.
