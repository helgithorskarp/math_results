# Five-point metric obstruction from two competing planar ears

This is an all-order obstruction to covering a prescribed planar fragment by two geodesics. It explains why a second exterior route can defeat the [reviewed one-ear lollipop guard](../planar_two_geodesic_lollipop_spanning_cover_review1/REVIEW.md), even when the original ear exceeds its sharp safe-length threshold. The obstruction concerns **full fragment coverage**; it is not a counterexample to the half-balanced separator question in [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Infinite planar family

For any integer `r>=2`, put `m=r+7`. Let `C` be the cycle `0-1-...-(m-1)-0` and a pendant vertex `t=m` adjacent to `0`. Add two internally vertex-disjoint paths of length `r`, one from `1` to `3` and one from `1` to `5`, with all their internal vertices outside `C`; call the resulting graph `G_r`. Both ears can be drawn inside the cycle, as a noncrossing fan from `1`, so `G_r` is planar. Let `H_r=G_r-23`. The fragment `H_r[C]` remains connected. In `G_r`, both shortest restricted exterior routes `1-3` and `1-5` have length `r=m-7`; there is no restricted exterior `3-5` route.

**Theorem.** No union of two shortest paths in `H_r`, **even with arbitrary endpoints anywhere in `H_r`**, contains all vertices of `C`. In fact the five vertices

    L={2,3,5,m-1,t}

are in strict geodesic general position: no shortest path contains three of them. Consequently the all-spanning two-geodesic fragment-cover property fails in `G_r` for every `r>=2`.

This shows an unbounded interaction between exterior routes. If the `1-5` ear is omitted, the `1-3` ear has length `r=m-7>=m-8`, and the [one-ear theorem](../planar_two_geodesic_lollipop_spanning_cover/README.md) gives the all-spanning two-path cover. Adding the second ear changes the ambient shortest-path metric and destroys that cover after one internal edge deletion.

## Exact five-point certificate

Write `q=m-1`. Suppressing degree-two vertices on the long `q`-to-`5` arc and on the ears gives a seven-vertex weighted skeleton on `{0,1,2,3,5,q,t}`. Its edges and lengths are

| edge | length | edge | length |
| --- | ---: | --- | ---: |
| `0-1` | 1 | `1-2` | 1 |
| `0-q` | 1 | `0-t` | 1 |
| `q-5` | `r+1` | `5-3` | 2 |
| `1-3` | `r` | `1-5` | `r` |

Suppression preserves distances between the seven displayed vertices. Comparing the finitely many simple skeleton paths gives this exact distance matrix for the landmarks in order `(2,3,5,q,t)`:

|  | `2` | `3` | `5` | `q` | `t` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `2` | 0 | `r+1` | `r+1` | 3 | 3 |
| `3` | `r+1` | 0 | 2 | `r+2` | `r+2` |
| `5` | `r+1` | 2 | 0 | `r+1` | `r+2` |
| `q` | 3 | `r+2` | `r+1` | 0 | 2 |
| `t` | 3 | `r+2` | `r+2` | 2 | 0 |

Every triangle inequality on three **distinct** landmarks is strict for `r>=2`. More explicitly, each slack `d(a,b)+d(b,c)-d(a,c)` is affine in `r`, has nonnegative slope, and is at least one at `r=2`. If a geodesic contained three landmarks in order `a,b,c`, its subpaths would give the equality `d(a,c)=d(a,b)+d(b,c)`, a contradiction. Each geodesic therefore hits at most two of the five landmarks, and two geodesics miss at least one vertex of `C`. `□`

The five-point argument applies to shortest paths with exterior endpoints, which is stronger than the anchored failure checked for the earlier ten-cycle example. It is a local coverage obstruction, not a claim that `G_r` or `H_r` lacks some other half-balanced two-path separator.

## Reproduction and trust boundary

From the repository root, using Python 3.11 or later and only the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_two_ear_metric_obstruction/verify.py
```

Expected output:

```text
affine_simple_paths=32 minimum_triangle_slack_r2=1 planar_bfs_controls=16 PASS
```

The checker enumerates all 32 simple skeleton paths joining landmark pairs. It verifies each proposed affine distance against **every** alternative for all integer `r>=2` by checking the slope and its value at `r=2`, and verifies all ordered strict-triangle slacks in the same way. It separately constructs the unweighted graphs for `m=9,...,24`, checks a spherical rotation with four faces for each, deletes `23`, and compares all landmark BFS distances with the formula. The all-order result rests on the symbolic affine inequalities and the explicit skeleton reduction; the 16 full-graph cases are independent finite controls. No large artifact or external dependency is required.

Literature status checked 28 September 2026: the [workshop problem list](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) still prints Problem 31 as a question. The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html) announces a disproof of an unspecified Codsi conjecture about planar balanced separators but does not identify its exact statement or witness, so no conclusion about Problem 31 is drawn from it here.
