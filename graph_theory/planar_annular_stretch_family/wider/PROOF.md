# Wider cylinders and sharp proxy depth

All paths called geodesic are shortest in the original specified metric.
Paths may intersect, and a singleton is allowed. For a nonnegative vertex
mass of total `W`, half balance means that every residual component has mass
at most `W/2` after deleting the union of the paths.

## Construction and theorem

For even `m>=6` and integer `h>=1`, define `G(m,h)` with caps `0,1` and
vertices `v(i,j)=2+h*i+j`, with `i` modulo `m` and `0<=j<h`. Join:

- cap `0` to all `v(i,0)` and cap `1` to all `v(i,h-1)`;
- `v(i,j)` to `v(i+1,j)` within each row;
- `v(i,j)` to `v(i,j+1)` for `j<h-1` (vertical edges);
- `v(i,j)` to `v(i+1,j+1)` if `i+j` is even, and `v(i+1,j)` to
  `v(i,j+1)` otherwise, for `j<h-1`.

Nested row cycles on an annulus, one diagonal per quadrilateral, and two
cap disks give a simple planar embedding. Each nonvertical edge has length
1. Each vertical edge independently is deleted or has any real length
at least 1. Deletions preserve planarity.

**Theorem.** Every nonnegative real vertex mass has a half-balanced union
of at most two ambient geodesics when either `m=10,h>=2`, or `m=12,h>=4`.

The proof has a finite component certificate and an unbounded-height
reduction. It makes no assertion for the missing case `m=12,h=3` in this
metric regime.

## Exact finite boundary lemmas

Give every edge of `K=G(m,k)` length 1. For the two parameter choices

```
(m,k,q) = (10,3,1) or (12,4,2),
```

put `A={0} union {v(i,j): j<q}`. If `A` has mass at least `W/2`, one of
the path unions in [certificate.json](certificate.json) is half-balanced.
Each union uses at most two ambient geodesics, avoids every vertical edge,
and avoids the proxy cap `1`. The three-row kernel has three candidate
unions; the four-row kernel has thirteen. The file also gives eight unions
for the unit graph `G(10,2)` without an anchor assumption. Those paths may
use both caps, but still avoid all vertical edges.

Here is the finite proof rule used to check these assertions. Start with
the mandatory set `A` for an anchored kernel and no mandatory set otherwise.
For each displayed cut, compute all components after deleting its paths.
If every cut failed half balance, some component behind each cut would
have mass strictly greater than `W/2`. Such a heavy component must intersect
every previous heavy component, and also `A` if present. In the given cut
order, exactly one component has all those intersections at every step
except the last. Add that component to the mandatory sets. At the final
step no component has all the required intersections, a contradiction.

The checker independently reconstructs the kernel edge rule, computes BFS
distances, confirms that every listed path is simple and ambient shortest,
checks the forbidden edges and proxy, and computes components by set
traversal. It applies the stated rule directly. The compatible-component
counts are respectively

```
m=10,k=3:  1,1,0
m=12,k=4:  1,1,1,1,1,1,1,1,1,1,1,1,0
m=10,k=2:  1,1,1,1,1,1,1,0.
```

This proves the finite lemmas for all nonnegative real masses, including
an anchor of exactly half the total. For zero total mass the conclusion is
immediate. The certificate has no premise about enumerating all geodesics
or all masses; only the displayed paths and their component tables matter.

## Interior rows: disjoint arcs save one edge

Let `r=m/2-1`. A cyclic row has two disjoint consecutive blocks of `m/2`
vertices, so the row is the union of two paths of length `r`. The two edges
between those blocks need not be on either path: a vertex separator only
requires that their endpoints be deleted.

For endpoints of either path in row `j`, every cap-avoiding route costs at
least `r`, because the cyclic column distance is `r` and every edge changes
the column by at most one and costs at least 1. A route visiting cap `0`
costs at least `2(j+1)`, and one visiting cap `1` costs at least `2(h-j)`.
For example, these last bounds follow from the level function taking values
`0,j+1,h+1` on cap `0`, row `j`, and cap `1`: its change across every edge
is at most that edge's length. Thus both row blocks are ambient geodesics
whenever

```
r <= 2(j+1) and r <= 2(h-j).
```

For `m=10`, this holds for `1<=j<=h-2`. For `m=12`, it holds for
`2<=j<=h-3`. These are precisely the rows outside the `q` boundary rows
at each end in the preceding table. No edge skips a row, so deleting such
a row separates all vertices above it from all vertices below it.

