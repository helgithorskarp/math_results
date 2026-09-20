# The weight-three sharp 398-coclique branch has only three support cores

This directory proves a structural reduction for the still-open degree-57
diameter-two Moore graph problem.  It continues the sharp 398-coclique branch
from Discovery Net contributions
`bafkreiev5wvmyqs2gmz626ew3ugh3bqyq2fh372a3654igguqysczvj34m` and
`bafkreidrcqwagnryekdj6rwp7p6sluy7riwrv2eesm7gtg5aicxzpe7lla`.

## Theorem

Suppose that a strongly regular graph with parameters `(3250,57,0,1)` has an
independent set `S` of size 398 in the sharp weight-five-star branch of the
height-2827 theorem.  On its 24 weight-bearing Moore branches, write

```text
w_x = 8 - |N(x) intersect S| in {1,2,3}.
```

The preceding theorem gives total branch weight seven and, for one
`t in {0,1,2,3}`,

```text
(n_1,n_2,n_3) = (150+3t, 9-3t, t).
```

Assume `t=3`.  Let `W` be the negative support and `F=G[W]`.  Then:

1. `|W|=162`, the total weight is 168, there are 159 weight-one and three
   weight-three vertices, and no weight-two vertex.
2. Every weight-three vertex has one weight-one neighbour in every other one
   of the 24 branches.  Moreover its nonreturning length-two paths in `F`
   reach every support vertex outside its own branch and its neighbourhood,
   exactly once.
3. The three weight-three vertices have one of exactly three core types:

   | type | weight-three branch pattern | common weight-one vertices | degree multiset of `F` |
   |---|---|---|---|
   | D1 | `1+1+1` | one vertex common to all three | `23^3, 3^1, 7^66, 9^92` |
   | D2 | `1+1+1` | three distinct pair-common vertices | `23^3, 5^3, 7^63, 9^93` |
   | P | `2+1` | two distinct pair-common vertices | `23^3, 5^2, 7^65, 9^92` |

   In every type `F` has exactly 681 edges.

Thus the entire `t=3` profile is reduced to three explicitly named
girth-five support cores.  This does **not** prove that the cores exist or
exclude them.

## Proof

The pointwise equation from the sharp branch is

```text
A_F w = 7w + 2*1.                                      (1)
```

Fix a weight-three vertex `u`, and put `d=deg_F(u)`.  Equation (1) says that
the total weight on `N_F(u)` is 23 and

```text
(A_F^2 w)_u = 7*23 + 2d = 161 + 2d.                   (2)
```

The returning two-walks contribute `3d`.  All nonreturning endpoints are
distinct, because the Moore graph has no triangles or four-cycles.  None is
in `u`'s own branch: such a vertex already has the branch root as its unique
common neighbour with `u`.  None is in `N_F(u)`.  The available endpoint
weight is therefore at most

```text
168 - 7 - 23 = 138.
```

Consequently `161+2d <= 3d+138`, so `d>=23`.  A vertex has at most one
neighbour in each of the other 23 Moore branches, hence `d=23`.  Equality
holds throughout: every neighbour has weight one, every other branch is met,
and every available positive-weight endpoint occurs exactly once among the
nonreturning two-walks.  This proves item 2, including distance-two
saturation.

With no weight two, a branch containing `c` weight-three vertices contains
`7-3c` weight-one vertices.  Three weight-three vertices can therefore be
distributed only as `1+1+1` or `2+1`, giving branch support sizes five and
three respectively (ordinary branches have support size seven).

Two weight-three vertices in the same branch already share its root, so they
have no common neighbour in `W`.  Two in distinct branches are nonadjacent;
distance-two saturation gives a common weight-one neighbour in `W`, and the
Moore property makes it unique.  In the `1+1+1` case the three pair-common
vertices are either all distinct or all equal: equality for any two pairs
makes that vertex adjacent to all three.  In the `2+1` case the two common
vertices involving the singleton-branch vertex are distinct, since otherwise
the same-branch pair would acquire a second common neighbour.

For a weight-one vertex `y`, let `k_y` be its number of weight-three
neighbours.  Equation (1) leaves `9-3k_y` weight-one neighbours, so

```text
deg_F(y) = k_y + (9-3k_y) = 9-2k_y.                   (3)
```

There are `3*23=69` incidences between the two weight classes.  Applying (3)
to the three common-neighbour patterns yields exactly D1, D2 and P in the
table.  Each displayed degree sum is 1362, hence every core has 681 edges.

## Why pairwise matching balance is not enough

`raw_matching_countermodel.json` gives 24 sets of size 56, all 276 pairwise
perfect matchings, and the D1 branch weights.  For every point `x` it satisfies

```text
sum(weight of the 23 matched partners of x) = 2 + 7*weight(x).
```

The direct checker verifies all 15,456 matching edges and all 1,344 pointwise
equations.  The countermodel contains many triangles and four-cycles, so it
is not a Moore subgraph.  Its role is precise: branch totals, pairwise perfect
matchings, and the pointwise balance equations alone cannot eliminate
`t=3`; a continuation must use short-cycle compatibility (or a stronger
global invariant).

## Reproduction

Requires CPython 3.11 or later and only the standard library.

```bash
python3 verify.py
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The certificate is a feasible witness checked from definitions; its
generation by HiGHS is outside the trust boundary.  The universal
classification is the written counting proof, while `verify.py` audits its
integer identities and the separate raw-matching countermodel.

## Scope and literature

The degree-57 Moore graph existence problem remains open.  The theorem does
not construct a Moore graph, exclude a 398-coclique, handle `t=0,1,2`, or
show that any of D1, D2, P admits the necessary cycle-compatible completion.
Faber and Keegan explain why permutation systems without the correct global
compatibility do not settle existence; Ishida gives the current automorphism
restriction.  The proposed new content here is the exact `t=3` support-core
classification and distance-two saturation in this 398-coclique branch, not
the classical Moore parameters or local branch decomposition.

- V. Faber and J. Keegan, *Existence of a Moore graph of degree 57 is still
  open*, arXiv:2210.09577.
- Y. Ishida, *No involutions in the missing Moore graph*, arXiv:2606.29183.

