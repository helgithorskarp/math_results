# Exact exterior-ear threshold for covering a deleted planar lollipop

This note sharpens the [one-shortcut obstruction](../planar_two_geodesic_single_shortcut_obstruction/README.md) by varying the length of its sole exterior ear. The outcome is an exact all-order threshold for a **complete-coverage** test used in guarded descent. It does not settle the half-balanced separator question in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf). In particular, failure of full coverage below is not a counterexample to Problem 31.

## Family and result

Fix integers `m>=5` and `s>=2`. Let `C_m` be the cycle `0-1-...-(m-1)-0` with a leaf `t` at `0`. Form `F_(m,s)` by adding an internally vertex-disjoint path of `s` edges from `1` to `3` outside `C_m`. Delete edge `12` to form `H_(m,s)`, and put `D=V(C_m)`. Both graphs are finite, simple, connected, planar unit-edge graphs. The induced fragment `C_m=F_(m,s)-interior(ear)` is isometric in `F_(m,s)`: an exterior `1`-to-`3` excursion of length `s>=2` can be replaced by the internal two-edge route `1-2-3`.

**Theorem.** Two `H_(m,s)`-geodesics cover all of the connected target `D` **if and only if** `s>=m-8`. When `2<=s<m-8`, the maximum number of target vertices covered by two geodesics is exactly `m`, one fewer than `|D|=m+1`.

The proof also gives a metric-free covering rule for any cycle with two leaves at vertices `A,B`: if the `A`-to-`B` arcs have lengths `a>=3` and `L>=2`, and the target consists of both leaves, every vertex of the length-`L` arc, and the first internal vertex of the length-`a` arc, then two geodesics cover the target exactly when `a>=L-4`. Below this threshold their maximum coverage is one target vertex short.

The first failed case is `(m,s)=(11,2)`, the 13-vertex obstruction already published. Increasing the ear from two to three edges repairs that particular deletion at `m=11`; the critical ear length grows linearly with `m`. The theorem concerns deletion of `12` and complete coverage of `D`. It does not assert the same threshold for other edge deletions or for half balance.

## Proof

After deletion, `H_(m,s)` is a cycle with pendant leaves `t` at `A=0` and `2` at `B=3`. Its `A`-to-`B` arc through `1` and the exterior ear has length `a=s+1`; call this the ear arc. The other arc has length `L=m-3>=2`, with vertices `p_0=A,p_1,...,p_L=B`. The target `D` contains both leaves, `A,B`, the vertex `1` of the ear arc, and all `L-1` internal vertices of the old cycle arc. The other internal vertices of the ear arc are outside `D`.

First suppose `a>=L-4`, equivalently `s>=m-8`. If `a<=L`, use the leaf-to-leaf path `t,A,...,1,...,B,2` along the ear arc and the path `p_1,...,p_(L-1)` along the other arc. The first is shortest because `a<=L`. The second has length `L-2` and is shortest because its complementary route has length `1+a+1=a+2>=L-2`. Their union covers `D`. If `a>L`, use the leaf-to-leaf path along the old cycle arc and the singleton path `[1]`. The leaf-to-leaf path is shortest and covers all of `D` except `1`. This proves sufficiency.

Now suppose `a<L-4`. Write `N=L+a` for the new cycle length and `q=floor(N/2)`. Thus `q<=L-3<L-1`. Every geodesic containing exactly one leaf traverses at most `q` cycle edges. A geodesic containing both leaves must use the ear arc because `a<L`. It covers no internal vertex of the other arc. To cover all of `p_1,...,p_(L-1)`, the second path would need the `L-2`-edge span from `p_1` to `p_(L-1)`. That span is not shortest: the route via `A`, the ear arc, and `B` has length `a+2<L-2`.

It remains to consider one geodesic from each leaf. Since `L>q`, no leaf-rooted geodesic can traverse the entire long arc and then enter the ear arc. If neither meets the ear arc, `1` is missed. If neither traverses that arc in full, any path meeting it cannot also reach the other arc's interior. At most one path then covers long-arc internal vertices, reaching at most `q<L-1` of them. If exactly one path traverses the ear arc in full, both paths can reach long-arc internal vertices only from the same end; their union reaches at most `q<L-1` of them. If both traverse it in full, they do so in opposite directions and together reach at most `2(q-a)<=L-a<L-1` long-arc internal vertices. Hence full coverage is impossible.

The deficiency is exactly one. In the failed range, `q<L-1` and `L-q-1<=q`. Take the geodesics `t,p_0,p_1,...,p_q` and `2,p_L,p_(L-1),...,p_(q+1)`. They cover all of `D` except `1`: each follows at most `q` cycle edges, so each is shortest. This completes the proof.

## Exact reproduction

Run with Python 3.11 or later, using only its standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_ear_length_threshold/verify.py
```

The checker constructs an explicit spherical rotation for each graph, checks all pairwise distances establishing isometry, enumerates all geodesic vertex masks using shortest-path DAGs, and checks every pair against the target. A second enumerator independently lists every simple path and filters by Floyd-Warshall distances in six fixtures on both sides of the threshold. It checks both constructive witnesses across 153 sampled instances, including every `5<=m<=18`, `2<=s<=m` and boundary cases at `m=20,30`. The infinite theorem is the written proof, not finite enumeration.

Selected output: `(m,s)=(11,2)` covers `11/12`, `(11,3)` covers `12/12`, `(30,21)` covers `30/31`, and `(30,22)` covers `31/31`; the last line is `PASS 153 exact instances`.

The earlier two-edge obstruction is recovered by setting `s=2`: the criterion is `m<=10` for full coverage and `m>=11` for failure. This parameterized boundary specifies exactly how much ear length repairs that one deletion, while leaving the universal separator question open.