## Median row and boundary contraction

If a cap has mass at least `W/2`, delete it as a singleton; if `W=0`, use
the empty separator. Otherwise, choose the least `j` such that cap `0`
and rows `0,...,j` have mass at least `W/2`. It exists since cap `1` has
less than half. The mass strictly above row `j`, including cap `0`, is
less than half; the mass strictly below it, including cap `1`, is at most
half. If this is an interior row from the preceding section, its two
geodesic blocks give the separator.

Assume `h>=k` for the relevant `(m,k,q)`. If `j<q`, the near cap and first
`q` rows carry at least half. Keep cap `0` and the first `k` rows; map
every other vertex, including cap `1`, to the proxy cap of `G(m,k)`.
Keep the column and row coordinates on the retained vertices. Every edge
maps to a unit kernel edge or to a single vertex. Since all surviving
original edges cost at least 1, the map `phi` satisfies

```
d_K(phi(x),phi(y)) <= d_G(x,y).
```

Aggregate masses over fibres. The kernel anchor has at least half the
mass, so choose its certified balanced path union. These paths avoid the
proxy and vertical edges; hence every used vertex has a singleton fibre,
and every used edge lifts to an existing unit edge. The lifted path has
the same length as the kernel distance between its endpoints. The displayed
inequality then proves its ambient shortestness in the original graph.

A surviving original component maps to a connected set avoiding the kernel
separator. It lies over one residual kernel component, and its mass is at
most that component's aggregated mass. Hence balance lifts as well. For
`h=k` the map is just the identity on vertices; stretching or deleting
vertical edges only increases distances and splits residual components.

If `j>=h-q`, the last `q` rows and cap `1` have more than half the mass,
because the prefix strictly before the median row has less than half.
Apply the same reduction from the other end. Explicitly, interchange caps
and send `(i,j)` to `(i+s,h-1-j)`, where `s=0` for odd `h` and `s=1` for
even `h`. A square `(i,j)` maps to `(i+s,h-2-j)`, reversing its diagonal
orientation and its index-sum parity since `s+h` is odd. Modulo even `m`
preserves parity. Thus this reflection preserves the graph's edge classes
and merely permutes the arbitrary vertical lengths and deletions.

These cases cover `m=10,h>=3` and `m=12,h>=4`. For `m=10,h=2`, use its
unanchored finite certificate. Its paths use only nonvertical unit edges
and were geodesic in the unit supergraph. Stretching or deleting vertical
edges cannot shorten distances, so these paths remain geodesic; deleting
edges cannot join residual components, so their balance remains valid.
This completes the theorem.

## A general necessary boundary depth, attained here

Consider the unit kernel `G(m,k)` with proxy cap `1`. Suppose a proposed
boundary lemma assumes that cap `0` and some positive number of its first
rows carry at least half the mass, and requires both separator geodesics
to avoid the proxy. Even if it permits vertical edges, such a lemma is
**false whenever `m>2(k+2)`**.

First, the unit diameter is at most `k+1`. For grid endpoints in rows
`j,l`, routes through the two caps have lengths `j+l+2` and `2k-j-l`;
the smaller is at most `k+1`. These routes use the vertical columns where
necessary. Distances from a cap to any grid vertex are at most `k`, and
the cap-to-cap distance is at most `k+1`. Consequently each geodesic has
at most `k+2` vertices, so two delete at most `2(k+2)` vertices.

Put mass 1 on each of the `m` first-row vertices, mass `m` on the proxy,
and zero elsewhere. The anchor has exactly half of the total `2m`. The
`m` vertical columns are vertex-disjoint until they meet the proxy. If
the proxy survives and fewer than `m` column vertices are deleted, an
intact column joins one positive first-row mass to it. That component has
mass at least `m+1`, exceeding half. This proves the obstruction.

For circumference 10 it forces `k>=3`, and the three-row anchored
certificate attains this bound. For circumference 12 it forces `k>=4`,
and the four-row certificate attains it, even with the stronger two-row
anchor. This is optimality of the kernel depth for the stated kind of
proxy-avoiding lemma, not optimality of a separator in arbitrary planar
graphs. Indeed, in the obstruction mass assignment the proxy singleton
itself is a half-balanced separator of the actual kernel. It cannot be
used in the lifting reduction because it represents many original vertices.

The positive theorem does not follow for circumference 14 or beyond from
the depth bound. The necessity proof supplies no sufficiency in those cases.
